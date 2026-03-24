import unittest

from src.service.decision_loop.service import (
    compare_decisions_service,
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
        self.assertIn("execution_boundary", out)
        self.assertEqual(out["execution_boundary"]["status"], "ALLOW")
        self.assertIn("execution_boundary", out["audit"])
        self.assertEqual(
            out["audit"]["execution_boundary"]["status"],
            out["execution_boundary"]["status"],
        )
        self.assertEqual(out["audit"]["tenant_id"], "tenant_test_001")
        self.assertEqual(out["audit"]["user_id"], "test_user")
        self.assertEqual(out["audit"]["scenario_type"], "draft_trade")
        self.assertIn("envelope_id", out["audit"])
        self.assertEqual(out["audit"]["persist"]["persisted"], True)
        self.assertIn("stability", out["audit"])
        self.assertEqual(out["audit"]["stability"]["mode"], "observe_only")
        self.assertIn("drift", out["audit"])
        self.assertEqual(out["audit"]["drift"]["mode"], "observe_only")
        self.assertEqual(out["audit"]["stability"]["registry_version"], "stage8b.2")
        self.assertIn("decision_result", out["audit"]["stability"]["invariants"])
        self.assertIn("action_proposal", out["audit"]["stability"]["invariants"])
        self.assertIn("execution_snapshot", out["audit"]["stability"]["invariants"])

        self.assertEqual(len(persisted_records), 1)
        self.assertEqual(persisted_records[0].tenant_id, "tenant_test_001")
        self.assertEqual(
            persisted_records[0].result["report"]["governing_objective"],
            "cut_payroll",
        )

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

    def test_compare_decisions_service_requires_two_ids(self):
        out, status = compare_decisions_service(
            tenant_id="tenant_test_001",
            envelope_ids=["abcdef0123456789"],
            comparison_objective="cut_payroll",
            requested_depth="standard",
            persist_enabled=True,
            get_record_fn=lambda **kwargs: None,
            compare_fn=lambda **kwargs: {"ok": True},
        )

        self.assertEqual(status, 400)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "at least two envelope_ids are required")


    def test_compare_decisions_service_rejects_invalid_id(self):
        out, status = compare_decisions_service(
            tenant_id="tenant_test_001",
            envelope_ids=["abcdef0123456789", "bad!"],
            comparison_objective="cut_payroll",
            requested_depth="standard",
            persist_enabled=True,
            get_record_fn=lambda **kwargs: None,
            compare_fn=lambda **kwargs: {"ok": True},
        )

        self.assertEqual(status, 400)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "invalid envelope_id")


    def test_compare_decisions_service_requires_persistence(self):
        out, status = compare_decisions_service(
            tenant_id="tenant_test_001",
            envelope_ids=["abcdef0123456789", "fedcba9876543210"],
            comparison_objective="cut_payroll",
            requested_depth="standard",
            persist_enabled=False,
            get_record_fn=lambda **kwargs: None,
            compare_fn=lambda **kwargs: {"ok": True},
        )

        self.assertEqual(status, 400)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "comparison_requires_persistence")


    def test_compare_decisions_service_rejects_tenant_mismatch(self):
        def get_record_fn(**kwargs):
            return {
                "tenant_id": "other_tenant",
                "envelope_id": kwargs["envelope_id"],
                "result": {"ok": True, "report": {"governing_objective": "cut_payroll"}},
            }

        out, status = compare_decisions_service(
            tenant_id="tenant_test_001",
            envelope_ids=["abcdef0123456789", "fedcba9876543210"],
            comparison_objective="cut_payroll",
            requested_depth="standard",
            persist_enabled=True,
            get_record_fn=get_record_fn,
            compare_fn=lambda **kwargs: {"ok": True},
        )

        self.assertEqual(status, 403)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "tenant_mismatch")


    def test_compare_decisions_service_returns_compare_payload(self):
        def get_record_fn(**kwargs):
            return {
                "tenant_id": "tenant_test_001",
                "envelope_id": kwargs["envelope_id"],
                "result": {
                    "ok": True,
                    "report": {
                        "governing_objective": "cut_payroll",
                        "confidence": "medium",
                        "tradeoffs": {
                            "upside": [],
                            "downside": [],
                            "key_tradeoffs": [],
                            "asymmetry": [],
                        },
                        "sensitivity": [],
                        "next_actions": [],
                    },
                    "audit": {
                        "tenant_id": "tenant_test_001",
                        "scenario_type": "draft_trade",
                    },
                },
            }

        def compare_fn(**kwargs):
            self.assertEqual(kwargs["tenant_id"], "tenant_test_001")
            self.assertEqual(len(kwargs["artifacts"]), 2)
            self.assertEqual(kwargs["comparison_objective"], "cut_payroll")
            return {
                "ok": True,
                "comparison_report": {"comparison_summary": "test"},
                "audit": {"tenant_id": "tenant_test_001"},
            }

        out, status = compare_decisions_service(
            tenant_id="tenant_test_001",
            envelope_ids=["abcdef0123456789", "fedcba9876543210"],
            comparison_objective="cut_payroll",
            requested_depth="standard",
            persist_enabled=True,
            get_record_fn=get_record_fn,
            compare_fn=compare_fn,
        )

        self.assertEqual(status, 200)
        self.assertTrue(out["ok"])
        self.assertIn("comparison_report", out)


if __name__ == "__main__":
    unittest.main()
