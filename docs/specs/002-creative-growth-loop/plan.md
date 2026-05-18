# Implementation Plan: Creative Growth Sample Loop

**Branch**: `workstream/a-creative-growth`
**Date**: `2026-05-15`
**Spec**: `docs/specs/002-creative-growth-loop/spec.md`
**Owner Workstream**: `A Creative`

## Summary

Implement the smallest creative growth loop by adding synthetic creative sample payloads, validator support, and tests. The first implementation should prove object traceability before any real generation, publishing, or platform integration.

## Technical Context

- **Runtime / Language**: Python 3.9 in the existing `.venv`.
- **Primary Directories**: `data/sample/`, `scripts/`, `tests/`, `docs/`, optional `app/frontend/pages/creative-workbench/`.
- **Storage**: JSON sample files only for this slice.
- **External Systems**: None.
- **Testing**: `unittest`, local API contract validator.
- **Security Constraints**: No secrets, real ad data, private media, runtime DBs, logs, or `.env` files.

## Project Gates

- [x] Uses existing docs and contracts before adding new fields.
- [x] Keeps `data / meta / errors` API envelope where API payloads are involved.
- [x] Keeps `snake_case` JSON fields.
- [x] Updates sample payloads and `scripts/validate_api_contracts.py` for contract changes.
- [x] Does not introduce real tokens, real ad data, runtime DBs, logs, or `.env` files.
- [x] Includes test or validation path before implementation is called complete.

## Implementation Changes

### Data / Contracts

- Add `data/sample/creative-opportunities.sample.json`.
- Add `data/sample/creative-assets.sample.json`.
- Add `data/sample/creative-performance.sample.json`.
- Keep object shapes aligned with `docs/api-contracts.md`.

### Backend / Scripts

- Extend `scripts/validate_api_contracts.py` with validators for creative opportunities, creative assets, and creative performance reports.
- Add tests in `tests/test_validate_api_contracts.py` or a new `tests/test_validate_creative_contracts.py`.

### Frontend / Experience

- Optional first UI consumer may read the sample files later.
- This slice is complete without a frontend page if sample validation and tests pass.

### Docs

- Update `docs/api-contracts.md` only if the implementation reveals missing fields.
- Update `docs/brain/object-glossary.md` only if a new object is introduced.

## Validation Plan

- [ ] `.venv/bin/python scripts/validate_api_contracts.py`
- [ ] `.venv/bin/python -m unittest discover -s tests`
- [ ] Inspect the three creative sample files and confirm no real private data is present.

## Rollout / Integration

1. Implement on `workstream/a-creative-growth`.
2. Keep the work independent from Meta live sync.
3. Merge into `dev` after validator and tests pass.
4. Use the samples as inputs for creative workbench and later Recommendation/ActionIntent integration.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Creative samples become disconnected from Meta data | Use `metric_refs`, `platform`, and `market_region` fields consistently. |
| Teammate treats sample as production rule | Keep `RuleUpdate.status=draft` and `approval_state=pending_review`. |
| Scope expands into real generation tools | Keep image/video generation out of this first slice. |
| Real material leaks into sample files | Use synthetic copy and null media URIs. |
