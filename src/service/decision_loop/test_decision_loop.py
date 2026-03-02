import unittest

from src.service.decision_loop.engine import run_decision_loop
from src.service.decision_loop.models import Scenario


class TestDecisionLoopEngine(unittest.TestCase):
    def test_report_shape(self):
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
        self.assertIn("executive_summary", report)
        self.assertIn("confidence", report)
        self.assertIn("sensitivity", report)
        self.assertIn("next_actions", report)

    def test_missing_inputs_sets_unknown_confidence(self):
        s = Scenario(
            scenario_type="draft_trade",
            governing_objective="cut_payroll",
            prompt="Missing picks",
            facts={},
        )
        r = run_decision_loop(tenant_id="t1", user_id="u1", scenario=s)
        self.assertEqual(r.confidence, "unknown")


if __name__ == "__main__":
    unittest.main()
