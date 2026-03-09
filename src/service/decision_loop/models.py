from dataclasses import dataclass
from typing import Any, Dict, List

# Other imports and code if necessary

@dataclass(frozen=True)
class DecisionArtifact:
    """
    Canonical structured runtime output for the current decision loop.
    This is the implementation-facing bridge toward the broader runtime object
    model, where DecisionArtifact is the named output object.
    """

    # Existing fields in your schema (replace this with the original fields you already had)
    executive_summary: str
    confidence: str  # Adjust based on your type, assuming it's a string
    confidence_rationale: List[str]
    governing_objective: str
    tradeoffs: Dict[str, List[str]]  # keys: upside/downside/key_tradeoffs/asymmetry
    sensitivity: List[str]  # Adjust based on your type, assuming it's a list of strings
    next_actions: List[str]
    audit: Dict[str, Any]

    # New fields for Prime Directive & Balance Sheet Logic
    value_assessment: str  # For value creation/destruction
    risk_reward_assessment: str  # For risk/reward analysis
    supply_demand_assessment: str  # For supply/demand dynamics
    asset_assessment: str  # For asset evaluation
    liability_assessment: str  # For liability evaluation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": True,
            "report": {
                "executive_summary": self.executive_summary,
                "confidence": self.confidence,
                "confidence_rationale": self.confidence_rationale,
                "governing_objective": self.governing_objective,
                "tradeoffs": self.tradeoffs,
                "sensitivity": self.sensitivity,
                "next_actions": self.next_actions,
                # New fields added for the Prime Directive logic
                "value_assessment": self.value_assessment,
                "risk_reward_assessment": self.risk_reward_assessment,
                "supply_demand_assessment": self.supply_demand_assessment,
                "asset_assessment": self.asset_assessment,
                "liability_assessment": self.liability_assessment,
            },
        }
