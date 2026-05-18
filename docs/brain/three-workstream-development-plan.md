# 三工作线 V0 分工开发计划

本文件是给团队进入 V0 分工开发使用的执行版本。它保留原始三条工作线，不把两位同事的实际人手情况改写成新的产品结构。

## V0 要验证什么

V0 先验证：

```text
投放优化师工作台 + 受控 agent 建议链路
```

V0 最小闭环是：

```text
数据同步 -> 规则命中 -> EvidenceObject -> ContextPackage -> agent 建议 -> Recommendation -> ActionIntent 草稿 -> 审批/拒绝 -> ActionAudit -> 复盘样本
```

V0 必须跑通：

- 用户能看到全量账户层级数据，而不是只看风险卡片。
- 诊断能引用规则版本、历史基线、样本量和证据对象。
- Agent 只能基于系统给定的 `ContextPackage` 输出建议。
- 建议能转成 `ActionIntent` 草稿。
- `ActionIntent` 可以审批或拒绝，但 V0 不直接执行真实投放动作。
- 每条建议能追溯到数据来源、时间窗口、指标口径、Agent 输入输出和工具日志。

## 三条工作线

| 工作线 | 分支 | 负责人 | V0 职责 | 第一阶段规格 |
| --- | --- | --- | --- | --- |
| 成员 A：素材增长中台 | `workstream/a-creative-growth` | 杨益 | 素材对象、素材标签、素材表现和素材复盘，给诊断链路提供“哪个素材表现怎样”。 | `docs/specs/002-creative-growth-loop/` |
| 成员 B：账户智能投放引擎 + Meta 广告数据 | `workstream/b-account-intelligence` | 思锐 | Meta API 只读接入、广告账户层级、广告指标、账户诊断、规则配置、Recommendation、ActionIntent、账户诊断 Agent 任务。 | `docs/specs/001-meta-readonly-sync/` + `docs/specs/003-account-intelligence-loop/` |
| 成员 C：内部业务系统 + 后链路归因 | `workstream/c-data-foundation` | 崔凯 | 公司内部业务系统只读接入、业务事件、归因关系、业务数据质量说明。 | `docs/specs/004-business-system-readonly-attribution/` |

这次调整后，数据来源被拆成两类：B 负责广告平台数据，C 负责公司内部业务后链路。两者都属于 MVP 输入，但不能互相替代。

## 成员 A：素材增长中台

### 目标

让素材不再是散落文件，而是能进入主线大脑的增长资产。A 线给 B 线提供“素材 ID、素材标签、素材状态、素材表现和复盘”，不负责广告平台 API、业务成交数据或最终诊断结论。

第一阶段链路：

```text
OpportunityCard -> ContextPackage -> MasterAsset -> PlatformVersion -> CreativeAsset -> PerformanceReport -> LearningObject 候选
```

### 第一阶段交付

- `data/sample/creative-opportunities.sample.json`
- `data/sample/creative-assets.sample.json`
- `data/sample/creative-performance.sample.json`
- creative sample validator 和 tests。
- 素材增长中台页面或 mock 数据入口。

### 不做

- 不接真实小红书、TikTok、YouTube 或 Google。
- 不做真实图片/视频生成。
- 不自动发布。
- 不改预算、不创建广告。

## 成员 B：账户智能投放引擎

### 目标

让投放优化师能看到 Meta 广告账户数据、广告指标、规则命中、证据对象、Agent 建议和 ActionIntent 草稿。B 线同时负责 Meta API 只读接入和账户智能诊断，但只消费 C 线提供的业务事件与归因结果，不实现内部业务系统。

第一阶段链路：

```text
Meta API / fixture
-> Account / Campaign / AdGroup / Ad / Creative
-> MetricFact
-> BusinessEvent / AttributionLink 引用
-> RuleDefinition / RuleHit
-> EvidenceObject
-> ContextPackage
-> Recommendation
-> ActionIntent
-> ActionAudit
```

### 第一阶段交付

- Meta hierarchy normalization。
- Meta scalar insights 和 `actions` 拆成原子 `MetricFact`。
- `accounts-tree`、`account-metrics`、`sync-status`、`metric-facts` 样例稳定。
- 账户分析与诊断页 mock 或 API 消费入口。
- 规则配置中心的样例规则和规则命中样例。
- `EvidenceObject`、`Recommendation`、`ActionIntent` 样例 payload。
- Agent 任务样例：只基于 `ContextPackage` 输出建议。
- 预留读取 C 线 `BusinessEvent` 和 `AttributionLink` 的接口依赖。

### 不做

- 不实现公司内部业务系统接入。
- 不伪造预约、到课、成交等后链路结果。
- 不执行真实投放动作。
- 不让 Agent 直接连数据库或平台 API 执行花钱动作。

## 成员 C：内部业务系统与后链路归因

### 目标

让公司内部业务系统的数据以只读方式进入统一对象，并让 B 线能知道广告带来的有效线索、预约、到课、成交、退款等后链路结果是否能可靠归因。

第一阶段链路：

```text
Internal business system readonly
-> BusinessEvent
-> AttributionLink
-> Business data quality note
-> B 线诊断输入
```

### 第一阶段交付

- 内部业务系统只读接口调研和字段映射。
- `BusinessEvent` 样例：有效线索、预约、到课、成交、退款等。
- `AttributionLink` 样例：业务事件如何回到 account / campaign / ad_group / ad / creative。
- 业务数据质量说明：哪些能确认、哪些不能确认、哪些只能弱归因。
- 数据与 Harness 监控页需要的业务系统同步状态和警告。

### 不做

- 不接 Meta 广告 API。
- 不做广告指标同步。
- 不生成 Recommendation。
- 不生成 ActionIntent。
- 不写回内部业务系统。

## 集成顺序

### 第 1 轮：共享契约和样例

- B 线稳定 Meta sample 和 validator。
- A 线补 creative sample 和 validator。
- C 线补 business event / attribution sample 和接口说明。
- B 线基于广告指标、素材表现和业务事件定义 RuleHit、EvidenceObject、Recommendation、ActionIntent 的 mock 契约。

验收：

```bash
.venv/bin/python scripts/validate_api_contracts.py
.venv/bin/python -m unittest discover -s tests
```

### 第 2 轮：页面和任务入口

- A 线让素材增长中台能读取 creative sample。
- B 线让账户/数据监控页能读取 Meta sample 或 normalization output，并让账户分析、规则配置、ActionIntent 页面能读取 mock 契约。
- C 线让数据与 Harness 监控页能展示内部业务系统同步状态和归因质量。

### 第 3 轮：V0 主链路串联

把三条线接成：

```text
CreativeAsset + MetricFact
-> BusinessEvent / AttributionLink
-> RuleHit
-> EvidenceObject
-> ContextPackage
-> Recommendation
-> ActionIntent
-> ActionAudit
```

这一轮只做可审批草稿和复盘样本，不做真实执行。

## 分支与合并

1. 每个人从自己的 `workstream/*` 分支开发。
2. 工作线内部可以拆 `feature/<short-task>`。
3. 小任务先合回自己的 `workstream/*`。
4. 三条工作线阶段性交付后合回 `dev` 做集成验证。
5. `dev` 验证稳定后合并到 `main`。

## 每日同步格式

每条工作线每天同步：

```text
昨天完成：
今天计划：
依赖别人：
阻塞点：
是否影响契约：
```

只要“是否影响契约”为是，就必须先同步 `docs/api-contracts.md`、`docs/data-model.md`、sample、validator 和 tests。

## 第一阶段完成定义

第一阶段完成不是“所有页面都完美”，而是：

- A 线有素材对象和素材表现样例。
- B 线有 Meta 对象、MetricFact、规则命中、证据、建议、ActionIntent 样例。
- C 线有业务事件、归因关系和业务数据质量样例。
- 三条线都通过 validator 和 tests。
- V0 最小闭环可以用样例从数据同步走到审批/拒绝和复盘样本。
