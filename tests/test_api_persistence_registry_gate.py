from types import SimpleNamespace

import pytest

import src.service.api as api
from src.service.tenant.errors import TenantNotFound


def test_persist_execution_enforcement_enabled_missing_tenant_does_not_upsert_or_insert(monkeypatch):
    # Turn on persistence + registry enforcement
    monkeypatch.setenv("EXECALC_PERSIST_EXECUTIONS", "1")
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "1")

    # If either of these is called, the test should fail immediately.
    def boom_upsert(*args, **kwargs):
        raise AssertionError("upsert_tenant must not be called when registry enforcement is enabled")

    def boom_insert(*args, **kwargs):
        raise AssertionError("insert_execution_record must not be called when tenant is not registered")

    def fake_ensure(_tenant_id: str) -> None:
        raise TenantNotFound("tenant missing")

    monkeypatch.setattr(api, "upsert_tenant", boom_upsert)
    monkeypatch.setattr(api, "insert_execution_record", boom_insert)
    monkeypatch.setattr(api, "ensure_tenant_registered", fake_ensure)

    rec = SimpleNamespace(tenant_id="tenant_missing", envelope_id="env_1", result={"ok": True})

    out = api._persist_execution(rec)

    assert out["persisted"] is False
    assert out["persist_table"] == "execution_records"
    assert "persist_error" in out


def test_persist_execution_enforcement_enabled_registered_tenant_inserts_without_upsert(monkeypatch):
    monkeypatch.setenv("EXECALC_PERSIST_EXECUTIONS", "1")
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "1")

    insert_calls = {"n": 0}

    def boom_upsert(*args, **kwargs):
        raise AssertionError("upsert_tenant must not be called when registry enforcement is enabled")

    def fake_insert(*args, **kwargs):
        insert_calls["n"] += 1
        return None

    def fake_ensure(_tenant_id: str) -> None:
        return None  # tenant is registered

    monkeypatch.setattr(api, "upsert_tenant", boom_upsert)
    monkeypatch.setattr(api, "insert_execution_record", fake_insert)
    monkeypatch.setattr(api, "ensure_tenant_registered", fake_ensure)

    rec = SimpleNamespace(tenant_id="tenant_ok", envelope_id="env_2", result={"ok": True})

    out = api._persist_execution(rec)

    assert out["persisted"] is True
    assert out["persist_table"] == "execution_records"
    assert insert_calls["n"] == 1
