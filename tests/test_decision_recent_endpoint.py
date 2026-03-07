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


def test_decision_recent_returns_records_when_persist_enabled(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")
    monkeypatch.setenv("EXECALC_PERSIST_EXECUTIONS", "1")
    monkeypatch.setenv("EXECALC_DB_HOST", "db-host")
    monkeypatch.setenv("EXECALC_DB_NAME", "execalc")
    monkeypatch.setenv("EXECALC_DB_USER", "user")
    monkeypatch.setenv("EXECALC_DB_PASSWORD", "pass")
    monkeypatch.setattr(api, "get_conn", object())

    def fake_list_execution_records(*, tenant_id: str, limit: int):
        assert tenant_id == "t1"
        assert limit == 10
        return [
            {
                "tenant_id": "t1",
                "envelope_id": "env_a",
                "ok": True,
                "created_at": "2026-03-06T00:00:00+00:00",
            },
            {
                "tenant_id": "t1",
                "envelope_id": "env_b",
                "ok": True,
                "created_at": "2026-03-05T00:00:00+00:00",
            },
        ]

    monkeypatch.setattr(api, "list_execution_records", fake_list_execution_records)

    c = api.app.test_client()
    r = c.get(
        "/decision/recent?limit=10",
        headers={"X-Tenant-Id": "t1", "X-Role": "operator", "X-User-Id": "u1"},
    )

    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
    assert body["persist_enabled"] is True
    assert len(body["records"]) == 2
    assert body["records"][0]["envelope_id"] == "env_a"
