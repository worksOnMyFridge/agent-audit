# Example — auditing a support-ticket agent

This is illustrative output from the v0.2 engine, auditing a hypothetical
customer-support agent that reads tickets, drafts replies, and can issue
refunds via a `billing` tool.

```
Agent Audit - ./support-agent
Score: 58/100 | 3 critical | 4 major | 2 minor

D2
  [CRITICAL] Each tool has least-privilege scope (tools/billing.py:14)
    -> The billing tool holds full refund + charge scope for a drafting task.
  [CRITICAL] Secrets are kept out of code and loaded from env (config.py:7)
    -> STRIPE_KEY is hardcoded. Load from env and remove from history.
  [MAJOR] Tool failures are handled (agent.py:132)
    -> billing calls have no timeout or retry; a hung API stalls the run.

D3
  [MAJOR] Short-term context is bounded (memory.py:20)
    -> Full ticket history is appended every turn; context grows unbounded.

D6
  [CRITICAL] Human-in-the-loop on irreversible actions (agent.py:88)
    -> Refunds execute with no approval step. Gate refunds behind confirmation.
  [MAJOR] Untrusted input is defended against prompt injection (agent.py:61)
    -> Ticket text is concatenated into the system prompt. Isolate it as data.
  [MAJOR] Guardrails fail closed under uncertainty (agent.py:150)
    -> On classifier error the agent proceeds with a refund. Default to deny.

D4
  [MINOR] An evaluation set exists
    -> No eval harness found. Add labeled cases for reply quality + refund calls.

D1
  [MINOR] Explicit task contract
    -> Goal and done-definition are implicit. Write them down.
```

**Reading it:** the two ship-blockers are the un-gated refund (`D6`) and the
over-privileged billing tool (`D2`) — a prompt-injected ticket could talk the
agent into issuing a refund. Fix those before anything else.
