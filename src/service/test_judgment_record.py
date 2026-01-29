import unittest

from src.service.judgment_record import JudgmentRecord


class TestJudgmentRecord(unittest.TestCase):
    def test_judgment_record_is_immutable_and_complete(self):
        record = JudgmentRecord(
            judgment_id="judgment_001",
            decision="Proceed with acquisition",
            rationale="Strong strategic fit and favorable risk profile",
            context={
                "execution_id": "exec_001",
                "scenario": "m&a_decision",
            },
        )

        self.assertEqual(record.judgment_id, "judgment_001")
        self.assertEqual(record.decision, "Proceed with acquisition")
        self.assertTrue(record.rationale.startswith("Strong strategic fit"))
        self.assertEqual(record.context["scenario"], "m&a_decision")
        self.assertIsNotNone(record.created_at)

        with self.assertRaises(Exception):
            record.decision = "Reverse decision"


if __name__ == "__main__":
    unittest.main()
