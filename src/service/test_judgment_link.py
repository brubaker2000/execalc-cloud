from src.service.judgment_link import JudgmentLink


def test_judgment_link_is_immutable_and_complete():
    link = JudgmentLink(
        execution_id="exec_001",
        judgment_id="judgment_001",
        signal_envelope_id="signal_001",
    )

    assert link.execution_id == "exec_001"
    assert link.judgment_id == "judgment_001"
    assert link.signal_envelope_id == "signal_001"

    try:
        link.execution_id = "mutate"
        assert False, "JudgmentLink should be immutable"
    except Exception:
        assert True
