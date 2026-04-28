import unittest
from datetime import UTC, datetime, timedelta

from src.service.decision_loop.execution_boundary_engine import evaluate_execution_boundary
from src.service.decision_loop.models import ActionProposal, ExecutionSnapshot


class TestExecutionBoundaryEngine(unittest.TestCase):
    def _proposal(self, **overrides):
        base = dict(
            proposal_id="prop_001",
            tenant_id="tenant_test_001",
            user_id="test_user",
            action_type="send_offer",
            target_ref="deal_123",
            decision_envelope_id="env_123",
            issued_at=datetime(2026, 3, 20, 12, 0, tzinfo=UTC),
            expires_at=datetime(2026, 3, 20, 13, 0, tzinfo=UTC),
            authority_context={"role": "operator"},
            risk_level="medium",
            requires_human_review=False,
        )
        base.update(overrides)
        return ActionProposal(**base)

    def _snapshot(self, **overrides):
        base = dict(
            snapshot_time=datetime(2026, 3, 20, 12, 30, tzinfo=UTC),
            tenant_id="tenant_test_001",
            user_id="test_user",
            current_authority={"role": "operator"},
            current_state_hash="abc123",
            constraint_flags=[],
            policy_flags=[],
            required_inputs_present=True,
            risk_posture="normal",
            execution_window_open=True,
        )
        base.update(overrides)
        return ExecutionSnapshot(**base)

    def test_allow_when_all_checks_pass(self):
        decision = evaluate_execution_boundary(self._proposal(), self._snapshot())

        self.assertEqual(decision.status, "ALLOW")
        self.assertEqual(decision.blocking_checks, [])
        self.assertFalse(decision.requires_human_review)
        self.assertIn("execution_boundary_passed", decision.reasons)

    def test_block_when_proposal_expired(self):
        proposal = self._proposal(
            expires_at=datetime(2026, 3, 20, 12, 0, tzinfo=UTC),
        )
        snapshot = self._snapshot(
            snapshot_time=datetime(2026, 3, 20, 12, 1, tzinfo=UTC),
        )

        decision = evaluate_execution_boundary(proposal, snapshot)

        self.assertEqual(decision.status, "BLOCK")
        self.assertIn("proposal_expired", decision.reasons)
        self.assertIn("expiration_check", decision.blocking_checks)

    def test_block_when_authority_missing(self):
        snapshot = self._snapshot(current_authority={})

        decision = evaluate_execution_boundary(self._proposal(), snapshot)

        self.assertEqual(decision.status, "BLOCK")
        self.assertIn("missing_current_authority", decision.reasons)
        self.assertIn("authority_check", decision.blocking_checks)

    def test_block_when_policy_flag_present(self):
        snapshot = self._snapshot(policy_flags=["policy_block"])

        decision = evaluate_execution_boundary(self._proposal(), snapshot)

        self.assertEqual(decision.status, "BLOCK")
        self.assertIn("policy_block_present", decision.reasons)
        self.assertIn("policy_check", decision.blocking_checks)

    def test_recompute_when_required_inputs_missing(self):
        snapshot = self._snapshot(required_inputs_present=False)

        decision = evaluate_execution_boundary(self._proposal(), snapshot)

        self.assertEqual(decision.status, "RECOMPUTE")
        self.assertIn("required_inputs_missing_at_execution", decision.reasons)
        self.assertIn("required_inputs_check", decision.blocking_checks)

    def test_recompute_when_material_state_changed(self):
        snapshot = self._snapshot(constraint_flags=["state_changed"])

        decision = evaluate_execution_boundary(self._proposal(), snapshot)

        self.assertEqual(decision.status, "RECOMPUTE")
        self.assertIn("material_state_change_detected", decision.reasons)
        self.assertIn("state_change_check", decision.blocking_checks)

    def test_escalate_when_risk_posture_high(self):
        snapshot = self._snapshot(risk_posture="high")

        decision = evaluate_execution_boundary(self._proposal(), snapshot)

        self.assertEqual(decision.status, "ESCALATE")
        self.assertTrue(decision.requires_human_review)
        self.assertIn("risk_posture_requires_escalation", decision.reasons)
        self.assertIn("risk_posture_check", decision.blocking_checks)

    def test_escalate_when_proposal_requires_human_review(self):
        proposal = self._proposal(requires_human_review=True)

        decision = evaluate_execution_boundary(proposal, self._snapshot())

        self.assertEqual(decision.status, "ESCALATE")
        self.assertTrue(decision.requires_human_review)
        self.assertIn("proposal_marked_for_human_review", decision.reasons)
        self.assertIn("human_review_required", decision.blocking_checks)


if __name__ == "__main__":
    unittest.main()
