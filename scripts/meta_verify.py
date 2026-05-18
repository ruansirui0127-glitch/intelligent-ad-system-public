#!/usr/bin/env python3
"""Verify Meta Marketing API read access without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_API_VERSION = "v25.0"


def load_env_text(text: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        env[key.strip()] = value
    return env


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return load_env_text(path.read_text())


def redact_token(token: str) -> str:
    if len(token) < 12:
        return "****"
    return f"{token[:4]}...{token[-4:]}"


def normalize_account_id(account_id: str) -> str:
    account_id = account_id.strip()
    if account_id.startswith("act_"):
        return account_id
    return f"act_{account_id}"


def has_placeholder_values(env: dict[str, str]) -> bool:
    token = env.get("META_ACCESS_TOKEN", "").strip()
    account_id = env.get("META_AD_ACCOUNT_ID", "").strip()
    placeholders = {
        "your_system_user_token",
        "act_your_ad_account_id",
        "your_ad_account_id",
    }
    return token in placeholders or account_id in placeholders


def build_graph_url(
    api_version: str, object_id: str, edge: str | None = None, params: dict[str, str] | None = None
) -> str:
    base = f"https://graph.facebook.com/{api_version}/{object_id}"
    if edge:
        base = f"{base}/{edge}"
    if params:
        return f"{base}?{urllib.parse.urlencode(params)}"
    return base


def graph_get(
    api_version: str, object_id: str, edge: str | None, params: dict[str, str], token: str
) -> dict:
    query = dict(params)
    query["access_token"] = token
    url = build_graph_url(api_version, object_id, edge, query)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def summarize_list(payload: dict, sample_fields: list[str]) -> dict:
    data = payload.get("data", [])
    first = data[0] if data else {}
    return {
        "count_returned": len(data),
        "sample": {field: first.get(field) for field in sample_fields if field in first},
    }


def run_checks(env: dict[str, str]) -> int:
    token = env.get("META_ACCESS_TOKEN", "")
    account_id = env.get("META_AD_ACCOUNT_ID", "")
    api_version = env.get("META_API_VERSION", DEFAULT_API_VERSION)
    if not token or not account_id:
        print("Missing META_ACCESS_TOKEN or META_AD_ACCOUNT_ID.")
        print("Create config/private/meta/.env from config/examples/meta.env.example.")
        return 2
    if has_placeholder_values(env):
        print("META_ACCESS_TOKEN or META_AD_ACCOUNT_ID still uses template values.")
        print("Edit config/private/meta/.env with your real System User Token and Ad Account ID.")
        return 2

    account_id = normalize_account_id(account_id)
    print(f"Meta API version: {api_version}")
    print(f"Ad account: {account_id}")
    print(f"Token: {redact_token(token)}")

    checks = [
        (
            "me",
            "me",
            None,
            {"fields": "id,name"},
            ["id", "name"],
        ),
        (
            "ad_account",
            account_id,
            None,
            {"fields": "id,name,currency,timezone_name,account_status"},
            ["id", "name", "currency", "timezone_name", "account_status"],
        ),
        (
            "campaigns",
            account_id,
            "campaigns",
            {"fields": "id,name,objective,status,effective_status", "limit": "3"},
            ["id", "name", "objective", "status", "effective_status"],
        ),
        (
            "adsets",
            account_id,
            "adsets",
            {"fields": "id,name,campaign_id,optimization_goal,billing_event,bid_strategy,status,effective_status", "limit": "3"},
            ["id", "name", "campaign_id", "optimization_goal", "status", "effective_status"],
        ),
        (
            "ads",
            account_id,
            "ads",
            {"fields": "id,name,campaign_id,adset_id,creative,status,effective_status", "limit": "3"},
            ["id", "name", "campaign_id", "adset_id", "creative", "status", "effective_status"],
        ),
        (
            "insights",
            account_id,
            "insights",
            {
                "fields": "date_start,date_stop,spend,impressions,reach,frequency,clicks,inline_link_clicks,ctr,cpc,cpm,actions,cost_per_action_type",
                "level": "campaign",
                "date_preset": "last_7d",
                "limit": "3",
            },
            ["date_start", "date_stop", "spend", "impressions", "clicks", "actions"],
        ),
    ]

    ok = True
    for label, obj, edge, params, fields in checks:
        try:
            payload = graph_get(api_version, obj, edge, params, token)
            if "data" in payload:
                summary = summarize_list(payload, fields)
            else:
                summary = {field: payload.get(field) for field in fields if field in payload}
            print(f"[OK] {label}: {json.dumps(summary, ensure_ascii=False)}")
        except Exception as exc:  # noqa: BLE001 - command-line diagnostic should continue.
            ok = False
            print(f"[FAIL] {label}: {exc}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Meta Marketing API read access.")
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
