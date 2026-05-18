# 统一对象词典

本文件定义主线大脑使用的统一对象。团队新增对象、页面、API、AgentTask 或样例数据前，应先检查这里是否已有对应概念。

## 对象分层

| 层级 | 作用 | 代表对象 |
| --- | --- | --- |
| 机会层 | 把市场、竞品、历史表现和业务目标转成可执行方向。 | `MarketSignal`, `OpportunityCard` |
| 上下文层 | 给人和 Agent 提供生成、诊断、建议所需的事实包。 | `ContextPackage`, `BrandRule`, `PlatformRule` |
| 素材层 | 管理素材策略、平台版本、素材资产和标签。 | `MasterAsset`, `PlatformVersion`, `CreativeAsset`, `CreativeTag` |
| 投放准备层 | 把素材组织成测试、发布或广告创建草稿。 | `LaunchPlan`, `AdGroupDraft`, `TrackingSpec` |
| 数据事实层 | 保存平台数据、业务事件和归因关系。 | `MetricFact`, `BusinessEvent`, `AttributionLink` |
| 诊断证据层 | 把规则命中和指标事实组织成可引用证据。 | `RuleDefinition`, `RuleHit`, `EvidenceObject` |
| 建议审批层 | 把诊断输出转成可审批动作和审计记录。 | `Recommendation`, `ActionIntent`, `ActionAudit` |
| Agent 运行层 | 管理 Agent 输入、输出、权限、工具和评估。 | `AgentTask`, `ToolPermission`, `ToolCallAudit`, `EvaluationResult` |
| 学习层 | 把动作结果、素材表现和人工判断沉淀为可复用经验。 | `PerformanceReport`, `LearningObject`, `RuleUpdate` |

## 核心对象

| 统一对象 | 来源 | 归属模块 | 简要定义 | V0 状态 |
| --- | --- | --- | --- | --- |
| `MarketSignal` | 素材规划 | `intelligence` / `creative` | 市场热点、竞品动作、平台趋势、教育节点或用户讨论的原始信号。 | 可作为样例或手工录入。 |
| `OpportunityCard` | 素材规划 | `creative` | 经过去重、评分和业务判断后的素材/投放机会卡。 | 建议纳入 V0 creative 样例。 |
| `ContextPackage` | 主仓 + 素材规划 | `harness` / `creative` | Agent 输入上下文包，包含业务目标、对象范围、证据、素材、规则、禁止动作和缺失信息。 | 主线对象，必须保留。 |
| `BrandRule` | 素材规划 | `creative` / `rules` | 品牌语气、禁区、合规限制、可用证据和敏感表达规则。 | V0 可先作为 ContextPackage 子集。 |
| `PlatformRule` | 素材规划 | `platform` / `creative` | 平台内容规格、广告限制、尺寸、语气和审核注意事项。 | V0 先服务 Meta，其他平台预留。 |
| `MasterAsset` | 素材规划 | `creative` | 一个机会和上下文生成出的跨平台素材母版，包含核心观点、卖点、证据、CTA 和风险。 | 建议新增到数据模型。 |
| `PlatformVersion` | 素材规划 | `creative` / `platform` | `MasterAsset` 面向特定平台、市场和素材形态的派生版本。 | 建议新增到数据模型。 |
| `CreativeAsset` | 主仓 + 素材规划 | `creative` | 可复用素材资产，可以是文案、图片、视频、脚本、brief 或剪辑指令。 | 主线对象，需扩展来源和血缘字段。 |
| `CreativeTag` | 主仓 + 素材规划 | `creative` | 素材标签，描述市场、人群、痛点、卖点、形式、生命周期、表现等。 | 主线对象，需统一 tag 类型。 |
| `LaunchPlan` | 素材规划 | `action` / `creative` | 发布或投放准备计划，组织素材、平台、目标、预算边界、追踪和测试组合。 | V0 可作为草稿对象。 |
| `AdGroupDraft` | 素材规划 | `action` / `platform` | 广告组或投放结构草稿，不等于真实广告创建。 | 必须通过 ActionIntent 才能进入执行审批。 |
| `MetricFact` | 主仓 | `data` | 标准指标事实，保存平台指标、时间窗口、来源、版本和维度。 | 主线对象，V0 优先。 |
| `BusinessEvent` | 主仓 | `data` | 留资、有效线索、接通、约课、到课、成交、退款等后链路事件。 | C 线负责内部业务系统只读接入或脱敏样例。 |
| `AttributionLink` | 主仓 | `data` | 业务事件与广告对象、素材之间的归因关系。 | C 线负责说明确认、弱归因、未确认或缺少来源 ID。 |
| `RuleDefinition` | 主仓 | `rules` | 诊断规则定义，包括阈值、窗口、样本量、风险等级和版本。 | 主线对象。 |
| `RuleHit` | 主仓 | `rules` | 某条规则在某对象上触发的命中记录。 | 主线对象。 |
| `EvidenceObject` | 主仓 | `account` / `rules` | 诊断和建议引用的证据包，必须包含指标、基线、样本量、数据质量和规则版本。 | 主线对象。 |
| `Recommendation` | 主仓 | `account` / `action` | 系统建议，必须引用 EvidenceObject。 | 主线对象。 |
| `ActionIntent` | 主仓 | `action` | 可审批动作草稿，描述目标对象、建议变更、风险、预算边界和审批状态。 | 主线对象，V0 不直接执行真实投放。 |
| `ActionAudit` | 主仓 | `action` | 审批、拒绝、执行状态和结果复盘记录。 | 主线对象。 |
| `AgentTask` | 主仓 | `harness` | Agent 任务记录，管理输入、输出、状态、模型、错误和耗时。 | 主线对象。 |
| `ToolCallAudit` | 主仓 | `harness` | Agent 调用工具的审计记录。 | 主线对象。 |
| `PerformanceReport` | 素材规划 | `learning` / `creative` | 素材、平台或投放计划的表现复盘报告。 | 建议作为 LearningObject 输入。 |
| `LearningObject` | 主仓 + 素材规划 | `learning` / `rules` | 经过确认或回测的学习沉淀，反哺规则、素材、brief 和 playbook。 | 主线对象，需扩展素材来源。 |
| `RuleUpdate` | 素材规划 | `rules` / `learning` | 由复盘提出的规则更新候选。 | 必须人工批准后才能影响生产规则。 |

## 命名原则

- 面向业务的系统对象使用英文 PascalCase，例如 `CreativeAsset`。
- API 字段和 JSON payload 使用 `snake_case`。
- 平台原始字段不能直接成为业务契约，应放入 `raw_*` 字段、`dimensions` 或 adapter 层。
- “草稿”对象不能等同于真实执行。`AdGroupDraft` 只是草稿，真实执行必须走 `ActionIntent` 和审批。
- “学习”对象不能自动变成生产规则。`RuleUpdate` 必须经过人工确认或回测。

## 需要补进 `docs/data-model.md` 的候选对象

以下对象已进入主线大脑，但尚未完全进入主数据模型：

- `MarketSignal`
- `OpportunityCard`
- `BrandRule`
- `PlatformRule`
- `MasterAsset`
- `PlatformVersion`
- `LaunchPlan`
- `AdGroupDraft`
- `TrackingSpec`
- `PerformanceReport`
- `RuleUpdate`

这些对象进入开发前，应先补充字段定义、ID 规则、状态机、归属模块和 API wire shape。
