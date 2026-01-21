from src.service.tenant.injector import inject_tenant_context
from src.service.tenant.context import TenantContext


def test_inject_tenant_context_attaches_context():
    envelope = {}
    tenant_record = {
        "tenant_id": "tenant_test_001",
        "tenant_name": "Test Tenant",
    }

    result = inject_tenant_context(envelope, tenant_record)

    assert "tenant_context" in result
    assert isinstance(result["tenant_context"], TenantContext)
    assert result["tenant_context"].tenant_id == "tenant_test_001"
    assert result["tenant_context"].tenant_name == "Test Tenant"
