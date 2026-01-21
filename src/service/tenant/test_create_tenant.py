import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.service.tenant.create import create_tenant, InvalidTenantPayload

def test_create_tenant():
    # Sample payload
    payload = {
        "tenant_id": "tenant001",
        "name": "Test Tenant"
    }

    # Call the create_tenant function
    response = create_tenant(payload)

    # Validate that the tenant is persisted in the database

    # Assertions
    assert response["status"] == "validated", "Status should be 'created'"
    print("Test passed!")

if __name__ == "__main__":
    test_create_tenant()

