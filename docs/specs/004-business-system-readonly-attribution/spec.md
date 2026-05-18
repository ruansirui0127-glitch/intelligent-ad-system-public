# Feature Specification: Business System Read-Only Events and Attribution

**Feature Branch**: `workstream/c-data-foundation`
**Created**: `2026-05-17`
**Status**: `Draft`
**Owner Workstream**: `C Business System + Attribution`
**Source Docs**: `docs/brain/README.md`, `docs/brain/three-workstream-development-plan.md`, `docs/integration-plan.md`, `docs/data-model.md`, `docs/api-contracts.md`

## Summary

Build the first internal business-system read-only slice: extract or mock downstream business events such as valid lead, booking, attendance, purchase, and refund; then connect those events back to Meta account, campaign, ad group, ad, or creative objects through attribution links and data-quality notes.

This feature does not call Meta Ads API, generate recommendations, create ActionIntent, write back to the internal business system, or decide ad optimization actions.

## User Scenarios & Testing

### User Story 1 - Capture Business Events (Priority: P1)

As an account intelligence consumer, I need downstream business events represented consistently so that diagnosis can see more than Facebook lead counts.

**Independent Test**: A business event sample contains event type, event time, source system, status, and enough source references for attribution review.

**Acceptance Scenarios**:

1. **Given** an internal valid lead, booking, attendance, purchase, or refund record, **When** it is represented as a business event, **Then** it includes event ID, lead or customer reference, event type, event time, market region, source system, status, and value when available.
2. **Given** the business meaning is not confirmed, **When** the event is represented, **Then** the data quality note says it is unconfirmed instead of treating it as a final conversion.

### User Story 2 - Link Business Events Back to Ads (Priority: P1)

As an optimizer, I need to know whether a downstream event can be attributed to a campaign, ad group, ad, or creative so that recommendations do not rely only on CPL.

**Independent Test**: An attribution link sample connects a business event ID to a Meta object ID with match method, confidence, attribution window, and quality flag.

**Acceptance Scenarios**:

1. **Given** a business event can be matched to a Meta object, **When** an attribution link is created, **Then** it records object type, object ID, match method, confidence, attribution window, and quality flag.
2. **Given** attribution is weak or missing, **When** a link is created or omitted, **Then** the output explains the limitation rather than forcing a confident match.

### User Story 3 - Report Business-System Sync Quality (Priority: P2)

As an integrator, I need to see whether business data is current, partial, failed, or not configured so that B-line recommendations can carry correct confidence.

**Independent Test**: A business sync status sample includes system name, date range, object counts, status, warnings, and missing-field notes.

## Scope

### In Scope

- Read-only internal business system field mapping.
- `BusinessEvent` sample shape.
- `AttributionLink` sample shape.
- Business-system sync status and data quality notes.
- Synthetic or redacted samples that B can cite.

### Out of Scope

- Meta Ads API.
- Ad metrics or `MetricFact` generation.
- Recommendation, EvidenceObject, ActionIntent, or agent output.
- Writes to CRM, scheduling, payment, or sales systems.
- Final ROI or LTV modeling.

## Requirements

- **FR-001**: System MUST represent downstream outcomes as `BusinessEvent`.
- **FR-002**: System MUST represent event-to-ad relationships as `AttributionLink`.
- **FR-003**: Attribution MUST include match method, confidence, attribution window, and quality flag.
- **FR-004**: Weak, missing, or unconfirmed attribution MUST be explicit.
- **FR-005**: Samples MUST avoid real customer data, real phone numbers, real names, raw private IDs, logs, and secrets.
- **FR-006**: C-line output MUST be read-only and must not write back to internal systems.

## Success Criteria

- **SC-001**: B line can cite at least one business event and attribution link in an account diagnosis sample.
- **SC-002**: C line can tell which events are confirmed, weakly attributed, unconfirmed, or missing source IDs.
- **SC-003**: MVP demo can show an ad with good front-end metrics but weak downstream business quality.
