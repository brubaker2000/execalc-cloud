from src.service.artifact_attribution import ArtifactAttribution
from src.service.tenant.context import TenantContext
from src.service.execution_record import ExecutionRecord


def test_artifact_attribution_is_immutable_and_complete():
    tenant = TenantContext(
        tenant_id="tenant_test_001",
        tenant_name="Test Tenant",
    )

    execution = ExecutionRecord(
        execution_id="exec_001",
        scenario="test_scenario",
    )

    attribution = ArtifactAttribution(
        tenant_context=tenant,
        execution_record=execution,
        seat_id="seat_123",
    )

    assert attribution.tenant_context.tenant_id == "tenant_test_001"
    assert attribution.execution_record.execution_id == "exec_001"
    assert attribution.seat_id == "seat_123"
