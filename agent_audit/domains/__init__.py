"""The six GH-600 competency domains, in exam order."""

from agent_audit.domains import (
    d1_architecture,
    d2_tools,
    d3_memory,
    d4_evaluation,
    d5_multiagent,
    d6_guardrails,
)

ALL_DOMAINS = [
    d1_architecture.DOMAIN,
    d2_tools.DOMAIN,
    d3_memory.DOMAIN,
    d4_evaluation.DOMAIN,
    d5_multiagent.DOMAIN,
    d6_guardrails.DOMAIN,
]

TOTAL_CHECKS = sum(len(d.checks) for d in ALL_DOMAINS)
