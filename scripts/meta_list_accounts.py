#!/usr/bin/env python3
"""List ad accounts visible to a Meta System User Token."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from facebook_business.adobjects.user import User
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError

try:
    from meta_verify import DEFAULT_API_VERSION, has_placeholder_values, load_env_file, redact_token
except ModuleNotFoundError:
    from scripts.meta_verify import DEFAULT_API_VERSION, has_placeholder_values, load_env_file, redact_token


STATUS_LABELS = {
    1: "ACTIVE",
    2: "DISABLED",
    3: "UNSETTLED",
    7: "PENDING_RISK_REVIEW",
    8: "PENDING_SETTLEMENT",
    9: "IN_GRACE_PERIOD",
    100: "PENDING_CLOSURE",
    101: "CLOSED",
    201: "ANY_ACTIVE",
    202: "ANY_CLOSED",
}


def normalize_status(value) -> str:
    try:
        return STATUS_LABELS.get(int(value), str(value))
    except (TypeError, ValueError):
        return str(value)


def account_summary(account: dict) -> dict:
    return {
        "id": account.get("id"),
        "name": account.get("name"),
        "currency": account.get("currency"),
        "timezone": account.get("timezone_name"),
        "status": normalize_status(account.get("account_status")),
        "amount_spent": account.get("amount_spent"),
        "balance": account.get("balance"),
    }


def run(env: dict[str, str]) -> int:
    token = env.get("META_ACCESS_TOKEN", "")
    api_version = env.get("META_API_VERSION", DEFAULT_API_VERSION)
    app_secret = env.get("META_APP_SECRET", "") or None
    if not token:
        print("Missing META_ACCESS_TOKEN.")
        return 2
    if has_placeholder_values({"META_ACCESS_TOKEN": token, "META_AD_ACCOUNT_ID": "act_123"}):
        print("META_ACCESS_TOKEN still uses template value.")
        return 2

    FacebookAdsApi.init(access_token=token, app_secret=app_secret, api_version=api_version)
    print(f"Meta API version: {api_version}")
    print(f"Token: {redact_token(token)}")
    print("Visible ad accounts:")
    fields = ["id", "name", "currency", "timezone_name", "account_status", "amount_spent", "balance"]
    try:
        accounts = User(fbid="me").get_ad_accounts(fields=fields, params={"limit": 100})
        rows = [account_summary(dict(account)) for account in accounts]
    except FacebookRequestError as exc:
        print(f"[FAIL] {exc.api_error_message()}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {exc}")
        return 1

    if not rows:
        print("No ad accounts returned for this token.")
        return 1
    for idx, row in enumerate(rows, 1):
        print(f"{idx}. {json.dumps(row, ensure_ascii=False)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List Meta ad accounts visible to this token.")
    parser.add_argument("--env", default="config/private/meta/.env")
    args = parser.parse_args(argv)
    env = dict(os.environ)
    env.update(load_env_file(Path(args.env)))
    return run(env)


if __name__ == "__main__":
    sys.exit(main())
