import unittest

from src.service.decision_loop.service import (
    get_decision_service,
    list_recent_decisions_service,
    run_decision_service,
)
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

    def test_get_decision_service_rejects_invalid_envelope_id(self):
        out, status = get_decision_service(
            tenant_id="tenant_test_001",
            envelope_id="bad!",
            persist_enabled=True,
            get_record_fn=lambda **kwargs: None,
        )

        self.assertEqual(status, 400)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "invalid envelope_id")

    def test_get_decision_service_returns_not_found_when_persistence_disabled(self):
        out, status = get_decision_service(
            tenant_id="tenant_test_001",
            envelope_id="abcdef0123456789",
            persist_enabled=False,
            get_record_fn=lambda **kwargs: None,
        )

        self.assertEqual(status, 404)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "not_found")

    def test_get_decision_service_returns_db_unavailable_when_reader_missing(self):
        out, status = get_decision_service(
            tenant_id="tenant_test_001",
            envelope_id="abcdef0123456789",
            persist_enabled=True,
            get_record_fn=None,
        )

        self.assertEqual(status, 503)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "db_unavailable")

    def test_get_decision_service_returns_record_payload(self):
        def get_record_fn(**kwargs):
            self.assertEqual(kwargs["tenant_id"], "tenant_test_001")
            self.assertEqual(kwargs["envelope_id"], "abcdef0123456789")
            return {
                "tenant_id": "tenant_test_001",
                "envelope_id": "abcdef0123456789",
                "ok": True,
                "result": {"ok": True, "report": {"governing_objective": "cut_payroll"}},
                "created_at": "2026-03-12T00:00:00+00:00",
            }

        out, status = get_decision_service(
            tenant_id="tenant_test_001",
            envelope_id="abcdef0123456789",
            persist_enabled=True,
            get_record_fn=get_record_fn,
        )

        self.assertEqual(status, 200)
        self.assertTrue(out["ok"])
        self.assertEqual(out["envelope_id"], "abcdef0123456789")
        self.assertEqual(out["created_at"], "2026-03-12T00:00:00+00:00")
        self.assertIn("result", out)

    def test_list_recent_decisions_service_rejects_non_integer_limit(self):
        out, status = list_recent_decisions_service(
            tenant_id="tenant_test_001",
            raw_limit="abc",
            persist_enabled=True,
            list_records_fn=lambda **kwargs: [],
        )

        self.assertEqual(status, 400)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "limit must be an integer")

    def test_list_recent_decisions_service_returns_empty_when_persistence_disabled(self):
        out, status = list_recent_decisions_service(
            tenant_id="tenant_test_001",
            raw_limit="25",
            persist_enabled=False,
            list_records_fn=lambda **kwargs: [{"unexpected": True}],
        )

        self.assertEqual(status, 200)
        self.assertTrue(out["ok"])
        self.assertEqual(out["records"], [])
        self.assertEqual(out["persist_enabled"], False)

    def test_list_recent_decisions_service_returns_db_unavailable_when_reader_missing(self):
        out, status = list_recent_decisions_service(
            tenant_id="tenant_test_001",
            raw_limit="25",
            persist_enabled=True,
            list_records_fn=None,
        )

        self.assertEqual(status, 503)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "db_unavailable")

    def test_list_recent_decisions_service_clamps_limit_and_returns_rows(self):
        def list_records_fn(**kwargs):
            self.assertEqual(kwargs["tenant_id"], "tenant_test_001")
            self.assertEqual(kwargs["limit"], 100)
            return [
                {
                    "tenant_id": "tenant_test_001",
                    "envelope_id": "entry_2",
                    "ok": True,
                    "created_at": "2026-03-12T00:00:00+00:00",
                }
            ]

        out, status = list_recent_decisions_service(
            tenant_id="tenant_test_001",
            raw_limit="500",
            persist_enabled=True,
            list_records_fn=list_records_fn,
        )

        self.assertEqual(status, 200)
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["records"]), 1)
        self.assertEqual(out["persist_enabled"], True)


if __name__ == "__main__":
    unittest.main()
