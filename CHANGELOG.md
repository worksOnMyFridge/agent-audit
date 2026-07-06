# Changelog

## 0.1.0

First release. Distributed on PyPI as `agentaudit`; the command is `agent-audit`.

- Six-domain, GH-600-aligned checklist (36 checks) and a stdlib-only CLI that
  prints the methodology (`--list`) or a fill-in audit template.
- LLM engine (`--engine`) with structured outputs, prompt caching across the six
  domain calls, context-aware severity and not-applicable handling, and
  relevance-ranked file coverage.
- `--format json`, `--fail-on <severity>` gating, and a `.agent-audit-ignore`
  baseline; findings are framed as candidates for human review.
- UTF-8-safe output; model configurable via `AGENT_AUDIT_MODEL`.
- Test suite on CI (Python 3.11-3.13), a gitleaks scan, and a scheduled
  self-audit workflow.
