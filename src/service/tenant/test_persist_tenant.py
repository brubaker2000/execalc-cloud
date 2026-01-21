import sqlite3
from src.service.tenant.persistence import persist_tenant, TenantPersistenceError

DB_PATH = "src/service/tenant/tenant.db"


def setup_function():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tenants")
    conn.commit()
    conn.close()


def test_persist_valid_tenant():
    payload = {
        "tenant_id": "tenant_test_001",
        "tenant_name": "Test Tenant",
    }

    result = persist_tenant(payload)

    assert result["status"] == "persisted"
    assert result["tenant_id"] == payload["tenant_id"]


def test_duplicate_tenant_raises():
    payload = {
        "tenant_id": "tenant_test_002",
        "tenant_name": "Duplicate Tenant",
    }

    persist_tenant(payload)

    try:
        persist_tenant(payload)
        assert False, "Expected TenantPersistenceError"
    except TenantPersistenceError:
        assert True
