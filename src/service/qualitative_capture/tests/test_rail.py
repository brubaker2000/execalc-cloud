import unittest
from datetime import UTC, datetime
from unittest.mock import patch

from src.service.qualitative_capture.models import (
    ExecutiveConclusion,
    PreservedIdea,
    RailArtifact,
    RightRailCard,
)
from src.service.qualitative_capture.rail import (
    persist_card_as_artifact,
    project_conclusion_to_rail,
    project_idea_to_rail,
    publish_conclusions_to_rail,
)


def _make_conclusion(**kw) -> ExecutiveConclusion:
    defaults = dict(
        conclusion_id="c1",
        tenant_id="t1",
        session_id="s1",
        conclusion_text="Key doctrine signal.",
        source_nugget_ids=["n1", "n2"],
        claim_types_present=["doctrine"],
        reconstruction_confidence=0.50,
        domain="strategy",
        polarity="neutral",
        rail_card_type="executive_conclusion",
        generated_at=datetime.now(UTC),
    )
    defaults.update(kw)
    return ExecutiveConclusion(**defaults)


def _make_idea(**kw) -> PreservedIdea:
    defaults = dict(
        idea_id="i1",
        tenant_id="t1",
        nugget_id="n1",
        session_id="s1",
        source_event_id="evt1",
        selected_text="Fire hose problem.",
        memorialized_by="u1",
        memorialized_at=datetime.now(UTC),
    )
    defaults.update(kw)
    return PreservedIdea(**defaults)


class TestProjectConclusionToRail(unittest.TestCase):
    def test_returns_right_rail_card(self):
        card = project_conclusion_to_rail(_make_conclusion())
        self.assertIsInstance(card, RightRailCard)
        self.assertEqual(card.card_type, "executive_conclusion")
        self.assertFalse(card.is_memorialized)
        self.assertFalse(card.is_pinned)
        self.assertFalse(card.is_dismissed)

    def test_card_text_matches_conclusion(self):
        c = _make_conclusion(conclusion_text="Doctrine signal captured.")
        card = project_conclusion_to_rail(c)
        self.assertEqual(card.card_text, "Doctrine signal captured.")

    def test_display_rank_applied(self):
        card = project_conclusion_to_rail(_make_conclusion(), display_rank=3)
        self.assertEqual(card.display_rank, 3)


class TestProjectIdeaToRail(unittest.TestCase):
    def test_returns_memorialized_card(self):
        card = project_idea_to_rail(_make_idea())
        self.assertIsInstance(card, RightRailCard)
        self.assertEqual(card.card_type, "preserved_idea")
        self.assertTrue(card.is_memorialized)

    def test_card_text_is_selected_text(self):
        idea = _make_idea(selected_text="Fire hose problem solved by garden hose.")
        card = project_idea_to_rail(idea)
        self.assertEqual(card.card_text, "Fire hose problem solved by garden hose.")


class TestPersistCardAsArtifact(unittest.TestCase):
    @patch("src.service.qualitative_capture.rail.insert_rail_artifact")
    def test_returns_rail_artifact(self, mock_insert):
        mock_insert.return_value = True
        card = project_conclusion_to_rail(_make_conclusion())
        artifact = persist_card_as_artifact(card, operator_action="preserved", actioned_by="u1")
        self.assertIsInstance(artifact, RailArtifact)
        self.assertEqual(artifact.operator_action, "preserved")
        self.assertEqual(artifact.second_order_deconstruction_status, "pending")
        mock_insert.assert_called_once()

    def test_invalid_action_raises(self):
        card = project_conclusion_to_rail(_make_conclusion())
        with self.assertRaises(ValueError):
            persist_card_as_artifact(card, operator_action="deleted")


class TestPublishConclusionsToRail(unittest.TestCase):
    @patch("src.service.qualitative_capture.rail.insert_rail_card")
    def test_publishes_all_conclusions(self, mock_insert):
        mock_insert.return_value = True
        conclusions = [_make_conclusion(conclusion_id=f"c{i}") for i in range(3)]
        cards = publish_conclusions_to_rail(conclusions)
        self.assertEqual(len(cards), 3)
        self.assertEqual(mock_insert.call_count, 3)


if __name__ == "__main__":
    unittest.main()
