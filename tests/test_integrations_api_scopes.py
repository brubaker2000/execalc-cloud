import importlib
import pathlib
import sys

import pytest  # noqa: F401

# Ensure repo root is on sys.path so "src.service..." imports work under pytest.
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load_app(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")
    # Policy: echo is allowlisted and requires echo.readonly scope.
    monkeypatch.setenv("EXECALC_CONNECTOR_ALLOWLIST", '{"*":["echo","null"]}')
    monkeypatch.setenv("EXECALC_CONNECTOR_REQUIRED_SCOPES", '{"echo":["echo.readonly"],"null":["null.readonly"]}')

    import src.service.api as api
    api = importlib.reload(api)
    return api.app


def test_scopes_from_header_allows(monkeypatch):
    app = _load_app(monkeypatch)
    client = app.test_client()

    resp = client.post(
        "/integrations/echo/healthcheck",
        json={"actor_id": "u1"},
        headers={
            "X-User-Id": "u1",
            "X-Tenant-Id": "tenant_test_001",
            "X-Role": "operator",
            "X-Scopes": "echo.readonly",
        },
    )

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["data"]["connector"] == "echo"


def test_scopes_in_body_is_rejected(monkeypatch):
    app = _load_app(monkeypatch)
    client = app.test_client()

    resp = client.post(
        "/integrations/echo/healthcheck",
        json={"actor_id": "u1", "scopes": ["echo.readonly"]},
        headers={
            "X-User-Id": "u1",
            "X-Tenant-Id": "tenant_test_001",
            "X-Role": "operator",
        },
    )

    assert resp.status_code == 400
    data = resp.get_json()
    assert data["ok"] is False
    assert "X-Scopes" in data["error"]


def test_missing_scope_still_denied(monkeypatch):
    app = _load_app(monkeypatch)
    client = app.test_client()

    resp = client.post(
        "/integrations/echo/healthcheck",
        json={"actor_id": "u1"},
        headers={
            "X-User-Id": "u1",
            "X-Tenant-Id": "tenant_test_001",
            "X-Role": "operator",
        },
    )

    assert resp.status_code == 403
    data = resp.get_json()
    assert data["ok"] is False
    assert "Missing required scopes" in data["error"]
