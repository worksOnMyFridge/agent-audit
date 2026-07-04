# agent-audit

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
$ pipx install agent-audit
$ agent-audit ./my-agent
```

```
Agent Audit - ./my-agent
Score: 62/100 | 3 critical | 5 major | 4 minor

D6
  [CRITICAL] Untrusted input is defended against prompt injection (agent.py:88)
    -> Sanitize and isolate untrusted content as data; never let it become instructions.
  [MAJOR] Outputs are validated before use (schema / allowlist)
    -> Validate the structure and content of model output before acting on it.

D3
  [MAJOR] Short-term context is bounded (memory.py:20)
    -> Compact or summarize long histories; unbounded context degrades quality and cost.
```

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
agent-audit <path>        # manual audit template (stdlib only, no API key)
agent-audit <path> --engine   # LLM-scored audit (needs [engine] extra + key)
agent-audit --list        # print the full audit methodology
agent-audit --version
```

The engine treats all repository content as untrusted data, not instructions,
and fails closed: any check it cannot verify is reported as such, never as a
silent pass. See a complete example in
[`examples/sample_report.md`](examples/sample_report.md).

## Development

```
pip install -e ".[dev]"
python -m pytest
```

The checklist, report renderer, and CLI have no runtime dependencies. The engine
is unit-tested with an injected fake LLM call, so the suite runs without an API
key. CI runs the tests on Python 3.11-3.13.

## Status / roadmap

- **v0** — methodology, 36-check checklist, and a stdlib-only CLI that emits a
  fill-in audit template.
- **v0.2 (current)** — the LLM engine (`agent_audit/engine.py`): gathers repo
  context and scores each domain's checks via the Anthropic SDK. Enable with
  `pip install ".[engine]"`, set `ANTHROPIC_API_KEY`, and pass `--engine`.
- **later** — JSON output, CI mode (fail the build on new critical findings),
  per-language heuristics.

## License

MIT © worksOnMyFridge
