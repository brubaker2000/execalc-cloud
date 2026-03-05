import unittest
from src.service.decision_loop.persistence_helpers import save_decision_entry, get_decision_entry, get_all_decisions_for_tenant

class TestPersistenceHelpers(unittest.TestCase):

    def test_save_and_retrieve_decision(self):
        decision_data = {"decision_type": "trade", "details": {"pick": 8, "counterparty": 18}}
        entry_id = save_decision_entry(tenant_id="t1", user_id="u1", decision_data=decision_data)
        entry = get_decision_entry(entry_id)
        self.assertEqual(entry[1], "t1")
        self.assertEqual(entry[2], "u1")

    def test_get_all_decisions_for_tenant(self):
        decisions = get_all_decisions_for_tenant(tenant_id="t1")
        self.assertGreater(len(decisions), 0)

if __name__ == "__main__":
    unittest.main()
