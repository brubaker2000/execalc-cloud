import unittest

from src.service.decision_loop.engine import run_decision_loop
from src.service.decision_loop.models import Scenario


class TestDecisionLoopEngine(unittest.TestCase):
    def test_report_shape_includes_rebuild_fields(self):
        s = Scenario(
            scenario_type="draft_trade",
            governing_objective="cut_payroll",
            prompt="Pick 8 vs 18 trade-down scenario under payroll mandate",
            facts={"you_pick": 8, "counterparty_pick": 18},
        )
        r = run_decision_loop(tenant_id="t1", user_id="u1", scenario=s)
        d = r.to_dict()

        self.assertTrue(d.get("ok"))
        report = d.get("report") or {}
        audit = d.get("audit") or {}

        self.assertIn("executive_summary", report)
        self.assertIn("confidence", report)
        self.assertIn("confidence_rationale", report)
        self.assertIn("governing_objective", report)
        self.assertIn("tradeoffs", report)
        self.assertIn("sensitivity", report)
        self.assertIn("next_actions", report)

        # Prime Directive guardrails
        self.assertIn("value_assessment", report)
        self.assertIn("risk_reward_assessment", report)
        self.assertIn("supply_demand_assessment", report)
        self.assertIn("asset_assessment", report)
        self.assertIn("liability_assessment", report)

        # Polymorphia guardrails
        self.assertIn("actors", report)
        self.assertIn("incentives", report)
        self.assertIn("asymmetries", report)

        # Execution / audit guardrails
        self.assertIn("execution_trace", report)
        self.assertEqual(audit.get("tenant_id"), "t1")
        self.assertEqual(audit.get("user_id"), "u1")
        self.assertEqual(audit.get("scenario_type"), "draft_trade")
        self.assertEqual(audit.get("governing_objective"), "cut_payroll")
        self.assertEqual(audit.get("version"), "stage4b")

    def test_missing_inputs_sets_unknown_confidence_and_sensitivity(self):
        s = Scenario(
            scenario_type="draft_trade",
            governing_objective="cut_payroll",
            prompt="Missing picks",
            facts={},
        )
        r = run_decision_loop(tenant_id="t1", user_id="u1", scenario=s)

        self.assertEqual(r.confidence, "unknown")
        self.assertGreater(len(r.sensitivity), 0)
        self.assertTrue(any(v.name == "you_pick" for v in r.sensitivity))
        self.assertTrue(any(v.name == "counterparty_pick" for v in r.sensitivity))


    def test_missing_inputs_activate_missing_critical_input_reflex(self):
        s = Scenario(
            scenario_type="draft_trade",
            governing_objective="cut_payroll",
            prompt="Missing picks",
            facts={},
        )
        r = run_decision_loop(tenant_id="t1", user_id="u1", scenario=s)

        self.assertEqual(
            r.execution_trace["support_stack"]["reflex_gate"]["allowed_reflexes"],
            ["missing_critical_input"],
        )

    def test_complete_inputs_sets_medium_confidence(self):
        s = Scenario(
            scenario_type="draft_trade",
            governing_objective="cut_payroll",
            prompt="Complete picks",
            facts={"you_pick": 8, "counterparty_pick": 18},
        )
        r = run_decision_loop(tenant_id="t1", user_id="u1", scenario=s)

        self.assertEqual(r.confidence, "medium")
        self.assertEqual(len(r.sensitivity), 0)

    def test_execution_trace_contains_scenario_type(self):
        s = Scenario(
            scenario_type="draft_trade",
            governing_objective="cut_payroll",
            prompt="Trace test",
            facts={"you_pick": 8, "counterparty_pick": 18},
        )
        r = run_decision_loop(tenant_id="t1", user_id="u1", scenario=s)

        self.assertEqual(r.execution_trace.get("scenario_type"), "draft_trade")
        self.assertIn("timestamp", r.execution_trace)
        self.assertIn("actions_taken", r.execution_trace)
        self.assertIn("support_stack", r.execution_trace)
        self.assertIn("reflex_gate", r.execution_trace["support_stack"])
        self.assertIn("procedure_plan", r.execution_trace["support_stack"])
        self.assertIn("boundary_decision", r.execution_trace["support_stack"])


if __name__ == "__main__":
    unittest.main()
