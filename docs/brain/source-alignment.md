# 来源融合说明

本文件用于统一三个来源的角色和边界，避免团队把不同层级的东西混成一个产品主线。

## 来源一：`intelligent-ad-system`

### 角色

这是当前唯一主线。它承载系统级产品愿景、架构、数据模型、Meta 第一阶段接入、ActionIntent 审批、Agent Harness 和集成计划。

### 必须保留

- 「智能投放系统」定位：广告增长团队的智能投放操作系统。
- 第一阶段 Meta 主线：先跑通广告数据、指标事实、诊断证据和审批闭环。
- 业务系统驱动 Agent：系统保管事实、权限、审批和学习结果，Agent 只能在边界内建议和生成草稿。
- V0 不自动真钱投放，不直接改预算、出价、暂停、创建广告。
- 统一对象和共享契约优先于单个页面或单个生成工具。

### 当前短板

- 素材上游的机会发现、母版生成、多平台版本和素材复盘对象还不够完整。
- Agent 决策方法需要更明确的深挖、收敛、质检和人工确认门。
- 主文档已经较多，需要一个统一入口解释哪些文档是源头、哪些只是输入材料。

## 来源二：素材增长规划包

### 角色

这是素材增长脑。它补足从市场信号到素材资产再到复盘学习的完整素材链路：

```text
OpportunityCard -> ContextPackage -> MasterAsset -> PlatformVersion -> CreativeAsset -> LaunchPlan -> LearningItem
```

### 吸收内容

| 内容 | 融合方式 |
| --- | --- |
| `OpportunityCard` | 进入主线对象词典，用于把市场信号、竞品素材和历史表现转成可执行机会。 |
| `MasterAsset` | 进入 creative 模块，表示跨平台素材母版和核心创意策略。 |
| `PlatformVersion` | 进入 creative/platform 交界，表示母版在 Meta、小红书、TikTok 等平台的派生版本。 |
| `LaunchPlan` / `AdGroupDraft` | 进入 action/creative 交界，作为投放准备草稿，后续必须通过 ActionIntent 审批。 |
| `PerformanceReport` / `LearningItem` / `RuleUpdate` | 进入学习闭环，作为素材表现复盘和规则更新候选。 |
| 6 条素材工作流 | 作为 creative 模块的业务流程底稿，不直接覆盖系统全局流程。 |

### 不直接吸收

- 不把素材包的一级导航原样迁入主仓。
- 不把小红书、TikTok、YouTube 等作为 V0 平台接入主线。
- 不把 AI 生成内容质量作为 V0 第一验收标准。
- 不让 AI 自动发布高风险内容、自动创建真钱广告或自动修改生产规则。

### 融合原则

素材链路是主线大脑的上游和学习资产层。它必须接入 `CreativeAsset`、`MetricFact`、`EvidenceObject`、`Recommendation` 和 `LearningObject`，而不是成为一套独立素材系统。

## 来源三：`agentic-skill-orchestration`

### 角色

这是 Agent 决策脑。它提供一套方法，让团队在复杂问题里避免直接跳到执行：

- 用深挖方法处理根因、约束和真实优化目标。
- 用产品决策方法处理范围、价值、优先级和确认门。
- 用质量检查方法处理 skill、prompt、工作流和输出可靠性。
- 用有限发散方法生成 2-3 个候选方向，再回到主线决策。

### 吸收内容

| 内容 | 融合方式 |
| --- | --- |
| Lead skill / hook skill 思想 | 转化为 AgentTask 的阶段：主任务负责闭环，辅助任务只提供有边界的分析输入。 |
| Outcome gate | 用于重大产品、架构、平台接入和自动化能力开工前。 |
| Quality gate | 用于生成建议、素材、规则更新、skill 优化和 Agent 输出评估。 |
| Anti-loop 规则 | 用于限制 Agent 互相调用、反复发散和绕过人工确认。 |

### 不直接吸收

- 不把外部 skill 名称写进业务对象。
- 不把 skill 编排当成产品主线。
- 不让 Agent 决策方法覆盖系统数据模型和审批机制。

## 融合后的完整角色图

```text
系统主脑：定义主线、对象、数据、审批、审计
素材增长脑：提供机会、母版、平台版本、素材资产、素材学习
Agent 决策脑：提供深挖、收敛、质检、确认门
```

三者的正确关系是：

```text
素材增长脑产生候选机会和素材资产
系统主脑用数据和证据判断是否值得行动
Agent 决策脑在边界内解释、生成建议和检查质量
最终动作进入 ActionIntent，由人审批
复盘结果进入 LearningObject，再反哺素材和规则
```

## 集成边界

| 问题 | 裁决 |
| --- | --- |
| 谁是主线？ | `intelligent-ad-system`。 |
| 素材规划是否独立成新系统？ | 否，作为 creative 和 learning 能力并入主线。 |
| Agent skill 是否成为大脑核心？ | 方法层可以吸收，业务主线不能交给 skill 编排。 |
| V0 是否全平台？ | 否，V0 仍以 Meta 数据和受控建议闭环为主。 |
| 是否能自动执行投放？ | V0 不能，所有高风险动作必须通过 ActionIntent 审批。 |
