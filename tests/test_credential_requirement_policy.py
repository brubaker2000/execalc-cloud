import pathlib
import sys

import pytest

# Ensure repo root is on sys.path so "src.service..." imports work under pytest.
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.service.integrations.credentials import CredentialStoreError, CredentialRequirementPolicy


def test_no_env_means_not_required(monkeypatch):
    monkeypatch.delenv("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED", raising=False)
    pol = CredentialRequirementPolicy.from_env()

    assert pol.requires_credentials("tenant_any", "echo") is False
    assert pol.requires_credentials("tenant_any", "null") is False


def test_wildcard_applies(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED", '{"*":["echo"]}')
    pol = CredentialRequirementPolicy.from_env()

    assert pol.requires_credentials("tenant_x", "echo") is True
    assert pol.requires_credentials("tenant_x", "null") is False


def test_tenant_specific_overrides_wildcard(monkeypatch):
    monkeypatch.setenv(
        "EXECALC_CONNECTOR_CREDENTIAL_REQUIRED",
        '{"*":["echo"],"tenant_a":["null"]}',
    )
    pol = CredentialRequirementPolicy.from_env()

    # tenant_a uses its own list (override semantics)
    assert pol.requires_credentials("tenant_a", "null") is True
    assert pol.requires_credentials("tenant_a", "echo") is False

    # other tenants fall back to wildcard
    assert pol.requires_credentials("tenant_b", "echo") is True
    assert pol.requires_credentials("tenant_b", "null") is False


def test_invalid_json_raises(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED", '{"*":[')  # invalid JSON
    with pytest.raises(CredentialStoreError):
        CredentialRequirementPolicy.from_env()


def test_top_level_must_be_mapping(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED", '["not","a","mapping"]')
    with pytest.raises(CredentialStoreError):
        CredentialRequirementPolicy.from_env()


def test_entries_must_be_list_of_strings(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED", '{"*":["ok",1]}')
    with pytest.raises(CredentialStoreError):
        CredentialRequirementPolicy.from_env()

    monkeypatch.setenv("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED", '{"*":"not-a-list"}')
    with pytest.raises(CredentialStoreError):
        CredentialRequirementPolicy.from_env()
