"""The LLM audit engine (WIP — v0.2).

Intended flow:
  1. Gather target repo context (source files, configs, tool/skill definitions),
     respecting size limits and .gitignore.
  2. For each domain, send its checks to Claude via the Anthropic SDK using a
     structured-output schema, so the model returns one pass/fail + evidence per
     check instead of prose.
  3. Collect the results into Finding objects for report.render_findings().

Kept out of the v0 path so the checklist and CLI install with zero dependencies
and no API key. Install the engine extra to enable it: `pipx install
"agent-audit[engine]"` and set ANTHROPIC_API_KEY.
"""

from __future__ import annotations

from agent_audit.model import Finding


def audit(path: str) -> list[Finding]:
    """Run the LLM audit against the project at `path`. Not implemented yet."""
    raise NotImplementedError(
        "The LLM engine lands in v0.2. For now use `agent-audit <path>` for a "
        "manual audit template, or `agent-audit --list` for the methodology."
    )
