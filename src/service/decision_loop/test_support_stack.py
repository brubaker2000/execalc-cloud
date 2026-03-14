import unittest

from src.service.decision_loop.support_stack import (
    BoundaryDecision,
    ProcedurePlan,
    Reflex,
    ReflexRegistry,
    default_boundary_decision,
    default_procedure_plan,
    support_stack_trace,
)


class TestSupportStackScaffolding(unittest.TestCase):
    def test_reflex_registry_orders_enabled_reflexes_by_priority_then_name(self):
        registry = ReflexRegistry(
            [
                Reflex(name="zeta", description="late", priority=200),
                Reflex(name="alpha", description="first", priority=10),
                Reflex(name="beta", description="second", priority=10),
                Reflex(name="disabled", description="off", enabled=False, priority=1),
            ]
        )

        reflexes = registry.all()
        self.assertEqual([r.name for r in reflexes], ["alpha", "beta", "zeta"])

    def test_reflex_gate_returns_default_allow_decision(self):
        registry = ReflexRegistry([Reflex(name="cap_table", description="Cap table reflex")])
        gate = registry.gate()

        self.assertEqual(gate.allowed_reflexes, ["cap_table"])
        self.assertEqual(gate.denied_reflexes, [])
        self.assertIn("phase1_default_allow", gate.reasons)

    def test_default_procedure_plan_has_deterministic_steps(self):
        plan = default_procedure_plan()

        self.assertIsInstance(plan, ProcedurePlan)
        self.assertEqual(
            plan.step_names(),
            [
                "validate_inputs",
                "assign_confidence",
                "generate_tradeoffs",
                "apply_prime_directive",
                "apply_polymorphia",
                "build_artifact",
            ],
        )


    def test_default_procedure_plan_inserts_resolution_step_when_missing_input_reflex_active(self):
        plan = default_procedure_plan(active_reflexes=["missing_critical_input"])

        self.assertEqual(
            plan.step_names(),
            [
                "validate_inputs",
                "resolve_missing_critical_inputs",
                "assign_confidence",
                "generate_tradeoffs",
                "apply_prime_directive",
                "apply_polymorphia",
                "build_artifact",
            ],
        )

    def test_default_boundary_decision_allows_with_placeholder_checks(self):
        decision = default_boundary_decision()

        self.assertIsInstance(decision, BoundaryDecision)
        self.assertTrue(decision.allowed)
        self.assertIn("phase1_default_allow", decision.reasons)
        self.assertIn("tenant_scope_placeholder", decision.checks)
        self.assertIn("authorization_placeholder", decision.checks)

    def test_support_stack_trace_contains_expected_sections(self):
        trace = support_stack_trace()

        self.assertIn("reflex_gate", trace)
        self.assertIn("procedure_plan", trace)
        self.assertIn("boundary_decision", trace)

        self.assertEqual(trace["reflex_gate"]["allowed_reflexes"], [])
        self.assertEqual(
            trace["procedure_plan"]["steps"],
            [
                "validate_inputs",
                "assign_confidence",
                "generate_tradeoffs",
                "apply_prime_directive",
                "apply_polymorphia",
                "build_artifact",
            ],
        )
        self.assertTrue(trace["boundary_decision"]["allowed"])


    def test_support_stack_trace_activates_missing_critical_input_reflex(self):
        trace = support_stack_trace(missing_critical_fields=["you_pick", "counterparty_pick"])

        self.assertEqual(
            trace["reflex_gate"]["allowed_reflexes"],
            ["missing_critical_input"],
        )
        self.assertIn("phase1_default_allow", trace["reflex_gate"]["reasons"])
        self.assertEqual(
            trace["procedure_plan"]["steps"],
            [
                "validate_inputs",
                "resolve_missing_critical_inputs",
                "assign_confidence",
                "generate_tradeoffs",
                "apply_prime_directive",
                "apply_polymorphia",
                "build_artifact",
            ],
        )


if __name__ == "__main__":
    unittest.main()
