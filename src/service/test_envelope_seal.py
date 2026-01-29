import unittest

from src.service.envelope import IngressEnvelope
from src.service.envelope_seal import seal_envelope
from src.service.tenant.identity import TenantIdentity


class TestEnvelopeSeal(unittest.TestCase):
    def test_seal_envelope_transitions_to_immutable(self):
        env = IngressEnvelope(
            input={"action": "test"},
            tenant_context=TenantIdentity(
                tenant_id="tenant_test_001",
                tenant_name="Test Tenant",
            ),
        )

        self.assertTrue(env.mutable)

        sealed = seal_envelope(env)

        self.assertFalse(sealed.mutable)


if __name__ == "__main__":
    unittest.main()
