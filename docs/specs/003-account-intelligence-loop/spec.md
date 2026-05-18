# Feature Specification: Account Intelligence Controlled Suggestion Loop

**Feature Branch**: `workstream/b-account-intelligence`
**Created**: `2026-05-15`
**Status**: `Draft`
**Owner Workstream**: `B Account Intelligence + Meta Ads Data`
**Source Docs**: `docs/brain/README.md`, `docs/brain/brain-workflow.md`, `docs/integration-plan.md`, `docs/data-model.md`, `docs/api-contracts.md`

## Summary

Build the first account intelligence sample loop: consume Meta account hierarchy, advertising `MetricFact` samples, creative performance, and C-line business event / attribution samples; then produce rule hits, evidence objects, context packages, recommendations, and ActionIntent drafts that can be approved or rejected without executing real advertising actions.

This feature does not implement the Meta sync itself, adjust budget, pause ads, create campaigns, write to internal business systems, or execute any spend-changing action. Meta sync is covered by `docs/specs/001-meta-readonly-sync/`.

## User Scenarios & Testing

### User Story 1 - Review Full Account Diagnosis Context (Priority: P1)

As an optimizer, I need to see account hierarchy, metrics, and rule hits together so that diagnosis is based on full account context, not isolated risk cards.

**Why this priority**: V0 must prove users can inspect account-level data before trusting agent suggestions.

**Independent Test**: An account diagnosis sample can reference account tree and metric fact sample IDs without using raw Meta fields directly.

**Acceptance Scenarios**:

1. **Given** account and metric samples exist, **When** diagnosis context is built, **Then** the output includes account object scope, time window, metric references, and rule hits.
2. **Given** a rule hit exists, **When** it is displayed or validated, **Then** it includes rule version, current value, baseline value, sample size, severity, and evidence reference.

### User Story 2 - Generate Evidence-Backed Recommendation (Priority: P1)

As an optimizer, I need every recommendation to cite an EvidenceObject so that agent output is explainable and auditable.

**Why this priority**: Recommendation without evidence would break the V0 controlled agent chain.

**Independent Test**: A recommendation sample fails validation if `evidence_id` is missing.

**Acceptance Scenarios**:

1. **Given** an EvidenceObject exists, **When** a recommendation is generated, **Then** it references the evidence, risk level, object scope, and recommendation type.
2. **Given** data quality is partial, **When** recommendation text is generated, **Then** it includes a limitation rather than pretending certainty.

### User Story 3 - Create ActionIntent Draft (Priority: P1)

As an optimizer, I need recommendations to become ActionIntent drafts that can be approved or rejected, while V0 does not execute real spend-changing actions.

**Why this priority**: ActionIntent is the central V0 proof that agent advice becomes a controlled workflow, not direct automation.

**Independent Test**: An ActionIntent sample has `approval_state=draft` or `pending_review` and no execution status indicating real platform mutation.

**Acceptance Scenarios**:

1. **Given** a recommendation exists, **When** an ActionIntent draft is created, **Then** it includes action type, target object, proposed change, budget boundary, cooldown policy, risk policy, approval state, and evidence ID.
2. **Given** a user rejects an ActionIntent, **When** ActionAudit is recorded, **Then** the audit includes decision, decided by, decided at, reject reason, and result summary.

## Scope

### In Scope

- RuleDefinition / RuleHit sample shape.
- EvidenceObject sample shape.
- ContextPackage sample shape for account diagnosis.
- Recommendation sample shape.
- ActionIntent and ActionAudit sample shape.
- Optional validator and tests for account intelligence samples.

### Out of Scope

- Meta API sync implementation, which belongs to `docs/specs/001-meta-readonly-sync/` in the same B workstream.
- Real budget, bid, pause, create, or edit actions.
- Full agent model integration.
- Multi-platform account diagnosis.
- Internal business-system integration, which belongs to C line.

## Requirements

### Functional Requirements

- **FR-001**: System MUST build diagnosis context from standard objects and MetricFact references, not raw platform payloads.
- **FR-002**: RuleHit MUST reference a RuleDefinition version and EvidenceObject.
- **FR-003**: Recommendation MUST reference EvidenceObject.
- **FR-004**: ActionIntent MUST reference Recommendation and EvidenceObject.
- **FR-005**: ActionIntent MUST remain draft or review-only in V0.
- **FR-006**: ActionAudit MUST record approve or reject decisions without implying real execution.
- **FR-007**: AgentTask output MUST be auditable through ContextPackage and ToolCallAudit references when agent samples are added.

### Data & Contract Requirements

- **DR-001**: Account intelligence sample payloads MUST use `data / meta / errors`.
- **DR-002**: JSON fields MUST use `snake_case`.
- **DR-003**: Samples MUST preserve object IDs from account, creative, metric, business event, and attribution samples.
- **DR-004**: New required fields MUST update `docs/api-contracts.md`, validator, tests, and samples together.

### Safety & Privacy Requirements

- **SR-001**: Samples MUST NOT contain real tokens, raw private ad data, local `.env`, runtime database files, or logs.
- **SR-002**: V0 MUST NOT execute real advertising actions.
- **SR-003**: Agent output MUST NOT claim certainty when evidence or data quality is incomplete.

## Key Entities

- **RuleDefinition**: Versioned diagnostic rule with threshold, baseline method, sample size, and risk level.
- **RuleHit**: A rule firing against an account, campaign, ad group, ad, creative, or other object.
- **EvidenceObject**: Evidence package with metrics, baseline, comparison, sample size, data quality, and rule version.
- **ContextPackage**: Agent input package with object scope, metrics, rules, evidence IDs, allowed tools, and forbidden actions.
- **Recommendation**: Evidence-backed suggestion generated by system or agent.
- **ActionIntent**: Reviewable draft action derived from a recommendation.
- **ActionAudit**: Approval or rejection record and later execution/result placeholder.

## Success Criteria

- **SC-001**: Account intelligence sample payloads pass contract validation when added.
- **SC-002**: Existing Meta and creative sample validation continues to pass.
- **SC-003**: A teammate can trace each recommendation to EvidenceObject, ContextPackage, MetricFact, and source object.
- **SC-004**: A teammate can approve or reject an ActionIntent sample without any real platform mutation.

## Dependencies

- Meta read-only sync samples from `docs/specs/001-meta-readonly-sync/`.
- Creative asset samples from `docs/specs/002-creative-growth-loop/` when creative performance is referenced.
- `docs/api-contracts.md`
- `docs/data-model.md`
- `docs/brain/brain-workflow.md`

## Assumptions

- First account intelligence samples can use synthetic Meta object IDs already present in `data/sample/`.
- Rule thresholds can be sample values until business thresholds are confirmed.
- Agent output can be represented as deterministic sample JSON before model integration.

## Open Questions

- Which first rule should be used for the V0 demo: CPL over threshold, zero conversion stop-loss, CTR decline, or creative fatigue?
- Which ActionIntent action types should be allowed in V0 samples?
- Should ActionAudit initially support both approve and reject examples, or only reject to emphasize no execution?
