# 平台 API 同步对齐

## 目标

第一阶段以 Meta/Facebook 为主线，同时把小红书聚光的对象和报表口径拉齐到同一套系统模型。这样后续账户诊断、EvidenceObject、Recommendation 和 ActionIntent 不需要为每个平台各写一套业务逻辑。

本文件只定义同步对齐口径，不代表 V0 要同时深度开发两个平台。V0 的主同步链路是 Meta；小红书用于校准多平台抽象，后续按同一模型接入。

## 统一同步层

平台 API 不直接进入诊断引擎，必须经过三层：

1. Raw Zone：保存平台原始对象和原始报表响应。
2. FieldMapping：把平台字段转为系统统一对象。
3. Standard Facts：写入 `AdAccount`、`Campaign`、`AdGroup`、`Ad`、`CreativeAsset`、`MetricFact`、`BusinessEvent`、`AttributionLink`。

所有进入诊断的指标必须带：

- `platform`
- `platform_object_type`
- `external_object_id`
- `metric_name`
- `metric_value`
- `date`
- `time_window`
- `metric_version`
- `sync_batch`
- `raw_metric_name`
- `dimensions`
- `attribution_window`
- `source_quality`

## 对象层级对齐

| 系统对象 | Meta/Facebook | 小红书聚光 | 说明 |
| --- | --- | --- | --- |
| `AdAccount` | Ad Account (`act_*`) | Advertiser (`advertiser_id`) | 广告账户或广告主。 |
| `Campaign` | Campaign | Campaign / 计划 | 投放目标、预算层级、状态和时间周期。 |
| `AdGroup` | Ad Set | Unit / 单元 | 投放控制层，承载定向、出价、优化目标、预算和归因设置。 |
| `Ad` | Ad | 可由 Creativity / Note / Keyword 场景派生 | Meta 有明确 Ad 层；聚光重点是创意、关键词和单元表现。 |
| `CreativeAsset` | Ad Creative | Creativity / 创意 / Note | 素材、文案、媒体、链接、组件、审核状态。 |
| `MetricFact` | Insights | Realtime Report / Offline Report / DataReportDTO | 统一指标事实表。 |
| `BusinessEvent` | Lead / Pixel / Conversion / Offline Event | Leads / ValidLeads / Message / ExternalLeads / 回传事件 | 后链路事件。 |
| `AttributionLink` | attribution_setting / action attribution windows | 7日/24小时/回传口径字段 | 归因窗口和事件来源解释。 |

## Meta 同步口径

### 对象同步

Meta 第一阶段按以下顺序同步：

1. Ad Account
2. Campaign
3. Ad Set
4. Ad
5. Ad Creative
6. Insights

字段映射：

| Meta 字段 | 系统字段 |
| --- | --- |
| `account_id` / `id` | `AdAccount.external_account_id` |
| `name` | `AdAccount.account_name` / `Campaign.name` / `AdGroup.name` / `Ad.name` |
| `currency` | `AdAccount.currency` |
| `timezone_name` | `AdAccount.timezone` |
| `account_status` | `AdAccount.status` |
| `campaign.id` | `Campaign.external_campaign_id` |
| `campaign.objective` | `Campaign.objective` |
| `campaign.status` / `effective_status` | `Campaign.status` |
| `daily_budget` / `lifetime_budget` | `Campaign.budget_amount` or `AdGroup.budget_amount` |
| `adset.id` | `AdGroup.external_ad_group_id` |
| `adset.optimization_goal` | `AdGroup.optimization_goal` |
| `adset.billing_event` | `AdGroup.billing_event` |
| `adset.bid_strategy` | `AdGroup.bid_strategy` |
| `adset.targeting` | `AdGroup.targeting_summary` and raw targeting dimensions |
| `adset.attribution_spec` / `attribution_setting` | `AttributionLink.attribution_window` or metric dimensions |
| `ad.id` | `Ad.external_ad_id` |
| `ad.creative.id` | `Ad.creative_id` / `CreativeAsset.external_creative_id` |
| `creative.object_story_spec` / media fields | `CreativeAsset.copy` / `CreativeAsset.media_uri` / raw creative payload |

### Insights 到 MetricFact

Meta Insights 建议先拉三个层级：

- `level=campaign`
- `level=adset`
- `level=ad`

第一阶段指标：

| Meta Insights 字段 | 统一 `metric_name` | 备注 |
| --- | --- | --- |
| `spend` | `spend` | 统一金额单位，记录币种。 |
| `impressions` | `impressions` | 曝光。 |
| `reach` | `reach` | 去重触达。 |
| `frequency` | `frequency` | 频次。 |
| `clicks` | `clicks` | 点击。 |
| `inline_link_clicks` | `link_clicks` | 链接点击优先用于落地页/表单链路。 |
| `ctr` | `ctr` | 点击率，保留 Meta 原始口径。 |
| `cpc` | `cpc` | 平均点击成本。 |
| `cpm` | `cpm` | 千次曝光成本。 |
| `actions[action_type=lead]` | `leads` | Lead Ads 或转化事件。 |
| `cost_per_action_type[action_type=lead]` | `leads_cpl` | 表单/线索成本。 |
| `actions[*]` | `platform_action_count` | 保留 `action_type` 到 dimensions。 |
| `cost_per_action_type[*]` | `platform_action_cost` | 保留 `action_type` 到 dimensions。 |
| `conversion_values` | `conversion_value` | 如果账户已配置价值回传。 |
| `purchase_roas` | `roas` | 有购买或价值回传时使用。 |

Meta 的 `actions` 必须拆成多行 `MetricFact`，不能只保留一个总转化。`dimensions.action_type` 保存 Meta 原始 action type，`raw_metric_name` 保存 `actions` 或 `cost_per_action_type`。

## 小红书聚光同步口径

### 对象同步

小红书聚光接入需要覆盖以下平台对象：

| 聚光对象 | 系统对象 | 关键字段 |
| --- | --- | --- |
| Advertiser | `AdAccount` | `advertiser_id` |
| Campaign / 计划 | `Campaign` | `campaign_id`、`campaign_name`、`marketing_target`、`optimize_target`、`promotion_target`、`campaign_enabled`、`campaign_filter_state`、`origin_campaign_day_budget` |
| Unit / 单元 | `AdGroup` | `unit_id`、`unit_name`、`campaign_id`、`unit_enable`、`event_bid` |
| Creativity / 创意 | `CreativeAsset` and optional `Ad` | `creativity_id`、`creativity_name`、`note_id`、`image`、`jump_url`、`audit_status`、`conversion_type`、`material_type` |
| Keyword / 关键词 | `MetricFact` dimension or search targeting object | `keyword_id`、`keyword`、`unit_id`、`campaign_id`、`keyword_filter_state` |
| TargetSnapshot | `AdGroup.targeting_summary` / dimensions | `target_type`、`target_gender`、`target_age`、`target_city`、`keywords`、`interest_keywords`、`crowd_package_names` |

### 报表到 MetricFact

聚光的 `DataReportDTO` 字段需要转成统一指标：

| 聚光字段 | 统一 `metric_name` | 备注 |
| --- | --- | --- |
| `fee` | `spend` | 推广消费金额。 |
| `impression` | `impressions` | 推广展现量。 |
| `click` | `clicks` | 推广点击量。 |
| `ctr` | `ctr` | 聚光点击率原始口径。 |
| `acp` | `cpc` | 平均点击成本。 |
| `cpm` | `cpm` | 千次曝光成本。 |
| `leads` | `leads` | 表单提交。 |
| `leads_cpl` | `leads_cpl` | 表单成本。 |
| `valid_leads` | `valid_leads` | 有效表单。 |
| `valid_leads_cpl` | `valid_leads_cpl` | 有效表单成本。 |
| `leads_cvr` | `leads_cvr` | 表单转化率。 |
| `message_consult` | `message_consult` | 私信咨询数。 |
| `message_consult_cpl` | `message_consult_cpl` | 私信咨询成本。 |
| `msg_leads_num` | `message_leads` | 私信留资数。 |
| `msg_leads_cost` | `message_leads_cost` | 私信留资成本。 |
| `external_leads` | `external_leads` | 外链回传转化。 |
| `external_leads_cpl` | `external_leads_cpl` | 外链转化成本。 |
| `action_button_click` | `action_button_clicks` | 行动按钮点击。 |
| `action_button_ctr` | `action_button_ctr` | 行动按钮点击率。 |
| `roi` / `purchase_order_roi_7d` / `external_roi_*` | `roi` | 必须保留 raw metric 和归因窗口。 |

聚光离线报表支持 campaign、unit、creative、keyword 层级；实时报表支持 campaign、unit、creativity、keyword。系统统一写入 `MetricFact.object_type`：

- `campaign`
- `ad_group`
- `creative`
- `keyword`

其中 `keyword` 暂不提升为核心实体，先作为搜索投放维度和诊断维度使用。

## Meta 与小红书的关键差异

| 差异 | Meta | 小红书聚光 | 系统处理 |
| --- | --- | --- | --- |
| 投放控制层名称 | Ad Set | Unit / 单元 | 都写入 `AdGroup`，保留 `platform_object_type`。 |
| 创意与广告关系 | Ad 引用 Ad Creative | Creativity 更接近素材/投放创意，另有 Note | `Ad` 与 `CreativeAsset` 分开，聚光可以先弱化 Ad。 |
| 转化指标表达 | `actions` / `cost_per_action_type` 数组 | `DataReportDTO` 多个具名字段 | 都拆成多行 `MetricFact`，保留 raw metric/action type。 |
| 归因窗口 | attribution setting / action attribution windows | 字段名常含 7d/24h/30d 或回传说明 | 写入 `attribution_window` 和 `dimensions`。 |
| 定向 | Ad Set targeting | Unit target config / TargetSnapshot | 写入 `AdGroup.targeting_summary` 和 raw targeting。 |
| 搜索关键词 | 通常通过 breakdown/placement 或命名间接分析 | Keyword 层级报表明确存在 | `keyword` 作为 MetricFact 维度和诊断层。 |
| 审核状态 | Ad / Creative effective status | creativity audit/filter state | 统一进 `review_status`、`status` 和 raw status。 |

## V0 同步顺序

### 成员 C：数据与内部系统底座

1. 建立 `platform_sync_jobs` 和 `raw_platform_objects`。
2. 先实现 Meta read-only sync：AdAccount、Campaign、AdSet、Ad、Creative、Insights。
3. 按本文件实现 Meta FieldMapping。
4. 用小红书聚光字段做对照测试，确认 `Campaign`、`AdGroup`、`CreativeAsset`、`MetricFact` 没有被 Meta 特化。
5. 输出 `MetricDefinition` 初版，标注 Meta 与小红书各自 raw metric。

### 成员 B：账户智能投放引擎

1. 诊断规则只依赖统一 `MetricFact` 和 `EvidenceObject`。
2. 第一批规则基于 `spend`、`impressions`、`clicks`、`ctr`、`cpc`、`cpm`、`leads`、`leads_cpl`。
3. 所有规则命中必须记录 `platform`、`object_type`、`object_id`、`metric_version` 和 `source_quality`。

### 成员 A：素材增长中台

1. Meta Creative 和小红书 Creativity 都进入 `CreativeAsset`。
2. 素材表现不直接读平台字段，而是通过 `MetricFact.object_type=creative` 或 `Ad` 关联统计。
3. 素材标签独立于平台字段，平台字段只作为标签生成线索。

## 不能做的对齐

- 不把 Meta `Ad Set` 翻译成系统里的 `Campaign`。
- 不把小红书 `Unit` 当作独立平台特例散落在诊断代码里。
- 不把 Meta `actions` 压成一个总转化。
- 不把小红书 `DataReportDTO` 简化为 `fee/leads/click/impression/ctr` 等少数字段。
- 不把关键词、placement、action type、归因窗口这些差异丢掉。
