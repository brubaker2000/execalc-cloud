import unittest

from src.service.tenant.request_context import request_context
from src.service.tenant.injector import inject_tenant_context
from src.service.tenant.context import peek_tenant_context
from src.service.tenant.errors import InvalidTenantPayload


class TestTenantImmutability(unittest.TestCase):
    def test_cannot_switch_tenant_mid_request(self):
        with request_context({"tenant_id": "t1"}, user_id="u1", role="admin"):
            self.assertEqual(peek_tenant_context(), "t1")
            with self.assertRaises(InvalidTenantPayload):
                inject_tenant_context({"tenant_id": "t2"})
            self.assertEqual(peek_tenant_context(), "t1")


if __name__ == "__main__":
    unittest.main()
