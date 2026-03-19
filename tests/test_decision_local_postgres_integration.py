import os

import pytest
import src.service.api as api


def _db_ready() -> bool:
    required = [
        "EXECALC_DB_HOST",
        "EXECALC_DB_NAME",
        "EXECALC_DB_USER",
        "EXECALC_DB_PASSWORD",
    ]
    return all((os.getenv(k) or "").strip() for k in required)


def test_local_postgres_happy_path(monkeypatch):
    if not _db_ready():
        pytest.skip("local Postgres env not configured")

    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")
    monkeypatch.setenv("EXECALC_PERSIST_EXECUTIONS", "1")

    tenant_id = "stage7a_itest_t1"

    conn = api.get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("DELETE FROM execution_records WHERE tenant_id = %s", (tenant_id,))
            cur.execute("DELETE FROM tenants WHERE tenant_id = %s", (tenant_id,))
    finally:
        conn.close()

    c = api.app.test_client()

    run_resp = c.post(
        "/decision/run",
        headers={"X-Tenant-Id": tenant_id, "X-User-Id": "u1", "X-Role": "operator"},
        json={
            "scenario": {
                "scenario_type": "draft_trade",
                "governing_objective": "cut_payroll",
                "prompt": "Pick 8 vs 18 trade-down scenario under payroll mandate",
                "facts": {"you_pick": 8, "counterparty_pick": 18},
            }
        },
    )

    assert run_resp.status_code == 200
    run_body = run_resp.get_json()
    assert run_body["ok"] is True
    assert run_body["audit"]["persist"]["persisted"] is True

    envelope_id = run_body["audit"]["envelope_id"]

    get_resp = c.get(
        f"/decision/{envelope_id}",
        headers={"X-Tenant-Id": tenant_id, "X-User-Id": "u1", "X-Role": "operator"},
    )

    assert get_resp.status_code == 200
    get_body = get_resp.get_json()
    assert get_body["ok"] is True
    assert get_body["envelope_id"] == envelope_id

    recent_resp = c.get(
        "/decision/recent?limit=5",
        headers={"X-Tenant-Id": tenant_id, "X-User-Id": "u1", "X-Role": "operator"},
    )

    assert recent_resp.status_code == 200
    recent_body = recent_resp.get_json()
    assert recent_body["ok"] is True
    assert recent_body["persist_enabled"] is True
    assert any(r["envelope_id"] == envelope_id for r in recent_body["records"])
