"""Command-line entry point for agent-audit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_audit import __version__, report
from agent_audit.domains import ALL_DOMAINS


def main(argv: list[str] | None = None) -> int:
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
        try:
            findings = engine.audit(str(target))
        except Exception as exc:  # noqa: BLE001 - surface any engine/SDK error cleanly
            sys.stderr.write(f"error: engine failed: {exc}\n")
            return 3
        sys.stdout.write(report.render_findings(findings, str(target)))
        return 0

    # Default (v0): emit a manual audit template - stdlib only, no API key.
    sys.stdout.write(report.render_template(ALL_DOMAINS, str(target)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
