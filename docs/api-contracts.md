# V0 API 契约

## 目标

本文件定义智能投放系统 V0 的最小可开发接口协议，优先服务 Meta 只读数据同步、指标拆分、账户浏览和数据监控。

V0 先统一数据底座和页面 mock 契约，不先实现诊断结论、智能优化建议或自动创建计划。

## 通用约定

### 响应壳

所有接口返回统一结构：

```json
{
  "data": {},
  "meta": {
    "request_id": "req_20260515_001",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00"
  },
  "errors": []
}
```

约定：

- `data`：业务数据。列表接口使用数组或带分页对象。
- `meta`：请求追踪、版本、生成时间、分页、同步批次等非业务字段。
- `errors`：错误数组。成功时为空数组。
- 单个请求可以同时返回部分 `data` 和 `errors`，用于数据质量警告或部分对象同步失败。

### 错误对象

```json
{
  "code": "DATA_QUALITY_LOW",
  "message": "Metric facts are incomplete for the requested window.",
  "severity": "warning",
  "source": "meta_sync",
  "details": {
    "sync_batch": "sync_meta_20260515_001"
  }
}
```

`severity` 可选值：

- `info`
- `warning`
- `error`
- `critical`

### 对象 ID

V0 统一使用系统 ID，不直接把平台原始 ID 当业务主键：

```text
{platform}:{object_type}:{external_id}
```

示例：

- `meta:account:act_123`
- `meta:campaign:1200000000001`
- `meta:ad_group:1200000000002`
- `meta:ad:1200000000003`

每个对象仍必须保留平台原始 ID：

```json
{
  "id": "meta:campaign:1200000000001",
  "platform": "meta",
  "object_type": "campaign",
  "external_id": "1200000000001"
}
```

非平台原始对象使用领域 ID，形状为：

```text
{domain}:{object_type}:{local_id}
```

示例：

- `creative:opportunity:opp_sample_001`
- `creative:master_asset:ma_sample_001`
- `creative:platform_version:pv_sample_001`
- `creative:asset:creative_sample_001`
- `action:launch_plan:lp_sample_001`

平台对象仍必须使用 `{platform}:{object_type}:{external_id}`，例如 `meta:ad_group:1200000000002`。领域 ID 不能伪装成平台对象 ID。

### 时间窗口

查询参数统一使用：

```text
date_start=2026-05-01
date_stop=2026-05-14
time_grain=day
timezone=Asia/Shanghai
```

约定：

- `date_start`、`date_stop` 使用 `YYYY-MM-DD`。
- `date_stop` 为闭区间日期。
- `time_grain` 可选：`day`、`week`、`month`、`lifetime`。
- 默认时区优先使用广告账户时区；未指定时返回 `Asia/Shanghai`。

### 枚举

`platform`：

- `meta`
- `google`
- `douyin`
- `tencent_ads`
- `xiaohongshu`

`object_type`：

- `account`
- `campaign`
- `ad_group`
- `ad`
- `creative`
- `keyword`
- `audience`
- `region`

`domain_object_type`：

- `market_signal`
- `opportunity`
- `context_package`
- `master_asset`
- `platform_version`
- `creative_asset`
- `launch_plan`
- `ad_group_draft`
- `performance_report`
- `learning_object`
- `rule_update`

`goal_type`：

- `quality_lead`
- `lead_form`
- `h5_booking`
- `messaging`
- `engagement`
- `unknown`

`metric_stage`：

- `delivery`
- `click`
- `landing`
- `conversion`
- `business`
- `cost`
- `quality`

`source_quality`：

- `complete`
- `partial`
- `estimated`
- `missing`
- `unknown`

## 共享对象 Wire Shape

### AccountNode

用于账户树接口。

```json
{
  "id": "meta:account:act_123",
  "platform": "meta",
  "object_type": "account",
  "external_id": "act_123",
  "name": "FB-Account",
  "status": "ACTIVE",
  "currency": "USD",
  "timezone": "Asia/Shanghai",
  "market_region": "Region A",
  "children_count": {
    "campaigns": 12,
    "ad_groups": 86,
    "ads": 220
  }
}
```

### AdObject

用于 Campaign / AdGroup / Ad 的统一返回。

```json
{
  "id": "meta:ad_group:1200000000002",
  "platform": "meta",
  "object_type": "ad_group",
  "external_id": "1200000000002",
  "parent_id": "meta:campaign:1200000000001",
  "name": "Region A-Quality-H5-Test",
  "status": "ACTIVE",
  "platform_object_type": "adset",
  "objective": "OUTCOME_LEADS",
  "optimization_goal": "QUALITY_LEAD",
  "goal_type": "quality_lead",
  "market_region": "Region A",
  "started_at": "2026-05-01T00:00:00+08:00",
  "ended_at": null
}
```

### MetricFact

Meta `actions`、`cost_per_action_type` 等数组型指标必须拆成原子事实。

```json
{
  "fact_id": "fact_meta_20260515_001",
  "platform": "meta",
  "object_type": "ad_group",
  "object_id": "meta:ad_group:1200000000002",
  "metric_name": "quality_lead",
  "metric_value": 18,
  "unit": "count",
  "date": "2026-05-14",
  "time_window": {
    "date_start": "2026-05-14",
    "date_stop": "2026-05-14",
    "time_grain": "day",
    "timezone": "Asia/Shanghai"
  },
  "metric_stage": "conversion",
  "goal_type": "quality_lead",
  "metric_version": "meta_v0_202605",
  "sync_batch": "sync_meta_20260515_001",
  "source_quality": "complete",
  "raw_metric_name": "actions",
  "dimensions": {
    "action_type": "offsite_conversion.fb_pixel_custom",
    "attribution_window": "7d_click",
    "optimization_goal": "QUALITY_LEAD",
    "business_mapping": "custom_business_event_bundle",
    "business_event_codes": ["sample_event_alpha", "sample_event_beta", "sample_event_gamma"]
  },
  "attribution_window": "7d_click"
}
```

最低要求：

- 花费、曝光、点击等普通字段也必须写成 `MetricFact`。
- `raw_metric_name` 保留平台来源字段。
- `dimensions.action_type` 保留 Meta 原始 action type。
- `offsite_conversion.fb_pixel_custom` 当前解释为自定义业务事件合集，包括 `sample_event_alpha`、`sample_event_beta`、`sample_event_gamma` 等。
- `purchase` / `fb_pixel_purchase` 当前解释为 H5 链路的线索，不等于真实成交或付款。

### SyncStatus

```json
{
  "platform": "meta",
  "status": "success",
  "last_sync_batch": "sync_meta_20260515_001",
  "last_started_at": "2026-05-15T09:55:00+08:00",
  "last_finished_at": "2026-05-15T09:58:00+08:00",
  "date_start": "2026-05-01",
  "date_stop": "2026-05-14",
  "objects_synced": {
    "accounts": 1,
    "campaigns": 12,
    "ad_groups": 86,
    "ads": 220,
    "metric_facts": 14560
  },
  "warnings": [
    {
      "code": "CUSTOM_EVENT_BUNDLE",
      "message": "offsite_conversion.fb_pixel_custom is a confirmed custom business event bundle, not a single business event."
    }
  ]
}
```

`status` 可选值：

- `not_configured`
- `running`
- `success`
- `partial_success`
- `failed`

### OpportunityCard

用于素材增长中台和今日工作台展示候选机会。

```json
{
  "id": "creative:opportunity:opp_sample_001",
  "domain_object_type": "opportunity",
  "title": "Region A家长暑期数学衔接焦虑",
  "market_region": "Region A",
  "recommended_platforms": ["meta"],
  "target_audience": "4-12岁孩子家长",
  "pain_point": "担心暑期后数学思维断层",
  "angle": "暑期衔接与思维训练",
  "reason_to_try": "历史暑期素材点击率较高，且当前市场讨论升温。",
  "evidence_refs": ["creative:market_signal:sig_sample_001"],
  "risk_notes": ["避免承诺短期提分结果。"],
  "recommended_asset_formats": ["copy", "image_brief", "short_video_script"],
  "priority_score": 82,
  "status": "ready_for_context"
}
```

### MasterAsset

用于表达跨平台素材母版。

```json
{
  "id": "creative:master_asset:ma_sample_001",
  "domain_object_type": "master_asset",
  "opportunity_id": "creative:opportunity:opp_sample_001",
  "context_package_id": "harness:context_package:ctx_sample_001",
  "title": "暑期数学思维衔接母版",
  "core_claim": "暑期是孩子补齐数学思维习惯的窗口。",
  "proof_points": [
    {
      "type": "business_fact",
      "summary": "课程以小班直播和互动练习为主。"
    }
  ],
  "pain_point": "家长担心孩子开学后跟不上节奏。",
  "selling_point": "通过持续互动训练建立数学思考习惯。",
  "cta": "预约试听",
  "risk_notes": ["不能承诺保证提分。"],
  "status": "draft"
}
```

### PlatformVersion

用于表达母版在某个平台的派生版本。

```json
{
  "id": "creative:platform_version:pv_sample_meta_001",
  "domain_object_type": "platform_version",
  "master_asset_id": "creative:master_asset:ma_sample_001",
  "platform": "meta",
  "market_region": "Region A",
  "asset_format": "image_ad",
  "placement": "feed",
  "copy_variant_ids": ["creative:asset:copy_sample_001"],
  "creative_asset_ids": ["creative:asset:image_brief_sample_001"],
  "adaptation_reason": "Meta feed 需要短钩子、清晰痛点和明确试听 CTA。",
  "cta": "预约试听",
  "risk_level": "medium",
  "status": "ready_for_review"
}
```

### CreativeAsset

用于表达可复用素材资产。

```json
{
  "id": "creative:asset:image_brief_sample_001",
  "domain_object_type": "creative_asset",
  "asset_type": "image_brief",
  "title": "暑期数学衔接 Meta 图片 brief",
  "copy": "开学前，先帮孩子找回数学思考节奏",
  "media_uri": null,
  "market_region": "Region A",
  "platform": "meta",
  "persona": "4-12岁孩子家长",
  "pain_point": "暑期后数学衔接焦虑",
  "selling_point": "小班直播互动训练",
  "format": "feed_image",
  "opportunity_id": "creative:opportunity:opp_sample_001",
  "master_asset_id": "creative:master_asset:ma_sample_001",
  "platform_version_id": "creative:platform_version:pv_sample_meta_001",
  "approval_status": "pending_review",
  "servable_status": "draft",
  "tags": [
    {
      "tag_type": "market_region",
      "tag_value": "Region A",
      "confidence": 1.0,
      "source": "human"
    }
  ]
}
```

### LaunchPlan

用于表达发布或投放准备草稿。它不是平台执行结果。

```json
{
  "id": "action:launch_plan:lp_sample_001",
  "domain_object_type": "launch_plan",
  "name": "Region A暑期衔接 Meta 素材测试",
  "goal_type": "quality_lead",
  "market_region": "Region A",
  "platforms": ["meta"],
  "creative_asset_ids": ["creative:asset:image_brief_sample_001"],
  "platform_version_ids": ["creative:platform_version:pv_sample_meta_001"],
  "budget_boundary": {
    "currency": "USD",
    "daily_budget_max": 50
  },
  "audience_summary": "Region A地区 4-12 岁孩子家长",
  "tracking_spec_id": "action:tracking_spec:trk_sample_001",
  "test_hypothesis": "暑期衔接痛点比泛数学启蒙角度更容易带来高质量线索。",
  "approval_state": "draft",
  "status": "draft"
}
```

### PerformanceReport

用于表达素材、平台版本或投放计划的表现复盘。

```json
{
  "id": "learning:performance_report:pr_sample_001",
  "domain_object_type": "performance_report",
  "scope_type": "creative_asset",
  "scope_id": "creative:asset:image_brief_sample_001",
  "time_window": {
    "date_start": "2026-05-01",
    "date_stop": "2026-05-14",
    "time_grain": "day",
    "timezone": "Asia/Shanghai"
  },
  "metric_refs": ["fact_meta_sample_20260514_quality_lead_001"],
  "business_event_refs": [],
  "summary": "样例素材带来较高点击，但后链路质量仍需业务数据确认。",
  "winning_factors": ["暑期衔接痛点明确"],
  "losing_factors": ["缺少真实家长案例证据"],
  "data_quality": "partial",
  "author_type": "agent_draft"
}
```

### RuleUpdate

用于表达规则更新候选。它不能自动更新生产规则。

```json
{
  "id": "learning:rule_update:ru_sample_001",
  "domain_object_type": "rule_update",
  "source_learning_id": "learning:object:learn_sample_001",
  "target_rule_id": "rule_creative_fatigue_001",
  "update_type": "threshold_adjustment",
  "proposed_change": {
    "lookback_window": "7d",
    "min_sample_size": 1000
  },
  "reasoning": "样例复盘显示素材疲劳判断需要同时看频次和转化质量。",
  "evidence_refs": ["learning:performance_report:pr_sample_001"],
  "risk_level": "medium",
  "approval_state": "pending_review",
  "status": "draft"
}
```

## V0 先行接口

### GET /api/v0/creatives/opportunities

用途：给今日工作台和素材增长中台展示候选机会。V0 可先返回手工维护或样例机会。

查询参数：

```text
market_region=Region A
platform=meta
status=ready_for_context
limit=20
```

响应：

```json
{
  "data": {
    "items": [
      {
        "id": "creative:opportunity:opp_sample_001",
        "domain_object_type": "opportunity",
        "title": "Region A家长暑期数学衔接焦虑",
        "market_region": "Region A",
        "recommended_platforms": ["meta"],
        "target_audience": "4-12岁孩子家长",
        "pain_point": "担心暑期后数学思维断层",
        "angle": "暑期衔接与思维训练",
        "priority_score": 82,
        "status": "ready_for_context"
      }
    ]
  },
  "meta": {
    "request_id": "req_20260515_creative_001",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00",
    "pagination": {
      "limit": 20,
      "next_cursor": null
    }
  },
  "errors": []
}
```

### GET /api/v0/creatives

用途：给素材增长中台和账户诊断页提供素材资产列表。V0 可先使用脱敏样例。

查询参数：

```text
platform=meta
market_region=Region A
asset_type=image_brief
approval_status=pending_review
limit=20
```

响应：

```json
{
  "data": {
    "items": [
      {
        "id": "creative:asset:image_brief_sample_001",
        "domain_object_type": "creative_asset",
        "asset_type": "image_brief",
        "title": "暑期数学衔接 Meta 图片 brief",
        "market_region": "Region A",
        "platform": "meta",
        "opportunity_id": "creative:opportunity:opp_sample_001",
        "master_asset_id": "creative:master_asset:ma_sample_001",
        "platform_version_id": "creative:platform_version:pv_sample_meta_001",
        "approval_status": "pending_review",
        "servable_status": "draft",
        "tags": [
          {
            "tag_type": "market_region",
            "tag_value": "Region A",
            "confidence": 1.0,
            "source": "human"
          }
        ]
      }
    ]
  },
  "meta": {
    "request_id": "req_20260515_creative_002",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00",
    "pagination": {
      "limit": 20,
      "next_cursor": null
    }
  },
  "errors": []
}
```

### GET /api/v0/accounts/tree

用途：给账户分析页和数据监控页提供账户、计划、单元、广告的层级骨架。

查询参数：

```text
platform=meta
account_id=meta:account:act_123
include=campaigns,ad_groups,ads
status=ACTIVE
```

响应：

```json
{
  "data": {
    "accounts": [
      {
        "id": "meta:account:act_123",
        "platform": "meta",
        "object_type": "account",
        "external_id": "act_123",
        "name": "FB-Account",
        "status": "ACTIVE",
        "currency": "USD",
        "timezone": "Asia/Shanghai",
        "market_region": "Region A",
        "children": [
          {
            "id": "meta:campaign:1200000000001",
            "platform": "meta",
            "object_type": "campaign",
            "external_id": "1200000000001",
            "name": "Region A-Quality-测试",
            "status": "ACTIVE",
            "objective": "OUTCOME_LEADS",
            "goal_type": "quality_lead",
            "children": [
              {
                "id": "meta:ad_group:1200000000002",
                "platform": "meta",
                "object_type": "ad_group",
                "external_id": "1200000000002",
                "name": "Region A-Quality-H5-Test",
                "status": "ACTIVE",
                "platform_object_type": "adset",
                "optimization_goal": "QUALITY_LEAD",
                "goal_type": "quality_lead",
                "children": []
              }
            ]
          }
        ]
      }
    ]
  },
  "meta": {
    "request_id": "req_20260515_001",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00",
    "sync_batch": "sync_meta_20260515_001"
  },
  "errors": []
}
```

### GET /api/v0/accounts/{id}/metrics

用途：给账户分析页提供某个账户或下级对象的指标摘要。

路径参数：

- `id`：系统对象 ID，URL 中需要编码。例如 `meta%3Aaccount%3Aact_123`。

查询参数：

```text
object_type=account
date_start=2026-05-01
date_stop=2026-05-14
time_grain=day
goal_type=quality_lead
metrics=spend,impressions,clicks,link_clicks,landing_page_view,quality_lead,leads
breakdown=object
```

响应：

```json
{
  "data": {
    "object": {
      "id": "meta:account:act_123",
      "platform": "meta",
      "object_type": "account",
      "name": "FB-Account"
    },
    "time_window": {
      "date_start": "2026-05-01",
      "date_stop": "2026-05-14",
      "time_grain": "day",
      "timezone": "Asia/Shanghai"
    },
    "metrics": [
      {
        "metric_name": "spend",
        "metric_value": 1200.5,
        "unit": "currency",
        "metric_stage": "cost",
        "goal_type": "quality_lead"
      },
      {
        "metric_name": "quality_lead",
        "metric_value": 83,
        "unit": "count",
        "metric_stage": "conversion",
        "goal_type": "quality_lead"
      }
    ],
    "series": [
      {
        "date": "2026-05-14",
        "metrics": {
          "spend": 88.2,
          "impressions": 12000,
          "clicks": 340,
          "link_clicks": 210,
          "landing_page_view": 160,
          "quality_lead": 8,
          "leads": 11
        }
      }
    ]
  },
  "meta": {
    "request_id": "req_20260515_002",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00",
    "metric_version": "meta_v0_202605",
    "sync_batch": "sync_meta_20260515_001"
  },
  "errors": []
}
```

### GET /api/v0/sync/meta/status

用途：给数据与 Harness 监控页展示 Meta 同步状态、批次、警告和失败原因。

查询参数：

```text
account_id=meta:account:act_123
limit=10
```

响应：

```json
{
  "data": {
    "current": {
      "platform": "meta",
      "status": "success",
      "last_sync_batch": "sync_meta_20260515_001",
      "last_started_at": "2026-05-15T09:55:00+08:00",
      "last_finished_at": "2026-05-15T09:58:00+08:00",
      "date_start": "2026-05-01",
      "date_stop": "2026-05-14",
      "objects_synced": {
        "accounts": 1,
        "campaigns": 12,
        "ad_groups": 86,
        "ads": 220,
        "metric_facts": 14560
      },
      "warnings": []
    },
    "history": []
  },
  "meta": {
    "request_id": "req_20260515_003",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00"
  },
  "errors": []
}
```

### GET /api/v0/data/metric-facts

用途：给开发、数据监控和诊断前置验证使用，直接查询标准化后的原子指标事实。

查询参数：

```text
platform=meta
object_type=ad_group
object_id=meta:ad_group:1200000000002
date_start=2026-05-01
date_stop=2026-05-14
metric_name=quality_lead
goal_type=quality_lead
limit=100
cursor=
```

响应：

```json
{
  "data": {
    "items": [
      {
        "fact_id": "fact_meta_20260515_001",
        "platform": "meta",
        "object_type": "ad_group",
        "object_id": "meta:ad_group:1200000000002",
        "metric_name": "quality_lead",
        "metric_value": 18,
        "unit": "count",
        "date": "2026-05-14",
        "time_window": {
          "date_start": "2026-05-14",
          "date_stop": "2026-05-14",
          "time_grain": "day",
          "timezone": "Asia/Shanghai"
        },
        "metric_stage": "conversion",
        "goal_type": "quality_lead",
        "metric_version": "meta_v0_202605",
        "sync_batch": "sync_meta_20260515_001",
        "source_quality": "complete",
        "raw_metric_name": "actions",
        "dimensions": {
          "action_type": "offsite_conversion.fb_pixel_custom",
          "optimization_goal": "QUALITY_LEAD",
          "business_mapping": "custom_business_event_bundle"
        },
        "attribution_window": "7d_click"
      }
    ]
  },
  "meta": {
    "request_id": "req_20260515_004",
    "api_version": "v0",
    "generated_at": "2026-05-15T10:00:00+08:00",
    "pagination": {
      "limit": 100,
      "next_cursor": null
    }
  },
  "errors": []
}
```

### GET /api/v0/business/events

用途：给账户诊断和数据监控提供内部业务系统的只读后链路事件，例如有效线索、预约、到课、成交、退款。

V0 可先返回脱敏或合成样例；真实内部业务系统只读接入由 C 线负责。

查询参数：

```text
source_platform=meta
source_object_id=meta:ad:1200000000003
event_type=booking
date_start=2026-05-01
date_stop=2026-05-14
```

响应必须使用 `data / meta / errors` 响应壳，业务事件对象遵循 `docs/data-model.md` 的 `BusinessEvent`。

### GET /api/v0/business/attribution-links

用途：给 B 线诊断提供业务事件与广告对象之间的归因关系。它回答“这个预约、到课或成交能不能回到某个 Campaign / Ad Set / Ad / Creative”。

V0 必须显式表达 `match_method`、`confidence`、`attribution_window` 和 `quality_flag`，不能把弱归因包装成确定结论。

查询参数：

```text
business_event_id=business:event:booking_sample_001
platform=meta
object_type=ad
object_id=meta:ad:1200000000003
```

响应必须使用 `data / meta / errors` 响应壳，归因对象遵循 `docs/data-model.md` 的 `AttributionLink`。

## Mock 与协作要求

B 线先提供 Meta 广告侧脱敏 mock：

- `data/sample/accounts-tree.meta.sample.json`
- `data/sample/account-metrics.meta.sample.json`
- `data/sample/sync-status.meta.sample.json`
- `data/sample/metric-facts.meta.sample.json`

C 线先提供内部业务系统和归因脱敏 mock：

- `data/sample/business-events.sample.json`
- `data/sample/attribution-links.sample.json`

要求：

- mock 必须符合本文件响应壳。
- mock 不包含真实 token、私有投放数据或敏感账户信息。
- 字段新增或含义变化必须先更新本文件，再更新 `docs/data-model.md`。
- A/B/C 不能绕过 API 契约直接依赖 Meta 原始字段或内部业务系统原始字段。

本地校验命令：

```bash
.venv/bin/python scripts/validate_api_contracts.py
```

也可以指定单个文件：

```bash
.venv/bin/python scripts/validate_api_contracts.py data/sample/metric-facts.meta.sample.json
```

## 暂不进入 V0 的接口

以下接口可以保留文档方向，但不作为下一轮开发入口：

- 智能诊断结论生成。
- 自动预算调整。
- 自动创建 Campaign / Ad Set / Ad。
- 真实投放动作执行。
- Google、抖音、腾讯广告、小红书深度同步。
