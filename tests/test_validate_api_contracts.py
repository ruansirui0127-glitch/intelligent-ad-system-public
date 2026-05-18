import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_api_contracts import (
    ContractError,
    validate_account_metrics_payload,
    validate_accounts_tree_payload,
    validate_metric_facts_payload,
    validate_response_envelope,
    validate_sample_file,
    validate_sync_status_payload,
)


class ValidateApiContractsTests(unittest.TestCase):
    def test_response_envelope_requires_data_meta_and_errors(self):
        with self.assertRaises(ContractError) as ctx:
            validate_response_envelope({"data": {}, "meta": {}})

        self.assertIn("errors", str(ctx.exception))

    def test_accounts_tree_rejects_invalid_goal_type(self):
        payload = {
            "data": {
                "accounts": [
                    {
                        "id": "meta:account:act_sample",
                        "platform": "meta",
                        "object_type": "account",
                        "external_id": "act_sample",
                        "name": "Sample",
                        "status": "ACTIVE",
                        "children": [
                            {
                                "id": "meta:campaign:cmp_sample",
                                "platform": "meta",
                                "object_type": "campaign",
                                "external_id": "cmp_sample",
                                "parent_id": "meta:account:act_sample",
                                "name": "Campaign",
                                "status": "ACTIVE",
                                "platform_object_type": "campaign",
                                "goal_type": "bad_goal",
                                "children": [],
                            }
                        ],
                    }
                ]
            },
            "meta": {"request_id": "req", "api_version": "v0", "generated_at": "2026-05-15T10:00:00+08:00"},
            "errors": [],
        }

        with self.assertRaises(ContractError) as ctx:
            validate_accounts_tree_payload(payload)

        self.assertIn("goal_type", str(ctx.exception))

    def test_metric_facts_require_metric_stage_and_raw_metric_name(self):
        payload = {
            "data": {
                "items": [
                    {
                        "fact_id": "fact_1",
                        "platform": "meta",
                        "object_type": "ad_group",
                        "object_id": "meta:ad_group:adset_sample",
                        "metric_name": "quality_lead",
                        "metric_value": 1,
                        "unit": "count",
                        "date": "2026-05-14",
                        "time_window": {
                            "date_start": "2026-05-14",
                            "date_stop": "2026-05-14",
                            "time_grain": "day",
                            "timezone": "Asia/Shanghai",
                        },
                        "goal_type": "quality_lead",
                        "metric_version": "meta_v0_202605",
                        "sync_batch": "sync_1",
                        "source_quality": "complete",
                        "dimensions": {},
                        "attribution_window": "7d_click",
                    }
                ]
            },
            "meta": {
                "request_id": "req",
                "api_version": "v0",
                "generated_at": "2026-05-15T10:00:00+08:00",
                "pagination": {"limit": 100, "next_cursor": None},
            },
            "errors": [],
        }

        with self.assertRaises(ContractError) as ctx:
            validate_metric_facts_payload(payload)

        self.assertIn("metric_stage", str(ctx.exception))

    def test_sample_payloads_pass_contract_validation(self):
        sample_dir = Path("data/sample")
        for name in [
            "accounts-tree.meta.sample.json",
            "account-metrics.meta.sample.json",
            "sync-status.meta.sample.json",
            "metric-facts.meta.sample.json",
        ]:
            with self.subTest(name=name):
                validate_sample_file(sample_dir / name)

    def test_unknown_sample_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unknown.meta.sample.json"
            path.write_text(json.dumps({"data": {}, "meta": {}, "errors": []}))

            with self.assertRaises(ContractError) as ctx:
                validate_sample_file(path)

        self.assertIn("Unsupported sample file", str(ctx.exception))

    def test_account_metrics_and_sync_status_accept_minimal_valid_payloads(self):
        account_metrics = {
            "data": {
                "object": {
                    "id": "meta:account:act_sample",
                    "platform": "meta",
                    "object_type": "account",
                    "name": "Sample",
                },
                "time_window": {
                    "date_start": "2026-05-01",
                    "date_stop": "2026-05-14",
                    "time_grain": "day",
                    "timezone": "Asia/Shanghai",
                },
                "metrics": [
                    {
                        "metric_name": "spend",
                        "metric_value": 1.2,
                        "unit": "currency",
                        "metric_stage": "cost",
                        "goal_type": "quality_lead",
                    }
                ],
                "series": [],
            },
            "meta": {"request_id": "req", "api_version": "v0", "generated_at": "2026-05-15T10:00:00+08:00"},
            "errors": [],
        }
        sync_status = {
            "data": {
                "current": {
                    "platform": "meta",
                    "status": "success",
                    "last_sync_batch": "sync_1",
                    "last_started_at": "2026-05-15T09:55:00+08:00",
                    "last_finished_at": "2026-05-15T09:58:00+08:00",
                    "date_start": "2026-05-01",
                    "date_stop": "2026-05-14",
                    "objects_synced": {"accounts": 1, "campaigns": 1, "ad_groups": 1, "ads": 1, "metric_facts": 1},
                    "warnings": [],
                },
                "history": [],
            },
            "meta": {"request_id": "req", "api_version": "v0", "generated_at": "2026-05-15T10:00:00+08:00"},
            "errors": [],
        }

        validate_account_metrics_payload(account_metrics)
        validate_sync_status_payload(sync_status)


if __name__ == "__main__":
    unittest.main()
