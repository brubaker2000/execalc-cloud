import unittest
from unittest.mock import patch

from src.service.decision_loop import persistence_helpers as ph


class TestPersistenceHelpers(unittest.TestCase):
    def test_save_and_retrieve_decision(self):
        decision_data = {
            "envelope_id": "entry_1",
            "decision_type": "trade",
            "details": {"pick": 8, "counterparty": 18},
        }

        with (
            patch.object(ph, "insert_execution_record") as mock_insert,
            patch.object(
                ph,
                "get_execution_record",
                return_value={
                    "tenant_id": "t1",
                    "envelope_id": "entry_1",
                    "ok": True,
                    "result": decision_data,
                    "created_at": "2026-03-08T00:00:00+00:00",
                },
            ) as mock_get,
        ):
            entry_id = ph.save_decision_entry(
                tenant_id="t1",
                user_id="u1",
                decision_data=decision_data,
            )
            self.assertEqual(entry_id, "entry_1")
            mock_insert.assert_called_once_with(
                tenant_id="t1",
                envelope_id="entry_1",
                result=decision_data,
            )

            entry = ph.get_decision_entry("entry_1", tenant_id="t1")
            self.assertEqual(entry["tenant_id"], "t1")
            self.assertEqual(entry["envelope_id"], "entry_1")
            mock_get.assert_called_once_with(tenant_id="t1", envelope_id="entry_1")

    def test_get_all_decisions_for_tenant(self):
        records = [
            {
                "tenant_id": "t1",
                "envelope_id": "entry_2",
                "ok": True,
                "created_at": "2026-03-08T00:00:00+00:00",
            },
            {
                "tenant_id": "t1",
                "envelope_id": "entry_1",
                "ok": True,
                "created_at": "2026-03-07T00:00:00+00:00",
            },
        ]

        with patch.object(ph, "list_execution_records", return_value=records) as mock_list:
            decisions = ph.get_all_decisions_for_tenant(tenant_id="t1")
            self.assertEqual(len(decisions), 2)
            self.assertEqual(decisions[0]["tenant_id"], "t1")
            mock_list.assert_called_once_with(tenant_id="t1", limit=100)


if __name__ == "__main__":
    unittest.main()
