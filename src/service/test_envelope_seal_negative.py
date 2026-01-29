import unittest

from src.service.envelope import IngressEnvelope
from src.service.envelope_seal import seal_envelope
from src.service.tenant.identity import TenantIdentity


class TestEnvelopeSealNegative(unittest.TestCase):
    def test_seal_fails_without_tenant_context(self):
        env = IngressEnvelope(input={"action": "test"})
        with self.assertRaisesRegex(RuntimeError, "Tenant context missing"):
            seal_envelope(env)

    def test_seal_fails_if_already_sealed(self):
        env = IngressEnvelope(
            input={"action": "test"},
            tenant_context=TenantIdentity(
                tenant_id="tenant_test_001",
                tenant_name="Test Tenant",
            ),
        )

        seal_envelope(env)

        with self.assertRaisesRegex(RuntimeError, "already sealed"):
            seal_envelope(env)


if __name__ == "__main__":
    unittest.main()
