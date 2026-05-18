# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[feature-or-workstream-branch]`
**Created**: `[YYYY-MM-DD]`
**Status**: `Draft | Ready | Implementing | Done`
**Owner Workstream**: `A Creative | B Account Intelligence | C Data Foundation | Shared`
**Source Docs**: `[README.md, docs/product-vision.md, docs/api-contracts.md, ...]`

## Summary

[Describe what this feature must achieve and why it matters to the intelligent advertising system. Focus on business workflow and user outcome, not implementation details.]

## User Scenarios & Testing

### User Story 1 - [Brief Title] (Priority: P1)

[Describe the user journey in plain language.]

**Why this priority**: [Why this is the smallest valuable slice.]

**Independent Test**: [How this story can be tested by itself.]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome].
2. **Given** [initial state], **When** [action], **Then** [expected outcome].

### User Story 2 - [Brief Title] (Priority: P2)

[Describe the user journey in plain language.]

**Why this priority**: [Why it follows P1.]

**Independent Test**: [How this story can be tested independently.]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome].

## Scope

### In Scope

- [Capability or behavior included.]

### Out of Scope

- [Capability or behavior explicitly excluded.]

## Requirements

### Functional Requirements

- **FR-001**: System MUST [specific testable capability].
- **FR-002**: System MUST [specific testable capability].
- **FR-003**: System MUST NOT [explicit boundary].

### Data & Contract Requirements

- **DR-001**: [Shared object, API payload, sample, or schema requirement.]
- **DR-002**: [Validation, sample, or source-quality requirement.]

### Safety & Privacy Requirements

- **SR-001**: System MUST NOT store or print real tokens, app secrets, raw private ad data, local `.env`, runtime database files, or logs.
- **SR-002**: Real credentials and runtime state MUST stay under ignored private directories such as `config/private/` or `runtime/private/`.

## Key Entities

- **[Entity]**: [What it represents and the fields that matter for this feature.]

## Success Criteria

- **SC-001**: [Measurable or directly verifiable outcome.]
- **SC-002**: [Measurable or directly verifiable outcome.]

## Dependencies

- [Existing docs, API contracts, sample files, scripts, auth state, platform access, or other workstreams.]

## Assumptions

- [Assumption that should be revisited if wrong.]

## Open Questions

- [Question that must be resolved before implementation or before release.]

