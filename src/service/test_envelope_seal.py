import pytest
from src.service.envelope import IngressEnvelope
from src.service.envelope_seal import seal_envelope
from src.service.tenant.context import TenantContext


def test_seal_envelope_transitions_to_immutable():
    env = IngressEnvelope(
        input={"action": "test"},
        tenant_context=TenantContext(
            tenant_id="tenant_test_001",
            tenant_name="Test Tenant",
        ),
    )

    assert env.mutable is True

    sealed = seal_envelope(env)

    assert sealed.mutable is False
