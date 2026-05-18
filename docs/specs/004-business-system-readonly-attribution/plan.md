# Implementation Plan: Business System Read-Only Events and Attribution

**Branch**: `workstream/c-data-foundation`
**Date**: `2026-05-17`
**Spec**: `docs/specs/004-business-system-readonly-attribution/spec.md`
**Owner Workstream**: `C Business System + Attribution`

## Summary

Implement the smallest business back-link slice by defining read-only internal business event samples, attribution link samples, and business data quality notes that B can consume during diagnosis.

The first implementation should use redacted or synthetic sample data while the real internal system permissions, fields, and stable IDs are confirmed.

## Technical Context

- **Runtime / Language**: Python 3.9 in the existing `.venv`.
- **Primary Directories**: `docs/`, `data/sample/`, `scripts/`, `tests/`.
- **Storage**: No committed runtime database. Any real export or API payload stays under private ignored paths.
- **External Systems**: Internal CRM, scheduling, sales, or payment systems, read-only only.
- **Testing**: Local sample validation and unittest.
- **Security Constraints**: No real customer PII, tokens, private raw exports, logs, local `.env`, or runtime DBs in git.

## Implementation Changes

### Data / Contracts

- Add business event sample payloads, for example `data/sample/business-events.sample.json`.
- Add attribution link sample payloads, for example `data/sample/attribution-links.sample.json`.
- Add business sync status or data quality sample if needed for the monitor.
- Keep IDs stable enough for B-line account diagnosis samples to reference.

### Backend / Scripts

- Extend `scripts/validate_api_contracts.py` only when sample contracts are added.
- Add tests for required `BusinessEvent` and `AttributionLink` fields.
- Keep real internal-system connectors out of committed code until credentials, access scope, and field mapping are confirmed.

### Docs

- Update `docs/data-model.md` and `docs/api-contracts.md` when sample fields become shared contract fields.
- Record unresolved field meanings and weak attribution cases explicitly.

## Validation Plan

- [ ] `.venv/bin/python scripts/validate_api_contracts.py`
- [ ] `.venv/bin/python -m unittest discover -s tests`
- [ ] Inspect samples to confirm no real PII, private IDs, tokens, raw exports, or logs are committed.

## Integration

1. C produces business event and attribution samples.
2. B consumes those IDs in account diagnosis evidence samples.
3. A provides creative IDs and performance samples.
4. Project owner + Codex verify that the MVP sample can connect advertising metrics, creative performance, and business outcomes.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Internal fields do not contain ad object IDs | Use explicit weak attribution notes and do not force confident matches. |
| Business event names are unclear | Keep event type as unconfirmed until the owner confirms the business meaning. |
| Samples accidentally expose customer data | Use synthetic values and review before staging. |
