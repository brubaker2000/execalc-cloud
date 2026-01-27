import unittest

from src.service.tenant.context import set_tenant_context, clear_tenant_context
from src.service.tenant.errors import InvalidTenantPayload
from src.service.tenant.guards import (
    assert_execution_tenant_context_set,
    assert_target_tenant_matches_execution,
)

class TestTenantGuards(unittest.TestCase):
    def tearDown(self):
        # Always clear context so tests are isolated.
        try:
            clear_tenant_context()
        except Exception:
            pass

    def test_execution_tenant_context_required(self):
        with self.assertRaises(InvalidTenantPayload):
            assert_execution_tenant_context_set()

    def test_execution_tenant_context_returns_id(self):
        set_tenant_context("tenant-2")
        self.assertEqual(assert_execution_tenant_context_set(), "tenant-2")

    def test_target_matches_execution(self):
        set_tenant_context("tenant-2")
        assert_target_tenant_matches_execution("tenant-2")  # should not raise

    def test_target_mismatch_raises(self):
        set_tenant_context("tenant-2")
        with self.assertRaises(InvalidTenantPayload):
            assert_target_tenant_matches_execution("tenant-3")

if __name__ == "__main__":
    unittest.main()
