# 架构设计

## 架构原则

本系统采用「业务系统驱动 agentic workflows」的架构。

业务系统负责事实、对象、规则、权限、审批、动作日志和学习结果；agent 负责在系统提供的上下文、证据和权限边界内完成诊断、摘要、建议和复盘。不要把它做成 agent 直接连接数据库、直接调用广告平台、直接花钱的系统。

V0 建议先做模块化单体：一个后端、多组接口、一个数据底座、一套 Agent Harness。三人团队最重要的是边界清晰、接口稳定、每周可集成，而不是一开始拆微服务。

## 总体分层

1. Experience Layer：前端工作台。
2. Application API：页面聚合 API 与领域 API。
3. Domain Modules：素材、账户、数据、平台、动作、规则。
4. Shared Contracts：统一对象、证据对象、动作对象、学习对象。
5. Agent Harness：任务、上下文、工具权限、评估、审计。
6. Data Layer：原始数据、标准事实、领域存储、审计与学习。
7. Integration & Jobs：平台接入、内部系统接入、同步任务、AI 任务。

## Experience Layer

前端不是普通报表，而是投放工作流入口。

- 今日工作台：预算、风险、机会、待审批、数据质量、今日建议。
- 账户分析与诊断：全量账户层级数据、趋势、历史基线、规则命中、证据抽屉、agent 建议。
- 规则配置中心：规则定义、阈值、窗口、样本量、风险等级、启用状态、规则版本和变更日志。
- ActionIntent 审批：动作建议、目标对象、证据、风险、参数调整、审批/拒绝、拒绝原因。
- 素材增长中台：洞察、brief、素材库、标签、版本、表现、生成任务。
- 数据与 Harness 监控：同步、口径、归因质量、AgentTask、ContextPackage、ToolCallAudit。

前端不直接读取 token，不直接调用平台 SDK，不在页面里硬编码诊断逻辑。

## Application API

后端 API 给前端提供聚合后的页面数据，复杂计算放在服务层。

V0 页面 API：

- `GET /api/v0/workbench/today`
- `GET /api/v0/accounts/analysis`
- `GET /api/v0/rules`
- `POST /api/v0/rules/{id}/draft`
- `GET /api/v0/action-intents`
- `POST /api/v0/action-intents/{id}/decision`
- `GET /api/v0/creatives`
- `GET /api/v0/creative-briefs`
- `GET /api/v0/ops/health`
- `GET /api/v0/agent/tasks`

API 返回标准对象、证据包、规则版本和状态，不把平台原始字段直接暴露给前端作为业务契约。

## Domain Modules

`creative`：素材库、标签、版本、素材表现、brief、竞品洞察、生成任务。

`account`：账户树、账户诊断、规则命中、建议生成、ActionIntent 草稿。

`data`：统一模型、指标事实、指标口径、后链路事件、归因质量、数据同步状态。

`platform`：平台鉴权、字段映射、拉数、分页、限流、错误归一化、后续执行回写。

`rules`：RuleDefinition、RuleVersion、RuleHit、RuleChangeLog。

`action`：Recommendation、ActionIntent、ApprovalGate、ActionAudit、冷却时间、回滚占位。

## Shared Contracts

共享契约是 V0 最重要的协作产物。

- `Account`
- `Campaign`
- `AdGroup`
- `Ad`
- `CreativeAsset`
- `CreativeTag`
- `MetricFact`
- `BusinessEvent`
- `AttributionLink`
- `RuleDefinition`
- `RuleHit`
- `EvidenceObject`
- `Recommendation`
- `ActionIntent`
- `ActionAudit`
- `AgentTask`
- `ContextPackage`
- `ToolCallAudit`
- `LearningObject`

素材线、账户线、数据线可以并行开发，但不能各自定义一套对象。

## Agent Harness

Harness 负责把 agent 管在业务系统边界内。

- `AgentTask`：任务类型、输入、输出、状态、模型、耗时、失败原因、重试状态。
- `ContextPackage`：业务目标、对象层级、指标、规则、证据、素材、历史基线、归因质量、禁止动作。
- `ToolPermission`：只读、生成草稿、审批后执行、低风险自动化分级。
- `EvaluationResult`：检查输出是否结构化、是否引用证据、是否越权、是否缺少规则版本。
- `ToolCallAudit`：记录 agent 调用了什么工具、传入什么对象、返回什么状态。

V0 里 agent 只能做观察、解释、建议和草稿生成，不能直接执行真实投放动作。

## Data Layer

数据层分四区：

- Raw Zone：平台原始字段、导入批次、同步日志。
- Standard Facts：标准对象、MetricFact、BusinessEvent、AttributionLink。
- Domain Stores：Creative、Insight、Diagnosis、Recommendation、Action、Rule、Attribution。
- Audit & Learning：操作日志、AgentTask、ToolCallAudit、EvaluationResult、LearningObject、规则版本。

关键要求：

- 保留原始数据，方便追溯平台字段。
- 标准化层必须带 `metric_version`、`sync_batch`、时间窗口和来源。
- 指标口径由 `MetricDefinition` 管理，不能散落在页面或规则里。
- 真实运行数据库放在 `runtime/private/` 或部署环境私有存储，不能提交。

## Platform Adapters

平台接入层按平台拆分：

- `integrations/meta-ads/`：Meta/Facebook 主链路，第一阶段优先接入。
- `integrations/xiaohongshu/`：小红书/聚光后续接入。
- `integrations/tencent-ads/`：腾讯广告/广点通后续接入。

Adapter 只负责鉴权、同步、字段映射、错误归一化和执行接口封装；诊断、建议和审批逻辑不能写进 Adapter。

## Token 与授权

真实 token、refresh token、app secret、授权状态文件只能保存在 `config/private/` 或 `runtime/private/`。代码通过配置路径或环境变量读取，不把 secret 写进代码、文档、样例数据或提交历史。

V0 授权优先处理 Meta：

- token 文件路径配置化。
- refresh_token 生命周期可观测。
- 刷新失败进入数据与 Harness 监控页。
- 授权状态只作为系统健康和同步前置条件，不是核心产品页面。

## 设计边界

本仓库从智能投放系统的目标出发设计，不以任何既有广告预警工具、运行数据库、日志、二进制或本地回填状态作为产品结构来源。

平台经验只能进入 Adapter、数据同步、字段映射、授权监控和运维排查能力；不能反向决定首页、模块边界、命名体系或核心工作流。
