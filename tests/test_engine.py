"""Engine logic, exercised with a fake verdict call (no API key needed)."""

from agent_audit import engine
from agent_audit.domains import d6_guardrails
from agent_audit.model import Finding

D6 = d6_guardrails.DOMAIN


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


def _verdicts(passed, evidence="ok"):
    return [{"check_id": c.id, "passed": passed, "evidence": evidence} for c in D6.checks]


def test_audit_maps_verdicts_to_findings():
    findings = engine.audit(".", verdict_call=lambda s, c: _verdicts(True), domains=[D6])
    assert len(findings) == len(D6.checks)
    assert all(isinstance(f, Finding) and f.passed for f in findings)


def test_audit_reports_failures():
    findings = engine.audit(".", verdict_call=lambda s, c: _verdicts(False, "missing"), domains=[D6])
    assert all(not f.passed for f in findings)
    assert all(f.evidence == "missing" for f in findings)


def test_context_block_wraps_and_is_cacheable():
    b = engine._context_block("some code here")
    assert b["text"].startswith("<repository_content>") and "some code here" in b["text"]
    assert b["cache_control"] == {"type": "ephemeral"}


def test_untrusted_content_is_delimited_and_cached():
    seen = {}

    def spy(system, content):
        seen["system"], seen["content"] = system, content
        return []

    engine.audit(".", verdict_call=spy, domains=[D6])
    ctx = seen["content"][0]  # first block is the cached repo context
    assert "<repository_content>" in ctx["text"]
    assert ctx["cache_control"] == {"type": "ephemeral"}
    assert "untrusted" in seen["system"].lower()


def test_empty_verdicts_fail_closed():
    findings = engine.audit(".", verdict_call=lambda s, c: [], domains=[D6])
    assert findings and all(not f.passed for f in findings)
    assert all("not verified" in f.evidence for f in findings)


def test_missing_verdict_for_a_check_fails_closed():
    first = D6.checks[0].id
    call = lambda s, c: [{"check_id": first, "passed": True, "evidence": "ok"}]  # noqa: E731
    findings = engine.audit(".", verdict_call=call, domains=[D6])
    passed = [f for f in findings if f.passed]
    assert len(passed) == 1 and passed[0].check.id == first
    assert any("not verified" in f.evidence for f in findings)


def test_unknown_verdict_ids_are_ignored():
    call = lambda s, c: _verdicts(True) + [{"check_id": "zzz.9", "passed": False, "evidence": "x"}]  # noqa: E731
    findings = engine.audit(".", verdict_call=call, domains=[D6])
    assert len(findings) == len(D6.checks)  # extraneous id dropped, count stable
    assert all(f.passed for f in findings)


def test_applicable_flag_propagates():
    call = lambda s, c: [  # noqa: E731
        {"check_id": c.id, "passed": False, "evidence": "no code", "applicable": False}
        for c in D6.checks
    ]
    findings = engine.audit(".", verdict_call=call, domains=[D6])
    assert all(not f.applicable for f in findings)


def test_missing_applicable_defaults_true():
    # verdicts without an "applicable" key stay applicable (fail-closed default)
    findings = engine.audit(".", verdict_call=lambda s, c: _verdicts(False), domains=[D6])
    assert all(f.applicable for f in findings)


def test_cap_severity_downgrade_and_ceiling():
    assert engine._cap_severity("minor", "critical") == "minor"   # downgrade allowed
    assert engine._cap_severity("major", "critical") == "major"
    assert engine._cap_severity("critical", "minor") == "minor"   # cannot exceed static ceiling
    assert engine._cap_severity("", "major") is None              # nothing valid -> use static
    assert engine._cap_severity("bogus", "major") is None


def test_audit_applies_capped_severity():
    # d6.1 is a critical check; the model downgrades it to minor for this context
    call = lambda s, c: [{"check_id": "d6.1", "passed": False, "evidence": "low impact", "severity": "minor"}]  # noqa: E731
    findings = engine.audit(".", verdict_call=call, domains=[D6])
    f61 = next(f for f in findings if f.check.id == "d6.1")
    assert f61.effective_severity == "minor"
