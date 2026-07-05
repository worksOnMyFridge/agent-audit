"""Render domains and findings to text reports (ASCII only, for portable output)."""

from __future__ import annotations

from agent_audit.model import Domain, Finding, SEVERITY_LABEL, SEVERITY_ORDER


def render_methodology(domains: list[Domain]) -> str:
    """The full audit methodology - every domain and check. Used by `--list`."""
    lines: list[str] = ["Agent Audit - methodology (GH-600 six domains)", ""]
    for d in domains:
        lines.append(f"{d.id} - {d.name}  ({d.weight})")
        for c in d.checks:
            lines.append(f"  [{SEVERITY_LABEL[c.severity]:<8}] {c.id}  {c.title}")
            lines.append(f"             -> {c.guidance}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_template(domains: list[Domain], target: str) -> str:
    """A fill-in audit template for a target - one checkbox per check.

    This is the v0 output: it does not judge the code yet, it hands a reviewer
    the exact checklist to walk through. The engine (v0.2) will auto-fill it.
    """
    total = sum(len(d.checks) for d in domains)
    lines = [
        f"Agent Audit - {target}",
        f"Template | {total} checks | engine not run (manual review)",
        "",
        "Mark each: [x] pass | [!] fail | [-] n/a",
        "",
    ]
    for d in domains:
        lines.append(f"{d.id} - {d.name}  ({d.weight})")
        for c in d.checks:
            lines.append(f"  [ ] {c.id}  {c.title}")
            lines.append(f"        if failed -> [{SEVERITY_LABEL[c.severity]}] {c.guidance}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_findings(findings: list[Finding], target: str) -> str:
    """Render engine results grouped by domain, worst severity first.

    Not-applicable checks (no relevant code to assess) are excluded from the
    score and listed separately, so a docs/config repo is not falsely penalized.
    """
    applicable = [f for f in findings if f.applicable]
    na = [f for f in findings if not f.applicable]
    failed = [f for f in applicable if not f.passed]
    by_sev = {s: sum(1 for f in failed if f.effective_severity == s) for s in SEVERITY_ORDER}
    passed_n = sum(1 for f in applicable if f.passed)
    total = len(applicable)
    score_str = f"{round(100 * passed_n / total)}/100" if total else "n/a"

    header = (
        f"Agent Audit - {target}\n"
        f"Score: {score_str} | "
        + " | ".join(f"{by_sev[s]} {s}" for s in SEVERITY_ORDER)
        + (f" | {len(na)} n/a" if na else "")
    )
    lines = [header, ""]

    # group failed findings by domain id (from check id prefix like "d6.1" -> "D6")
    order = {s: i for i, s in enumerate(SEVERITY_ORDER)}
    failed.sort(key=lambda f: (f.check.id, order[f.effective_severity]))
    current_domain = None
    for f in failed:
        dom = f.check.id.split(".")[0].upper()
        if dom != current_domain:
            current_domain = dom
            lines.append(f"{dom}")
        loc = f" ({f.evidence})" if f.evidence else ""
        lines.append(f"  [{SEVERITY_LABEL[f.effective_severity]}] {f.check.title}{loc}")
        lines.append(f"    -> {f.check.guidance}")
    if not failed:
        lines.append("No failing checks. [ok]")
    if na:
        lines.append("")
        lines.append(f"Not applicable ({len(na)}): " + ", ".join(f.check.id for f in na))
    return "\n".join(lines) + "\n"


def findings_report(findings: list[Finding], target: str) -> dict:
    """Machine-readable engine report - the stable JSON contract for CI."""
    applicable = [f for f in findings if f.applicable]
    failed = [f for f in applicable if not f.passed]
    by_sev = {s: sum(1 for f in failed if f.effective_severity == s) for s in SEVERITY_ORDER}
    passed_n = sum(1 for f in applicable if f.passed)
    total = len(applicable)
    na = sum(1 for f in findings if not f.applicable)
    return {
        "target": target,
        "score": round(100 * passed_n / total) if total else None,
        "summary": {
            **{s: by_sev[s] for s in SEVERITY_ORDER},
            "passed": passed_n,
            "applicable": total,
            "not_applicable": na,
            "total": len(findings),
        },
        "findings": [
            {
                "check_id": f.check.id,
                "domain": f.check.id.split(".")[0].upper(),
                "title": f.check.title,
                "severity": f.effective_severity,
                "passed": f.passed,
                "applicable": f.applicable,
                "evidence": f.evidence,
            }
            for f in findings
        ],
    }


def template_report(domains: list[Domain], target: str) -> dict:
    """Machine-readable checklist for the no-engine path."""
    return {
        "target": target,
        "engine": False,
        "checks": [
            {
                "check_id": c.id,
                "domain": d.id,
                "title": c.title,
                "severity": c.severity,
                "guidance": c.guidance,
            }
            for d in domains
            for c in d.checks
        ],
    }


def fails_threshold(findings: list[Finding], severity: str) -> bool:
    """True if any failing finding is at or above `severity` (critical > major > minor)."""
    limit = SEVERITY_ORDER.index(severity)
    return any(
        f.applicable and not f.passed and SEVERITY_ORDER.index(f.effective_severity) <= limit
        for f in findings
    )
