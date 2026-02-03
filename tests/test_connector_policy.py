import pathlib
import sys

import pytest

# Ensure repo root is on sys.path so "src.service..." imports work under pytest.
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.service.integrations.connector import ConnectorContext
from src.service.integrations.policy import ConnectorPolicy, ConnectorPolicyError


def test_allowed_connectors_no_allowlist_all_available(monkeypatch):
    monkeypatch.delenv("EXECALC_CONNECTOR_ALLOWLIST", raising=False)
    monkeypatch.delenv("EXECALC_CONNECTOR_REQUIRED_SCOPES", raising=False)

    policy = ConnectorPolicy.from_env()
    available = ["null", "echo"]

    assert policy.allowed_connectors("tenant_any", available) == ["echo", "null"]


def test_allowed_connectors_wildcard_and_tenant_specific(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_ALLOWLIST", '{"*":["null"],"tenant_a":["echo"]}')
    monkeypatch.delenv("EXECALC_CONNECTOR_REQUIRED_SCOPES", raising=False)

    policy = ConnectorPolicy.from_env()
    available = ["null", "echo"]

    assert policy.allowed_connectors("tenant_a", available) == ["echo"]
    assert policy.allowed_connectors("tenant_b", available) == ["null"]


def test_authorize_or_raise_missing_scope(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_ALLOWLIST", '{"*":["echo"]}')
    monkeypatch.setenv("EXECALC_CONNECTOR_REQUIRED_SCOPES", '{"echo":["echo.readonly"]}')

    policy = ConnectorPolicy.from_env()
    available = ["echo"]

    ctx_missing = ConnectorContext(tenant_id="tenant_test_001", actor_id="u1", scopes=[])
    with pytest.raises(PermissionError):
        policy.authorize_or_raise("echo", ctx_missing, available)

    ctx_ok = ConnectorContext(tenant_id="tenant_test_001", actor_id="u1", scopes=["echo.readonly"])
    policy.authorize_or_raise("echo", ctx_ok, available)  # no exception


def test_from_env_invalid_json_raises(monkeypatch):
    monkeypatch.setenv("EXECALC_CONNECTOR_ALLOWLIST", '{"*":[')  # invalid JSON
    monkeypatch.delenv("EXECALC_CONNECTOR_REQUIRED_SCOPES", raising=False)

    with pytest.raises(ConnectorPolicyError):
        ConnectorPolicy.from_env()
