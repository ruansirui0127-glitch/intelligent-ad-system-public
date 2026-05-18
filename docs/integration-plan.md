# 集成计划

## V0 目标

V0 要先验证「投放优化师工作台 + 受控 agent 建议链路」是否成立，而不是追求全自动投放或全平台覆盖。

V0 成功标准：

- 6 个核心页面能串成闭环。
- Meta 广告数据能进入统一对象和 MetricFact。
- 内部业务系统能以只读方式输出业务事件和归因关系。
- 规则命中能生成 EvidenceObject。
- agent 基于 ContextPackage 输出 Recommendation。
- Recommendation 能生成 ActionIntent 草稿。
- 用户可以审批或拒绝 ActionIntent。
- 数据与 Harness 监控页能追溯同步、口径、agent 任务和工具调用。

## 三条并行工作线

### 成员 A：素材增长中台

负责人：杨益。

负责：素材对象、素材标签、brief、素材表现和素材复盘。A 线给系统提供“哪个素材在什么人群、平台、时间表现怎样”，不负责广告平台 API、业务成交数据或诊断结论。

V0 交付物：

- 素材增长中台页面。
- CreativeAsset / CreativeTag 对象。
- Brief 样例。
- InsightCard 占位。
- 素材表现入口。

对外输出：`CreativeAsset`、`CreativeTag`、`Brief`、`InsightCard`、`CreativePerformance`。

### 成员 B：账户智能投放引擎 + Meta 广告数据

负责人：思锐。

负责：Meta API 只读接入、广告账户层级、广告指标、账户分析、规则配置、诊断、Recommendation、ActionIntent、账户诊断 agent 任务。B 线预留读取 C 线业务事件和归因结果的接口，但不实现内部业务系统。

V0 交付物：

- Meta 同步主链路。
- Account / Campaign / AdGroup / Ad / Creative / MetricFact。
- MetricDefinition。
- SyncJob。
- 账户分析与诊断页。
- 规则配置中心。
- RuleDefinition / RuleHit。
- Recommendation。
- ActionIntent 草稿。
- ContextPackage。

对外输出：`Account`、`Campaign`、`AdGroup`、`Ad`、`Creative`、`MetricFact`、`SyncJob`、`RuleDefinition`、`RuleHit`、`EvidenceObject`、`Recommendation`、`ActionIntent`、`ContextPackage`。

### 成员 C：内部业务系统与后链路归因

负责人：崔凯。

负责：公司内部业务系统只读接入、业务事件、归因关系和业务数据质量说明。C 线回答“广告带来的有效线索、预约、到课、成交等后链路结果是什么，以及能不能可靠归因回广告对象”，不负责 Meta 广告 API、投放建议或 ActionIntent。

V0 交付物：

- 内部业务系统只读字段映射。
- BusinessEvent 样例：有效线索、预约、到课、成交、退款等。
- AttributionLink 样例：业务事件如何回到 account / campaign / ad_group / ad / creative。
- 业务系统同步状态。
- 归因质量说明。
- 数据与 Harness 监控页的业务后链路接口。

对外输出：`BusinessEvent`、`AttributionLink`、业务系统 `SyncJob`、业务数据质量说明。

## Git 分支

- `main`：稳定版本，只合并已验证的集成结果。
- `dev`：集成版本，承接功能分支。
- `workstream/a-creative-growth`：成员 A 主分支，素材增长中台。
- `workstream/b-account-intelligence`：成员 B 主分支，账户智能投放引擎和 Meta 广告数据。
- `workstream/c-data-foundation`：成员 C 主分支，内部业务系统和后链路归因。

三条主分支直接对应三人分工，而不是直接按技术模块拆。技术模块可以作为各自工作线内部的短分支。

## 工作线内可选子分支

成员 A 可以从 `workstream/a-creative-growth` 拆：

- `feature/creative-assets`
- `feature/creative-briefs`
- `feature/insight-cards`
- `feature/creative-performance`

成员 B 可以从 `workstream/b-account-intelligence` 拆：

- `feature/meta-readonly-sync`
- `feature/account-diagnosis`
- `feature/rules-center`
- `feature/recommendations`
- `feature/action-intents`

成员 C 可以从 `workstream/c-data-foundation` 拆：

- `feature/business-system-readonly`
- `feature/business-events`
- `feature/attribution-links`
- `feature/business-data-quality`

## 集成顺序

1. 三条 `workstream/*` 都从 `dev` 创建。
2. 工作线内部的小任务先合回各自 `workstream/*`。
3. 每周或每个里程碑，把三条 `workstream/*` 合回 `dev`。
4. `dev` 做跨线集成验证：共享对象、页面 API、规则命中、EvidenceObject、ActionIntent、AgentTask 是否能串起来。
5. `dev` 稳定后合并到 `main`。

重要约束：共享契约由项目负责人 + Codex 统一把关。任何影响 `CreativeAsset`、`MetricFact`、`BusinessEvent`、`AttributionLink`、`EvidenceObject`、`Recommendation`、`ActionIntent`、`ContextPackage` 的字段变化，都要先更新 `docs/data-model.md` 和对应 API 说明。

## B/C 接口边界

B 给 C 的需求不是“帮我做诊断”，而是：给某个广告对象对应的预约、到课、成交等业务结果，以及这些结果能否可靠归因到广告对象。

C 给 B 的输出不是“广告指标”，而是：业务事件、归因关系和数据质量说明。

B 生成建议时必须同时说明广告侧指标、素材侧信息、业务后链路结果和数据质量限制。

## V0 页面验收

今日工作台：能看到风险摘要、机会摘要、待审批队列、数据质量提醒和 agent 摘要，并能跳转到对应页面。

账户分析与诊断页：能浏览账户、计划、单元、创意、素材、关键词/人群，能展开规则命中、历史基线、证据和 agent 建议。

规则配置中心：规则可编辑、可停用、可追溯；诊断结果必须引用规则版本。

ActionIntent 审批页：能查看动作类型、目标对象、证据链、风险和审批状态；V0 审批通过也不直接执行真实投放动作。

素材增长中台：素材能被账户诊断引用，并能看到素材 ID、标签、状态和表现。

数据与 Harness 监控：每条 agent 建议能查到输入、输出、上下文、工具日志、同步状态和口径状态。

内部业务系统监控：能看到业务系统只读同步状态、业务事件数量、归因成功/失败/弱归因数量和主要数据质量问题。

## 风险与待确认

- 近期开发待办：B 先开发 Meta 只读数据同步与指标拆分，C 先开发内部业务系统只读字段映射和业务事件样例，不先开发真实投放执行。
- 广告侧第一步应覆盖 raw 原始保存、standard 标准对象、MetricFact 原子指标、sample 脱敏样例。
- 业务侧第一步应覆盖 BusinessEvent、AttributionLink、业务系统同步状态和归因质量说明。
- Meta 指标拆分优先按点击漏斗处理：曝光、点击、链接点击、出站点击、落地页访问、转化、后链路结果。
- `offsite_conversion.fb_pixel_custom` 已确认是自定义业务事件合集，包括 `sample_event_alpha`、`sample_event_beta`、`sample_event_gamma` 等；仍需 C 线确认各子事件如何拆成 `BusinessEvent`。
- `purchase` / `fb_pixel_purchase` 已确认在当前 H5 链路中指 external lead sample，不代表真实成交；不能进入 ROI/ROAS 诊断。
- 各地区可接受 CPL 区间仍需业务确认。
- 有效线索、约课、到课、成交口径仍需数据同事确认。
- Meta 字段与统一模型的映射需要实测。
- 内部业务系统字段、权限和可归因 ID 需要崔凯确认。
- 真实执行动作的权限、冷却时间、回滚策略暂不进入 V0。
- Google、抖音、腾讯广告、小红书只保留扩展接口，不在 V0 深度实现。
