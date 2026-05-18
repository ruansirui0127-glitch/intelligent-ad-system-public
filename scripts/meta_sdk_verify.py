#!/usr/bin/env python3
"""Verify Meta Marketing API access with the official Business SDK."""

from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

try:
    from meta_verify import DEFAULT_API_VERSION, has_placeholder_values, load_env_file, redact_token
except ModuleNotFoundError:
    from scripts.meta_verify import DEFAULT_API_VERSION, has_placeholder_values, load_env_file, redact_token

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError


FIELD_MAP = {
    "ad_account": ["id", "name", "currency", "timezone_name", "account_status"],
    "campaigns": ["id", "name", "objective", "status", "effective_status"],
    "adsets": [
        "id",
        "name",
        "campaign_id",
        "optimization_goal",
        "billing_event",
        "bid_strategy",
        "status",
        "effective_status",
    ],
    "ads": ["id", "name", "campaign_id", "adset_id", "creative", "status", "effective_status"],
    "insights": [
        "date_start",
        "date_stop",
        "spend",
        "impressions",
        "reach",
        "frequency",
        "clicks",
        "inline_link_clicks",
        "ctr",
        "cpc",
        "cpm",
        "actions",
        "cost_per_action_type",
    ],
}


def fields_for(name: str) -> list[str]:
    return FIELD_MAP[name]


def normalize_account_id(account_id: str) -> str:
    account_id = account_id.strip()
    if account_id.startswith("act_"):
        return account_id
    return f"act_{account_id}"


def list_sample(edge, limit: int = 3) -> list[dict]:
    rows = []
    for idx, item in enumerate(edge):
        if idx >= limit:
            break
        rows.append(to_plain(item))
    return rows


def to_plain(value):
    if isinstance(value, dict):
        return {key: to_plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if hasattr(value, "export_all_data"):
        return to_plain(value.export_all_data())
    return value


def run_checks(env: dict[str, str]) -> int:
    token = env.get("META_ACCESS_TOKEN", "")
    account_id = env.get("META_AD_ACCOUNT_ID", "")
    api_version = env.get("META_API_VERSION", DEFAULT_API_VERSION)
    app_secret = env.get("META_APP_SECRET", "") or None

    if not token or not account_id:
        print("Missing META_ACCESS_TOKEN or META_AD_ACCOUNT_ID.")
        print("Create config/private/meta/.env from config/examples/meta.env.example.")
        return 2
    if has_placeholder_values(env):
        print("META_ACCESS_TOKEN or META_AD_ACCOUNT_ID still uses template values.")
        print("Edit config/private/meta/.env with your real System User Token and Ad Account ID.")
        return 2

    account_id = normalize_account_id(account_id)
    FacebookAdsApi.init(access_token=token, app_secret=app_secret, api_version=api_version)
    account = AdAccount(account_id)

    print(f"Meta SDK: facebook-business")
    print(f"Meta API version: {api_version}")
    print(f"Ad account: {account_id}")
    print(f"Token: {redact_token(token)}")

    checks = [
        ("ad_account", lambda: to_plain(account.api_get(fields=fields_for("ad_account")))),
        ("campaigns", lambda: list_sample(account.get_campaigns(fields=fields_for("campaigns")))),
        ("adsets", lambda: list_sample(account.get_ad_sets(fields=fields_for("adsets")))),
        ("ads", lambda: list_sample(account.get_ads(fields=fields_for("ads")))),
        (
            "insights",
            lambda: list_sample(
                account.get_insights(
                    fields=fields_for("insights"),
                    params={"level": "campaign", "date_preset": "last_7d", "limit": 3},
                )
            ),
        ),
    ]

    ok = True
    for label, fn in checks:
        try:
            payload = fn()
            print(f"[OK] {label}: {json.dumps(payload, ensure_ascii=False)[:2000]}")
        except FacebookRequestError as exc:
            ok = False
            print(f"[FAIL] {label}: {exc.api_error_message()}")
        except Exception as exc:  # noqa: BLE001 - command-line diagnostic should continue.
            ok = False
            print(f"[FAIL] {label}: {exc}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Meta Marketing API access via SDK.")
    parser.add_argument(
        "--env",
        default="config/private/meta/.env",
        help="Private env file path. Default: config/private/meta/.env",
    )
    args = parser.parse_args(argv)
    env = dict(os.environ)
    env.update(load_env_file(Path(args.env)))
    return run_checks(env)


if __name__ == "__main__":
    sys.exit(main())
