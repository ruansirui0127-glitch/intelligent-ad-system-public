# Implementation Plan: Account Intelligence Controlled Suggestion Loop

**Branch**: `workstream/b-account-intelligence`
**Date**: `2026-05-15`
**Spec**: `docs/specs/003-account-intelligence-loop/spec.md`
**Owner Workstream**: `B Account Intelligence + Meta Ads Data`

## Summary

Implement the smallest account intelligence loop by adding rule hit, evidence, recommendation, ActionIntent, and ActionAudit sample contracts and validation. The first version should prove the controlled suggestion chain across advertising metrics, creative performance, and C-line business outcomes before any real agent model or platform mutation exists.

## Technical Context

- **Runtime / Language**: Python 3.9 in the existing `.venv`.
- **Primary Directories**: `data/sample/`, `scripts/`, `tests/`, `docs/`, optional `app/frontend/pages/account-diagnosis/`, `app/frontend/pages/action-intents/`.
- **Storage**: JSON sample files only for this slice.
- **External Systems**: No direct writes. This slice consumes Meta outputs from `docs/specs/001-meta-readonly-sync/` and business outcome samples from `docs/specs/004-business-system-readonly-attribution/`.
- **Testing**: `unittest`, local API contract validator.
- **Security Constraints**: No secrets, real ad data, runtime DBs, logs, `.env`, or platform mutations.

## Project Gates

- [x] Uses existing docs and contracts before adding new fields.
- [x] Keeps `data / meta / errors` API envelope where API payloads are involved.
- [x] Keeps `snake_case` JSON fields.
- [x] Updates sample payloads and `scripts/validate_api_contracts.py` for contract changes.
- [x] Does not introduce real tokens, real ad data, runtime DBs, logs, or `.env` files.
- [x] Includes test or validation path before implementation is called complete.

## Implementation Changes

### Data / Contracts

- Add `data/sample/account-diagnosis.sample.json`.
- Add `data/sample/action-intents.sample.json`.
- Add optional `data/sample/agent-tasks.sample.json` if AgentTask examples are needed.
- Keep object references aligned with existing account, metric, creative, business event, and attribution sample IDs.

### Backend / Scripts

- Extend `scripts/validate_api_contracts.py` with account intelligence validators.
- Add tests in `tests/test_validate_account_intelligence_contracts.py` or extend existing validator tests.

### Frontend / Experience

- Optional first UI consumers:
  - `app/frontend/pages/account-diagnosis/`
  - `app/frontend/pages/action-intents/`
- This slice is complete without frontend if sample validation and tests pass.

### Docs

- Update `docs/api-contracts.md` if sample objects reveal missing required fields.
- Update `docs/brain/object-glossary.md` only if a new object is introduced.

## Validation Plan

- [ ] `.venv/bin/python scripts/validate_api_contracts.py`
- [ ] `.venv/bin/python -m unittest discover -s tests`
- [ ] Inspect account intelligence samples and confirm no real private data or execution status is included.

## Rollout / Integration

1. Implement on `workstream/b-account-intelligence`.
2. Use current Meta sample IDs from `data/sample/` rather than raw Meta payloads.
3. Merge into `dev` after validator and tests pass.
4. Integrate with A/C workstreams in the V0 main chain.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Recommendations appear unsupported | Require `evidence_id` and metric references in samples. |
| ActionIntent looks like real execution | Keep `approval_state` as draft/pending and execution status empty or not executed. |
| B line depends too early on live C line sync | Use C-line sample IDs and data quality notes first. |
| Agent output becomes free-form | Require ContextPackage and structured Recommendation fields. |
