import unittest

from src.service.tenant.entrypoint import run_as_request
from src.service.tenant.errors import TenantNotFound
from src.service.tenant.service import get_tenant_service


class TestEntrypoint(unittest.TestCase):
    def test_run_as_request_executes_under_context(self):
        envelope = {"tenant_id": "t_test"}

        # get_tenant_service should run and raise TenantNotFound (tenant doesn't exist),
        # proving context was established and RBAC allows viewer read.
        with self.assertRaises(TenantNotFound):
            run_as_request(
                envelope,
                user_id="u1",
                role="viewer",
                fn=get_tenant_service,
                args=("t_test",),
            )


if __name__ == "__main__":
    unittest.main()
