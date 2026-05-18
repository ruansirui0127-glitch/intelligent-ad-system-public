import unittest

from scripts.meta_sdk_verify import fields_for, to_plain


class MetaSdkVerifyTests(unittest.TestCase):
    def test_fields_for_known_objects(self):
        self.assertIn("account_status", fields_for("ad_account"))
        self.assertIn("objective", fields_for("campaigns"))
        self.assertIn("optimization_goal", fields_for("adsets"))
        self.assertIn("creative", fields_for("ads"))

    def test_fields_for_unknown_object(self):
        with self.assertRaises(KeyError):
            fields_for("unknown")

    def test_to_plain_recurses_exportable_objects(self):
        class Exportable:
            def export_all_data(self):
                return {"creative": {"id": "123"}}

        self.assertEqual(to_plain({"ad": Exportable()}), {"ad": {"creative": {"id": "123"}}})


if __name__ == "__main__":
    unittest.main()
