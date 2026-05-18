# Tasks: Meta Read-Only Sync

**Input**: `docs/specs/001-meta-readonly-sync/spec.md` and `docs/specs/001-meta-readonly-sync/plan.md`
**Owner Workstream**: `B Account Intelligence + Meta Ads Data`

## Phase 1: Foundation

- [ ] T001 [FOUNDATION] Confirm branch is `workstream/b-account-intelligence` before implementation.
- [ ] T002 [FOUNDATION] Confirm source docs: `docs/api-contracts.md`, `docs/data-model.md`, `docs/meta-conversion-goals.md`.
- [ ] T003 [FOUNDATION] Run baseline validation: `.venv/bin/python scripts/validate_api_contracts.py`.
- [ ] T004 [FOUNDATION] Run baseline tests: `.venv/bin/python -m unittest discover -s tests`.

## Phase 2: User Story 1 - Sync Meta Object Hierarchy (P1)

**Goal**: Convert Meta account, campaign, ad set, and ad shape into standard hierarchy objects.

**Independent Test**: Generated account tree payload passes the local contract validator.

### Tests First

- [ ] T005 [P] [US1] Add fixture-based hierarchy normalization tests in `tests/test_meta_normalize.py`.

### Implementation

- [ ] T006 [US1] Add Meta hierarchy normalization code in `integrations/meta-ads/` or `scripts/` based on current repo conventions.
- [ ] T007 [US1] Generate or compare account tree output against `data/sample/accounts-tree.meta.sample.json`.
- [ ] T008 [US1] Run contract validator and unittest.

## Phase 3: User Story 2 - Split Meta Insights Into MetricFact (P1)

**Goal**: Convert scalar insights and Meta `actions` arrays into atomic `MetricFact` records.

**Independent Test**: Generated metric facts payload passes the local contract validator.

### Tests First

- [ ] T009 [P] [US2] Add fixture-based MetricFact normalization tests in `tests/test_meta_normalize.py`.

### Implementation

- [ ] T010 [US2] Normalize scalar fields: `spend`, `impressions`, `clicks`, `inline_link_clicks`.
- [ ] T011 [US2] Normalize action fields: `landing_page_view`, `lead`, `onsite_conversion.lead_grouped`, `offsite_conversion.fb_pixel_custom`, messaging actions, `purchase`.
- [ ] T012 [US2] Preserve raw `action_type`, `raw_metric_name`, `optimization_goal`, and confirmed business mapping notes in `dimensions`.
- [ ] T013 [US2] Generate or compare metric facts output against `data/sample/metric-facts.meta.sample.json`.
- [ ] T014 [US2] Run contract validator and unittest.

## Phase 4: User Story 3 - Report Sync Status (P2)

**Goal**: Produce a sync status payload with batch, date range, object counts, and warnings.

**Independent Test**: Generated sync status payload passes the local contract validator.

### Tests First

- [ ] T015 [P] [US3] Add sync status tests in `tests/test_meta_normalize.py`.

### Implementation

- [ ] T016 [US3] Generate sync status from normalization run metadata.
- [ ] T017 [US3] Include warnings or notes that `fb_pixel_custom` is a custom event bundle and Meta purchase actions represent H5 lead submissions, not real purchases.
- [ ] T018 [US3] Generate or compare sync status output against `data/sample/sync-status.meta.sample.json`.
- [ ] T019 [US3] Run contract validator and unittest.

## Phase 5: Polish & Integration

- [ ] T020 [P] Update docs if normalization adds new fields or enum values.
- [ ] T021 Check `git status --short` and confirm no private files are staged.
- [ ] T022 Commit to the correct workstream branch when requested.
- [ ] T023 Merge through `dev` after A/B consumers confirm sample compatibility.

## Dependencies

- Foundation tasks block implementation.
- US1 and US2 can proceed in parallel if they write separate helpers and tests.
- US3 depends on metadata from US1/US2 normalization runs.

## Parallel Work

- Workstream A can consume `data/sample/accounts-tree.meta.sample.json` and `data/sample/account-metrics.meta.sample.json`.
- Workstream B can design diagnosis inputs using `MetricFact`, but should not generate final recommendations until Meta samples and C-line business event samples are both stable.
- Project owner + Codex own shared contract acceptance; B must update validator/tests with any Meta contract changes.
