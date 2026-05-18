# Tasks: [FEATURE NAME]

**Input**: `[docs/specs/.../spec.md]` and `[docs/specs/.../plan.md]`
**Owner Workstream**: `A Creative | B Account Intelligence | C Data Foundation | Shared`

## Format

`[ID] [P?] [Story] Description`

- `[P]`: Can be done in parallel because it touches different files or has no dependency.
- `[Story]`: Maps task to a user story such as `US1`, `US2`, or `FOUNDATION`.
- Every implementation task should name exact file paths.

## Phase 1: Foundation

- [ ] T001 [FOUNDATION] Confirm source docs and current branch.
- [ ] T002 [FOUNDATION] Confirm validation commands for this feature.
- [ ] T003 [P] [FOUNDATION] Create or update required docs/spec artifacts.

## Phase 2: User Story 1 - [Title] (P1)

**Goal**: [Smallest independently useful outcome.]

**Independent Test**: [How to verify this story alone.]

### Tests First

- [ ] T004 [P] [US1] Add failing contract/unit test in `[path]`.

### Implementation

- [ ] T005 [US1] Implement minimum behavior in `[path]`.
- [ ] T006 [US1] Update docs/samples/contracts in `[path]`.
- [ ] T007 [US1] Run validation commands and record result.

## Phase 3: User Story 2 - [Title] (P2)

**Goal**: [Second independently useful outcome.]

**Independent Test**: [How to verify this story alone.]

- [ ] T008 [P] [US2] Add or update test in `[path]`.
- [ ] T009 [US2] Implement behavior in `[path]`.
- [ ] T010 [US2] Run validation commands and record result.

## Phase 4: Polish & Integration

- [ ] T011 [P] Update docs affected by the feature.
- [ ] T012 Run full validation.
- [ ] T013 Check `git status --short` and confirm no private files are staged.
- [ ] T014 Commit and push to the correct branch when requested.

## Dependencies

- Foundation tasks block story implementation.
- Each user story should be independently testable before moving on.
- Contract tests should be written before implementation when code behavior changes.

## Parallel Work

- Tasks marked `[P]` can run in parallel.
- Workstream A/B/C can work in parallel after shared contract and sample payloads are stable.

