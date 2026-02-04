import pathlib
import sys

import pytest

# Ensure repo root is on sys.path so "src.service..." imports work under pytest.
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.service.integrations.credentials import CredentialStoreError, EnvCredentialStore


def test_no_env_means_not_configured(monkeypatch):
    monkeypatch.delenv("EXECALC_CONNECTOR_SECRET_REFS", raising=False)
    store = EnvCredentialStore.from_env()

    s = store.status("tenant_any", "echo")
    assert s.configured is False
    assert s.secret_ref is None


def test_wildcard_applies(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_SECRET_REFS", '{"*":{"echo":"secret://ref-echo"}}')
    store = EnvCredentialStore.from_env()

    s = store.status("tenant_x", "echo")
    assert s.configured is True
    assert s.secret_ref == "secret://ref-echo"


def test_tenant_specific_overrides_wildcard(monkeypatch):
    monkeypatch.setenv(
        "EXECALC_CONNECTOR_SECRET_REFS",
        '{"*":{"echo":"secret://ref-echo-default"},"tenant_a":{"echo":"secret://ref-echo-tenant-a"}}',
    )
    store = EnvCredentialStore.from_env()

    s_a = store.status("tenant_a", "echo")
    assert s_a.configured is True
    assert s_a.secret_ref == "secret://ref-echo-tenant-a"

    s_b = store.status("tenant_b", "echo")
    assert s_b.configured is True
    assert s_b.secret_ref == "secret://ref-echo-default"


def test_missing_connector_returns_not_configured(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_SECRET_REFS", '{"*":{"echo":"secret://ref-echo"}}')
    store = EnvCredentialStore.from_env()

    s = store.status("tenant_any", "gmail")
    assert s.configured is False
    assert s.secret_ref is None


def test_invalid_json_raises(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_SECRET_REFS", '{"*":[')  # invalid JSON
    with pytest.raises(CredentialStoreError):
        EnvCredentialStore.from_env()


def test_top_level_must_be_mapping(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_SECRET_REFS", '["not","a","mapping"]')
    with pytest.raises(CredentialStoreError):
        EnvCredentialStore.from_env()


def test_per_tenant_value_must_be_mapping(monkeypatch):
    # Top-level is a mapping, but per-tenant entry is not mapping connector->ref.
    monkeypatch.setenv("EXECALC_CONNECTOR_SECRET_REFS", '{"*":["bad"]}')
    store = EnvCredentialStore.from_env()

    with pytest.raises(CredentialStoreError):
        store.status("tenant_any", "echo")
