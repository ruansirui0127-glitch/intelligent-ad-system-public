# 数据模型

## 设计目标

数据模型要支撑三件事：

1. 多平台广告对象统一浏览。
2. 诊断、建议和 ActionIntent 能引用清晰证据。
3. 后链路归因和历史学习能逐步接入。

V0 先服务 Meta 平台，但模型不能写死为 Meta 单平台。

## 核心对象

### MarketSignal

市场、平台、竞品或历史表现中出现的原始机会信号。

关键字段：`signal_id`、`source_type`、`source_uri`、`market_region`、`platform`、`topic`、`audience`、`pain_point`、`evidence_summary`、`captured_at`、`source_quality`。

信号可以来自人工录入、公开内容观察、竞品素材、平台趋势或历史投放复盘。V0 可以先用手工样例，不要求自动扫描。

### OpportunityCard

把一个或多个 `MarketSignal` 聚合成可执行的素材或投放机会。

关键字段：`opportunity_id`、`title`、`market_region`、`recommended_platforms`、`target_audience`、`pain_point`、`angle`、`reason_to_try`、`evidence_refs`、`risk_notes`、`recommended_asset_formats`、`priority_score`、`status`、`created_by`、`created_at`。

`OpportunityCard` 是素材增长脑进入主线大脑的入口。它不等于投放建议，也不能直接触发真钱投放；后续必须经过素材生成、证据诊断和 ActionIntent 审批。

### Platform

平台来源。

关键字段：`platform_id`、`platform_code`、`name`、`status`、`capabilities`、`created_at`、`updated_at`。

示例平台：`meta`、`google`、`douyin`、`tencent_ads`、`xiaohongshu`。

### AdAccount

广告账户。

关键字段：`account_id`、`platform`、`external_account_id`、`account_name`、`currency`、`timezone`、`market_region`、`status`。

### Campaign

广告计划。

关键字段：`campaign_id`、`platform`、`external_campaign_id`、`account_id`、`name`、`objective`、`market_region`、`budget_type`、`budget_amount`、`status`、`started_at`、`ended_at`。

### AdGroup

广告单元或广告组。不同平台叫法不同，统一抽象为投放控制层。

关键字段：`ad_group_id`、`platform`、`external_ad_group_id`、`campaign_id`、`name`、`targeting_summary`、`bid_strategy`、`budget_amount`、`status`。

Meta 第一阶段对应 `Ad Set`；小红书聚光后续对应 `Unit / 单元`。必须保留 `platform_object_type`，避免把平台层级差异写进诊断逻辑。

### Ad

具体广告或投放对象。

关键字段：`ad_id`、`platform`、`external_ad_id`、`ad_group_id`、`creative_id`、`name`、`status`、`review_status`。

### CreativeAsset

素材资产。

关键字段：`creative_id`、`source`、`asset_type`、`title`、`copy`、`media_uri`、`owner`、`market_region`、`persona`、`pain_point`、`selling_point`、`format`、`version_of`、`approval_status`、`servable_status`、`opportunity_id`、`master_asset_id`、`platform_version_id`、`lineage_refs`、`reuse_score`、`performance_summary`。

`asset_type` 可以是 `copy`、`image`、`video`、`script`、`brief`、`edit_instruction`、`landing_page_snippet`。V0 不要求真实媒体文件入库，但所有素材样例必须能追溯来源机会、母版和平台版本。

### CreativeTag

素材标签。

关键字段：`tag_id`、`creative_id`、`tag_type`、`tag_value`、`confidence`、`source`。

标签类型建议包括：地区、人群、年龄段、痛点、卖点、创意形式、课程承诺、信任背书、竞品关联、素材生命周期。

### BrandRule

品牌、业务和合规口径规则。

关键字段：`brand_rule_id`、`rule_type`、`market_region`、`platform`、`rule_text`、`examples`、`risk_level`、`source`、`status`、`version`、`approved_by`。

`BrandRule` 可作为 `ContextPackage` 的一部分进入 Agent 输入，避免素材生成出现空泛承诺、夸大效果或不符合品牌语气。

### PlatformRule

平台内容和广告适配规则。

关键字段：`platform_rule_id`、`platform`、`content_format`、`placement`、`specs`、`policy_notes`、`cta_rules`、`tracking_requirements`、`status`、`version`。

V0 以 Meta 规则为主，其他平台先作为 `PlatformVersion` 的适配字段预留。

### MasterAsset

素材母版，表示一个机会和上下文生成出的跨平台核心素材策略。

关键字段：`master_asset_id`、`opportunity_id`、`context_package_id`、`title`、`core_claim`、`proof_points`、`pain_point`、`selling_point`、`cta`、`risk_notes`、`brand_rule_refs`、`status`、`created_by`、`created_at`。

`MasterAsset` 不直接发布或投放。它用于派生多个平台版本，并保留引用的公司证据和风险边界。

### PlatformVersion

素材母版在特定平台、市场和素材形态下的派生版本。

关键字段：`platform_version_id`、`master_asset_id`、`platform`、`market_region`、`asset_format`、`placement`、`copy_variant_ids`、`creative_asset_ids`、`platform_rule_refs`、`adaptation_reason`、`cta`、`risk_level`、`status`。

同一个 `MasterAsset` 可以生成多个 `PlatformVersion`。平台差异必须写在版本对象里，不能让前端或 Agent 隐式猜测。

### MetricDefinition

指标口径。

关键字段：`metric_name`、`display_name`、`definition`、`formula`、`unit`、`window`、`platform_support`、`owner`、`status`、`metric_version`。

第一阶段重点指标：消耗、曝光、点击、CTR、表单/H5/WhatsApp 线索、CPL、私信咨询、有效线索率、约课率、到课率、成交成本、ROI。

Meta 第一阶段必须支持多目标转化口径，详见 `docs/meta-conversion-goals.md`。不要把所有对象强行归到单一 `leads` 口径。

### ConversionGoalDefinition

平台转化目标定义。

关键字段：`goal_id`、`platform`、`goal_type`、`goal_name`、`primary_metric`、`secondary_metrics`、`raw_action_types`、`optimization_goals`、`name_signals`、`applicable_regions`、`status`、`version`。

Meta 第一阶段目标类型包括：`quality_lead`、`lead_form`、`h5_booking`、`messaging`、`engagement`。

当前业务链路是：曝光 -> 点击 -> 表单/H5/WhatsApp -> 线索 -> 预约试听 -> 到课 -> 成交。Meta 的 `purchase` / `offsite_conversion.fb_pixel_purchase` 在当前 H5 链路中指 external lead sample，不代表真实成交；`offsite_conversion.fb_pixel_custom` 是 `sample_event_alpha`、`sample_event_beta`、`sample_event_gamma` 等自定义业务事件的合集。

### MetricFact

标准指标事实表。

关键字段：`fact_id`、`platform`、`object_type`、`object_id`、`metric_name`、`metric_value`、`date`、`time_window`、`metric_version`、`sync_batch`、`source_quality`、`raw_metric_name`、`dimensions`、`attribution_window`。

`object_type` 可以是 `account`、`campaign`、`ad_group`、`ad`、`creative`、`keyword`、`audience`、`region`。

Meta 的 `actions` / `cost_per_action_type` 和小红书聚光的 `DataReportDTO` 都必须拆成标准 `MetricFact`。平台原始 action type、关键词、placement、归因窗口等差异写入 `dimensions` 和 `raw_metric_name`，不能丢掉。

### BusinessEvent

后链路业务事件。

关键字段：`event_id`、`lead_id`、`event_type`、`event_time`、`market_region`、`source_platform`、`source_object_id`、`status`、`value`、`source_system`。

事件类型包括：留资、有效线索、接通、约课、到课、成交、退款、无效原因。

V0 中 `BusinessEvent` 由 C 线从公司内部业务系统只读接入或提供脱敏样例。它回答“广告带来的后链路业务结果是什么”，不等于 Meta 后台的 action 或 `MetricFact`。

### AttributionLink

广告对象与业务事件的归因关系。

关键字段：`link_id`、`business_event_id`、`platform`、`object_type`、`object_id`、`match_method`、`confidence`、`attribution_window`、`quality_flag`。

V0 可以先用样例导入或手工映射，后续再接正式 CRM/约课/成交数据。C 线必须明确哪些归因是确认、弱归因、未确认或缺少来源 ID；B 线只能消费这些结果，不能自行伪造后链路归因。

### LaunchPlan

发布或投放准备计划，用于把素材组织成可审核的测试或投放草稿。

关键字段：`launch_plan_id`、`name`、`goal_type`、`market_region`、`platforms`、`creative_asset_ids`、`platform_version_ids`、`budget_boundary`、`audience_summary`、`tracking_spec_id`、`test_hypothesis`、`risk_notes`、`approval_state`、`status`。

`LaunchPlan` 是投放准备对象，不是平台执行对象。进入真实广告创建、预算调整或暂停动作前，必须转为 `ActionIntent` 并经过审批。

### AdGroupDraft

广告组或广告单元草稿。

关键字段：`ad_group_draft_id`、`launch_plan_id`、`platform`、`target_object_type`、`targeting_summary`、`optimization_goal`、`budget_boundary`、`creative_asset_ids`、`tracking_spec_id`、`draft_payload_ref`、`risk_level`、`status`。

`AdGroupDraft` 可以用于导出或人工创建广告，但 V0 不能自动写入真实平台。

### TrackingSpec

发布或投放追踪配置。

关键字段：`tracking_spec_id`、`launch_plan_id`、`platform`、`utm_source`、`utm_medium`、`utm_campaign`、`utm_content`、`conversion_goal_id`、`attribution_window`、`status`。

追踪配置必须能连接素材、平台版本、投放计划和后链路事件。

### RuleDefinition

诊断规则定义。

关键字段：`rule_id`、`name`、`description`、`object_type`、`metric_name`、`threshold`、`baseline_method`、`min_sample_size`、`lookback_window`、`risk_level`、`enabled`、`version`。

默认规则方向：CPL 超标、优秀扩量机会、零转化止损、余额风险、CTR 衰退、素材疲劳、定向低效。

### RuleHit

规则命中记录。

关键字段：`rule_hit_id`、`rule_id`、`rule_version`、`object_type`、`object_id`、`triggered_at`、`current_value`、`baseline_value`、`sample_size`、`severity`、`evidence_id`。

### EvidenceObject

诊断和建议引用的证据包。

关键字段：`evidence_id`、`source_type`、`source_id`、`time_window`、`metrics`、`baseline`、`comparison_group`、`sample_size`、`confidence`、`data_quality`、`rule_version`。

每条 Recommendation 和 ActionIntent 必须引用 EvidenceObject。

### Recommendation

系统建议。

关键字段：`recommendation_id`、`object_type`、`object_id`、`recommendation_type`、`summary`、`reasoning`、`evidence_id`、`risk_level`、`status`、`created_by`。

### ActionIntent

可审批动作草稿。

关键字段：`action_intent_id`、`recommendation_id`、`action_type`、`target_object_type`、`target_object_id`、`proposed_change`、`budget_boundary`、`cooldown_policy`、`risk_policy`、`approval_state`、`evidence_id`。

V0 的 ActionIntent 只改变审批状态，不直接执行真实广告动作。

### ActionAudit

动作审计。

关键字段：`audit_id`、`action_intent_id`、`decision`、`decided_by`、`decided_at`、`reject_reason`、`execution_status`、`before_snapshot`、`after_window`、`result_summary`。

### AgentTask

Agent 任务。

关键字段：`agent_task_id`、`task_type`、`context_package_id`、`input_hash`、`output`、`status`、`model`、`started_at`、`finished_at`、`error`。

### ContextPackage

Agent 上下文包。

关键字段：`context_package_id`、`business_goal`、`object_scope`、`metrics`、`rules`、`evidence_ids`、`creative_ids`、`attribution_quality`、`allowed_tools`、`forbidden_actions`。

### ToolCallAudit

工具调用审计。

关键字段：`tool_call_id`、`agent_task_id`、`tool_name`、`permission_level`、`input_ref`、`output_ref`、`status`、`created_at`。

### LearningObject

学习沉淀对象。

关键字段：`learning_id`、`source_action_id`、`source_report_id`、`learning_type`、`hypothesis`、`evidence`、`result`、`status`、`applicable_scope`、`recommended_rule_update_id`、`approved_by`。

只有经过确认或回测的经验才能反哺规则、prompt、brief 和 playbook。

### PerformanceReport

素材、平台版本、投放计划或广告对象的表现复盘。

关键字段：`performance_report_id`、`scope_type`、`scope_id`、`time_window`、`metric_refs`、`business_event_refs`、`summary`、`winning_factors`、`losing_factors`、`data_quality`、`author_type`、`created_at`。

`PerformanceReport` 可以由 Agent 草拟，但必须保留指标引用和数据质量说明。复盘结论要进入 `LearningObject` 后，才能反哺下一轮素材或规则。

### RuleUpdate

规则更新候选。

关键字段：`rule_update_id`、`source_learning_id`、`target_rule_id`、`update_type`、`proposed_change`、`reasoning`、`evidence_refs`、`risk_level`、`approval_state`、`status`。

`RuleUpdate` 不能自动成为生产规则。只有经过人工批准或回测验证后，才能更新 `RuleDefinition` 或生成新的规则版本。

## 数据质量与版本

所有可用于诊断的指标必须带：

- 数据来源。
- 同步批次。
- 时间窗口。
- 指标版本。
- 样本量。
- 置信度或质量标记。

如果数据质量不足，系统应输出 DataQualityIssue，而不是假装给出确定建议。
