from src.service.execution_record import ExecutionRecord
from src.service.tenant.context import TenantContext


def test_execution_record_defaults():
    record = ExecutionRecord(
        tenant_context=TenantContext(
            tenant_id="tenant_test_001",
            tenant_name="Test Tenant",
        )
    )

    assert record.seat_id is None
    assert record.input == {}
    assert record.output == {}
    assert record.meta == {}
    assert record.executed_at is not None

