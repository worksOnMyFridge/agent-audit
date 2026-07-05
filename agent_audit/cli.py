"""Command-line entry point for agent-audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agent_audit import __version__, report
from agent_audit.domains import ALL_DOMAINS


def main(argv: list[str] | None = None) -> int:
    # LLM evidence text may contain non-ASCII; keep output from crashing on a
    # non-UTF-8 console (e.g. Windows cp1252).
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        prog="agent-audit",
        description="Reliability audit for AI agents across the six GH-600 domains.",
    )
    parser.add_argument("path", nargs="?", help="path to the agent project to audit")
    parser.add_argument(
        "--list", action="store_true", help="print the full audit methodology and exit",
    )
    parser.add_argument(
        "--engine", action="store_true",
        help="run the LLM engine (needs the [engine] extra and ANTHROPIC_API_KEY)",
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="output format (default: text)",
    )
    parser.add_argument(
        "--fail-on", choices=["critical", "major", "minor"], default=None, dest="fail_on",
        help="exit 4 if a failing finding at or above this severity exists (engine mode)",
    )
    parser.add_argument(
        "--ignore", default=None, metavar="FILE",
        help="baseline file of check ids to suppress (default: <path>/.agent-audit-ignore)",
    )
    parser.add_argument("--version", action="version", version=f"agent-audit {__version__}")
    args = parser.parse_args(argv)

    if args.list:
        sys.stdout.write(report.render_methodology(ALL_DOMAINS))
        return 0

    if not args.path:
        parser.print_help()
        return 1

    target = Path(args.path)
    if not target.exists():
        sys.stderr.write(f"error: path not found: {target}\n")
        return 2

    if args.engine:
        from agent_audit import engine  # lazy: keeps the default path dependency-free
        cov: dict = {}
        try:
            findings = engine.audit(str(target), coverage=cov)
        except Exception as exc:  # noqa: BLE001 - surface any engine/SDK error cleanly
            sys.stderr.write(f"error: engine failed: {exc}\n")
            return 3
        ignore_file = args.ignore
        if ignore_file is None and target.is_dir():
            default_ignore = target / ".agent-audit-ignore"
            if default_ignore.exists():
                ignore_file = str(default_ignore)
        ignore = report.load_ignore(ignore_file) if ignore_file else set()
        active = [f for f in findings if f.check.id not in ignore]
        baselined = len(findings) - len(active)

        if args.format == "json":
            data = report.findings_report(active, str(target))
            data["coverage"] = cov
            data["baselined"] = baselined
            sys.stdout.write(json.dumps(data, indent=2) + "\n")
        else:
            sys.stdout.write(report.render_findings(active, str(target)))
            if baselined:
                sys.stdout.write(f"\nBaselined: {baselined} check(s) suppressed via ignore file.\n")
            if cov.get("truncated"):
                sys.stdout.write(
                    f"\nCoverage: audited {cov['files_included']} of "
                    f"{cov['files_total']} files (most relevant first; "
                    f"rest exceeded the size budget).\n"
                )
        if args.fail_on and report.fails_threshold(active, args.fail_on):
            return 4
        return 0

    # Default (no engine): the audit template - stdlib only, no API key.
    if args.format == "json":
        sys.stdout.write(json.dumps(report.template_report(ALL_DOMAINS, str(target)), indent=2) + "\n")
    else:
        sys.stdout.write(report.render_template(ALL_DOMAINS, str(target)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
