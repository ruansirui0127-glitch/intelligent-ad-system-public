# 主线大脑工作流

本文件定义智能投放系统的完整对象链路。它把素材增长、Meta 数据、诊断建议、审批和复盘学习放在同一条可追踪的主线上。

## 完整链路

```text
MarketSignal
-> OpportunityCard
-> ContextPackage
-> MasterAsset
-> PlatformVersion
-> CreativeAsset
-> LaunchPlan / AdGroupDraft
-> MetricFact / BusinessEvent
-> EvidenceObject
-> Recommendation
-> ActionIntent
-> ActionAudit
-> LearningObject / RuleUpdate
-> 下一轮 OpportunityCard / RuleDefinition / CreativeBrief
```

这条链路是主线大脑的判断基准。任何页面、Agent、脚本、API 或自动化任务，都应该说明自己服务链路中的哪一段。

## 阶段 1：机会进入系统

### 目标

把市场、竞品、平台趋势和历史表现转成可判断的机会，而不是只收集链接或热点。

### 输入

- 市场热点、教育节点、政策变化、用户讨论。
- 竞品广告、自然内容、落地页、评论反馈。
- 历史素材表现、广告表现、后链路质量。
- 当前业务目标、市场优先级和平台边界。

### 输出

- `MarketSignal`
- `OpportunityCard`

### 决策门

- 这个机会是否服务当前目标市场和业务阶段？
- 是否有足够证据进入素材生成？
- 是否存在合规、文化语境或平台限制？

## 阶段 2：上下文和素材母版

### 目标

让 Agent 基于公司事实、卖点、证据、禁区和平台规则生成素材策略，而不是空泛生成内容。

### 输入

- `OpportunityCard`
- 公司知识、产品信息、案例、FAQ、品牌语气。
- 已有素材和历史高表现样本。
- 平台内容规则和广告限制。

### 输出

- `ContextPackage`
- `MasterAsset`
- `PlatformVersion`

### 决策门

- 公司事实是否足够？缺失事实必须回到人工补充。
- 母版是否引用了明确证据和禁区？
- 平台版本是否说明目标、格式、CTA、风险和适配理由？

## 阶段 3：素材入库和投放准备

### 目标

把文案、图片、视频、脚本、brief 和剪辑指令变成可追踪、可复用、可复盘的素材资产，并组织成投放草稿。

### 输入

- `MasterAsset`
- `PlatformVersion`
- 人工上传或 AI 生成的素材。
- 平台、账号、预算边界、追踪规则和测试目标。

### 输出

- `CreativeAsset`
- `CreativeTag`
- `LaunchPlan`
- `AdGroupDraft`
- `TrackingSpec`

### 决策门

- 素材是否能追溯到机会、母版和平台版本？
- 标签是否足以支持后续诊断和复用？
- 投放草稿是否仍处于草稿状态，未绕过 ActionIntent？

## 阶段 4：数据事实和证据

### 目标

把平台数据和后链路事件变成可诊断的事实，再组织成可引用证据。

### 输入

- Meta 广告对象和 Insights。
- 后链路业务事件。
- 素材、广告对象、平台版本和投放计划关系。
- 同步批次、指标口径和数据质量状态。

### 输出

- `MetricFact`
- `BusinessEvent`
- `AttributionLink`
- `RuleHit`
- `EvidenceObject`

### 决策门

- 指标是否有来源、时间窗口、口径版本和同步批次？
- Meta `actions` 是否已拆成原子 `MetricFact`？
- 数据质量不足时是否输出数据质量问题，而不是生成确定建议？

## 阶段 5：建议、审批和审计

### 目标

让 Agent 基于证据输出可解释建议，再转成受控动作草稿，由人审批。

### 输入

- `EvidenceObject`
- `ContextPackage`
- 当前规则、历史基线、样本量、素材状态、禁止动作。

### 输出

- `Recommendation`
- `ActionIntent`
- `ActionAudit`
- `AgentTask`
- `ToolCallAudit`
- `EvaluationResult`

### 决策门

- 建议是否引用 EvidenceObject？
- Agent 是否越权、缺证据或缺规则版本？
- 动作是否进入 ActionIntent，而不是直接执行？
- 高风险动作是否有预算边界、冷却时间和审批状态？

## 阶段 6：复盘和学习回流

### 目标

把动作结果、素材表现和人工判断沉淀为可复用学习，反哺规则、素材 brief 和下一轮机会。

### 输入

- `ActionAudit`
- 素材表现、广告表现、后链路结果。
- 人工备注和归因异常说明。

### 输出

- `PerformanceReport`
- `LearningObject`
- `RuleUpdate`
- 下一轮 `OpportunityCard`
- 下一轮 `CreativeBrief`

### 决策门

- 学习结论是否有证据和适用范围？
- 是否区分保留、放大、淘汰、重写？
- 规则更新是否经过人工批准或回测？
- 学习是否能回到素材标签、生成偏好、规则或 playbook？

## V0 最小闭环

V0 不需要一次实现全链路自动化。最小闭环是：

```text
Meta 数据同步
-> MetricFact
-> RuleHit
-> EvidenceObject
-> ContextPackage
-> Recommendation
-> ActionIntent 草稿
-> 审批/拒绝
-> ActionAudit
-> LearningObject 样例
```

素材增长脑在 V0 的最小接入是：

```text
OpportunityCard 样例
-> MasterAsset 样例
-> PlatformVersion 样例
-> CreativeAsset / CreativeTag
-> 素材表现入口
```

两条最小链路必须通过 `CreativeAsset`、`MetricFact`、`EvidenceObject` 和 `LearningObject` 接上。

## 不允许的断点

- 素材生成后不入库。
- 素材没有来源机会、母版或平台版本。
- 平台数据直接进入页面，不经过标准对象或 MetricFact。
- Agent 建议没有 EvidenceObject。
- ActionIntent 审批通过就直接真钱执行。
- 复盘只写自然语言报告，不进入 LearningObject。
- AI 自动把 RuleUpdate 变成生产规则。
