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


def test_findings_report_json_contract():
    failing = {"d6.1", "d6.2"}
    rep = report.findings_report(_findings(lambda cid: cid not in failing), "./t")
    assert rep["target"] == "./t"
    assert rep["score"] == 94  # round(100 * 34/36)
    assert rep["summary"] == {
        "critical": 2, "major": 0, "minor": 0,
        "passed": 34, "applicable": 36, "not_applicable": 0, "total": 36,
    }
    assert len(rep["findings"]) == 36
    d61 = next(f for f in rep["findings"] if f["check_id"] == "d6.1")
    assert d61["domain"] == "D6" and d61["severity"] == "critical" and d61["passed"] is False
    assert d61["applicable"] is True


def _na_findings(applicable_map, passed=True):
    checks = [c for d in ALL_DOMAINS for c in d.checks]
    return [Finding(c, passed=passed, applicable=applicable_map(c.id)) for c in checks]


def test_not_applicable_excluded_from_score():
    d1_ids = {c.id for c in ALL_DOMAINS[0].checks}  # mark all of D1 (6) n/a, rest pass
    out = report.render_findings(_na_findings(lambda cid: cid not in d1_ids), "./t")
    assert "Score: 100/100" in out  # 30 applicable, all pass
    assert "6 n/a" in out
    assert "Not applicable (6):" in out


def test_all_na_scores_na():
    out = report.render_findings(_na_findings(lambda cid: False, passed=False), "./docs")
    assert "Score: n/a" in out
    assert "No failing checks" in out


def test_findings_report_na_in_summary():
    d1_ids = {c.id for c in ALL_DOMAINS[0].checks}
    rep = report.findings_report(_na_findings(lambda cid: cid not in d1_ids), "./t")
    assert rep["summary"]["not_applicable"] == 6
    assert rep["summary"]["applicable"] == 30
    assert rep["score"] == 100


def test_fails_threshold_ignores_na():
    checks = [c for d in ALL_DOMAINS for c in d.checks]
    # d2.1 is critical; failing but not applicable -> must not trip the gate
    findings = [Finding(c, passed=(c.id != "d2.1"), applicable=(c.id != "d2.1")) for c in checks]
    assert report.fails_threshold(findings, "critical") is False


def test_template_report_json_contract():
    rep = report.template_report(ALL_DOMAINS, "./t")
    assert rep["engine"] is False
    assert len(rep["checks"]) == 36
    assert {"check_id", "domain", "title", "severity", "guidance"} <= set(rep["checks"][0])


def test_fails_threshold():
    checks = [c for d in ALL_DOMAINS for c in d.checks]
    # one failing critical (d2.1 is critical), everything else passes
    crit_fail = [Finding(c, passed=(c.id != "d2.1")) for c in checks]
    assert report.fails_threshold(crit_fail, "critical") is True
    assert report.fails_threshold(crit_fail, "major") is True   # critical is above major
    # only a failing minor
    minor_fail = [Finding(c, passed=(c.severity != "minor")) for c in checks]
    assert report.fails_threshold(minor_fail, "critical") is False
    assert report.fails_threshold(minor_fail, "major") is False
    assert report.fails_threshold(minor_fail, "minor") is True
    # all pass -> never fails
    assert report.fails_threshold([Finding(c, passed=True) for c in checks], "minor") is False
