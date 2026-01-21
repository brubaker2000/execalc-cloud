import pytest
from src.service.envelope import IngressEnvelope
from src.service.envelope_seal import seal_envelope
from src.service.tenant.context import TenantContext


def test_seal_fails_without_tenant_context():
    env = IngressEnvelope(input={"action": "test"})

    with pytest.raises(RuntimeError, match="Tenant context missing"):
        seal_envelope(env)


def test_seal_fails_if_already_sealed():
    env = IngressEnvelope(
        input={"action": "test"},
        tenant_context=TenantContext(
            tenant_id="tenant_test_001",
            tenant_name="Test Tenant",
        ),
    )

    seal_envelope(env)

    with pytest.raises(RuntimeError, match="already sealed"):
        seal_envelope(env)
