# Example — a real run on this repository

Unedited output of `agent-audit --engine .` run against agent-audit's own
source, scored by an LLM (claude-opus-4-8) against the six-domain checklist.
This is the tool auditing itself — a real run, not an illustration. For a
hand-written richer example (with critical/major findings), see
[`sample_report.md`](sample_report.md).

```
Agent Audit - .
Score: 92/100 | 0 critical | 0 major | 3 minor

D4
  [MINOR] LLM-as-judge is robust (diverse judges, no correlated blind spots)
    -> Vary judge models and prompts; a single judge shares the generator's blind spots.
  [MINOR] Failures are logged and fed back into the eval set
    -> Capture production failures and grow the eval set from them.

D6
  [MINOR] Sensitive actions are logged (actor, action, timestamp)
    -> Record an audit trail for accountability and incident review.
```

The three findings are accurate and honest:

- **D4 — single judge.** The engine scores each domain with one model and one
  prompt (`_default_verdict_call`), so it shares blind spots with the generator.
- **D4 — no feedback loop.** Findings are only rendered; there is no capture of
  failures back into an eval set.
- **D6 — no audit trail.** The tool logs no record of which repository was sent
  to the API, by whom, and when.

All three map to open roadmap items rather than being hidden — which is the
point of the tool.
