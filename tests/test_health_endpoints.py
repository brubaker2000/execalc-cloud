import os

import src.service.api as api


def test_healthz_no_dev_harness_required(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "0")
    c = api.app.test_client()
    r = c.get("/healthz")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True



def test_livez_no_dev_harness_required(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "0")
    c = api.app.test_client()
    r = c.get("/livez")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True


def test_readyz_no_dev_harness_required(monkeypatch):
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "0")
    # default persist is off in tests, so ready should be true without DB.
    monkeypatch.delenv("EXECALC_PERSIST_EXECUTIONS", raising=False)
    c = api.app.test_client()
    r = c.get("/readyz")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
    assert body["ready"] is True
