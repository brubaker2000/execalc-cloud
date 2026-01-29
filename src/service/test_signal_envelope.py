import unittest

from src.service.signal_envelope import SignalEnvelope


class TestSignalEnvelope(unittest.TestCase):
    def test_signal_envelope_is_immutable_and_complete(self):
        envelope = SignalEnvelope(outputs={"result": "ok"})

        self.assertEqual(envelope.outputs["result"], "ok")
        self.assertEqual(envelope.meta, {})

        with self.assertRaises(Exception):
            envelope.outputs = {}


if __name__ == "__main__":
    unittest.main()
