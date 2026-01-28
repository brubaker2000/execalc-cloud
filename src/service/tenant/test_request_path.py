import unittest

from src.service.tenant.request_context import request_context
from src.service.tenant.context import peek_tenant_context
from src.service.tenant.actor_context import get_actor_context
from src.service.tenant.service import get_tenant_service
from src.service.tenant.errors import InvalidTenantPayload, TenantNotFound


class TestRequestPath(unittest.TestCase):
    def test_request_context_sets_and_clears_context(self):
        envelope = {"tenant_id": "t_test"}

        # Inside context: tenant + actor are set, and tenant-scoped service calls can run.
        with request_context(envelope, user_id="u1", role="viewer"):
            self.assertEqual(peek_tenant_context(), "t_test")
            _ = get_actor_context()  # should not raise

            # Tenant does not exist, but the call should reach persistence and raise TenantNotFound.
            with self.assertRaises(TenantNotFound):
                get_tenant_service("t_test")

        # After context: both tenant and actor contexts are cleared.
        self.assertIsNone(peek_tenant_context())
        with self.assertRaises(InvalidTenantPayload):
            _ = get_actor_context()


if __name__ == "__main__":
    unittest.main()
