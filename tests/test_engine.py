"""Engine logic, exercised with a fake LLM call (no API key needed)."""

import json

from agent_audit import engine
from agent_audit.domains import ALL_DOMAINS, d6_guardrails
from agent_audit.model import Finding


def test_gather_context_reads_source_and_skips_junk(tmp_path):
    (tmp_path / "agent.py").write_text("def run(): pass\n")
    (tmp_path / "notes.md").write_text("# hi\n")
    junk = tmp_path / "__pycache__"
    junk.mkdir()
    (junk / "x.py").write_text("cached = 1\n")
    (tmp_path / "logo.png").write_bytes(b"\x89PNG\x00")

    ctx = engine.gather_context(str(tmp_path))
    assert "def run()" in ctx and "# hi" in ctx
    assert "cached" not in ctx  # __pycache__ skipped
    assert "PNG" not in ctx  # binary skipped


def test_gather_context_respects_byte_budget(tmp_path):
    (tmp_path / "big.py").write_text("a" * 5000)
    ctx = engine.gather_context(str(tmp_path), max_bytes=500)
    assert "truncated" in ctx
    assert len(ctx) < 1500


def _fake_call_all(passed: bool, evidence: str = "ok"):
    def call(system, user):
        # echo back a verdict for every check_id present in the user prompt
        ids = [tok.rstrip(":") for tok in user.split() if tok.rstrip(":").count(".") == 1
               and tok[0] == "d"]
        return json.dumps([{"check_id": i, "passed": passed, "evidence": evidence} for i in ids])
    return call


def test_audit_maps_verdicts_to_findings():
    findings = engine.audit(".", llm_call=_fake_call_all(True), domains=[d6_guardrails.DOMAIN])
    assert len(findings) == len(d6_guardrails.DOMAIN.checks)
    assert all(isinstance(f, Finding) and f.passed for f in findings)


def test_audit_reports_failures():
    findings = engine.audit(".", llm_call=_fake_call_all(False, "missing"),
                            domains=[d6_guardrails.DOMAIN])
    assert all(not f.passed for f in findings)
    assert all(f.evidence == "missing" for f in findings)


def test_untrusted_content_is_delimited():
    seen = {}

    def spy(system, user):
        seen["system"] = system
        seen["user"] = user
        return "[]"

    engine.audit(".", llm_call=spy, domains=[d6_guardrails.DOMAIN])
    assert "<repository_content>" in seen["user"]
    assert "untrusted" in seen["system"].lower()


def test_malformed_json_fails_closed():
    findings = engine.audit(".", llm_call=lambda s, u: "not json at all",
                            domains=[d6_guardrails.DOMAIN])
    # every check must be reported not-passed, never a silent pass
    assert findings and all(not f.passed for f in findings)
    assert all("not verified" in f.evidence for f in findings)


def test_missing_verdict_for_a_check_fails_closed():
    # model returns a verdict for only the first check of the domain
    first = d6_guardrails.DOMAIN.checks[0].id

    def partial(system, user):
        return json.dumps([{"check_id": first, "passed": True, "evidence": "ok"}])

    findings = engine.audit(".", llm_call=partial, domains=[d6_guardrails.DOMAIN])
    passed = [f for f in findings if f.passed]
    assert len(passed) == 1 and passed[0].check.id == first
    assert any("not verified" in f.evidence for f in findings)
