---
name: intelligent-ad-system-brain
description: Use when planning, implementing, reviewing, or coordinating work in the intelligent advertising system, especially changes involving V0 scope, Meta, creative growth, account intelligence, data foundation, Agent Harness, Recommendation, ActionIntent, or shared project direction.
---

# Intelligent Ad System Brain

This skill is the project-local operating brain for the intelligent advertising system. Use it to keep product direction, workstream boundaries, shared contracts, and safety constraints aligned before changing code or docs.

## Required Reading

Read only the needed sections, but start from these files when the task affects direction, scope, shared contracts, or workstream handoff:

- `docs/brain/README.md`
- `docs/brain/source-alignment.md`
- `docs/brain/brain-workflow.md`
- `docs/brain/object-glossary.md`
- `docs/brain/decision-log.md`
- `docs/brain/three-workstream-development-plan.md`
- `docs/data-model.md`
- `docs/api-contracts.md`
- `docs/integration-plan.md`

For implementation slices, also read the matching spec folder:

- Meta advertising data and account intelligence: `docs/specs/001-meta-readonly-sync/` and `docs/specs/003-account-intelligence-loop/`
- Creative growth: `docs/specs/002-creative-growth-loop/`
- Internal business system and attribution: `docs/specs/004-business-system-readonly-attribution/`

## Core Product Truth

The main repository is the system brain. The creative planning package is absorbed as the creative growth brain. `agentic-skill-orchestration` is absorbed only as controlled-agent decision methodology.

Do not turn the product into:

- a standalone creative generation tool
- a pure skill-orchestration experiment
- a dashboard that only shows risk cards
- an agent that directly mutates real ad spend

V0 validates:

```text
投放优化师工作台 + 受控 agent 建议链路
```

The V0 minimum loop is:

```text
数据同步 -> 规则命中 -> EvidenceObject -> ContextPackage -> agent 建议 -> Recommendation -> ActionIntent 草稿 -> 审批/拒绝 -> ActionAudit -> 复盘样本
```

## Workstream Boundaries

| Workstream | Branch | Owns | Does Not Own |
| --- | --- | --- | --- |
| A Creative Growth | `workstream/a-creative-growth` | OpportunityCard, MasterAsset, PlatformVersion, CreativeAsset, CreativeTag, brief, creative performance, creative learning candidates | Real publishing, budget changes, final account diagnosis |
| B Account Intelligence + Meta Ads Data | `workstream/b-account-intelligence` | Meta read-only API, Account/Campaign/AdGroup/Ad/Creative normalization, MetricFact, SyncStatus, RuleHit, EvidenceObject, ContextPackage, Recommendation, ActionIntent, ActionAudit, account diagnosis agent task | Internal business-system implementation, direct platform mutation, creative asset production |
| C Business System + Attribution | `workstream/c-data-foundation` | Internal business system read-only integration, BusinessEvent, AttributionLink, business sync status, business data quality notes | Meta Ads API, ad metrics, Recommendations, ActionIntent, creative generation |

The data input is split in two: B owns advertising-platform data, C owns internal business events and attribution. Do not let either side silently redefine the other's data.

## Interface Rules

- A gives B: creative ID, creative tags, creative status, creative performance, and review notes.
- B gives C: the ad object IDs and time windows that need business outcomes.
- C gives B: business events, attribution links, and data quality notes.
- B recommendations must cite advertising metrics, creative information, business outcomes, and data-quality limitations when those inputs exist.
- You + Codex own final wording, shared objects, contracts, samples, validators, tests, and integration acceptance.

## Decision Rules

Before adding fields, endpoints, samples, tasks, pages, or agent behavior:

1. Locate the object in `docs/data-model.md`.
2. Locate or add the wire shape in `docs/api-contracts.md`.
3. Keep samples under `data/sample/` synthetic or redacted.
4. Keep API-style payloads in the `data / meta / errors` envelope.
5. Use `snake_case` for JSON fields.
6. Preserve stable IDs so other workstreams can reference them.
7. Update validator and tests together with contract changes.

Agent output is never free-form authority. It must be constrained by:

- `ContextPackage`
- allowed tools
- forbidden actions
- evidence references
- data quality notes
- `ToolCallAudit`
- human approval gate

## Communication Rule

Default to wording that a non-technical, non-ad-operations teammate can understand.

When mentioning technical or advertising-system terms, explain the plain business meaning first, then include the system term:

| Plain meaning | System term |
| --- | --- |
| 一条可被系统引用的指标事实 | `MetricFact` |
| 一包支持某个判断的证据 | `EvidenceObject` |
| 给 Agent 的限定材料和禁止动作清单 | `ContextPackage` |
| 系统建议，但还要人工确认 | `Recommendation` |
| 等待人工审批的动作草稿 | `ActionIntent` |
| 审批、拒绝或后续执行记录 | `ActionAudit` |

For planning, task assignment, meeting notes, and acceptance criteria, write in this order:

1. What business question this solves.
2. What input each person must provide.
3. What output counts as done.
4. Which project object, file, sample, validator, or test represents it.

Do not give teammates only file paths, JSON fields, validator names, or agent terminology without the plain-language layer.

## Safety Rules

Never commit or print:

- real tokens
- refresh tokens
- app secrets
- real ad data
- local `.env`
- runtime SQLite databases
- logs
- files under `config/private/` or `runtime/private/`

V0 must not execute real ad mutations. Approved `ActionIntent` is still a controlled workflow object unless a later phase explicitly implements execution with additional safety gates.

## Validation

Run these before calling work complete:

```bash
.venv/bin/python scripts/validate_api_contracts.py
.venv/bin/python -m unittest discover -s tests
```

If the change affects shared contracts, also inspect:

```bash
git status --short
git diff -- docs/api-contracts.md docs/data-model.md data/sample scripts/validate_api_contracts.py tests
```

## Common Mistakes

- Treating the two-person staffing workaround as a two-workstream product structure.
- Letting creative growth bypass account evidence and ActionIntent approval.
- Letting account intelligence read raw platform payloads instead of standard objects and `MetricFact`.
- Letting data foundation produce diagnosis or recommendations.
- Adding samples without validator coverage.
- Updating docs without keeping implementation tasks aligned.
