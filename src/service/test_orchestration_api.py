import os
import unittest

import src.service.api as api


class TestOrchestrationAPI(unittest.TestCase):
    def setUp(self):
        self._prev_harness = os.environ.get("EXECALC_DEV_HARNESS")
        os.environ["EXECALC_DEV_HARNESS"] = "1"

        self.client = api.app.test_client()
        self.headers = {
            "X-User-Id": "test_user",
            "X-Role": "operator",
            "X-Tenant-Id": "tenant_test_001",
        }

    def tearDown(self):
        if self._prev_harness is None:
            os.environ.pop("EXECALC_DEV_HARNESS", None)
        else:
            os.environ["EXECALC_DEV_HARNESS"] = self._prev_harness

    def test_orchestration_run_decision_turn(self):
        response = self.client.post(
            "/orchestration/run",
            json={"user_text": "What should we do?"},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["turn_class"], "decision_seeking")
        self.assertEqual(body["rail_state"]["mode"], "decision")
        self.assertEqual(body["scenario"]["navigation"]["workspace_id"], "workspace_default")
        self.assertIsNone(body["scenario"]["navigation"]["project_id"])
        self.assertIsNone(body["scenario"]["navigation"]["chat_id"])
        self.assertIsNone(body["scenario"]["navigation"]["thread_id"])

    def test_orchestration_run_action_turn(self):
        response = self.client.post(
            "/orchestration/run",
            json={"user_text": "Draft the next move."},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["turn_class"], "action_proposing")
        self.assertEqual(body["action_proposal"]["tenant_id"], "tenant_test_001")
        self.assertEqual(body["action_proposal"]["user_id"], "test_user")
        self.assertEqual(body["rail_state"]["mode"], "action_proposal")

    def test_orchestration_run_execution_turn(self):
        response = self.client.post(
            "/orchestration/run",
            json={"user_text": "Go ahead."},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["turn_class"], "execution_seeking")
        self.assertEqual(body["execution_boundary_result"]["status"], "ALLOW")
        self.assertTrue(body["action_proposal"]["requires_human_review"])
        self.assertEqual(body["rail_state"]["mode"], "execution_review")

    def test_orchestration_run_requires_user_text(self):
        response = self.client.post(
            "/orchestration/run",
            json={},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)
        body = response.get_json()
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"], "user_text is required")


if __name__ == "__main__":
    unittest.main()
