from datetime import datetime
from src.service.execution_record import ExecutionRecord


def test_execution_record_defaults():
    record = ExecutionRecord(
        tenant_id="tenant_test_001",
        envelope_id="env_123",
        result={"status": "ok"},
    )

    assert record.tenant_id == "tenant_test_001"
    assert record.envelope_id == "env_123"
    assert record.result == {"status": "ok"}
    assert isinstance(record.created_at, datetime)
