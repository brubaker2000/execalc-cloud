import unittest

from src.service.decision_loop.service import run_decision_service
from src.service.execution_record import ExecutionRecord


class TestDecisionService(unittest.TestCase):
    def test_run_decision_service_returns_api_ready_payload(self):
        persisted_records = []

        def persist_fn(record: ExecutionRecord):
            persisted_records.append(record)
            return {"persisted": True, "persist_table": "execution_records"}

        out = run_decision_service(
            tenant_id="tenant_test_001",
            user_id="test_user",
            scenario_in={
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
            },
            persist_fn=persist_fn,
        )

        self.assertTrue(out["ok"])
        self.assertIn("report", out)
        self.assertIn("audit", out)
        self.assertEqual(out["audit"]["tenant_id"], "tenant_test_001")
        self.assertEqual(out["audit"]["user_id"], "test_user")
        self.assertEqual(out["audit"]["scenario_type"], "draft_trade")
        self.assertIn("envelope_id", out["audit"])
        self.assertEqual(out["audit"]["persist"]["persisted"], True)

        self.assertEqual(len(persisted_records), 1)
        self.assertEqual(persisted_records[0].tenant_id, "tenant_test_001")
        self.assertEqual(persisted_records[0].result["report"]["governing_objective"], "cut_payroll")

    def test_run_decision_service_rejects_non_object_scenario(self):
        def persist_fn(record: ExecutionRecord):
            return {"persisted": True}

        with self.assertRaises(ValueError) as ctx:
            run_decision_service(
                tenant_id="tenant_test_001",
                user_id="test_user",
                scenario_in="not-an-object",
                persist_fn=persist_fn,
            )

        self.assertEqual(str(ctx.exception), "scenario must be an object")

    def test_run_decision_service_rejects_non_object_facts(self):
        def persist_fn(record: ExecutionRecord):
            return {"persisted": True}

        with self.assertRaises(ValueError) as ctx:
            run_decision_service(
                tenant_id="tenant_test_001",
                user_id="test_user",
                scenario_in={
                    "scenario_type": "draft_trade",
                    "governing_objective": "cut_payroll",
                    "prompt": "bad facts",
                    "facts": ["not", "a", "dict"],
                },
                persist_fn=persist_fn,
            )

        self.assertEqual(str(ctx.exception), "facts must be an object")


if __name__ == "__main__":
    unittest.main()
