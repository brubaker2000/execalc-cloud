from src.service.signal_envelope import SignalEnvelope
import pytest


def test_signal_envelope_is_immutable_and_complete():
    envelope = SignalEnvelope(
        outputs={"result": "ok"},
    )

    assert envelope.outputs["result"] == "ok"
    assert envelope.meta == {}

    with pytest.raises(Exception):
        envelope.outputs = {}
