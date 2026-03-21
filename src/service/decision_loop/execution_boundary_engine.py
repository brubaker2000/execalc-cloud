from __future__ import annotations

from datetime import UTC, datetime
from typing import List

from src.service.decision_loop.models import (
    ActionProposal,
    BoundaryDecision,
    ExecutionSnapshot,
)


BLOCKING_POLICY_FLAGS = {
    "policy_block",
    "manual_approval_required",
}

BLOCKING_CONSTRAINT_FLAGS = {
    "hard_constraint",
    "execution_prohibited",
}

ELEVATED_RISK_POSTURES = {
    "elevated",
    "high",
    "critical",
}


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _proposal_expired(proposal: ActionProposal, snapshot: ExecutionSnapshot) -> bool:
    if proposal.expires_at is None:
        return False
    return snapshot.snapshot_time > proposal.expires_at


def _authority_missing(snapshot: ExecutionSnapshot) -> bool:
    return not bool(snapshot.current_authority)


def _material_state_changed(snapshot: ExecutionSnapshot) -> bool:
    return "state_changed" in snapshot.constraint_flags


def evaluate_execution_boundary(
    proposal: ActionProposal,
    snapshot: ExecutionSnapshot,
) -> BoundaryDecision:
    reasons: List[str] = []
    blocking_checks: List[str] = []

    if proposal.requires_human_review:
        reasons.append("proposal_marked_for_human_review")
        return BoundaryDecision(
            status="ESCALATE",
            reasons=reasons,
            blocking_checks=["human_review_required"],
            requires_human_review=True,
            audit_payload=_build_audit_payload(proposal, snapshot, "ESCALATE", reasons, ["human_review_required"]),
        )

    if _proposal_expired(proposal, snapshot):
        reasons.append("proposal_expired")
        blocking_checks.append("expiration_check")
        return BoundaryDecision(
            status="BLOCK",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "BLOCK", reasons, blocking_checks),
        )

    if _authority_missing(snapshot):
        reasons.append("missing_current_authority")
        blocking_checks.append("authority_check")
        return BoundaryDecision(
            status="BLOCK",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "BLOCK", reasons, blocking_checks),
        )

    if not snapshot.execution_window_open:
        reasons.append("execution_window_closed")
        blocking_checks.append("execution_window_check")
        return BoundaryDecision(
            status="BLOCK",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "BLOCK", reasons, blocking_checks),
        )

    if any(flag in BLOCKING_POLICY_FLAGS for flag in snapshot.policy_flags):
        reasons.append("policy_block_present")
        blocking_checks.append("policy_check")
        return BoundaryDecision(
            status="BLOCK",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "BLOCK", reasons, blocking_checks),
        )

    if any(flag in BLOCKING_CONSTRAINT_FLAGS for flag in snapshot.constraint_flags):
        reasons.append("hard_constraint_present")
        blocking_checks.append("constraint_check")
        return BoundaryDecision(
            status="BLOCK",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "BLOCK", reasons, blocking_checks),
        )

    if not snapshot.required_inputs_present:
        reasons.append("required_inputs_missing_at_execution")
        blocking_checks.append("required_inputs_check")
        return BoundaryDecision(
            status="RECOMPUTE",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "RECOMPUTE", reasons, blocking_checks),
        )

    if _material_state_changed(snapshot):
        reasons.append("material_state_change_detected")
        blocking_checks.append("state_change_check")
        return BoundaryDecision(
            status="RECOMPUTE",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=False,
            audit_payload=_build_audit_payload(proposal, snapshot, "RECOMPUTE", reasons, blocking_checks),
        )

    if snapshot.risk_posture.lower() in ELEVATED_RISK_POSTURES:
        reasons.append("risk_posture_requires_escalation")
        blocking_checks.append("risk_posture_check")
        return BoundaryDecision(
            status="ESCALATE",
            reasons=reasons,
            blocking_checks=blocking_checks,
            requires_human_review=True,
            audit_payload=_build_audit_payload(proposal, snapshot, "ESCALATE", reasons, blocking_checks),
        )

    reasons.append("execution_boundary_passed")
    return BoundaryDecision(
        status="ALLOW",
        reasons=reasons,
        blocking_checks=[],
        requires_human_review=False,
        audit_payload=_build_audit_payload(proposal, snapshot, "ALLOW", reasons, []),
    )


def _build_audit_payload(
    proposal: ActionProposal,
    snapshot: ExecutionSnapshot,
    status: str,
    reasons: List[str],
    blocking_checks: List[str],
) -> dict:
    return {
        "proposal_id": proposal.proposal_id,
        "decision_envelope_id": proposal.decision_envelope_id,
        "tenant_id": proposal.tenant_id,
        "user_id": proposal.user_id,
        "action_type": proposal.action_type,
        "target_ref": proposal.target_ref,
        "proposal_risk_level": proposal.risk_level,
        "snapshot_time": snapshot.snapshot_time.isoformat(),
        "snapshot_tenant_id": snapshot.tenant_id,
        "snapshot_user_id": snapshot.user_id,
        "constraint_flags": list(snapshot.constraint_flags),
        "policy_flags": list(snapshot.policy_flags),
        "required_inputs_present": snapshot.required_inputs_present,
        "risk_posture": snapshot.risk_posture,
        "execution_window_open": snapshot.execution_window_open,
        "status": status,
        "reasons": list(reasons),
        "blocking_checks": list(blocking_checks),
        "evaluated_at": _utc_now().isoformat(),
    }
