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


def default_procedure_plan() -> ProcedurePlan:
    return ProcedurePlan(
        steps=[
            ProcedureStep("validate_inputs", "Validate scenario structure and critical fields."),
            ProcedureStep("assign_confidence", "Assign initial confidence from data completeness."),
            ProcedureStep("generate_tradeoffs", "Generate structured tradeoff analysis."),
            ProcedureStep("apply_prime_directive", "Generate Prime Directive assessments."),
            ProcedureStep("apply_polymorphia", "Generate Polymorphia fields."),
            ProcedureStep("build_artifact", "Assemble structured decision artifact output."),
        ]
    )


def default_boundary_decision() -> BoundaryDecision:
    return BoundaryDecision(
        allowed=True,
        reasons=["phase1_default_allow"],
        checks=["tenant_scope_placeholder", "authorization_placeholder"],
    )


def support_stack_trace() -> Dict[str, Any]:
    registry = ReflexRegistry()
    gate = registry.gate()
    plan = default_procedure_plan()
    boundary = default_boundary_decision()

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
