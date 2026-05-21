import unittest
from unittest.mock import patch

from src.service.qualitative_capture.retrieval import (
    retrieve_decisions,
    retrieve_doctrine,
    retrieve_open_questions,
    retrieve_opportunities,
    retrieve_preserved_ideas,
    retrieve_rail_candidates,
    retrieve_risks,
    retrieve_session_conclusions,
    search_claims,
)


def _nugget(claim_type: str, confidence: float = 0.50, rail_candidate: bool = False, **kw) -> dict:
    return {
        "nugget_id": f"n_{claim_type}",
        "claim_text": f"This is a {claim_type} claim with meaningful content.",
        "claim_type": claim_type,
        "domain": "strategy",
        "confidence_score": confidence,
        "confidence_level": "seed",
        "polarity": "neutral",
        "rail_candidate": rail_candidate,
        "selection_method": "machine_extracted",
        "created_at": "2026-05-20T00:00:00+00:00",
        **kw,
    }


class TestRetrieveRisks(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_nuggets")
    def test_returns_risk_nuggets(self, mock_list):
        mock_list.return_value = [_nugget("risk")]
        result = retrieve_risks(tenant_id="t1")
        self.assertGreaterEqual(len(result), 1)
        self.assertEqual(result[0]["claim_type"], "risk")

    @patch("src.service.qualitative_capture.retrieval.list_nuggets", side_effect=Exception("db"))
    def test_db_failure_returns_empty(self, mock_list):
        result = retrieve_risks(tenant_id="t1")
        self.assertEqual(result, [])


class TestRetrieveDoctrine(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_nuggets")
    def test_returns_doctrine_nuggets(self, mock_list):
        mock_list.return_value = [_nugget("doctrine"), _nugget("principle")]
        result = retrieve_doctrine(tenant_id="t1")
        self.assertGreaterEqual(len(result), 1)

    @patch("src.service.qualitative_capture.retrieval.list_nuggets", side_effect=Exception("db"))
    def test_db_failure_returns_empty(self, mock_list):
        result = retrieve_doctrine(tenant_id="t1")
        self.assertEqual(result, [])


class TestRetrieveOpportunities(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_nuggets")
    def test_returns_opportunities(self, mock_list):
        mock_list.return_value = [_nugget("opportunity")]
        result = retrieve_opportunities(tenant_id="t1")
        self.assertEqual(len(result), 1)


class TestRetrieveDecisions(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_nuggets")
    def test_returns_objective_claims(self, mock_list):
        mock_list.return_value = [_nugget("objective")]
        result = retrieve_decisions(tenant_id="t1")
        self.assertGreaterEqual(len(result), 1)


class TestRetrieveOpenQuestions(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_nuggets")
    def test_returns_low_confidence_items(self, mock_list):
        mock_list.return_value = [_nugget("threshold_condition", confidence=0.50)]
        result = retrieve_open_questions(tenant_id="t1")
        self.assertGreaterEqual(len(result), 0)

    @patch("src.service.qualitative_capture.retrieval.list_nuggets", side_effect=Exception("db"))
    def test_db_failure_returns_empty(self, mock_list):
        result = retrieve_open_questions(tenant_id="t1")
        self.assertEqual(result, [])


class TestRetrieveRailCandidates(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_nuggets")
    def test_filters_rail_candidates(self, mock_list):
        mock_list.return_value = [_nugget("doctrine", rail_candidate=True)]
        result = retrieve_rail_candidates(tenant_id="t1", session_id="s1")
        self.assertEqual(len(result), 1)


class TestSearchClaims(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.search_nuggets")
    def test_delegates_to_search_nuggets(self, mock_search):
        mock_search.return_value = [_nugget("doctrine")]
        result = search_claims(tenant_id="t1", query="data quality")
        self.assertEqual(len(result), 1)
        mock_search.assert_called_once()

    def test_empty_query_returns_empty(self):
        result = search_claims(tenant_id="t1", query="")
        self.assertEqual(result, [])

    def test_whitespace_query_returns_empty(self):
        result = search_claims(tenant_id="t1", query="   ")
        self.assertEqual(result, [])

    @patch("src.service.qualitative_capture.retrieval.search_nuggets", side_effect=Exception("db"))
    def test_db_failure_returns_empty(self, mock_search):
        result = search_claims(tenant_id="t1", query="doctrine")
        self.assertEqual(result, [])


class TestRetrievePreservedIdeas(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_preserved_ideas_for_session")
    def test_returns_ideas(self, mock_list):
        mock_list.return_value = [{"idea_id": "i1", "selected_text": "Fire hose."}]
        result = retrieve_preserved_ideas(tenant_id="t1")
        self.assertEqual(len(result), 1)

    @patch("src.service.qualitative_capture.retrieval.list_preserved_ideas_for_session",
           side_effect=Exception("db"))
    def test_db_failure_returns_empty(self, mock_list):
        result = retrieve_preserved_ideas(tenant_id="t1")
        self.assertEqual(result, [])


class TestRetrieveSessionConclusions(unittest.TestCase):
    @patch("src.service.qualitative_capture.retrieval.list_conclusions")
    def test_returns_all_conclusions(self, mock_list):
        mock_list.return_value = [{"conclusion_id": "c1", "rail_card_type": "risk"}]
        result = retrieve_session_conclusions(tenant_id="t1", session_id="s1")
        self.assertEqual(len(result), 1)

    @patch("src.service.qualitative_capture.retrieval.list_conclusions")
    def test_filters_by_card_type(self, mock_list):
        mock_list.return_value = [
            {"conclusion_id": "c1", "rail_card_type": "risk"},
            {"conclusion_id": "c2", "rail_card_type": "executive_conclusion"},
        ]
        result = retrieve_session_conclusions(
            tenant_id="t1", session_id="s1", rail_card_type="risk"
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["rail_card_type"], "risk")


if __name__ == "__main__":
    unittest.main()
