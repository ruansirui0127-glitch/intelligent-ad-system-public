import unittest

from scripts.meta_list_accounts import normalize_status, account_summary


class MetaListAccountsTests(unittest.TestCase):
    def test_normalize_status_known_values(self):
        self.assertEqual(normalize_status(1), "ACTIVE")
        self.assertEqual(normalize_status(2), "DISABLED")
        self.assertEqual(normalize_status("3"), "UNSETTLED")

    def test_account_summary_keeps_key_fields(self):
        row = account_summary(
            {
                "id": "act_123",
                "name": "Main",
                "currency": "USD",
                "timezone_name": "Asia/Hong_Kong",
                "account_status": 1,
                "amount_spent": "100",
                "balance": "20",
            }
        )
        self.assertEqual(row["id"], "act_123")
        self.assertEqual(row["status"], "ACTIVE")


if __name__ == "__main__":
    unittest.main()
