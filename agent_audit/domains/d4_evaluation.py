"""D4 — Evaluation (exam weight 15-20%)."""

from agent_audit.model import Check, Domain

DOMAIN = Domain(
    id="D4",
    name="Evaluation",
    weight="15-20%",
    checks=[
        Check(
            "d4.1", "An evaluation set / test cases exist (not manual vibes)",
            "major",
            "Build a labeled eval set that encodes what 'good' means for the task.",
        ),
        Check(
            "d4.2", "Evaluated offline before deploy and monitored online after",
            "major",
            "Gate releases on offline evals; monitor live outcomes in production.",
        ),
        Check(
            "d4.3", "Metrics are tied to task success, not surface plausibility",
            "major",
            "Measure task completion and correctness, not just whether output looks reasonable.",
        ),
        Check(
            "d4.4", "Prompt / model / tool changes run against regression tests",
            "major",
            "Re-run the eval set on every change to catch silent regressions.",
        ),
        Check(
            "d4.5", "LLM-as-judge is robust (diverse judges, no correlated blind spots)",
            "minor",
            "Vary judge models and prompts; a single judge shares the generator's blind spots.",
        ),
        Check(
            "d4.6", "Failures are logged and fed back into the eval set",
            "minor",
            "Capture production failures and grow the eval set from them.",
        ),
    ],
)
