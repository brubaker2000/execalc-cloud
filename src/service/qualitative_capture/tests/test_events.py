import unittest
from unittest.mock import patch

from src.service.qualitative_capture.events import ingest_event
from src.service.qualitative_capture.models import ConversationEvent


class TestIngestEvent(unittest.TestCase):
    @patch("src.service.qualitative_capture.events.insert_event")
    def test_returns_conversation_event(self, mock_insert):
        mock_insert.return_value = True
        evt = ingest_event(
            tenant_id="t1",
            session_id="s1",
            user_id="u1",
            role="operator",
            message_text="We will never compromise on data quality.",
        )
        self.assertIsInstance(evt, ConversationEvent)
        self.assertEqual(evt.tenant_id, "t1")
        self.assertEqual(evt.role, "operator")
        mock_insert.assert_called_once()

    @patch("src.service.qualitative_capture.events.insert_event")
    def test_event_id_is_generated(self, mock_insert):
        mock_insert.return_value = True
        evt = ingest_event(
            tenant_id="t1", session_id="s1", user_id="u1",
            role="operator", message_text="Some meaningful text here.",
        )
        self.assertTrue(len(evt.event_id) == 32)

    def test_invalid_role_raises(self):
        with self.assertRaises(ValueError):
            ingest_event(
                tenant_id="t1", session_id="s1", user_id="u1",
                role="robot", message_text="Some text.",
            )

    def test_empty_message_raises(self):
        with self.assertRaises(ValueError):
            ingest_event(
                tenant_id="t1", session_id="s1", user_id="u1",
                role="operator", message_text="   ",
            )

    @patch("src.service.qualitative_capture.events.insert_event", side_effect=Exception("db down"))
    def test_persistence_failure_returns_event(self, mock_insert):
        # DB failure should not raise — event is returned anyway
        evt = ingest_event(
            tenant_id="t1", session_id="s1", user_id="u1",
            role="operator", message_text="Data quality matters.",
        )
        self.assertIsInstance(evt, ConversationEvent)


if __name__ == "__main__":
    unittest.main()
