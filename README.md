# agent-audit

[![ci](https://github.com/worksOnMyFridge/agent-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/worksOnMyFridge/agent-audit/actions/workflows/ci.yml)

> Reliability audit for AI agents — based on the six competency domains of the
> **GitHub Agentic AI Developer** certification (exam GH-600).

`agent-audit` scans an AI-agent codebase and reports where it is weak on the
fundamentals that make agents safe and reliable in production: architecture,
tools, memory, evaluation, multi-agent design, and guardrails. Each finding
comes with a severity and a concrete fix.

It is **methodology-first**. The audit criteria are derived from the *public*
GH-600 exam outline and general agentic-systems best practice — not from any
private material — so the checklist itself is useful even before you run the
tool.

```
# not yet on PyPI — install from source
$ pipx install "git+https://github.com/worksOnMyFridge/agent-audit"
$ agent-audit ./my-agent            # audit checklist, no API key needed
$ agent-audit ./my-agent --engine   # LLM-scored (add the [engine] extra + a key)
```

```
Agent Audit - ./my-agent
Score: 78/100 | 1 critical | 2 major | 3 minor | 4 n/a

D6
  [CRITICAL] Untrusted input is defended against prompt injection (agent.py:88)
    -> Isolate untrusted content as data; never let it become instructions.
  [MAJOR] Outputs are validated before use (agent.py:140)
    -> Validate the structure and content of model output before acting on it.

Not applicable (4): d5.1, d5.2, d5.4, d5.6

Findings are candidates for human review, not authoritative verdicts.
```

## What it does

- **Six-domain checklist** derived from the public GH-600 outline — usable as a
  manual review even without the engine.
- **LLM engine** (`--engine`) scores each domain via the Anthropic SDK with
  structured outputs, treating repo content as untrusted data and failing closed.
- **Context-aware precision** — the model marks a check *not applicable* when the
  capability is absent by design, and lowers a check's severity to fit real-world
  impact, so a single-purpose or docs-only repo is not falsely penalized.
- **Relevance-ranked coverage** — audits the most important files first
  (entrypoints, memory / tool / guardrail modules) within a token budget, and
  reports how much of the repo it covered.
- **Cost-aware** — the repo context is prompt-cached across the six domain calls
  (~65–70% less input); the model is configurable via `AGENT_AUDIT_MODEL`.
- **CI-ready** — JSON output, a `--fail-on` gate, a `.agent-audit-ignore`
  baseline, and a scheduled self-audit workflow.

## Why

Most agent projects fail the same handful of checks: a tool holds far more
privilege than it needs, untrusted input flows straight into a shell, context
grows without bound, or there is no evaluation beyond "it looked fine once."
`agent-audit` turns that recurring list into a repeatable review.

## The methodology — six domains

The audit mirrors the GH-600 competency domains. Weights are the exam's own
emphasis and are informational only.

| Domain | Focus | Exam weight |
|---|---|---|
| **D1 · Architecture & SDLC** | task contract, planning, autonomy tier, recoverability | 15–20% |
| **D2 · Tools, MCP & environment** | least-privilege tools, typed schemas, sandboxing, secrets | 20–25% |
| **D3 · Memory** | context management, grounded retrieval, isolation | 10–15% |
| **D4 · Evaluation** | eval sets, offline + online, meaningful metrics | 15–20% |
| **D5 · Multi-agent** | clear roles, coordination, scope isolation, termination | 15–20% |
| **D6 · Guardrails** | injection defense, human-in-the-loop, fail-closed | 10–15% |

The full, per-check criteria live in [`checklists/gh600_domains.md`](checklists/gh600_domains.md).

## Usage

```
agent-audit <path>                              # manual audit template (stdlib only, no API key)
agent-audit <path> --engine                     # LLM-scored audit (needs [engine] extra + ANTHROPIC_API_KEY)
agent-audit <path> --engine --format json       # machine-readable report (score, findings, coverage)
agent-audit <path> --engine --fail-on critical  # exit non-zero on a critical finding (CI gate)
agent-audit --list                              # print the full audit methodology
```

The engine treats all repository content as untrusted data, not instructions,
and fails closed: any check it cannot verify is reported as such, never as a
silent pass. Findings are candidates for human review, not authoritative
verdicts; suppress already-triaged ones with a `.agent-audit-ignore` file
(one check id per line). Set `AGENT_AUDIT_MODEL` to choose the model (e.g. a
cheaper one for large sweeps). See a hand-written example in
[`examples/sample_report.md`](examples/sample_report.md), or a real run of the
tool on its own source in [`examples/self-audit.md`](examples/self-audit.md).

## Development

```
pip install -e ".[dev]"
python -m pytest
```

The checklist, report renderer, and CLI have no runtime dependencies. The engine
is unit-tested with an injected fake LLM call, so the suite runs without an API
key. CI runs the tests on Python 3.11–3.13, and a scheduled workflow audits this
repo with the engine itself.

## Status

Feature-complete v1: methodology + LLM engine (structured outputs, prompt
caching, context-aware severity and applicability), relevance-ranked coverage,
`--format json`, `--fail-on` gating, `.agent-audit-ignore` baseline, a scheduled
self-audit workflow, and a test suite on CI.

Not yet published to PyPI. Backlog (by need): per-language heuristics,
configurable severity thresholds, response caching between runs.

## License

MIT © worksOnMyFridge
