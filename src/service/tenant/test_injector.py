import unittest

from src.service.tenant.context import clear_tenant_context, get_tenant_context
from src.service.tenant.errors import InvalidTenantPayload
from src.service.tenant.injector import inject_tenant_context


class TestTenantInjector(unittest.TestCase):
    def tearDown(self):
        try:
            clear_tenant_context()
        except Exception:
            pass

    def test_inject_sets_context_when_missing(self):
        inject_tenant_context({"tenant_id": "tenant-2"})
        self.assertEqual(get_tenant_context(), "tenant-2")

    def test_inject_requires_tenant_id(self):
        with self.assertRaises(InvalidTenantPayload):
            inject_tenant_context({})

    def test_inject_rejects_midflight_switch(self):
        inject_tenant_context({"tenant_id": "tenant-2"})
        with self.assertRaises(InvalidTenantPayload):
            inject_tenant_context({"tenant_id": "tenant-3"})


if __name__ == "__main__":
    unittest.main()
