# Feature Specification: Meta Read-Only Sync

**Feature Branch**: `workstream/b-account-intelligence`
**Created**: `2026-05-15`
**Status**: `Draft`
**Owner Workstream**: `B Account Intelligence + Meta Ads Data`
**Source Docs**: `README.md`, `docs/architecture.md`, `docs/data-model.md`, `docs/meta-conversion-goals.md`, `docs/api-contracts.md`, `docs/integration-plan.md`

## Summary

Build the first Meta read-only data foundation slice: fetch or ingest Meta account hierarchy and insights data, preserve raw platform evidence, normalize standard ad objects, and split metrics into atomic `MetricFact` records that match the V0 API contract.

This feature does not diagnose performance, generate recommendations, create campaigns, adjust budgets, or execute spend-changing actions.

## User Scenarios & Testing

### User Story 1 - Sync Meta Object Hierarchy (Priority: P1)

As the Meta advertising data owner, I need Meta account, campaign, ad group, and ad objects represented in the standard object model so that account analysis and frontend mock consumers do not depend on Meta SDK raw shapes.

**Why this priority**: Without stable object hierarchy, account pages, metrics queries, and diagnostics cannot agree on object IDs or parent-child relationships.

**Independent Test**: A sync or fixture conversion can produce an account tree payload that passes `scripts/validate_api_contracts.py`.

**Acceptance Scenarios**:

1. **Given** a Meta account source payload, **When** the object hierarchy is normalized, **Then** each object has `id`, `platform`, `object_type`, `external_id`, `name`, `status`, and parent linkage where applicable.
2. **Given** a normalized object, **When** the object is exposed through the account tree contract, **Then** its system ID follows `{platform}:{object_type}:{external_id}`.

### User Story 2 - Split Meta Insights Into MetricFact (Priority: P1)

As the Meta advertising data owner, I need Meta insights fields and action arrays split into atomic `MetricFact` records so that downstream pages and diagnostics can aggregate metrics consistently.

**Why this priority**: Meta `actions` and `cost_per_action_type` are nested platform-specific arrays; leaving them raw would make every consumer reimplement mapping logic.

**Independent Test**: A fixture containing spend, impressions, clicks, link clicks, landing page views, leads, `offsite_conversion.fb_pixel_custom`, messaging, and purchase-like actions produces `MetricFact` records that pass the local contract validator.

**Acceptance Scenarios**:

1. **Given** a Meta insights row with scalar metrics, **When** it is normalized, **Then** spend, impressions, clicks, and link clicks are emitted as separate `MetricFact` records.
2. **Given** a Meta insights row with `actions`, **When** it is normalized, **Then** each supported `action_type` is emitted as a separate `MetricFact` while preserving the original `dimensions.action_type`.
3. **Given** `offsite_conversion.fb_pixel_custom`, **When** it is normalized, **Then** the system stores it as a confirmed custom business event bundle that can include `sample_event_alpha`, `sample_event_beta`, `sample_event_gamma`, and related events.
4. **Given** `purchase` or `offsite_conversion.fb_pixel_purchase`, **When** it is normalized, **Then** the system stores it as an H5 lead submission metric, not as a real purchase or payment.

### User Story 3 - Report Sync Status (Priority: P2)

As an operator, I need a read-only sync status payload so that the data and Harness monitor can show whether Meta data is current, partial, failed, or not configured.

**Why this priority**: Workstream A/B can only trust mock and synced data if they can see sync batch status and warnings.

**Independent Test**: The sync status sample or generated payload passes `scripts/validate_api_contracts.py`.

**Acceptance Scenarios**:

1. **Given** a completed sync, **When** status is requested, **Then** the payload includes status, last sync batch, date range, object counts, and warnings.
2. **Given** unconfirmed action mappings, **When** status is requested, **Then** warnings include the relevant unconfirmed mapping codes.

## Scope

### In Scope

- Meta account hierarchy normalization for account, campaign, ad group, and ad.
- Meta insights scalar metric normalization into `MetricFact`.
- Meta `actions` normalization into `MetricFact`.
- Raw field preservation through `raw_metric_name` and `dimensions`.
- V0 sample compatibility for `accounts-tree`, `account-metrics`, `sync-status`, and `metric-facts`.
- Local validation through `scripts/validate_api_contracts.py`.

### Out of Scope

- Diagnosis, Recommendation, EvidenceObject, ActionIntent, or agent output generation.
- Any real spend-changing action.
- Campaign, ad set, or ad creation.
- Budget adjustment.
- Internal business-system read/write, booked-class attendance sync, purchase confirmation, or ROI attribution implementation.
- Google, Douyin, Tencent Ads, or Xiaohongshu deep sync.
- Adding offline spreadsheets as a platform or data source.

## Requirements

### Functional Requirements

- **FR-001**: System MUST normalize Meta account hierarchy into standard object IDs and object types.
- **FR-002**: System MUST emit scalar Meta insights metrics as atomic `MetricFact` records.
- **FR-003**: System MUST emit supported Meta `actions` as atomic `MetricFact` records.
- **FR-004**: System MUST preserve original Meta `action_type` in `MetricFact.dimensions.action_type`.
- **FR-005**: System MUST record sync batch identity on every `MetricFact`.
- **FR-006**: System MUST expose or generate sync status with object counts and warnings.
- **FR-007**: System MUST treat `offsite_conversion.fb_pixel_custom` as a custom business event bundle, not a single business event.
- **FR-008**: System MUST treat `purchase` or `offsite_conversion.fb_pixel_purchase` as external lead sample submissions in the current account, not as real purchases or payments.
- **FR-009**: System MUST NOT execute or prepare real advertising mutations.

### Data & Contract Requirements

- **DR-001**: Account tree payloads MUST follow `docs/api-contracts.md`.
- **DR-002**: Account metrics payloads MUST follow `docs/api-contracts.md`.
- **DR-003**: Sync status payloads MUST follow `docs/api-contracts.md`.
- **DR-004**: Metric fact payloads MUST follow `docs/api-contracts.md`.
- **DR-005**: Sample payloads under `data/sample/` MUST pass `scripts/validate_api_contracts.py`.
- **DR-006**: New `goal_type`, `metric_stage`, `source_quality`, or `object_type` values MUST update docs, validator, tests, and samples together.

### Safety & Privacy Requirements

- **SR-001**: Real tokens, refresh tokens, app secrets, local `.env`, authorization state, runtime DB files, logs, and raw private ad data MUST NOT be committed.
- **SR-002**: Real credentials and runtime state MUST remain under ignored private directories such as `config/private/` or `runtime/private/`.
- **SR-003**: CLI output and docs MUST redact tokens and avoid printing private account details.

## Key Entities

- **AdAccount**: Meta ad account represented by a system ID, currency, timezone, market region, and status.
- **Campaign**: Meta campaign represented as a standard ad object with platform objective and inferred `goal_type`.
- **AdGroup**: Meta Ad Set represented as `object_type=ad_group`, preserving `platform_object_type=adset`, `optimization_goal`, and parent campaign.
- **Ad**: Meta ad represented with parent ad group and platform status.
- **MetricFact**: Atomic metric record with metric name, value, stage, goal type, time window, source quality, raw metric name, dimensions, and sync batch.
- **SyncStatus**: Read-only status object for sync health, object counts, date range, warnings, and batch tracking.

## Success Criteria

- **SC-001**: All four sample payloads pass `.venv/bin/python scripts/validate_api_contracts.py`.
- **SC-002**: Full test suite passes with `.venv/bin/python -m unittest discover -s tests`.
- **SC-003**: A developer can identify which fields come from Meta raw data versus standard contract fields.
- **SC-004**: Workstream A/B can use `data/sample/*.json` without depending on Meta SDK response shape.

## Dependencies

- Existing Meta API verification scripts in `scripts/`.
- V0 API contract in `docs/api-contracts.md`.
- Data model in `docs/data-model.md`.
- Meta conversion goal mapping in `docs/meta-conversion-goals.md`.
- Private credentials stored outside git when real API access is used.

## Assumptions

- V0 uses Meta as the first real platform.
- Default timezone remains the ad account timezone, currently represented as `Asia/Shanghai` in samples.
- `quality_lead`, `lead_form`, `h5_booking`, `messaging`, and `engagement` remain distinct goal types.
- Initial implementation may use synthetic samples or redacted fixtures before live sync is complete.

## Open Questions

- What is the internal split of `offsite_conversion.fb_pixel_custom` across `sample_event_alpha`, `sample_event_beta`, `sample_event_gamma`, and related events?
- Which internal business-system fields correspond to Meta optimization targets such as booking, call connected 30s, call connected 60s, attended class, and deal count?
- Which date range should the first real read-only backfill use?
- Should raw Meta payload snapshots be stored under `runtime/private/` only, or should a redacted raw fixture format be added under `data/sample/`?
