import unittest

from src.service.api import app


class TestIntegrationsFetchAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_fetch_requires_tenant_id(self):
        resp = self.client.post("/integrations/null/fetch", json={"query": {"x": 1}})
        self.assertEqual(resp.status_code, 400)

    def test_fetch_ok(self):
        resp = self.client.post(
            "/integrations/null/fetch",
            json={"tenant_id": "tenant_demo_999", "query": {"hello": "world"}},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["data"]["connector"], "null")
        self.assertEqual(data["data"]["tenant_id"], "tenant_demo_999")
        self.assertEqual(data["data"]["query"], {"hello": "world"})
