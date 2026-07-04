# The audit checklist — six GH-600 domains

Each check has a severity: **critical** (ship-blocker), **major** (fix before
production), **minor** (worth addressing). Weights are the GH-600 exam's own
emphasis and are informational only. Criteria are derived from the public exam
outline and general agentic-systems best practice.

---

## D1 · Architecture & SDLC — 15–20%

- **d1.1** · *major* — Explicit task contract (goal, inputs, success criteria, definition of done).
  Without it, success is unverifiable.
- **d1.2** · *major* — Agent plans and decomposes before acting. Break multi-step work into verifiable sub-steps.
- **d1.3** · *minor* — Autonomy tier is appropriate and not over-engineered. Simplest tier that solves the task.
- **d1.4** · *major* — Control flow is code-orchestrated where possible. Model handles judgment, not plumbing.
- **d1.5** · *major* — Steps are idempotent / recoverable after failure. Checkpoints so a crash does not corrupt state.
- **d1.6** · *minor* — Agent config is versioned and reproducible. Pin model IDs; prompts in version control.

## D2 · Tools, MCP & environment — 20–25%

- **d2.1** · *critical* — Each tool has least-privilege scope. A read task should not hold write/delete power.
- **d2.2** · *major* — Tools have clear descriptions and typed input schemas, so the model calls them correctly.
- **d2.3** · *major* — Third-party MCP servers are vetted and pinned. Review external code and permissions first.
- **d2.4** · *critical* — Tool execution is sandboxed / isolated, especially code or shell, with resource limits.
- **d2.5** · *major* — Tool failures are handled: timeouts, bounded retries, graceful degradation.
- **d2.6** · *critical* — Secrets are kept out of code and loaded from env / secret store. Never in version control.

## D3 · Memory — 10–15%

- **d3.1** · *major* — Short-term context is bounded (summarization / compaction). No unbounded growth.
- **d3.2** · *minor* — Durable memory is separated from transient working state.
- **d3.3** · *major* — Retrieved memory is grounded and cited. Guard against fabricated recall.
- **d3.4** · *minor* — Stored memory is filtered for lasting relevance. Point to transactional data, do not ingest it.
- **d3.5** · *major* — Volatile / stale facts are re-verified before being trusted.
- **d3.6** · *critical* — Memory is scoped so no data leaks across users / sessions.

## D4 · Evaluation — 15–20%

- **d4.1** · *major* — An evaluation set / test cases exist, not manual vibes.
- **d4.2** · *major* — Evaluated offline before deploy and monitored online after.
- **d4.3** · *major* — Metrics are tied to task success, not surface plausibility.
- **d4.4** · *major* — Prompt / model / tool changes run against regression tests.
- **d4.5** · *minor* — LLM-as-judge is robust: diverse judges, no correlated blind spots.
- **d4.6** · *minor* — Failures are logged and fed back into the eval set.

## D5 · Multi-agent orchestration — 15–20%

- **d5.1** · *major* — Each agent has a clear, bounded role. No do-everything agent.
- **d5.2** · *major* — An explicit coordination mechanism is defined (orchestrator, blackboard, hand-off).
- **d5.3** · *critical* — Agents run with least authority and isolated scope. Isolate the blast radius.
- **d5.4** · *minor* — Hand-off contracts are explicit. Do not pass full context by default.
- **d5.5** · *minor* — Multi-agent complexity is justified over a single agent.
- **d5.6** · *major* — Delegation is bounded: termination conditions, no infinite loops.

## D6 · Guardrails — 10–15%

- **d6.1** · *critical* — Untrusted input is defended against prompt injection. Content is data, never instructions.
- **d6.2** · *critical* — Human-in-the-loop on irreversible / high-risk actions (money, delete, deploy, external send).
- **d6.3** · *major* — Outputs are validated before use (schema / allowlist).
- **d6.4** · *major* — Guardrails fail closed (deny by default) under uncertainty.
- **d6.5** · *major* — Input, tool-call, and output stages are all guarded. One guard leaves gaps.
- **d6.6** · *minor* — Sensitive actions are logged (actor, action, timestamp).
