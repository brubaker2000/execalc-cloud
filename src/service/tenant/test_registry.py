import os
import unittest
from unittest import mock

import src.service.tenant.registry as reg
import src.service.tenant.request_context as rc
from src.service.tenant.errors import TenantNotFound


class TestTenantRegistry(unittest.TestCase):
    def test_registry_enforcement_disabled_is_noop(self):
        with mock.patch.dict(os.environ, {"EXECALC_ENFORCE_TENANT_REGISTRY": "0"}, clear=False):
            reg.ensure_tenant_registered("tenant_any")  # should not raise

    def test_registry_enforcement_enabled_db_missing_raises(self):
        with mock.patch.dict(os.environ, {"EXECALC_ENFORCE_TENANT_REGISTRY": "1"}, clear=False):
            # Force DB module unavailable to prove deterministic failure when enforcement is on.
            with mock.patch.object(reg, "get_conn", None, create=True):
                with self.assertRaisesRegex(RuntimeError, "tenant registry DB module not available"):
                    reg.ensure_tenant_registered("tenant_any")

    def test_registry_enforcement_enabled_missing_tenant(self):
        with mock.patch.dict(os.environ, {"EXECALC_ENFORCE_TENANT_REGISTRY": "1"}, clear=False):
            with mock.patch.object(reg, "tenant_exists", lambda _tid: False, create=True):
                with self.assertRaises(TenantNotFound):
                    reg.ensure_tenant_registered("tenant_missing")

    def test_registry_enforcement_enabled_existing_tenant(self):
        with mock.patch.dict(os.environ, {"EXECALC_ENFORCE_TENANT_REGISTRY": "1"}, clear=False):
            with mock.patch.object(reg, "tenant_exists", lambda _tid: True, create=True):
                reg.ensure_tenant_registered("tenant_ok")  # should not raise

    def test_request_context_calls_registry_gate(self):
        with mock.patch.dict(os.environ, {"EXECALC_ENFORCE_TENANT_REGISTRY": "1"}, clear=False):
            called = {}

            def fake_gate(tid: str) -> None:
                called["tenant_id"] = tid

            # request_context imports ensure_tenant_registered into its module namespace
            with mock.patch.object(rc, "ensure_tenant_registered", fake_gate, create=True):
                with rc.request_context({"tenant_id": "tenant_abc"}, user_id="u1", role="admin"):
                    pass

            self.assertEqual(called.get("tenant_id"), "tenant_abc")


if __name__ == "__main__":
    unittest.main()
