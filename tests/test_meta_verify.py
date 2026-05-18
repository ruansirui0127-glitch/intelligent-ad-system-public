import unittest

from scripts.meta_verify import load_env_text, redact_token, build_graph_url, has_placeholder_values


class MetaVerifyTests(unittest.TestCase):
    def test_load_env_text_ignores_comments_and_quotes(self):
        env = load_env_text(
            """
            # comment
            META_ACCESS_TOKEN="abc123"
            META_AD_ACCOUNT_ID='act_456'
            EMPTY=
            """
        )
        self.assertEqual(env["META_ACCESS_TOKEN"], "abc123")
        self.assertEqual(env["META_AD_ACCOUNT_ID"], "act_456")
        self.assertEqual(env["EMPTY"], "")

    def test_redact_token_keeps_no_secret_material(self):
        self.assertEqual(redact_token("EAABCD1234567890"), "EAAB...7890")
        self.assertEqual(redact_token("short"), "****")

    def test_build_graph_url_normalizes_account_id(self):
        url = build_graph_url("v25.0", "act_123", "campaigns", {"fields": "id,name"})
        self.assertIn("https://graph.facebook.com/v25.0/act_123/campaigns?", url)
        self.assertIn("fields=id%2Cname", url)

    def test_detects_template_values(self):
        self.assertTrue(
            has_placeholder_values(
                {
                    "META_ACCESS_TOKEN": "your_system_user_token",
                    "META_AD_ACCOUNT_ID": "act_your_ad_account_id",
                }
            )
        )
        self.assertFalse(
            has_placeholder_values(
                {
                    "META_ACCESS_TOKEN": "EAABCD1234567890",
                    "META_AD_ACCOUNT_ID": "act_123456789",
                }
            )
        )


if __name__ == "__main__":
    unittest.main()
