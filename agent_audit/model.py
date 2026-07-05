"""Core data model shared by the checklist, the report renderer, and the engine."""

from __future__ import annotations

from dataclasses import dataclass, field

# Severity ordering, worst first. Used to sort findings and pick display labels.
SEVERITY_ORDER = ("critical", "major", "minor")
SEVERITY_LABEL = {"critical": "CRITICAL", "major": "MAJOR", "minor": "MINOR"}


@dataclass(frozen=True)
class Check:
    """One audit criterion within a domain.

    `severity` is the severity a *failed* check is reported at — it encodes how
    much this criterion matters, independent of any specific target.
    """

    id: str
    title: str
    severity: str
    guidance: str

    def __post_init__(self) -> None:
        if self.severity not in SEVERITY_ORDER:
            raise ValueError(f"{self.id}: bad severity {self.severity!r}")


@dataclass(frozen=True)
class Domain:
    """A GH-600 competency domain and its checks."""

    id: str
    name: str
    weight: str  # exam weight range, informational only
    checks: list[Check] = field(default_factory=list)


@dataclass(frozen=True)
class Finding:
    """The result of evaluating one check against a target (produced by the engine)."""

    check: Check
    passed: bool
    evidence: str = ""  # where/why, e.g. "engine.py:88"
    applicable: bool = True  # False = no relevant code to assess (excluded from score)
