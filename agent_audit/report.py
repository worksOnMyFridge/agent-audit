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
    """Render engine results grouped by domain, worst severity first."""
    failed = [f for f in findings if not f.passed]
    by_sev = {s: sum(1 for f in failed if f.check.severity == s) for s in SEVERITY_ORDER}
    passed_n = sum(1 for f in findings if f.passed)
    score = round(100 * passed_n / len(findings)) if findings else 0

    header = (
        f"Agent Audit - {target}\n"
        f"Score: {score}/100 | "
        + " | ".join(f"{by_sev[s]} {s}" for s in SEVERITY_ORDER)
    )
    lines = [header, ""]

    # group failed findings by domain id (from check id prefix like "d6.1" -> "D6")
    order = {s: i for i, s in enumerate(SEVERITY_ORDER)}
    failed.sort(key=lambda f: (f.check.id, order[f.check.severity]))
    current_domain = None
    for f in failed:
        dom = f.check.id.split(".")[0].upper()
        if dom != current_domain:
            current_domain = dom
            lines.append(f"{dom}")
        loc = f" ({f.evidence})" if f.evidence else ""
        lines.append(f"  [{SEVERITY_LABEL[f.check.severity]}] {f.check.title}{loc}")
        lines.append(f"    -> {f.check.guidance}")
    if not failed:
        lines.append("No failing checks. [ok]")
    return "\n".join(lines) + "\n"
