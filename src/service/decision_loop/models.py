from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

Confidence = Literal["high", "medium", "low", "unknown"]


@dataclass(frozen=True)
class Scenario:
    scenario_type: str
    governing_objective: str
    prompt: str
    facts: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    requested_depth: str = "standard"


@dataclass(frozen=True)
class SensitivityVariable:
    name: str
    impact: str  # plain language directional impact


@dataclass(frozen=True)
class DecisionArtifact:
    """
    Canonical structured runtime output for the current decision loop.

    This is the implementation-facing bridge toward the broader runtime object
    model, where DecisionArtifact is the named output object.
    """
    executive_summary: str
    confidence: Confidence
    confidence_rationale: List[str]
    governing_objective: str
    tradeoffs: Dict[str, List[str]]  # keys: upside/downside/key_tradeoffs/asymmetry
    sensitivity: List[SensitivityVariable]
    next_actions: List[str]
    audit: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": True,
            "report": {
                "executive_summary": self.executive_summary,
                "confidence": self.confidence,
                "confidence_rationale": self.confidence_rationale,
                "governing_objective": self.governing_objective,
                "tradeoffs": self.tradeoffs,
                "sensitivity": [{"name": s.name, "impact": s.impact} for s in self.sensitivity],
                "next_actions": self.next_actions,
            },
            "audit": self.audit,
        }


# Backward-compatible alias while callers and API surfaces still refer to the
# stage-specific name.
DecisionReport = DecisionArtifact
