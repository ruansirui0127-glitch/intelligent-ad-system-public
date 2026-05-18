# Feature Specification: Creative Growth Sample Loop

**Feature Branch**: `workstream/a-creative-growth`
**Created**: `2026-05-15`
**Status**: `Draft`
**Owner Workstream**: `A Creative`
**Source Docs**: `docs/brain/README.md`, `docs/brain/object-glossary.md`, `docs/brain/brain-workflow.md`, `docs/data-model.md`, `docs/api-contracts.md`

## Summary

Build the first creative growth sample loop: represent an opportunity, context-backed master asset, platform version, creative asset, and performance report using synthetic sample data that follows the system brain and V0 API contract.

This feature does not generate real images or videos, publish content, create ads, adjust budgets, or call any external platform API.

## User Scenarios & Testing

### User Story 1 - Review Creative Opportunities (Priority: P1)

As a creative growth owner, I need a stable `OpportunityCard` sample list so that the team can see what market or platform opportunity is being turned into assets.

**Why this priority**: Without an opportunity object, generated assets cannot be traced back to a business reason.

**Independent Test**: `data/sample/creative-opportunities.sample.json` passes the local contract validator.

**Acceptance Scenarios**:

1. **Given** a creative opportunity sample, **When** it is validated, **Then** each item has an ID, market region, recommended platforms, pain point, angle, evidence references, priority score, and status.
2. **Given** an opportunity is not ready, **When** it is represented in the sample, **Then** its status explains whether it needs context, review, or archival.

### User Story 2 - Trace Assets To Source (Priority: P1)

As a creative teammate, I need every creative asset to trace back to an opportunity, master asset, and platform version so that assets do not become loose files.

**Why this priority**: The system brain requires creative assets to be reusable and auditable, not scattered outputs.

**Independent Test**: `data/sample/creative-assets.sample.json` passes validation and all `CreativeAsset` items include lineage fields.

**Acceptance Scenarios**:

1. **Given** a creative asset sample, **When** it is validated, **Then** it includes `opportunity_id`, `master_asset_id`, `platform_version_id`, `approval_status`, `servable_status`, and tags.
2. **Given** a platform version sample, **When** it is inspected, **Then** it explains platform, placement, CTA, risk level, and adaptation reason.

### User Story 3 - Record Creative Performance Learning (Priority: P2)

As a project owner, I need a performance report sample so that the first learning loop can explain what worked, what did not, and what should change next.

**Why this priority**: Learning must enter structured objects before the team builds Recommendation and ActionIntent.

**Independent Test**: `data/sample/creative-performance.sample.json` passes validation and links performance back to a creative asset.

**Acceptance Scenarios**:

1. **Given** a performance report sample, **When** it is validated, **Then** it includes scope, time window, metric references, summary, winning factors, losing factors, data quality, and author type.
2. **Given** a report proposes a rule update, **When** the sample is inspected, **Then** the update remains a draft and requires review.

## Scope

### In Scope

- Synthetic `OpportunityCard`, `MasterAsset`, `PlatformVersion`, `CreativeAsset`, and `PerformanceReport` samples.
- Contract validator support for creative sample files.
- Tests for creative sample validation.
- Optional frontend/backend mock consumption of creative samples.

### Out of Scope

- Real social listening, competitor crawling, image generation, video generation, or editing automation.
- Real platform publishing or ad creation.
- Real budget, bid, campaign, ad set, or ad mutation.
- Deep integration with Xiaohongshu, TikTok, YouTube, Google, or Meta publishing APIs.
- Automatic production rule updates.

## Requirements

### Functional Requirements

- **FR-001**: System MUST represent creative opportunities as `domain_object_type=opportunity`.
- **FR-002**: System MUST represent creative assets as `domain_object_type=creative_asset`.
- **FR-003**: System MUST preserve asset lineage through `opportunity_id`, `master_asset_id`, and `platform_version_id`.
- **FR-004**: System MUST represent performance reports as structured objects instead of free-form notes only.
- **FR-005**: System MUST NOT treat `RuleUpdate` drafts as production rules.
- **FR-006**: System MUST NOT publish content or create ads from this sample loop.

### Data & Contract Requirements

- **DR-001**: Creative sample payloads MUST use the `data / meta / errors` response envelope.
- **DR-002**: Creative sample payloads MUST use `snake_case` JSON fields.
- **DR-003**: Domain IDs MUST follow `{domain}:{object_type}:{local_id}`.
- **DR-004**: Existing Meta sample payload validation MUST continue to pass.
- **DR-005**: Validator and tests MUST be updated when creative sample payloads are added.

### Safety & Privacy Requirements

- **SR-001**: Samples MUST NOT include real tokens, app secrets, raw private ad data, local `.env`, runtime database files, or logs.
- **SR-002**: Samples MUST use synthetic or explicitly sanitized business content.
- **SR-003**: Any generated media URI in samples MUST be null or point to a safe local placeholder, not a private asset.

## Key Entities

- **OpportunityCard**: A scored creative opportunity with market, platform, audience, pain point, angle, evidence, and risk notes.
- **MasterAsset**: A cross-platform creative strategy derived from opportunity and context.
- **PlatformVersion**: A platform-specific adaptation of a master asset.
- **CreativeAsset**: A reusable asset such as copy, image brief, video script, or edit instruction.
- **PerformanceReport**: Structured performance learning tied to an asset, platform version, or launch plan.

## Success Criteria

- **SC-001**: Creative sample files pass `.venv/bin/python scripts/validate_api_contracts.py`.
- **SC-002**: Full test suite passes with `.venv/bin/python -m unittest discover -s tests`.
- **SC-003**: A teammate can trace each creative asset from opportunity to platform version.
- **SC-004**: A teammate can explain how creative performance would feed the next learning loop.

## Dependencies

- `docs/brain/object-glossary.md`
- `docs/brain/brain-workflow.md`
- `docs/data-model.md`
- `docs/api-contracts.md`
- `scripts/validate_api_contracts.py`
- Existing sample validation tests.

## Assumptions

- First creative samples can use synthetic Hong Kong / Macau Meta examples.
- Creative output quality is not the first-stage success metric; object flow and traceability are.
- Creative samples may be frontend-ready before any real backend implementation exists.

## Open Questions

- Which first opportunity should be used as the team demo sample?
- Should creative sample payloads live as three files or one combined fixture?
- Which frontend page consumes the creative sample first: today workbench or creative workbench?
