---
name: api-contract-designer
description: Use when designing, changing, reviewing, or validating API contracts, mock payloads, shared wire shapes, interface boundaries, or third-party platform adapters for the intelligent advertising system. Especially relevant for docs/api-contracts.md, data/sample/*.json, scripts/validate_api_contracts.py, Meta MetricFact mapping, frontend/backend handoffs, and workstream interface changes.
---

# API Contract Designer

This project is contract-first. Use this skill before changing API docs, sample payloads, shared objects, adapter output, frontend data dependencies, or validation logic.

## Project Defaults

- Keep the response envelope: `data`, `meta`, `errors`.
- Use `snake_case` for API fields and JSON payloads.
- Preserve system IDs shaped as `{platform}:{object_type}:{external_id}`.
- Keep platform raw fields out of frontend contracts unless they are stored under explicit raw/source fields such as `raw_metric_name` or `dimensions`.
- Treat all third-party API responses as untrusted input. Validate at the adapter boundary before creating standard objects.
- Prefer additive changes. Do not rename or remove existing fields without updating docs, samples, validators, and consumers together.
- Never include real tokens, real account data, raw private ad data, logs, or local `.env` content in docs, samples, or skill files.

## Required Reading

Before contract work, inspect only the files needed for the task:

- `docs/api-contracts.md`: source of truth for V0 API envelope, enums, wire shapes, and sample file names.
- `docs/data-model.md`: source of truth for shared domain objects.
- `docs/meta-conversion-goals.md`: source of truth for Meta `goal_type`, action type mapping, and unconfirmed business meanings.
- `data/sample/*.json`: executable mock payloads for frontend/backend handoff.
- `scripts/validate_api_contracts.py`: local validator that must move with contract changes.

## Workflow

1. Identify the contract surface: endpoint, mock file, shared object, adapter output, or frontend dependency.
2. Check the existing source of truth before inventing fields.
3. Define the smallest stable wire shape that supports the current workflow.
4. Keep API semantics business-facing, not platform-SDK-facing.
5. Put platform-specific details under `dimensions`, `raw_metric_name`, adapter-local code, or documented extension fields.
6. Update docs, samples, validator, and tests in one coherent change.
7. Run validation before saying the contract is ready.

## Response Envelope

Every API-style payload should use:

```json
{
  "data": {},
  "meta": {
    "request_id": "req_sample",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00"
  },
  "errors": []
}
```

Use `errors[]` for warnings, partial failures, and data quality issues. Do not switch to a separate `{ "error": ... }` shape.

## Meta Mapping Rules

- Meta `actions` and `cost_per_action_type` arrays must be split into atomic `MetricFact` records.
- Always preserve the original Meta `action_type` in `dimensions.action_type`.
- Keep `offsite_conversion.fb_pixel_custom` as unconfirmed business meaning until the business mapping is confirmed.
- Keep `purchase` and `offsite_conversion.fb_pixel_purchase` as platform actions until the business confirms whether they represent real purchases, bookings, or another event.
- Do not collapse `quality_lead`, `lead_form`, `h5_booking`, `messaging`, and `engagement` into a generic `leads` metric.

## Compatibility Rules

When changing a contract:

- Add optional fields before making required fields.
- Version breaking semantics through `metric_version`, `api_version`, or an explicit migration note.
- Keep sample payloads valid at all times.
- Update `scripts/validate_api_contracts.py` when adding required fields or enums.
- Add or update tests in `tests/test_validate_api_contracts.py`.

## Validation Commands

Run these after any contract, mock, or validator change:

```bash
.venv/bin/python scripts/validate_api_contracts.py
.venv/bin/python -m unittest discover -s tests
```

If GitHub push fails from terminal connectivity, use the machine proxy for the push command:

```bash
HTTP_PROXY=http://127.0.0.1:15236 HTTPS_PROXY=http://127.0.0.1:15236 ALL_PROXY=socks5://127.0.0.1:15235 git push origin main
```

Only use the proxy command when needed; do not store it as a project secret or hard requirement.

