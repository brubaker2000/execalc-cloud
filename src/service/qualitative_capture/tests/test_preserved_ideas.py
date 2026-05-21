import unittest
from unittest.mock import patch

from src.service.qualitative_capture.models import PreservedIdea
from src.service.qualitative_capture.preserved_ideas import memorialize


class TestMemorialize(unittest.TestCase):
    @patch("src.service.qualitative_capture.preserved_ideas.insert_preserved_idea")
    @patch("src.service.qualitative_capture.preserved_ideas.insert_nugget")
    @patch("src.service.qualitative_capture.preserved_ideas.admit_memorialized_item", create=True)
    def test_returns_preserved_idea(self, mock_admit, mock_nugget, mock_idea):
        mock_nugget.return_value = True
        mock_idea.return_value = True
        with patch("src.service.memory.qcr_bridge.admit_memorialized_item", return_value=True):
            idea = memorialize(
                tenant_id="t1",
                session_id="s1",
                source_event_id="evt1",
                selected_text="Fire hose problem is real.",
                memorialized_by="u1",
                claim_type="doctrine",
                domain="strategy",
            )
        self.assertIsInstance(idea, PreservedIdea)
        self.assertEqual(idea.tenant_id, "t1")
        self.assertEqual(idea.selected_text, "Fire hose problem is real.")
        self.assertEqual(idea.corroboration_count, 1)

    @patch("src.service.qualitative_capture.preserved_ideas.insert_preserved_idea")
    @patch("src.service.qualitative_capture.preserved_ideas.insert_nugget")
    def test_nugget_and_idea_ids_differ(self, mock_nugget, mock_idea):
        mock_nugget.return_value = True
        mock_idea.return_value = True
        with patch("src.service.memory.qcr_bridge.admit_memorialized_item", return_value=True):
            idea = memorialize(
                tenant_id="t1",
                session_id="s1",
                source_event_id="evt1",
                selected_text="Data quality matters greatly.",
                memorialized_by="u1",
                claim_type="principle",
            )
        self.assertNotEqual(idea.idea_id, idea.nugget_id)

    @patch("src.service.qualitative_capture.preserved_ideas.insert_preserved_idea")
    @patch("src.service.qualitative_capture.preserved_ideas.insert_nugget")
    def test_db_failure_does_not_raise(self, mock_nugget, mock_idea):
        mock_nugget.side_effect = Exception("db down")
        mock_idea.side_effect = Exception("db down")
        with patch("src.service.memory.qcr_bridge.admit_memorialized_item", return_value=True):
            idea = memorialize(
                tenant_id="t1",
                session_id="s1",
                source_event_id="evt1",
                selected_text="Something important was said here.",
                memorialized_by="u1",
                claim_type="doctrine",
            )
        self.assertIsInstance(idea, PreservedIdea)


if __name__ == "__main__":
    unittest.main()
