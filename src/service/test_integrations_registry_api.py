import os
import unittest

import src.service.api as api
from src.service.integrations.credentials import CredentialRequirementPolicy
from src.service.integrations.policy import ConnectorPolicy


class TestIntegrationsAPI(unittest.TestCase):
    def setUp(self):
        # Enable dev harness for verified-claims headers
        self._prev_harness = os.environ.get("EXECALC_DEV_HARNESS")
        os.environ["EXECALC_DEV_HARNESS"] = "1"

        # Pin integration policy to deterministic test config
        self._prev_policy = api._CONNECTOR_POLICY
        self._prev_cred_req = api._CREDENTIAL_REQ_POLICY
        api._CONNECTOR_POLICY = ConnectorPolicy(allowlist_by_tenant=None, required_scopes_by_connector=None)
        api._CREDENTIAL_REQ_POLICY = CredentialRequirementPolicy(required_by_tenant=None)

        self.client = api.app.test_client()
        self.headers = {
            "X-User-Id": "test_user",
            "X-Role": "operator",
            "X-Tenant-Id": "tenant_test_001",
        }

    def tearDown(self):
        api._CONNECTOR_POLICY = self._prev_policy
        api._CREDENTIAL_REQ_POLICY = self._prev_cred_req

        if self._prev_harness is None:
            os.environ.pop("EXECALC_DEV_HARNESS", None)
        else:
            os.environ["EXECALC_DEV_HARNESS"] = self._prev_harness

    def test_list_integrations(self):
        resp = self.client.get("/integrations", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertIn("null", body["connectors"])

    def test_null_healthcheck(self):
        resp = self.client.post("/integrations/null/healthcheck", headers=self.headers, json={})
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["data"]["connector"], "null")
        self.assertEqual(body["data"]["tenant_id"], "tenant_test_001")
