# Tasks: Business System Read-Only Events and Attribution

**Input**: `docs/specs/004-business-system-readonly-attribution/spec.md` and `docs/specs/004-business-system-readonly-attribution/plan.md`
**Owner Workstream**: `C Business System + Attribution`

## Phase 1: Foundation

- [ ] T001 [FOUNDATION] Confirm branch is `workstream/c-data-foundation` before implementation.
- [ ] T002 [FOUNDATION] Confirm source docs: `docs/data-model.md`, `docs/api-contracts.md`, `docs/brain/three-workstream-development-plan.md`.
- [ ] T003 [FOUNDATION] Run baseline validation: `.venv/bin/python scripts/validate_api_contracts.py`.
- [ ] T004 [FOUNDATION] Run baseline tests: `.venv/bin/python -m unittest discover -s tests`.

## Phase 2: User Story 1 - Capture Business Events (P1)

**Goal**: Represent valid lead, booking, attendance, purchase, refund, and unknown outcomes as business events.

**Independent Test**: `data/sample/business-events.sample.json` passes local validation when validator coverage is added.

### Tests First

- [ ] T005 [P] [US1] Add business event sample validation tests.

### Implementation

- [ ] T006 [US1] Create `data/sample/business-events.sample.json` with synthetic event examples.
- [ ] T007 [US1] Validate required fields: `event_id`, `lead_id` or equivalent reference, `event_type`, `event_time`, `market_region`, `source_platform`, `source_object_id`, `status`, `source_system`.
- [ ] T008 [US1] Include unconfirmed event meaning examples where business meaning is not yet verified.
- [ ] T009 [US1] Run contract validator and unittest.

## Phase 3: User Story 2 - Link Business Events Back to Ads (P1)

**Goal**: Represent how business outcomes connect back to Meta account, campaign, ad group, ad, or creative objects.

**Independent Test**: `data/sample/attribution-links.sample.json` includes confident and weak attribution examples.

### Tests First

- [ ] T010 [P] [US2] Add attribution link sample validation tests.

### Implementation

- [ ] T011 [US2] Create `data/sample/attribution-links.sample.json` with synthetic attribution examples.
- [ ] T012 [US2] Validate required fields: `link_id`, `business_event_id`, `platform`, `object_type`, `object_id`, `match_method`, `confidence`, `attribution_window`, `quality_flag`.
- [ ] T013 [US2] Include weak or missing attribution notes instead of forcing confident matches.
- [ ] T014 [US2] Run contract validator and unittest.

## Phase 4: User Story 3 - Report Business-System Sync Quality (P2)

**Goal**: Provide business-system sync status and data-quality notes for B-line recommendations.

### Implementation

- [ ] T015 [US3] Add business sync status sample if needed for the data and Harness monitor.
- [ ] T016 [US3] Include current status, date range, object counts, missing fields, warnings, and last sync time.
- [ ] T017 [US3] Run contract validator and unittest.

## Phase 5: Integration

- [ ] T018 Update `docs/api-contracts.md` and `docs/data-model.md` if sample fields change shared object definitions.
- [ ] T019 Give B line stable sample IDs for account diagnosis evidence.
- [ ] T020 Check `git status --short` and confirm no private files are staged.
- [ ] T021 Commit to `workstream/c-data-foundation` when requested.

## Dependencies

- B line provides Meta object IDs that attribution links can target.
- A line provides creative IDs when attribution links point to creative-level performance.
- Project owner + Codex resolve shared contract disputes.
