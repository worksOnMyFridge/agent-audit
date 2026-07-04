"""D6 — Guardrails (exam weight 10-15%)."""

from agent_audit.model import Check, Domain

DOMAIN = Domain(
    id="D6",
    name="Guardrails",
    weight="10-15%",
    checks=[
        Check(
            "d6.1", "Untrusted input is defended against prompt injection",
            "critical",
            "Sanitize and isolate untrusted content as data; never let it become instructions.",
        ),
        Check(
            "d6.2", "Human-in-the-loop on irreversible / high-risk actions",
            "critical",
            "Require confirmation before actions that move money, delete, deploy, or send externally.",
        ),
        Check(
            "d6.3", "Outputs are validated before use (schema / allowlist)",
            "major",
            "Validate the structure and content of model output before acting on it.",
        ),
        Check(
            "d6.4", "Guardrails fail closed (deny by default) under uncertainty",
            "major",
            "On ambiguity or error, refuse rather than proceed.",
        ),
        Check(
            "d6.5", "Input, tool-call, and output stages are all guarded",
            "major",
            "Cover all three chokepoints; a single guard leaves gaps.",
        ),
        Check(
            "d6.6", "Sensitive actions are logged (actor, action, timestamp)",
            "minor",
            "Record an audit trail for accountability and incident review.",
        ),
    ],
)
