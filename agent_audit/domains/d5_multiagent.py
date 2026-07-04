"""D5 — Multi-agent orchestration (exam weight 15-20%)."""

from agent_audit.model import Check, Domain

DOMAIN = Domain(
    id="D5",
    name="Multi-agent orchestration",
    weight="15-20%",
    checks=[
        Check(
            "d5.1", "Each agent has a clear, bounded role",
            "major",
            "Give each agent one responsibility with a defined interface; avoid do-everything agents.",
        ),
        Check(
            "d5.2", "An explicit coordination mechanism is defined",
            "major",
            "Choose and document how agents coordinate (orchestrator, blackboard, hand-off).",
        ),
        Check(
            "d5.3", "Agents run with least authority and isolated scope",
            "critical",
            "Each agent gets only the tools and data its role needs; isolate the blast radius.",
        ),
        Check(
            "d5.4", "Hand-off contracts are explicit",
            "minor",
            "Define the payload each hand-off carries; do not pass full context by default.",
        ),
        Check(
            "d5.5", "Multi-agent complexity is justified over a single agent",
            "minor",
            "Prefer one agent unless parallelism or specialization genuinely pays off.",
        ),
        Check(
            "d5.6", "Delegation is bounded (termination conditions, no infinite loops)",
            "major",
            "Cap delegation depth and define stop conditions.",
        ),
    ],
)
