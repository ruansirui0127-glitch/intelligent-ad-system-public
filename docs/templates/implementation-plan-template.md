# Implementation Plan: [FEATURE NAME]

**Branch**: `[feature-or-workstream-branch]`
**Date**: `[YYYY-MM-DD]`
**Spec**: `[docs/specs/.../spec.md]`
**Owner Workstream**: `A Creative | B Account Intelligence | C Data Foundation | Shared`

## Summary

[Translate the feature spec into the smallest technical implementation that satisfies the P1 user story first.]

## Technical Context

- **Runtime / Language**: [Python, Node, browser app, docs-only, etc.]
- **Primary Directories**: [`app/`, `integrations/`, `intelligence/`, `config/`, `runtime/`, `data/`, `docs/`, `scripts/`, `tests/`]
- **Storage**: [N/A, JSON files, SQLite under runtime/private, etc.]
- **External Systems**: [Meta API, local files, mock data, none.]
- **Testing**: [unittest, contract validator, browser QA, manual checks.]
- **Security Constraints**: [No secrets in docs/samples/logs; private paths only.]

## Project Gates

- [ ] Uses existing docs and contracts before adding new fields.
- [ ] Keeps `data / meta / errors` API envelope where API payloads are involved.
- [ ] Keeps `snake_case` JSON fields.
- [ ] Updates sample payloads and `scripts/validate_api_contracts.py` for contract changes.
- [ ] Does not introduce real tokens, real ad data, runtime DBs, logs, or `.env` files.
- [ ] Includes test or validation path before implementation is called complete.

## Implementation Changes

### Data / Contracts

- [Contract, sample, schema, or mapping changes.]

### Backend / Scripts

- [Backend, adapter, CLI, validation, or sync changes.]

### Frontend / Experience

- [UI surface, mock consumption, or frontend data dependency changes.]

### Docs

- [Docs that must change with the implementation.]

## Validation Plan

- [ ] `.venv/bin/python scripts/validate_api_contracts.py`
- [ ] `.venv/bin/python -m unittest discover -s tests`
- [ ] [Feature-specific smoke test or manual verification.]

## Rollout / Integration

- [How this lands into a workstream branch, then `dev`, then `main`.]

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| [Risk] | [Mitigation] |

