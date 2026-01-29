import unittest

from src.service.ingress_runner import execute_ingress
from src.service.tenant.context import peek_tenant_context


class TestIngressClearsTenantContext(unittest.TestCase):
    def test_execute_ingress_sets_and_clears_tenant_context(self):
        # Before: no tenant context set
        self.assertIsNone(peek_tenant_context())

        seen_inside_fn = {}

        def fn():
            # During: tenant context should be set
            seen_inside_fn["tenant_id"] = peek_tenant_context()
            return {"status": "OK"}

        record = execute_ingress(
            {"tenant_id": "tenant_test_001"},
            user_id="u1",
            role="viewer",
            fn=fn,
        )

        # After: tenant context should be cleared
        self.assertIsNone(peek_tenant_context())

        # Verify the context inside the function was correct
        self.assertEqual(seen_inside_fn.get("tenant_id"), "tenant_test_001")

        # Verify result payload shape
        self.assertTrue(record.result.get("ok"))
        self.assertEqual(record.result.get("data"), {"status": "OK"})
