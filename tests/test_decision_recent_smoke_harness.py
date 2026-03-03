import src.service.api as api


def test_decision_recent_smoke_harness_allows_access(monkeypatch):
    # Smoke harness ON; dev harness OFF.
    monkeypatch.setenv("EXECALC_SMOKE_HARNESS", "1")
    monkeypatch.setenv("EXECALC_SMOKE_KEY", "test_smoke_key")
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "0")

    # Lock smoke harness to a single tenant for safety.
    monkeypatch.setenv("EXECALC_SMOKE_TENANT_ID", "t1")

    # Persistence disabled: endpoint should return an empty timeline, but still 200.
    monkeypatch.delenv("EXECALC_PERSIST_EXECUTIONS", raising=False)

    c = api.app.test_client()
    r = c.get(
        "/decision/recent?limit=5",
        headers={
            "X-Smoke-Key": "test_smoke_key",
            "X-Tenant-Id": "t1",
            "X-Role": "operator",
            "X-User-Id": "smoke-user",
        },
    )

    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
    assert body["persist_enabled"] is False
    assert body["records"] == []
