from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict, List, Literal, Optional

Confidence = Literal["high", "medium", "low", "unknown"]


@dataclass(frozen=True)
class Scenario:
    scenario_type: str
    governing_objective: str
    prompt: str
    facts: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    requested_depth: str = "standard"

    # Expanded decision-context fields
    decision_horizon: Optional[str] = None
    stakeholder_scope: Optional[str] = None
    risk_surface: Optional[str] = None
    assumptions: Optional[str] = None
    decision_notes: Optional[str] = None

    # Incremental alignment with the canonical runtime object model.
    scenario_id: Optional[str] = None
    tenant_id: Optional[str] = None
    operator_id: Optional[str] = None
    domain: Optional[str] = None
    urgency: Optional[str] = None
    source_surface: Optional[str] = None
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    chat_id: Optional[str] = None
    thread_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class SensitivityVariable:
    name: str
    impact: str  # plain language directional impact


@dataclass(frozen=True)
class DecisionReport:
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

    # Prime Directive
    value_assessment: str
    risk_reward_assessment: str
    supply_demand_assessment: str
    asset_assessment: str
    liability_assessment: str

    # Polymorphia
    actors: List[str]
    incentives: List[str]
    asymmetries: List[str]

    # Support / execution trace
    execution_trace: Dict[str, Any]

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
                "value_assessment": self.value_assessment,
                "risk_reward_assessment": self.risk_reward_assessment,
                "supply_demand_assessment": self.supply_demand_assessment,
                "asset_assessment": self.asset_assessment,
                "liability_assessment": self.liability_assessment,
                "actors": self.actors,
                "incentives": self.incentives,
                "asymmetries": self.asymmetries,
                "execution_trace": self.execution_trace,
            },
            "audit": self.audit,
        }



BoundaryStatus = Literal["ALLOW", "BLOCK", "RECOMPUTE", "ESCALATE"]


@dataclass(frozen=True)
class ActionProposal:
    proposal_id: str
    tenant_id: str
    user_id: str
    action_type: str
    target_ref: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    decision_envelope_id: Optional[str] = None
    issued_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: Optional[datetime] = None
    authority_context: Dict[str, Any] = field(default_factory=dict)
    risk_level: str = "unknown"
    requires_human_review: bool = False


@dataclass(frozen=True)
class ExecutionSnapshot:
    snapshot_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    tenant_id: str = ""
    user_id: str = ""
    current_authority: Dict[str, Any] = field(default_factory=dict)
    current_state_hash: Optional[str] = None
    constraint_flags: List[str] = field(default_factory=list)
    policy_flags: List[str] = field(default_factory=list)
    required_inputs_present: bool = True
    risk_posture: str = "normal"
    execution_window_open: bool = True


@dataclass(frozen=True)
class BoundaryDecision:
    status: BoundaryStatus
    reasons: List[str] = field(default_factory=list)
    blocking_checks: List[str] = field(default_factory=list)
    requires_human_review: bool = False
    audit_payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "reasons": self.reasons,
            "blocking_checks": self.blocking_checks,
            "requires_human_review": self.requires_human_review,
            "audit_payload": self.audit_payload,
        }

# Backward-compatible aliases while callers and API surfaces still refer to the
# stage-specific or older names.
DecisionArtifact = DecisionReport
