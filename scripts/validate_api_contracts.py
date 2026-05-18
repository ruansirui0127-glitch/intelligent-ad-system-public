#!/usr/bin/env python3
"""Validate local V0 API sample payloads against the project contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


GOAL_TYPES = {
    "quality_lead",
    "lead_form",
    "h5_booking",
    "messaging",
    "engagement",
    "unknown",
}
METRIC_STAGES = {
    "delivery",
    "click",
    "landing",
    "conversion",
    "business",
    "cost",
    "quality",
}
OBJECT_TYPES = {
    "account",
    "campaign",
    "ad_group",
    "ad",
    "creative",
    "keyword",
    "audience",
    "region",
}
PLATFORMS = {
    "meta",
    "google",
    "douyin",
    "tencent_ads",
    "xiaohongshu",
}
SOURCE_QUALITIES = {
    "complete",
    "partial",
    "estimated",
    "missing",
    "unknown",
}
SYNC_STATUSES = {
    "not_configured",
    "running",
    "success",
    "partial_success",
    "failed",
}
TIME_GRAINS = {
    "day",
    "week",
    "month",
    "lifetime",
}


class ContractError(ValueError):
    """Raised when a payload violates the local V0 API contract."""


def require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{path} must be an object")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{path} must be an array")
    return value


def require_field(obj: dict[str, Any], field: str, path: str) -> Any:
    if field not in obj:
        raise ContractError(f"{path}.{field} is required")
    return obj[field]


def require_non_empty_string(obj: dict[str, Any], field: str, path: str) -> str:
    value = require_field(obj, field, path)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{path}.{field} must be a non-empty string")
    return value


def require_enum(obj: dict[str, Any], field: str, allowed: set[str], path: str) -> str:
    value = require_non_empty_string(obj, field, path)
    if value not in allowed:
        raise ContractError(f"{path}.{field} must be one of {sorted(allowed)}, got {value!r}")
    return value


def require_number(obj: dict[str, Any], field: str, path: str) -> int | float:
    value = require_field(obj, field, path)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ContractError(f"{path}.{field} must be a number")
    return value


def validate_error_object(error: Any, path: str) -> None:
    error = require_mapping(error, path)
    require_non_empty_string(error, "code", path)
    require_non_empty_string(error, "message", path)
    require_enum(error, "severity", {"info", "warning", "error", "critical"}, path)
    require_non_empty_string(error, "source", path)
    if "details" in error:
        require_mapping(error["details"], f"{path}.details")


def validate_response_envelope(payload: dict[str, Any]) -> None:
    require_mapping(payload, "$")
    require_field(payload, "data", "$")
    meta = require_mapping(require_field(payload, "meta", "$"), "$.meta")
    errors = require_list(require_field(payload, "errors", "$"), "$.errors")
    require_non_empty_string(meta, "request_id", "$.meta")
    api_version = require_non_empty_string(meta, "api_version", "$.meta")
    if api_version != "v0":
        raise ContractError(f"$.meta.api_version must be 'v0', got {api_version!r}")
    require_non_empty_string(meta, "generated_at", "$.meta")
    for idx, error in enumerate(errors):
        validate_error_object(error, f"$.errors[{idx}]")


def validate_object_id(value: str, object_type: str, path: str) -> None:
    prefix = f"meta:{object_type}:"
    if object_type == "account":
        prefix = "meta:account:"
    if not value.startswith(prefix):
        raise ContractError(f"{path} must start with {prefix!r}, got {value!r}")


def validate_time_window(value: Any, path: str) -> None:
    window = require_mapping(value, path)
    require_non_empty_string(window, "date_start", path)
    require_non_empty_string(window, "date_stop", path)
    require_enum(window, "time_grain", TIME_GRAINS, path)
    require_non_empty_string(window, "timezone", path)


def validate_ad_object(obj: Any, path: str, expected_type: str | None = None) -> None:
    obj = require_mapping(obj, path)
    object_type = require_enum(obj, "object_type", OBJECT_TYPES, path)
    if expected_type and object_type != expected_type:
        raise ContractError(f"{path}.object_type must be {expected_type!r}, got {object_type!r}")
    require_enum(obj, "platform", PLATFORMS, path)
    object_id = require_non_empty_string(obj, "id", path)
    validate_object_id(object_id, object_type, f"{path}.id")
    require_non_empty_string(obj, "external_id", path)
    require_non_empty_string(obj, "name", path)
    require_non_empty_string(obj, "status", path)
    if object_type != "account":
        require_non_empty_string(obj, "parent_id", path)
        require_non_empty_string(obj, "platform_object_type", path)
        require_enum(obj, "goal_type", GOAL_TYPES, path)
    if "children" in obj:
        children = require_list(obj["children"], f"{path}.children")
        for idx, child in enumerate(children):
            validate_ad_object(child, f"{path}.children[{idx}]")


def validate_accounts_tree_payload(payload: dict[str, Any]) -> None:
    validate_response_envelope(payload)
    data = require_mapping(payload["data"], "$.data")
    accounts = require_list(require_field(data, "accounts", "$.data"), "$.data.accounts")
    for idx, account in enumerate(accounts):
        validate_ad_object(account, f"$.data.accounts[{idx}]", expected_type="account")


def validate_metric_summary(value: Any, path: str) -> None:
    metric = require_mapping(value, path)
    require_non_empty_string(metric, "metric_name", path)
    require_number(metric, "metric_value", path)
    require_non_empty_string(metric, "unit", path)
    require_enum(metric, "metric_stage", METRIC_STAGES, path)
    require_enum(metric, "goal_type", GOAL_TYPES, path)


def validate_account_metrics_payload(payload: dict[str, Any]) -> None:
    validate_response_envelope(payload)
    data = require_mapping(payload["data"], "$.data")
    obj = require_mapping(require_field(data, "object", "$.data"), "$.data.object")
    require_non_empty_string(obj, "id", "$.data.object")
    require_enum(obj, "platform", PLATFORMS, "$.data.object")
    require_enum(obj, "object_type", OBJECT_TYPES, "$.data.object")
    require_non_empty_string(obj, "name", "$.data.object")
    validate_time_window(require_field(data, "time_window", "$.data"), "$.data.time_window")
    metrics = require_list(require_field(data, "metrics", "$.data"), "$.data.metrics")
    for idx, metric in enumerate(metrics):
        validate_metric_summary(metric, f"$.data.metrics[{idx}]")
    require_list(require_field(data, "series", "$.data"), "$.data.series")
    if "breakdowns" in data:
        require_list(data["breakdowns"], "$.data.breakdowns")


def validate_sync_status(value: Any, path: str) -> None:
    status = require_mapping(value, path)
    require_enum(status, "platform", PLATFORMS, path)
    require_enum(status, "status", SYNC_STATUSES, path)
    require_non_empty_string(status, "last_sync_batch", path)
    require_non_empty_string(status, "last_started_at", path)
    require_non_empty_string(status, "last_finished_at", path)
    require_non_empty_string(status, "date_start", path)
    require_non_empty_string(status, "date_stop", path)
    objects_synced = require_mapping(require_field(status, "objects_synced", path), f"{path}.objects_synced")
    for field in ["accounts", "campaigns", "ad_groups", "ads", "metric_facts"]:
        require_number(objects_synced, field, f"{path}.objects_synced")
    warnings = require_list(require_field(status, "warnings", path), f"{path}.warnings")
    for idx, warning in enumerate(warnings):
        warning = require_mapping(warning, f"{path}.warnings[{idx}]")
        require_non_empty_string(warning, "code", f"{path}.warnings[{idx}]")
        require_non_empty_string(warning, "message", f"{path}.warnings[{idx}]")


def validate_sync_status_payload(payload: dict[str, Any]) -> None:
    validate_response_envelope(payload)
    data = require_mapping(payload["data"], "$.data")
    validate_sync_status(require_field(data, "current", "$.data"), "$.data.current")
    history = require_list(require_field(data, "history", "$.data"), "$.data.history")
    for idx, item in enumerate(history):
        validate_sync_status(item, f"$.data.history[{idx}]")


def validate_metric_fact(value: Any, path: str) -> None:
    fact = require_mapping(value, path)
    require_non_empty_string(fact, "fact_id", path)
    require_enum(fact, "platform", PLATFORMS, path)
    object_type = require_enum(fact, "object_type", OBJECT_TYPES, path)
    object_id = require_non_empty_string(fact, "object_id", path)
    validate_object_id(object_id, object_type, f"{path}.object_id")
    require_non_empty_string(fact, "metric_name", path)
    require_number(fact, "metric_value", path)
    require_non_empty_string(fact, "unit", path)
    require_non_empty_string(fact, "date", path)
    validate_time_window(require_field(fact, "time_window", path), f"{path}.time_window")
    require_enum(fact, "metric_stage", METRIC_STAGES, path)
    require_enum(fact, "goal_type", GOAL_TYPES, path)
    require_non_empty_string(fact, "metric_version", path)
    require_non_empty_string(fact, "sync_batch", path)
    require_enum(fact, "source_quality", SOURCE_QUALITIES, path)
    require_non_empty_string(fact, "raw_metric_name", path)
    require_mapping(require_field(fact, "dimensions", path), f"{path}.dimensions")
    require_field(fact, "attribution_window", path)


def validate_metric_facts_payload(payload: dict[str, Any]) -> None:
    validate_response_envelope(payload)
    data = require_mapping(payload["data"], "$.data")
    items = require_list(require_field(data, "items", "$.data"), "$.data.items")
    for idx, item in enumerate(items):
        validate_metric_fact(item, f"$.data.items[{idx}]")
    pagination = require_mapping(require_field(payload["meta"], "pagination", "$.meta"), "$.meta.pagination")
    require_number(pagination, "limit", "$.meta.pagination")
    require_field(pagination, "next_cursor", "$.meta.pagination")


VALIDATORS = {
    "accounts-tree.meta.sample.json": validate_accounts_tree_payload,
    "account-metrics.meta.sample.json": validate_account_metrics_payload,
    "sync-status.meta.sample.json": validate_sync_status_payload,
    "metric-facts.meta.sample.json": validate_metric_facts_payload,
}


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ContractError(f"{path}: invalid JSON: {exc}") from exc
    return require_mapping(payload, "$")


def validate_sample_file(path: Path) -> None:
    validator = VALIDATORS.get(path.name)
    if validator is None:
        raise ContractError(f"Unsupported sample file: {path.name}")
    validator(load_json_file(path))


def default_sample_files(root: Path) -> list[Path]:
    return [root / "data" / "sample" / name for name in VALIDATORS]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local V0 API sample payload contracts.")
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Sample JSON files to validate. Defaults to the four V0 Meta sample files.",
    )
    args = parser.parse_args(argv)

    root = Path.cwd()
    files = args.files or default_sample_files(root)
    failed = False
    for path in files:
        try:
            validate_sample_file(path)
            print(f"[OK] {path}")
        except ContractError as exc:
            failed = True
            print(f"[FAIL] {path}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
