# 项目基础口径

## 核心判断

本仓库是「智能投放系统」的全新主仓库，不以任何既有广告工具、预警工具或本地诊断脚本作为产品底座。

`docs/planning/` 中的材料只作为产品方向、业务约束和工程拆解输入。进入本仓库后，所有思路都要被重新整理为当前系统的统一对象、平台接入、诊断证据、ActionIntent 审批和复盘学习能力。

## 规划输入

当前规划输入集中在 `docs/planning/`：

| 文件 | 对当前项目的作用 |
| --- | --- |
| `智能投放系统需求清单-小红书深挖填写版.docx` | 小红书深挖需求输入 |
| `full-stack-intelligent-ad-system-prd.html` | 全系统产品蓝图，定义智能投放操作系统、全链路闭环、产品原则和长期模块 |
| `full-stack-intelligent-ad-system-engineering-prd.html` | 工程交接 PRD，定义问题、用户、架构、模块边界、验收和风险 |
| `intelligent-ad-system-module-tech-map.html` | 模块与技术图谱，定义三条业务线、系统驱动 agentic 架构、数据闭环和学习闭环 |
| `intelligent-ad-system-v0-development-breakdown.html` | V0 可开发拆解，定义核心页面、API、Agent Harness、数据对象和里程碑 |
| `intelligent-ad-system-v0-product-prototype.html` | V0 产品原型，定义页面地图、核心工作流和验收标准 |
| `business-profile.md` | 业务画像，定义海外华人少儿数学直播课、地区、转化路径、竞品和默认诊断口径 |

这些材料不代表必须保留其原始实现假设。凡是与当前主仓库目标冲突的历史表达，都应融合改写为全新系统口径。

## 当前主线

系统围绕以下主线建设：

- 系统定位：智能投放操作系统，而不是单点广告预警工具。
- 架构原则：系统驱动 agentic workflows，业务系统保管事实、权限、审批、日志和学习结果。
- V0 闭环：数据同步、规则命中、证据对象、ContextPackage、Recommendation、ActionIntent 审批、复盘学习。
- 三条业务线：素材增长中台、账户智能投放引擎、数据与内部系统底座。
- 第一阶段平台：Meta/Facebook。
- 扩展平台：Google、抖音、广点通/腾讯广告、小红书。
- 业务校准：从 CPL 逐步升级到有效线索、约课、到课、成交、ROI/LTV。

## 平台经验的使用方式

平台侧已有经验只能作为设计输入，不能决定当前项目的产品结构、目录结构、首页逻辑或技术路线。

可吸收的内容包括：

- 平台鉴权和 token 生命周期的运维要求。
- 平台 SDK/API 的对象、分页、限流和错误处理经验。
- 广告对象层级、报表字段、指标口径和归因窗口差异。
- 本地开发、同步任务、健康检查和故障排查经验。

进入当前项目时，这些内容必须被重新表达为：

- `integrations/<platform>/` 的 Adapter 能力。
- Raw Zone、FieldMapping、Standard Facts 和 MetricDefinition。
- 数据与 Harness 监控页的同步状态、授权状态和质量提示。
- ActionIntent、ToolCallAudit、ActionAudit 的审批与审计边界。

## 私有配置边界

真实 token、refresh token、app secret、授权状态文件、运行数据库、日志和真实业务数据只能放在 `.gitignore` 排除的私有目录，例如：

- `config/private/`
- `runtime/private/`

对外只提交 `config/examples/` 下的模板。文档、样例数据、最终回复和提交记录中都不能打印真实 token 或真实广告数据。

## 文档更新原则

后续核心文档先参考 `docs/planning/` 的产品方向，再沉淀到 `docs/` 的当前执行口径。`docs/` 要表达当前主仓库的设计，而不是记录来源、搬运过程或历史项目结构。
