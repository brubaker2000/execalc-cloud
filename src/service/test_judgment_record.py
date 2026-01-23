from src.service.judgment_record import JudgmentRecord
import pytest


def test_judgment_record_is_immutable_and_complete():
    record = JudgmentRecord(
        judgment_id="judgment_001",
        decision="Proceed with acquisition",
        rationale="Strong strategic fit and favorable risk profile",
        context={
            "execution_id": "exec_001",
            "scenario": "m&a_decision",
        },
    )

    assert record.judgment_id == "judgment_001"
    assert record.decision == "Proceed with acquisition"
    assert record.rationale.startswith("Strong strategic fit")
    assert record.context["scenario"] == "m&a_decision"
    assert record.created_at is not None

    with pytest.raises(Exception):
        record.decision = "Reverse decision"
