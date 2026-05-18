# 主线大脑

本目录是智能投放系统的统一决策入口。它不替代 `docs/product-vision.md`、`docs/architecture.md`、`docs/data-model.md` 和 `docs/integration-plan.md`，而是把团队不同来源的规划、素材链路和 Agent 方法收敛到同一套主线判断里。

## 大脑定位

智能投放系统的大脑不是单个模型、单个脚本或单个页面，而是一套可追溯的增长决策系统：

```text
统一对象 -> 可信证据 -> 受控 Agent -> 可审批动作 -> 复盘学习
```

业务系统负责事实、对象、规则、权限、审批、日志和学习结果；Agent 只能在系统给定的上下文、证据和权限边界内生成解释、建议、草稿和复盘。

## 当前唯一主线

当前主线仓库是 `intelligent-ad-system`。第一阶段以 Meta 平台为广告数据和投放诊断主线，V0 先验证：

```text
数据同步 -> 规则命中 -> EvidenceObject -> ContextPackage -> Agent 建议 -> Recommendation -> ActionIntent 草稿 -> 审批/拒绝 -> ActionAudit -> 复盘样本
```

素材增长、Agent 技能编排、多平台内容生成都必须服务这条主线，而不是另起一套产品结构。

## 三个大脑分层

| 层级 | 来源 | 在主线中的角色 | 不做什么 |
| --- | --- | --- | --- |
| 系统主脑 | `intelligent-ad-system` | 定义产品边界、数据模型、Meta 主线、审批、审计和学习闭环。 | 不被外部规划反向改成单点素材工具或纯 Agent 实验。 |
| 素材增长脑 | 素材同事的广告素材自动化规划 | 补足从市场机会到素材资产、投放计划、素材复盘学习的链路。 | 不替代 Meta 第一阶段主线，不直接成为一级产品结构。 |
| Agent 决策脑 | `agentic-skill-orchestration` | 提供深挖、收敛、质检和确认门的工作方法。 | 不直接成为业务数据模型，不绕过审批执行投放动作。 |

## 核心文档

- `source-alignment.md`：说明三个来源如何融合、哪些吸收、哪些拒绝。
- `object-glossary.md`：统一对象词典，任何新对象进入系统前必须先对齐这里。
- `brain-workflow.md`：完整主链路，从市场信号到学习回流。
- `decision-log.md`：关键决策记录，解决团队口径冲突。
- `three-workstream-development-plan.md`：按成员 A/B/C 三条工作线推进 V0 的开发版本。

## 决策优先级

当文档、同事方案或外部仓库之间出现冲突时，按以下顺序裁决：

1. `docs/brain/decision-log.md` 中已经确认的决策。
2. `docs/product-vision.md` 和 `docs/architecture.md` 中的产品边界与架构原则。
3. `docs/data-model.md` 和 `docs/api-contracts.md` 中的对象与契约。
4. `docs/integration-plan.md` 中的工作线和集成约束。
5. 素材规划、外部 skill、临时方案和个人草稿。

涉及真实 token、私有投放数据、预算、投放执行、平台授权和生产规则变更时，必须人工确认。

## 更新规则

- 重要产品判断、对象新增、数据模型变化、平台接入约束和 Agent 权限变化，必须同步更新本目录。
- 新对象先进入 `object-glossary.md`，再进入 `docs/data-model.md` 或 API 契约。
- 新判断先进入 `decision-log.md`，再影响路线图、开发计划和分支任务。
- 任何文档不能打印真实 token、私有投放数据、私有账号信息或本地 `.env` 内容。
