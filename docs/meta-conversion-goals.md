# Meta 转化目标体系公开版

本文件说明系统如何处理 Meta 转化目标，不记录真实账户 ID、真实账户名称、真实 Ad Set 数量、真实命名信号或真实后台截图。

## 人话说明

Meta 后台里的 action 名称不一定等于业务最终结果。系统需要先保留平台原始字段，再映射成自己的诊断目标。这样团队看到一条建议时，能知道它来自哪个平台指标，也能知道系统把它解释成什么业务含义。

## 系统目标类型

第一阶段保留五类目标：

| 目标类型 | 业务含义 | 系统用途 |
| --- | --- | --- |
| `quality_lead` | 质量线索或高意向线索 | 判断线索质量方向的广告效果 |
| `lead_form` | 表单线索 | 判断传统表单获客效率 |
| `h5_booking` | 站外页面或预约链路线索 | 判断落地页和站外转化链路 |
| `messaging` | 私信或聊天承接 | 判断对话链路是否有效 |
| `engagement` | 内容互动 | 判断素材和内容信号 |

## 平台字段处理原则

- `optimization_goal` 用来判断广告对象的主要目标。
- `actions.action_type` 必须原样写入 `MetricFact.dimensions.action_type`。
- 系统指标只做诊断聚合，不能覆盖平台原始字段。
- 同一个平台 action 可能在不同账户里有不同业务解释，需要由私有配置或人工校准确认。
- 公开仓库只保留映射框架，不保留真实账户分布和真实 action 统计。

## 示例映射

| 平台字段 | 系统目标类型 | 系统指标 |
| --- | --- | --- |
| `QUALITY_LEAD` | `quality_lead` | `quality_lead` |
| `LEAD_GENERATION` | `lead_form` | `leads` |
| `OFFSITE_CONVERSIONS` | `h5_booking` | `landing_page_view` / `h5_lead` |
| messaging action type | `messaging` | `messaging_started` |
| engagement action type | `engagement` | `post_engagement` |

## 待私有确认

以下内容不写入公开仓库：

- 真实账户里各目标类型的数量分布。
- 真实广告命名规则。
- 真实自定义事件名称。
- 真实业务系统字段名。
- 真实阈值、基线、预算和可接受成本区间。

这些信息可以放在私有配置或团队内部文档中，公开仓库只保留抽象后的接口和规则框架。
