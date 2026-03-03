import src.service.api as api


def test_decision_run_returns_envelope_and_persist_metadata(monkeypatch):
    # Enable dev harness so we can authenticate via headers.
    monkeypatch.setenv("EXECALC_DEV_HARNESS", "1")

    # Keep persistence off (default). We want to assert best-effort metadata indicates not persisted.
    monkeypatch.delenv("EXECALC_PERSIST_EXECUTIONS", raising=False)

    c = api.app.test_client()

    r = c.post(
        "/decision/run",
        headers={"X-Tenant-Id": "t1", "X-User-Id": "u1", "X-Role": "operator"},
        json={
            "scenario": {
                "scenario_type": "draft_trade",
                "governing_objective": "cut_payroll",
                "prompt": "Pick 8 vs 18 trade-down scenario under payroll mandate",
                "facts": {"you_pick": 8, "counterparty_pick": 18},
            }
        },
    )

    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True

    audit = body.get("audit") or {}
    assert isinstance(audit.get("envelope_id"), str)
    assert len(audit["envelope_id"]) >= 16

    persist = audit.get("persist") or {}
    assert persist.get("persisted") is False
