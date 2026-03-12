import os
import unittest

import src.service.api as api


class TestDecisionAPI(unittest.TestCase):
    def setUp(self):
        self._prev_harness = os.environ.get("EXECALC_DEV_HARNESS")
        self._prev_persist = os.environ.get("EXECALC_PERSIST_EXECUTIONS")
        os.environ["EXECALC_DEV_HARNESS"] = "1"
        os.environ["EXECALC_PERSIST_EXECUTIONS"] = "0"

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

        if self._prev_persist is None:
            os.environ.pop("EXECALC_PERSIST_EXECUTIONS", None)
        else:
            os.environ["EXECALC_PERSIST_EXECUTIONS"] = self._prev_persist

    def test_decision_run_returns_structured_report(self):
        resp = self.client.post(
            "/decision/run",
            headers=self.headers,
            json={
                "scenario": {
                    "scenario_type": "draft_trade",
                    "governing_objective": "cut_payroll",
                    "prompt": "Pick 8 vs 18 trade-down scenario under payroll mandate",
                    "facts": {"you_pick": 8, "counterparty_pick": 18},
                    "constraints": {"cap_pressure": True},
                    "decision_horizon": "current season",
                    "stakeholder_scope": "gm, coach, ownership",
                    "risk_surface": "medium",
                    "assumptions": "counterparty is motivated",
                    "decision_notes": "Need flexibility without giving away too much upside",
                }
            },
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()

        self.assertTrue(body["ok"])
        self.assertIn("report", body)
        self.assertIn("audit", body)

        report = body["report"]
        audit = body["audit"]

        self.assertEqual(report["governing_objective"], "cut_payroll")
        self.assertIn("value_assessment", report)
        self.assertIn("risk_reward_assessment", report)
        self.assertIn("supply_demand_assessment", report)
        self.assertIn("asset_assessment", report)
        self.assertIn("liability_assessment", report)
        self.assertIn("actors", report)
        self.assertIn("incentives", report)
        self.assertIn("asymmetries", report)
        self.assertIn("execution_trace", report)

        self.assertEqual(audit["tenant_id"], "tenant_test_001")
        self.assertEqual(audit["user_id"], "test_user")
        self.assertEqual(audit["scenario_type"], "draft_trade")
        self.assertEqual(audit["governing_objective"], "cut_payroll")
        self.assertIn("envelope_id", audit)
        self.assertIn("persist", audit)

    def test_decision_run_rejects_non_object_scenario(self):
        resp = self.client.post(
            "/decision/run",
            headers=self.headers,
            json={"scenario": "not-an-object"},
        )
        self.assertEqual(resp.status_code, 400)
        body = resp.get_json()
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"], "scenario must be an object")

    def test_decision_run_rejects_non_object_facts(self):
        resp = self.client.post(
            "/decision/run",
            headers=self.headers,
            json={
                "scenario": {
                    "scenario_type": "draft_trade",
                    "governing_objective": "cut_payroll",
                    "prompt": "bad facts",
                    "facts": ["not", "a", "dict"],
                }
            },
        )
        self.assertEqual(resp.status_code, 400)
        body = resp.get_json()
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"], "facts must be an object")


if __name__ == "__main__":
    unittest.main()
