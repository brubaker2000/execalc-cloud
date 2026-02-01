import json
import os
import unittest

from src.service.api import app


class TestIntegrationsAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_list_integrations(self):
        resp = self.client.get("/integrations")
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertIn("null", body["connectors"])

    def test_null_healthcheck(self):
        resp = self.client.post(
            "/integrations/null/healthcheck",
            data=json.dumps({"tenant_id": "tenant_demo_999"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["data"]["connector"], "null")
        self.assertEqual(body["data"]["tenant_id"], "tenant_demo_999")


if __name__ == "__main__":
    unittest.main()
