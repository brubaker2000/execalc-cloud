from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Reflex:
    name: str
    description: str
    enabled: bool = True
    priority: int = 100


@dataclass(frozen=True)
class ReflexGateDecision:
    allowed_reflexes: List[str] = field(default_factory=list)
    denied_reflexes: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)


class ReflexRegistry:
    """
    Minimal Phase 1 scaffolding for Support Stack reflex registration.

    This is intentionally simple:
    - registry is in-memory
    - no tenant-specific policy yet
    - no advanced conflict handling yet
    """

    def __init__(self, reflexes: Optional[List[Reflex]] = None):
        self._reflexes = list(reflexes or [])

    def register(self, reflex: Reflex) -> None:
        self._reflexes.append(reflex)

    def all(self) -> List[Reflex]:
        return sorted(
            [r for r in self._reflexes if r.enabled],
            key=lambda r: (r.priority, r.name),
        )

    def gate(self) -> ReflexGateDecision:
        allowed = [r.name for r in self.all()]
        return ReflexGateDecision(
            allowed_reflexes=allowed,
            denied_reflexes=[],
            reasons=["phase1_default_allow"],
        )


@dataclass(frozen=True)
class ProcedureStep:
    name: str
    description: str


@dataclass(frozen=True)
class ProcedurePlan:
    steps: List[ProcedureStep] = field(default_factory=list)

    def step_names(self) -> List[str]:
        return [s.name for s in self.steps]


@dataclass(frozen=True)
class BoundaryCheck:
    name: str
    description: str


@dataclass(frozen=True)
class BoundaryDecision:
    allowed: bool
    reasons: List[str] = field(default_factory=list)
    checks: List[str] = field(default_factory=list)


def default_procedure_plan(*, active_reflexes: Optional[List[str]] = None) -> ProcedurePlan:
    active_reflexes = list(active_reflexes or [])

    steps = [
        ProcedureStep("validate_inputs", "Validate scenario structure and critical fields."),
    ]

    if "missing_critical_input" in active_reflexes:
        steps.append(
            ProcedureStep(
                "resolve_missing_critical_inputs",
                "Identify and resolve missing critical inputs before final commitment.",
            )
        )

    steps.extend(
        [
            ProcedureStep("assign_confidence", "Assign initial confidence from data completeness."),
            ProcedureStep("generate_tradeoffs", "Generate structured tradeoff analysis."),
            ProcedureStep("apply_prime_directive", "Generate Prime Directive assessments."),
            ProcedureStep("apply_polymorphia", "Generate Polymorphia fields."),
            ProcedureStep("build_artifact", "Assemble structured decision artifact output."),
        ]
    )

    return ProcedurePlan(steps=steps)


def default_boundary_decision(*, active_reflexes: Optional[List[str]] = None) -> BoundaryDecision:
    active_reflexes = list(active_reflexes or [])

    reasons = ["phase1_default_allow"]
    checks = ["tenant_scope_placeholder", "authorization_placeholder"]

    if "missing_critical_input" in active_reflexes:
        reasons.append("missing_critical_inputs_detected")
        checks.append("final_commitment_requires_input_resolution")

    return BoundaryDecision(
        allowed=True,
        reasons=reasons,
        checks=checks,
    )



def default_reflexes(*, missing_critical_fields: Optional[List[str]] = None) -> List[Reflex]:
    reflexes: List[Reflex] = []
    if missing_critical_fields:
        reflexes.append(
            Reflex(
                name="missing_critical_input",
                description="Detects missing critical inputs that materially reduce underwriting confidence.",
                priority=10,
            )
        )
    return reflexes


def support_stack_trace(*, missing_critical_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    registry = ReflexRegistry(default_reflexes(missing_critical_fields=missing_critical_fields))
    gate = registry.gate()
    plan = default_procedure_plan(active_reflexes=gate.allowed_reflexes)
    boundary = default_boundary_decision(active_reflexes=gate.allowed_reflexes)

    return {
        "reflex_gate": {
            "allowed_reflexes": gate.allowed_reflexes,
            "denied_reflexes": gate.denied_reflexes,
            "reasons": gate.reasons,
        },
        "procedure_plan": {
            "steps": plan.step_names(),
        },
        "boundary_decision": {
            "allowed": boundary.allowed,
            "reasons": boundary.reasons,
            "checks": boundary.checks,
        },
    }
