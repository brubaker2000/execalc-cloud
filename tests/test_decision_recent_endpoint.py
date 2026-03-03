import src.service.api as api


def test_decision_recent_returns_empty_when_persist_disabled(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")
    monkeypatch.delenv("EXECALC_PERSIST_EXECUTIONS", raising=False)

    c = api.app.test_client()
    r = c.get(
        "/decision/recent?limit=10",
        headers={"X-Tenant-Id": "t1", "X-Role": "operator", "X-User-Id": "u1"},
    )

    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
    assert body["persist_enabled"] is False
    assert body["records"] == []
