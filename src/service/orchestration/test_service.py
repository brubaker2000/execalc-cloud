import unittest

from src.service.orchestration.service import run_orchestration


class TestOrchestrationService(unittest.TestCase):
    def test_decision_seeking_turn_routes_to_decision_path(self):
        out = run_orchestration(user_text="What should we do?")
        self.assertTrue(out["ok"])
        self.assertEqual(out["turn_class"], "decision_seeking")
        self.assertIsNotNone(out["decision_result"])
        self.assertIsNone(out["action_proposal"])
        self.assertIsNotNone(out["execution_boundary_result"])
        self.assertEqual(out["execution_boundary_result"]["status"], "ALLOW")
        self.assertEqual(out["rail_state"]["mode"], "decision")

    def test_action_proposing_turn_emits_shared_action_proposal_fields(self):
        out = run_orchestration(user_text="Draft the next move.")
        self.assertTrue(out["ok"])
        self.assertEqual(out["turn_class"], "action_proposing")
        self.assertIsNotNone(out["action_proposal"])
        self.assertEqual(out["action_proposal"]["action_type"], "proposed_action")
        self.assertEqual(out["action_proposal"]["tenant_id"], "tenant_test_001")
        self.assertEqual(out["action_proposal"]["user_id"], "test_user")
        self.assertEqual(
            out["action_proposal"]["decision_envelope_id"],
            out["scenario"]["scenario_id"],
        )
        self.assertEqual(out["action_proposal"]["risk_level"], "unknown")
        self.assertFalse(out["action_proposal"]["requires_human_review"])
        self.assertIsNone(out["execution_boundary_result"])
        self.assertEqual(out["rail_state"]["mode"], "action_proposal")

    def test_execution_seeking_turn_requires_boundary_review(self):
        out = run_orchestration(user_text="Go ahead.")
        self.assertTrue(out["ok"])
        self.assertEqual(out["turn_class"], "execution_seeking")
        self.assertIsNotNone(out["action_proposal"])
        self.assertEqual(out["action_proposal"]["tenant_id"], "tenant_test_001")
        self.assertEqual(out["action_proposal"]["user_id"], "test_user")
        self.assertEqual(
            out["action_proposal"]["decision_envelope_id"],
            out["scenario"]["scenario_id"],
        )
        self.assertEqual(out["action_proposal"]["risk_level"], "elevated")
        self.assertTrue(out["action_proposal"]["requires_human_review"])
        self.assertIsNotNone(out["execution_boundary_result"])
        self.assertEqual(out["execution_boundary_result"]["status"], "ESCALATE")
        self.assertEqual(out["rail_state"]["mode"], "execution_review")

    def test_conversational_turn_does_not_create_execution_state(self):
        out = run_orchestration(user_text="Talk this through with me.")
        self.assertTrue(out["ok"])
        self.assertEqual(out["turn_class"], "conversational")
        self.assertIsNone(out["decision_result"])
        self.assertIsNone(out["action_proposal"])
        self.assertIsNone(out["execution_boundary_result"])
        self.assertEqual(out["rail_state"]["mode"], "conversation")


if __name__ == "__main__":
    unittest.main()
