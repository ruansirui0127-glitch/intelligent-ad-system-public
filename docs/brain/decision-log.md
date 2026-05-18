# 决策记录

本文件记录影响主线大脑的关键决策。新增决策时使用追加方式，不删除历史记录；如果决策被替换，新增一条 supersedes 记录。

## 记录模板

```markdown
## DEC-YYYYMMDD-NNN - 标题

**日期**：YYYY-MM-DD
**状态**：accepted | superseded | proposed
**决策人**：姓名或团队
**影响范围**：docs | data-model | api | creative | account | action | harness | integration

### 结论
一句话说明采用什么判断。

### 原因
- 原因 1
- 原因 2

### 吸收
- 会纳入主线的内容。

### 不吸收
- 明确拒绝或暂缓的内容。

### 后续动作
- 要更新的文件或要确认的问题。
```

## DEC-20260515-001 - 主线仓库归属

**日期**：2026-05-15
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：docs, integration, architecture

### 结论

`intelligent-ad-system` 是智能投放系统唯一主线仓库和系统主脑。

### 原因

- 它已经承载产品愿景、架构、数据模型、Meta 第一阶段主线、ActionIntent、Agent Harness 和集成计划。
- 它符合当前项目定位：智能投放操作系统，而不是单点素材生成工具或 Agent 技能实验。
- 它有敏感配置边界、工作线分工和统一对象契约。

### 吸收

- 吸收素材增长规划中的机会、母版、平台版本、素材资产、投放准备和素材学习对象。
- 吸收 Agent 技能编排中的深挖、收敛、质检和确认门方法。

### 不吸收

- 不让任何外部仓库或素材规划反向覆盖主仓产品结构。
- 不把外部 skill 编排直接作为业务数据模型。

### 后续动作

- 维护 `docs/brain/` 作为统一决策入口。
- 后续对象变更先更新 `object-glossary.md`，再进入数据模型和 API 契约。

## DEC-20260515-002 - 素材增长规划融合方式

**日期**：2026-05-15
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：creative, data-model, docs, learning

### 结论

素材同事的广告素材自动化规划作为素材增长脑并入主线，不独立成为第二套产品系统。

### 原因

- 素材规划补足了主仓当前较弱的上游链路：机会卡、公司知识包、母版、平台版本、素材入库、投放计划和复盘学习。
- 主仓已经要求把素材变成可学习资产，素材规划正好提供对象流和工作流。
- 如果独立成系统，会造成导航、对象、数据和学习闭环重复。

### 吸收

- `OpportunityCard`
- `MasterAsset`
- `PlatformVersion`
- `LaunchPlan`
- `AdGroupDraft`
- `PerformanceReport`
- `LearningItem` / `RuleUpdate`
- 素材洞察、脚本生成、图片生成、视频生成、素材管理、投放复盘 6 条工作流。

### 不吸收

- 不直接迁移素材包的一级导航。
- 不把小红书、TikTok、YouTube 作为 V0 平台主线。
- 不把内容生成质量作为 V0 第一验收标准。

### 后续动作

- 将候选对象补充到 `docs/data-model.md` 前，先确认字段、状态机和 API wire shape。
- 将素材工作流改写成 creative 模块的开发规格，而不是独立项目 README。

## DEC-20260515-003 - Agent 决策方法融合方式

**日期**：2026-05-15
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：harness, docs, rules

### 结论

`agentic-skill-orchestration` 作为 Agent 决策方法脑使用，只吸收工作方法，不作为业务主线。

### 原因

- 它适合约束 Codex/Agent 的思考流程：先深挖、再收敛、再质检、再确认。
- 它没有广告对象、Meta 数据、审批、审计或投放业务模型。
- 直接作为主线会把项目变成技能系统，而不是智能投放系统。

### 吸收

- Outcome gate：重大范围、平台、架构和自动化决策前确认价值与边界。
- Quality gate：检查 Agent 输出是否引用证据、是否越权、是否缺规则版本。
- Hook 思想：辅助分析只能提供有边界输入，不能替代主任务闭环。

### 不吸收

- 不把外部 skill 名称写入业务对象。
- 不让 Agent 互相调用绕过人工审批。
- 不让技能编排决定数据模型和产品导航。

### 后续动作

- 在 Agent Harness 设计中加入任务类型、权限等级、评估结果和人工确认门。
- 对高风险自动化保持人工审批。

## DEC-20260515-004 - V0 平台优先级

**日期**：2026-05-15
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：integration, platform, creative, data

### 结论

V0 继续以 Meta 作为广告数据和投放诊断主线；其他平台先作为对象和字段扩展预留。

### 原因

- 主仓规划和当前接入工作已经围绕 Meta 只读同步、指标拆分和多目标转化口径展开。
- 素材规划提到全平台内容能力，但这属于长期方向，不应打断 V0 数据闭环。
- 多平台抽象需要建立在 Meta 主链路跑通之后，否则容易陷入泛化过早。

### 吸收

- 在 `PlatformVersion`、`CreativeAsset` 和 `MetricFact.dimensions` 中预留多平台字段。
- 保留小红书、TikTok、Google、YouTube 的平台适配思路。

### 不吸收

- V0 不做全平台深度 API 接入。
- V0 不做自动发布或真钱投放。

### 后续动作

- Meta 同步、MetricFact、EvidenceObject 和 ActionIntent 优先。
- 素材多平台版本先用样例和字段预留验证。

## DEC-20260515-005 - 素材增长对象进入可开发契约

**日期**：2026-05-15
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：docs, data-model, api, creative

### 结论

素材增长脑中的候选对象先以增量方式进入 `docs/data-model.md` 和 `docs/api-contracts.md`，作为 V0 可选样例和后续开发契约，不强制当前 Meta 样例立刻全量实现。

### 原因

- 团队需要统一对象语言，不能让素材链路只停留在独立规划文档。
- 当前 Meta 数据底座仍是优先级最高的开发主线，素材对象应先以低风险方式接入。
- 只做加法可以避免破坏现有 `accounts-tree`、`account-metrics`、`sync-status` 和 `metric-facts` 样例校验。

### 吸收

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

### 不吸收

- 不把这些对象立刻设为所有接口必填。
- 不修改当前 Meta mock validator 的必填规则。
- 不把领域对象 ID 伪装成平台对象 ID。

### 后续动作

- 后续开发 creative 模块时，为 `GET /api/v0/creatives/opportunities` 和 `GET /api/v0/creatives` 增加脱敏样例 payload。
- 若这些样例进入 `data/sample/`，同步扩展 `scripts/validate_api_contracts.py` 和对应测试。

## DEC-20260515-006 - 两位同事采用 2+1 分工推进

**日期**：2026-05-15
**状态**：superseded
**决策人**：项目负责人 + Codex
**影响范围**：integration, docs, creative, data

### 结论

该决策已被 `DEC-20260515-007` 替代。原意是为了适配“两位同事”的实际人手，但容易误导为 V0 只剩两条工作线，因此废止。

### 原因

- 当前团队实际可推进的是两位同事，不适合同时打开三条完整工作线。
- 素材增长和 Meta 数据底座可以并行，且都能通过 sample 和 validator 独立验收。
- 账户诊断、Recommendation 和 ActionIntent 依赖数据底座稳定，不应先做结论层。

### 吸收

- 同事 A 使用 `docs/specs/002-creative-growth-loop/`。
- 同事 B 使用 `docs/specs/001-meta-readonly-sync/`。
- 团队使用 `docs/brain/two-colleague-development-plan.md` 作为分工入口。

### 不吸收

- 不要求两位同事同时承担三条完整工作线。
- 不在第一阶段做真实投放、自动发布或多平台深度同步。
- 不让账户诊断在 MetricFact 稳定前生成正式建议。

### 后续动作

- 使用 `docs/brain/three-workstream-development-plan.md` 作为新的分工入口。

## DEC-20260515-007 - V0 保持三工作线分工

**日期**：2026-05-15
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：integration, docs, creative, account, data

### 结论

V0 继续保持三条工作线：成员 A 负责素材增长中台，成员 B 负责账户智能投放引擎，成员 C 负责数据与内部系统底座。该决策的“三条工作线必须保留”仍然有效，但 B/C 具体数据边界已由 `DEC-20260517-008` 细化和替代。

### 原因

- 原始 V0 要验证的是「投放优化师工作台 + 受控 Agent 建议链路」，必须包含账户智能和 ActionIntent，不只是素材 + 数据。
- 账户诊断、规则命中、EvidenceObject、Recommendation 和 ActionIntent 是独立工作线，不能被数据底座吞掉。
- 三条工作线已经写入 `docs/integration-plan.md`，也是团队分支和集成顺序的基础。

### 吸收

- 成员 A 使用 `docs/specs/002-creative-growth-loop/`。
- 成员 B 使用 `docs/specs/001-meta-readonly-sync/` 和 `docs/specs/003-account-intelligence-loop/`。
- 成员 C 使用 `docs/specs/004-business-system-readonly-attribution/`。
- 团队使用 `docs/brain/three-workstream-development-plan.md` 作为分工入口。

### 不吸收

- 不再使用 `2+1` 作为产品分工口径。
- 不把账户智能投放引擎暂缓到 V0 之后。
- 不让 B 线在 C 线业务事件和归因质量不稳定前输出后链路确定性结论。

### 后续动作

- 三条工作线分别从对应 `workstream/*` 分支推进。
- 每次改契约必须同步 `docs/api-contracts.md`、sample、validator 和 tests。

## DEC-20260517-008 - B/C 数据边界调整

**日期**：2026-05-17
**状态**：accepted
**决策人**：项目负责人 + Codex
**影响范围**：integration, docs, account, data, attribution

### 结论

三条工作线保持不变，但 B/C 的数据边界调整：思锐负责账户智能投放引擎和 Meta API 广告平台数据接入；崔凯负责公司内部业务系统只读接入、业务事件和归因关系；杨益继续负责素材增长中台。最终口径、对象模型、接口契约和集成验收由项目负责人 + Codex 统一把关。

### 原因

- MVP 需要同时看广告前链路和业务后链路，二者来源不同，不能都塞进一个“数据底座”。
- Meta API、广告层级和广告指标更贴近账户智能诊断，适合由 B 线一起处理。
- 内部业务系统涉及有效线索、预约、到课、成交和归因质量，适合由 C 线独立接入并输出给 B 消费。

### 吸收

- 成员 A 使用 `docs/specs/002-creative-growth-loop/`。
- 成员 B 使用 `docs/specs/001-meta-readonly-sync/` 和 `docs/specs/003-account-intelligence-loop/`。
- 成员 C 使用 `docs/specs/004-business-system-readonly-attribution/`。
- B 线生成建议时必须引用广告侧指标、素材侧信息、业务后链路结果和数据质量说明。

### 不吸收

- 不让 C 线负责 Meta 广告 API 或投放建议。
- 不让 B 线实现内部业务系统接入。
- 不让 A 线承担业务成交数据或诊断结论。
- 不把多平台深度接入放进 MVP；MVP 广告平台只做 Meta。

### 后续动作

- 更新 `docs/brain/three-workstream-development-plan.md` 和 `docs/integration-plan.md`。
- 更新项目大脑 skill 的工作线边界。
- 为 C 线新增内部业务系统只读与归因规格。
