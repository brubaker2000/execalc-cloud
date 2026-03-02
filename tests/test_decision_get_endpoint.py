import src.service.api as api


def test_decision_get_returns_404_when_persistence_disabled(monkeypatch):
    # Enable dev harness claims via headers
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")

    # Ensure persistence is disabled
    monkeypatch.delenv("EXECALC_PERSIST_EXECUTIONS", raising=False)

    c = api.app.test_client()

    r = c.get(
        "/decision/0123456789abcdef0123456789abcdef",
        headers={"X-Tenant-Id": "t1", "X-User-Id": "u1", "X-Role": "operator"},
    )

    assert r.status_code == 404
    body = r.get_json()
    assert body["ok"] is False
    assert body["error"] == "not_found"
