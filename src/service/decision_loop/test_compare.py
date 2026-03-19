import unittest

from src.service.decision_loop.compare import compare_decision_artifacts


def _artifact(
    *,
    envelope_id: str,
    governing_objective: str,
    confidence: str,
    sensitivity_count: int,
    scenario_type: str = "draft_trade",
):
    return {
        "tenant_id": "tenant_test_001",
        "envelope_id": envelope_id,
        "result": {
            "ok": True,
            "report": {
                "executive_summary": f"Summary for {envelope_id}",
                "confidence": confidence,
                "confidence_rationale": ["deterministic test"],
                "governing_objective": governing_objective,
                "tradeoffs": {
                    "upside": ["u1"],
                    "downside": ["d1"],
                    "key_tradeoffs": ["k1"],
                    "asymmetry": ["a1"],
                },
                "sensitivity": [
                    {"name": f"s{i}", "impact": "test"} for i in range(sensitivity_count)
                ],
                "next_actions": ["n1", "n2"],
            },
            "audit": {
                "tenant_id": "tenant_test_001",
                "scenario_type": scenario_type,
            },
        },
    }


class TestDecisionCompare(unittest.TestCase):
    def test_compare_requires_at_least_two_artifacts(self):
        with self.assertRaises(ValueError) as ctx:
            compare_decision_artifacts(
                tenant_id="tenant_test_001",
                artifacts=[
                    _artifact(
                        envelope_id="abcdef0123456789",
                        governing_objective="cut_payroll",
                        confidence="medium",
                        sensitivity_count=1,
                    )
                ],
                comparison_objective="best_current_option",
                requested_depth="standard",
            )

        self.assertEqual(
            str(ctx.exception),
            "at least two decision artifacts are required",
        )

    def test_compare_returns_stable_shape(self):
        out = compare_decision_artifacts(
            tenant_id="tenant_test_001",
            artifacts=[
                _artifact(
                    envelope_id="abcdef0123456789",
                    governing_objective="cut_payroll",
                    confidence="medium",
                    sensitivity_count=1,
                ),
                _artifact(
                    envelope_id="fedcba9876543210",
                    governing_objective="maximize_upside",
                    confidence="low",
                    sensitivity_count=3,
                ),
            ],
            comparison_objective="cut_payroll",
            requested_depth="standard",
        )

        self.assertTrue(out["ok"])
        self.assertIn("comparison_report", out)
        self.assertIn("audit", out)

        report = out["comparison_report"]
        self.assertIn("comparison_summary", report)
        self.assertIn("decision_set", report)
        self.assertIn("what_changed", report)
        self.assertIn("what_stayed_constant", report)
        self.assertIn("tradeoff_shift_analysis", report)
        self.assertIn("governing_objective_alignment", report)
        self.assertIn("sensitivity_and_fragility", report)
        self.assertIn("recommendation", report)
        self.assertIn("next_actions", report)

    def test_compare_prefers_objective_alignment_then_confidence_then_fragility(self):
        out = compare_decision_artifacts(
            tenant_id="tenant_test_001",
            artifacts=[
                _artifact(
                    envelope_id="aaaaaaaaaaaaaaaa",
                    governing_objective="cut_payroll",
                    confidence="medium",
                    sensitivity_count=1,
                ),
                _artifact(
                    envelope_id="bbbbbbbbbbbbbbbb",
                    governing_objective="maximize_upside",
                    confidence="high",
                    sensitivity_count=0,
                ),
            ],
            comparison_objective="cut_payroll",
            requested_depth="standard",
        )

        rec = out["comparison_report"]["recommendation"]
        self.assertEqual(rec["preferred_envelope_id"], "aaaaaaaaaaaaaaaa")

    def test_compare_marks_lower_sensitivity_as_more_robust(self):
        out = compare_decision_artifacts(
            tenant_id="tenant_test_001",
            artifacts=[
                _artifact(
                    envelope_id="1111111111111111",
                    governing_objective="cut_payroll",
                    confidence="medium",
                    sensitivity_count=1,
                ),
                _artifact(
                    envelope_id="2222222222222222",
                    governing_objective="cut_payroll",
                    confidence="medium",
                    sensitivity_count=4,
                ),
            ],
            comparison_objective="cut_payroll",
            requested_depth="standard",
        )

        fragility = out["comparison_report"]["sensitivity_and_fragility"]
        fragility_by_id = {row["envelope_id"]: row["fragility"] for row in fragility}
        self.assertEqual(fragility_by_id["1111111111111111"], "more_robust")
        self.assertEqual(fragility_by_id["2222222222222222"], "more_fragile")


if __name__ == "__main__":
    unittest.main()
