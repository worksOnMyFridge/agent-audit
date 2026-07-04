"""Report rendering: content, structure, and ASCII-only output."""

from agent_audit import report
from agent_audit.domains import ALL_DOMAINS
from agent_audit.model import Finding


def test_methodology_lists_every_check_and_is_ascii():
    out = report.render_methodology(ALL_DOMAINS)
    assert out.isascii(), "output must be pure ASCII for portable terminals"
    for d in ALL_DOMAINS:
        for c in d.checks:
            assert c.id in out
            assert c.title in out


def test_template_has_a_checkbox_per_check():
    out = report.render_template(ALL_DOMAINS, "./x")
    assert out.isascii()
    assert out.count("[ ] ") == sum(len(d.checks) for d in ALL_DOMAINS)
    assert "./x" in out


def _findings(passed_map):
    checks = [c for d in ALL_DOMAINS for c in d.checks]
    return [Finding(c, passed=passed_map(c.id)) for c in checks]


def test_findings_score_and_grouping():
    # fail exactly the two D6 critical checks, pass everything else.
    failing = {"d6.1", "d6.2"}
    out = report.render_findings(_findings(lambda cid: cid not in failing), "./demo")
    assert out.isascii()
    # 34/36 passed -> round(100*34/36) = 94
    assert "Score: 94/100" in out
    assert "2 critical" in out and "0 major" in out
    lines = out.splitlines()
    assert "D6" in lines  # the failing domain appears as a group header
    # domains with no failing checks must not appear as group headers
    for other in ("D1", "D2", "D3", "D4", "D5"):
        assert other not in lines


def test_all_pass_reports_no_failures():
    out = report.render_findings(_findings(lambda cid: True), "./clean")
    assert "Score: 100/100" in out
    assert "No failing checks" in out
