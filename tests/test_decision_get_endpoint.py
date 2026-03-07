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


def test_decision_get_returns_record_when_persistence_enabled(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")
    monkeypatch.setenv("EXECALC_PERSIST_EXECUTIONS", "1")
    monkeypatch.setenv("EXECALC_DB_HOST", "db-host")
    monkeypatch.setenv("EXECALC_DB_NAME", "execalc")
    monkeypatch.setenv("EXECALC_DB_USER", "user")
    monkeypatch.setenv("EXECALC_DB_PASSWORD", "pass")
    monkeypatch.setattr(api, "get_conn", object())

    def fake_get_execution_record(*, tenant_id: str, envelope_id: str):
        assert tenant_id == "t1"
        assert envelope_id == "0123456789abcdef0123456789abcdef"
        return {
            "tenant_id": tenant_id,
            "envelope_id": envelope_id,
            "ok": True,
            "result": {"ok": True, "report": {"executive_summary": "stored decision"}},
            "created_at": "2026-03-06T00:00:00+00:00",
        }

    monkeypatch.setattr(api, "get_execution_record", fake_get_execution_record)

    c = api.app.test_client()
    r = c.get(
        "/decision/0123456789abcdef0123456789abcdef",
        headers={"X-Tenant-Id": "t1", "X-User-Id": "u1", "X-Role": "operator"},
    )

    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
    assert body["envelope_id"] == "0123456789abcdef0123456789abcdef"
    assert body["created_at"] == "2026-03-06T00:00:00+00:00"
    assert body["result"]["ok"] is True
