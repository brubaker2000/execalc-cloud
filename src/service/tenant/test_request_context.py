import unittest

from src.service.tenant.request_context import request_context
from src.service.tenant.context import get_tenant_context
from src.service.tenant.actor_context import get_actor_context
from src.service.tenant.errors import InvalidTenantPayload


class TestRequestContext(unittest.TestCase):
    def test_sets_and_clears_contexts(self):
        envelope = {"tenant_id": "tenant-1"}

        with request_context(envelope, user_id="user-1", role="admin"):
            self.assertEqual(get_tenant_context(), "tenant-1")
            actor = get_actor_context()
            self.assertEqual(actor["user_id"], "user-1")
            self.assertEqual(actor["role"], "admin")

        # After the block, both contexts must be cleared.
        with self.assertRaises(InvalidTenantPayload):
            _ = get_tenant_context()
        with self.assertRaises(InvalidTenantPayload):
            _ = get_actor_context()

    def test_clears_contexts_on_exception(self):
        envelope = {"tenant_id": "tenant-2"}

        class Boom(Exception):
            pass

        try:
            with request_context(envelope, user_id="user-2", role="admin"):
                raise Boom("forced")
        except Boom:
            pass

        # Contexts must still be cleared.
        with self.assertRaises(InvalidTenantPayload):
            _ = get_tenant_context()
        with self.assertRaises(InvalidTenantPayload):
            _ = get_actor_context()


if __name__ == "__main__":
    unittest.main()
