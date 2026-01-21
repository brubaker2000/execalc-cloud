import pytest
from src.service.tenant.context import TenantContext
from src.service.tenant.guards import assert_tenant_context_immutable


def test_guard_passes_with_immutable_tenant_context():
    envelope = {
        "tenant_context": TenantContext(
            tenant_id="tenant_test_001",
            tenant_name="Test Tenant",
        )
    }

    # Should not raise
    assert_tenant_context_immutable(envelope)


def test_guard_raises_when_missing_tenant_context():
    envelope = {}

    with pytest.raises(RuntimeError):
        assert_tenant_context_immutable(envelope)
