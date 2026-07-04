"""D1 — Architecture & SDLC (exam weight 15-20%)."""

from agent_audit.model import Check, Domain

DOMAIN = Domain(
    id="D1",
    name="Architecture & SDLC",
    weight="15-20%",
    checks=[
        Check(
            "d1.1", "Explicit task contract (goal, inputs, success criteria, done)",
            "major",
            "Define a written contract the agent commits to; without it, success is unverifiable.",
        ),
        Check(
            "d1.2", "Agent plans and decomposes before acting",
            "major",
            "Add a planning step; break multi-step work into verifiable sub-steps.",
        ),
        Check(
            "d1.3", "Autonomy tier is appropriate and not over-engineered",
            "minor",
            "Use the simplest tier that solves the task; reserve full agents for open-ended work.",
        ),
        Check(
            "d1.4", "Control flow is code-orchestrated where possible",
            "major",
            "Move loops and branching into code; let the model handle judgment, not plumbing.",
        ),
        Check(
            "d1.5", "Steps are idempotent / recoverable after failure",
            "major",
            "Add checkpoints and idempotency so a crash does not corrupt state.",
        ),
        Check(
            "d1.6", "Agent config is versioned and reproducible",
            "minor",
            "Pin model IDs and keep prompts in version control for reproducible runs.",
        ),
    ],
)
