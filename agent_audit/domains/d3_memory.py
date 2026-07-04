"""D3 — Memory (exam weight 10-15%)."""

from agent_audit.model import Check, Domain

DOMAIN = Domain(
    id="D3",
    name="Memory",
    weight="10-15%",
    checks=[
        Check(
            "d3.1", "Short-term context is bounded (summarization / compaction)",
            "major",
            "Compact or summarize long histories; unbounded context degrades quality and cost.",
        ),
        Check(
            "d3.2", "Durable memory is separated from transient working state",
            "minor",
            "Keep static knowledge and live run-state in different stores.",
        ),
        Check(
            "d3.3", "Retrieved memory is grounded and cited",
            "major",
            "Ground answers in retrieved sources and surface citations; guard against fabricated recall.",
        ),
        Check(
            "d3.4", "Stored memory is filtered for lasting relevance",
            "minor",
            "Store evergreen facts; keep pointers to transactional data instead of ingesting the noise.",
        ),
        Check(
            "d3.5", "Volatile / stale facts are re-verified before being trusted",
            "major",
            "Flag time-sensitive facts and re-check them before relying on them.",
        ),
        Check(
            "d3.6", "Memory is scoped so no data leaks across users / sessions",
            "critical",
            "Isolate memory per user and session; prevent cross-tenant leakage.",
        ),
    ],
)
