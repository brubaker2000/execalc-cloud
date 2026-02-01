import unittest

from src.service.integrations.connector import ConnectorContext
from src.service.integrations.null_connector import NullConnector
from src.service.integrations.registry import ConnectorRegistry, ConnectorRegistryError


class TestConnectorRegistry(unittest.TestCase):
    def test_empty_registry_lists_empty(self):
        r = ConnectorRegistry.empty()
        self.assertEqual(list(r.list()), [])

    def test_register_and_get(self):
        r = ConnectorRegistry.empty()
        c = NullConnector()
        r.register(c)

        got = r.get("null")
        self.assertIs(got, c)

        ctx = ConnectorContext(tenant_id="tenant_demo_999")
        hc = got.healthcheck(ctx)
        self.assertTrue(hc["ok"])
        self.assertEqual(hc["connector"], "null")
        self.assertEqual(hc["tenant_id"], "tenant_demo_999")

    def test_duplicate_register_raises(self):
        r = ConnectorRegistry.empty()
        r.register(NullConnector())
        with self.assertRaises(ConnectorRegistryError):
            r.register(NullConnector())

    def test_get_unknown_raises(self):
        r = ConnectorRegistry.empty()
        with self.assertRaises(ConnectorRegistryError):
            r.get("does_not_exist")

    def test_list_sorted(self):
        r = ConnectorRegistry.empty()

        class B:
            name = "b"
            def healthcheck(self, ctx):  # pragma: no cover
                return {}
            def fetch(self, ctx, query):  # pragma: no cover
                return {}

        class A:
            name = "a"
            def healthcheck(self, ctx):  # pragma: no cover
                return {}
            def fetch(self, ctx, query):  # pragma: no cover
                return {}

        r.register(B())
        r.register(A())
        self.assertEqual(list(r.list()), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
