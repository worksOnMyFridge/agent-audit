"""D2 — Tools, MCP & environment (exam weight 20-25%)."""

from agent_audit.model import Check, Domain

DOMAIN = Domain(
    id="D2",
    name="Tools, MCP & environment",
    weight="20-25%",
    checks=[
        Check(
            "d2.1", "Each tool has least-privilege scope",
            "critical",
            "Scope tools tightly; a read task should not hold write or delete power.",
        ),
        Check(
            "d2.2", "Tools have clear descriptions and typed input schemas",
            "major",
            "Give each tool a precise description and JSON schema so the model calls it correctly.",
        ),
        Check(
            "d2.3", "Third-party MCP servers are vetted and pinned",
            "major",
            "Review external MCP code and permissions before connecting; pin versions.",
        ),
        Check(
            "d2.4", "Tool execution is sandboxed / isolated (esp. code or shell)",
            "critical",
            "Run code-executing or untrusted tools in an isolated sandbox with resource limits.",
        ),
        Check(
            "d2.5", "Tool failures are handled (timeouts, bounded retries, degradation)",
            "major",
            "Wrap tool calls with timeouts, bounded retries, and explicit failure paths.",
        ),
        Check(
            "d2.6", "Secrets are kept out of code and loaded from env / secret store",
            "critical",
            "Never hardcode keys; load from env or a secret manager; keep them out of version control.",
        ),
    ],
)
