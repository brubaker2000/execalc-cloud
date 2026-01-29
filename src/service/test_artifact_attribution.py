import unittest

from src.service.artifact_attribution import ArtifactAttribution
from src.service.tenant.identity import TenantIdentity
from src.service.execution_record import ExecutionRecord


class TestArtifactAttribution(unittest.TestCase):
    def test_artifact_attribution_is_immutable_and_complete(self):
        tenant = TenantIdentity(tenant_id="tenant_test_001", tenant_name="Test Tenant")

        execution = ExecutionRecord(
            tenant_id="tenant_test_001",
            envelope_id="env_001",
            result={"result": "ok"},
        )

        attribution = ArtifactAttribution(
            tenant_context=tenant,
            execution_record=execution,
            seat_id="seat_123",
        )

        self.assertEqual(attribution.tenant_context.tenant_id, "tenant_test_001")
        self.assertEqual(attribution.execution_record.envelope_id, "env_001")
        self.assertEqual(attribution.execution_record.result["result"], "ok")
        self.assertEqual(attribution.seat_id, "seat_123")


if __name__ == "__main__":
    unittest.main()
