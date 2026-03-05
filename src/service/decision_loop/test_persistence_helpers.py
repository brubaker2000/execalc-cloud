import unittest
from unittest.mock import MagicMock, patch

from src.service.decision_loop import persistence_helpers as ph


class TestPersistenceHelpers(unittest.TestCase):
    def test_save_and_retrieve_decision(self):
        # Fake cursor/conn behavior
        cursor = MagicMock()
        cursor.fetchone.side_effect = [["entry_1"], ("entry_1", "t1", "u1", {"k": "v"})]
        cursor.fetchall.return_value = [("entry_1", "t1", "u1", {"k": "v"})]

        conn = MagicMock()
        conn.cursor.return_value = cursor

        with patch.object(ph, "get_conn", return_value=conn):
            decision_data = {"decision_type": "trade", "details": {"pick": 8, "counterparty": 18}}
            entry_id = ph.save_decision_entry(tenant_id="t1", user_id="u1", decision_data=decision_data)
            self.assertEqual(entry_id, "entry_1")

            entry = ph.get_decision_entry(entry_id)
            self.assertEqual(entry[1], "t1")
            self.assertEqual(entry[2], "u1")

    def test_get_all_decisions_for_tenant(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = [
            ("entry_2", "t1", "u1", {"decision_type": "x"}),
            ("entry_1", "t1", "u1", {"decision_type": "y"}),
        ]

        conn = MagicMock()
        conn.cursor.return_value = cursor

        with patch.object(ph, "get_conn", return_value=conn):
            decisions = ph.get_all_decisions_for_tenant(tenant_id="t1")
            self.assertEqual(len(decisions), 2)
            self.assertEqual(decisions[0][1], "t1")


if __name__ == "__main__":
    unittest.main()
