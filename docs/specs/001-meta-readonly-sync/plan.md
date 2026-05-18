# Implementation Plan: Meta Read-Only Sync

**Branch**: `workstream/b-account-intelligence`
**Date**: `2026-05-15`
**Spec**: `docs/specs/001-meta-readonly-sync/spec.md`
**Owner Workstream**: `B Account Intelligence + Meta Ads Data`

## Summary

Implement the smallest data foundation slice that turns Meta account hierarchy and insights payloads into standard account tree, sync status, account metrics, and `MetricFact` outputs that pass the existing V0 API contract validator.

The implementation should start from sample and fixture conversion before relying on live Meta API calls. Live credentials remain private.

## Technical Context

- **Runtime / Language**: Python 3.9 in the existing `.venv`.
- **Primary Directories**: `scripts/`, `tests/`, `data/sample/`, `integrations/meta-ads/`, `docs/`.
- **Storage**: No committed runtime DB for this feature. Raw live payloads, if used, stay under `runtime/private/`.
- **External Systems**: Meta Marketing API, only for read-only access.
- **Testing**: `unittest`, local API contract validator, redacted/synthetic fixture validation.
- **Security Constraints**: No real tokens, raw private ad data, local `.env`, runtime DBs, or logs in git.

## Project Gates

- [x] Uses existing docs and contracts before adding new fields.
- [x] Keeps `data / meta / errors` API envelope where API payloads are involved.
- [x] Keeps `snake_case` JSON fields.
- [x] Updates sample payloads and `scripts/validate_api_contracts.py` for contract changes.
- [x] Does not introduce real tokens, real ad data, runtime DBs, logs, or `.env` files.
- [x] Includes test or validation path before implementation is called complete.

## Implementation Changes

### Data / Contracts

- Keep `docs/api-contracts.md` as source of truth.
- Use existing sample payloads in `data/sample/` as expected output examples.
- Add contract fields only when a real normalization need appears.

### Backend / Scripts

- Add a Meta normalization module or script that can transform a redacted fixture into:
  - account tree payload
  - account metrics payload
  - sync status payload
  - metric facts payload
- Keep live API verification scripts separate from normalization logic.
- Extend `scripts/validate_api_contracts.py` if new required fields are introduced.

### Frontend / Experience

- No frontend implementation in this feature.
- Frontend workstreams consume `data/sample/*.json` while C builds the real sync path.

### Docs

- Keep this feature spec and plan updated as the source of implementation scope.
- Update `docs/data-model.md`, `docs/api-contracts.md`, and `docs/meta-conversion-goals.md` only when a shared contract changes.

## Validation Plan

- [ ] `.venv/bin/python scripts/validate_api_contracts.py`
- [ ] `.venv/bin/python -m unittest discover -s tests`
- [ ] Run the Meta normalization script against a synthetic fixture and validate generated payloads.
- [ ] If live API is used, verify output with redacted logging only.

## Rollout / Integration

1. Land this spec on `main` as shared planning foundation.
2. Create `dev` from `main`.
3. Create or update `workstream/b-account-intelligence` from `dev`.
4. Implement fixture-based normalization first.
5. Wire read-only Meta API fetch second.
6. Merge workstream output into `dev` for A/C integration.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Meta action type names do not match business wording | Preserve raw `action_type`; add explicit business mapping such as custom event bundle or H5 lead submission. |
| Frontend consumes raw Meta fields | Only expose contract samples and validator-backed payloads. |
| Real data leaks into git | Keep live payloads under `runtime/private/`; scan before commit. |
| Workstream B starts diagnosis before MetricFact is stable | Keep diagnosis out of scope until data contract and validator pass. |
