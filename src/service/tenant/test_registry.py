import pytest

import src.service.tenant.registry as reg
import src.service.tenant.request_context as rc
from src.service.tenant.errors import TenantNotFound


def test_registry_enforcement_disabled_is_noop(monkeypatch):
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "0")
    reg.ensure_tenant_registered("tenant_any")  # should not raise


def test_registry_enforcement_enabled_db_missing_raises(monkeypatch):
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "1")
    # Force DB module unavailable to prove deterministic failure when enforcement is on.
    monkeypatch.setattr(reg, "get_conn", None, raising=False)

    with pytest.raises(RuntimeError, match="tenant registry DB module not available"):
        reg.ensure_tenant_registered("tenant_any")


def test_registry_enforcement_enabled_missing_tenant(monkeypatch):
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "1")
    monkeypatch.setattr(reg, "tenant_exists", lambda _tid: False)

    with pytest.raises(TenantNotFound):
        reg.ensure_tenant_registered("tenant_missing")


def test_registry_enforcement_enabled_existing_tenant(monkeypatch):
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "1")
    monkeypatch.setattr(reg, "tenant_exists", lambda _tid: True)

    reg.ensure_tenant_registered("tenant_ok")  # should not raise


def test_request_context_calls_registry_gate(monkeypatch):
    monkeypatch.setenv("EXECALC_ENFORCE_TENANT_REGISTRY", "1")

    called = {}

    def fake_gate(tid: str) -> None:
        called["tenant_id"] = tid

    # request_context imports ensure_tenant_registered into its module namespace
    monkeypatch.setattr(rc, "ensure_tenant_registered", fake_gate)

    with rc.request_context({"tenant_id": "tenant_abc"}, user_id="u1", role="admin"):
        pass

    assert called.get("tenant_id") == "tenant_abc"
