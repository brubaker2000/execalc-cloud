import os
import unittest

import src.service.api as api
from src.service.integrations.credentials import CredentialRequirementPolicy
from src.service.integrations.policy import ConnectorPolicy


class TestIntegrationsFetchAPI(unittest.TestCase):
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
        self.base_headers = {"X-User-Id": "test_user", "X-Role": "operator"}

    def tearDown(self):
        api._CONNECTOR_POLICY = self._prev_policy
        api._CREDENTIAL_REQ_POLICY = self._prev_cred_req

        if self._prev_harness is None:
            os.environ.pop("EXECALC_DEV_HARNESS", None)
        else:
            os.environ["EXECALC_DEV_HARNESS"] = self._prev_harness

    def test_fetch_requires_tenant_id(self):
        # Tenant identity comes from verified claims (X-Tenant-Id), not the JSON body.
        resp = self.client.post(
            "/integrations/null/fetch",
            headers=self.base_headers,
            json={"query": {"x": 1}},
        )
        self.assertEqual(resp.status_code, 400)

    def test_fetch_ok(self):
        headers = dict(self.base_headers)
        headers["X-Tenant-Id"] = "tenant_test_001"

        resp = self.client.post(
            "/integrations/null/fetch",
            headers=headers,
            json={"query": {"hello": "world"}},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["data"]["connector"], "null")
        self.assertEqual(data["data"]["tenant_id"], "tenant_test_001")
        self.assertEqual(data["data"]["query"], {"hello": "world"})
