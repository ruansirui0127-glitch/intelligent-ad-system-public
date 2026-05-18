# Tasks: Creative Growth Sample Loop

**Input**: `docs/specs/002-creative-growth-loop/spec.md` and `docs/specs/002-creative-growth-loop/plan.md`
**Owner Workstream**: `A Creative`

## Phase 1: Foundation

- [ ] T001 [FOUNDATION] Confirm branch is `workstream/a-creative-growth` before implementation.
- [ ] T002 [FOUNDATION] Confirm source docs: `docs/brain/object-glossary.md`, `docs/api-contracts.md`, `docs/data-model.md`.
- [ ] T003 [FOUNDATION] Run baseline validation: `.venv/bin/python scripts/validate_api_contracts.py`.
- [ ] T004 [FOUNDATION] Run baseline tests: `.venv/bin/python -m unittest discover -s tests`.

## Phase 2: User Story 1 - Review Creative Opportunities (P1)

**Goal**: Add a synthetic opportunity sample that can become the first creative workbench input.

**Independent Test**: `data/sample/creative-opportunities.sample.json` passes local contract validation.

### Tests First

- [ ] T005 [P] [US1] Add creative opportunity sample validation test in `tests/test_validate_creative_contracts.py`.

### Implementation

- [ ] T006 [US1] Create `data/sample/creative-opportunities.sample.json` with `data.items`, `meta`, and `errors`.
- [ ] T007 [US1] Extend `scripts/validate_api_contracts.py` to recognize `creative-opportunities.sample.json`.
- [ ] T008 [US1] Validate opportunity fields: `id`, `domain_object_type`, `title`, `market_region`, `recommended_platforms`, `target_audience`, `pain_point`, `angle`, `evidence_refs`, `priority_score`, `status`.
- [ ] T009 [US1] Run contract validator and unittest.

## Phase 3: User Story 2 - Trace Assets To Source (P1)

**Goal**: Add creative asset samples with full lineage from opportunity to master asset and platform version.

**Independent Test**: `data/sample/creative-assets.sample.json` passes local contract validation.

### Tests First

- [ ] T010 [P] [US2] Add creative asset sample validation test in `tests/test_validate_creative_contracts.py`.

### Implementation

- [ ] T011 [US2] Create `data/sample/creative-assets.sample.json` with sample `MasterAsset`, `PlatformVersion`, `CreativeAsset`, and `CreativeTag` objects.
- [ ] T012 [US2] Extend `scripts/validate_api_contracts.py` to recognize `creative-assets.sample.json`.
- [ ] T013 [US2] Validate lineage fields: `opportunity_id`, `master_asset_id`, `platform_version_id`.
- [ ] T014 [US2] Validate review fields: `approval_status`, `servable_status`, `risk_level`, `status`.
- [ ] T015 [US2] Run contract validator and unittest.

## Phase 4: User Story 3 - Record Creative Performance Learning (P2)

**Goal**: Add creative performance samples that can later feed LearningObject and RuleUpdate.

**Independent Test**: `data/sample/creative-performance.sample.json` passes local contract validation.

### Tests First

- [ ] T016 [P] [US3] Add creative performance sample validation test in `tests/test_validate_creative_contracts.py`.

### Implementation

- [ ] T017 [US3] Create `data/sample/creative-performance.sample.json` with `PerformanceReport` and optional draft `RuleUpdate`.
- [ ] T018 [US3] Extend `scripts/validate_api_contracts.py` to recognize `creative-performance.sample.json`.
- [ ] T019 [US3] Validate `time_window`, `metric_refs`, `summary`, `winning_factors`, `losing_factors`, `data_quality`, `author_type`.
- [ ] T020 [US3] Validate draft rule update fields and ensure `approval_state` is not approved by default.
- [ ] T021 [US3] Run contract validator and unittest.

## Phase 5: Polish & Integration

- [ ] T022 [P] Update `docs/api-contracts.md` if any sample field changes.
- [ ] T023 Check `git status --short` and confirm no private files are staged.
- [ ] T024 Commit to `workstream/a-creative-growth` when requested.
- [ ] T025 Merge through `dev` after C data foundation confirms sample compatibility.

## Dependencies

- Foundation tasks block implementation.
- US1 and US2 can proceed in parallel after validator patterns are clear.
- US3 can proceed after at least one creative asset ID exists.

## Parallel Work

- Workstream C can continue Meta read-only sync independently.
- Workstream B should not require creative performance data until both creative samples and Meta MetricFact samples are stable.
- Project owner reviews any new object or enum before it becomes required.
