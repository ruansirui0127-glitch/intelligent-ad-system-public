# Tasks: Account Intelligence Controlled Suggestion Loop

**Input**: `docs/specs/003-account-intelligence-loop/spec.md` and `docs/specs/003-account-intelligence-loop/plan.md`
**Owner Workstream**: `B Account Intelligence + Meta Ads Data`

## Phase 1: Foundation

- [ ] T001 [FOUNDATION] Confirm branch is `workstream/b-account-intelligence` before implementation.
- [ ] T002 [FOUNDATION] Confirm source docs: `docs/api-contracts.md`, `docs/data-model.md`, `docs/brain/brain-workflow.md`, `docs/specs/001-meta-readonly-sync/`, `docs/specs/004-business-system-readonly-attribution/`.
- [ ] T003 [FOUNDATION] Run baseline validation: `.venv/bin/python scripts/validate_api_contracts.py`.
- [ ] T004 [FOUNDATION] Run baseline tests: `.venv/bin/python -m unittest discover -s tests`.

## Phase 2: User Story 1 - Review Full Account Diagnosis Context (P1)

**Goal**: Add account diagnosis sample data that connects account objects, metric references, rules, and evidence.

**Independent Test**: `data/sample/account-diagnosis.sample.json` passes local contract validation.

### Tests First

- [ ] T005 [P] [US1] Add account diagnosis sample validation test in `tests/test_validate_account_intelligence_contracts.py`.

### Implementation

- [ ] T006 [US1] Create `data/sample/account-diagnosis.sample.json` with `RuleDefinition`, `RuleHit`, `EvidenceObject`, and `ContextPackage` examples that can cite Meta metrics, creative performance, and C-line business outcomes.
- [ ] T007 [US1] Extend `scripts/validate_api_contracts.py` to recognize `account-diagnosis.sample.json`.
- [ ] T008 [US1] Validate `RuleHit` fields: `rule_id`, `rule_version`, `object_type`, `object_id`, `current_value`, `baseline_value`, `sample_size`, `severity`, `evidence_id`.
- [ ] T009 [US1] Validate `EvidenceObject` fields: `evidence_id`, `time_window`, `metrics`, `baseline`, `sample_size`, `confidence`, `data_quality`, `rule_version`.
- [ ] T010 [US1] Run contract validator and unittest.

## Phase 3: User Story 2 - Generate Evidence-Backed Recommendation (P1)

**Goal**: Add Recommendation samples that cite EvidenceObject and ContextPackage.

**Independent Test**: Recommendation sample validation fails if `evidence_id` is missing.

### Tests First

- [ ] T011 [P] [US2] Add recommendation validation test in `tests/test_validate_account_intelligence_contracts.py`.

### Implementation

- [ ] T012 [US2] Add `Recommendation` examples to `data/sample/account-diagnosis.sample.json` or a dedicated sample file.
- [ ] T013 [US2] Validate `recommendation_id`, `object_type`, `object_id`, `recommendation_type`, `summary`, `reasoning`, `evidence_id`, `risk_level`, `status`, `created_by`.
- [ ] T014 [US2] Ensure partial data quality produces limitation text in the sample.
- [ ] T015 [US2] Run contract validator and unittest.

## Phase 4: User Story 3 - Create ActionIntent Draft (P1)

**Goal**: Add ActionIntent and ActionAudit samples that prove approval/rejection without execution.

**Independent Test**: `data/sample/action-intents.sample.json` passes validation and contains no real execution state.

### Tests First

- [ ] T016 [P] [US3] Add ActionIntent sample validation test in `tests/test_validate_account_intelligence_contracts.py`.

### Implementation

- [ ] T017 [US3] Create `data/sample/action-intents.sample.json` with `ActionIntent` and `ActionAudit` examples.
- [ ] T018 [US3] Extend `scripts/validate_api_contracts.py` to recognize `action-intents.sample.json`.
- [ ] T019 [US3] Validate `ActionIntent` fields: `action_intent_id`, `recommendation_id`, `action_type`, `target_object_type`, `target_object_id`, `proposed_change`, `budget_boundary`, `cooldown_policy`, `risk_policy`, `approval_state`, `evidence_id`.
- [ ] T020 [US3] Validate `ActionAudit` fields: `audit_id`, `action_intent_id`, `decision`, `decided_by`, `decided_at`, `reject_reason`, `execution_status`, `result_summary`.
- [ ] T021 [US3] Ensure V0 samples do not indicate real platform mutation.
- [ ] T022 [US3] Run contract validator and unittest.

## Phase 5: Polish & Integration

- [ ] T023 [P] Update `docs/api-contracts.md` if sample object fields change.
- [ ] T024 Check `git status --short` and confirm no private files are staged.
- [ ] T025 Commit to `workstream/b-account-intelligence` when requested.
- [ ] T026 Merge through `dev` after A/C consumers confirm sample compatibility.

## Dependencies

- Foundation tasks block implementation.
- US1 blocks US2 and US3 because recommendations and ActionIntents must reference evidence.
- B line Meta samples provide object IDs and metric fact references.
- C line business samples provide business event IDs, attribution links, and data quality notes.
- A line creative samples are optional for first account diagnosis, but needed for creative fatigue or creative performance rules.

## Parallel Work

- Workstream A can continue creative samples independently.
- Workstream C can continue business-system readonly and attribution samples independently.
- Workstream B should use stable sample IDs and avoid depending on live API timing.
