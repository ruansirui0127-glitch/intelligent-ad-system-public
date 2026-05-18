# 智能投放系统

这是一个面向广告投放管理的公开安全版仓库，用来沉淀系统架构、接口契约、脱敏样例和本地验证脚本。

系统第一阶段以 Meta 平台为主线，目标是把广告对象、指标事实、诊断规则、建议草稿和人工审批流程串成一条可复盘的工作流。它不是自动花钱机器人，也不会在没有审批边界的情况下直接修改广告后台。

## 当前公开范围

本仓库公开保存：

- 产品和技术架构的脱敏说明。
- API 契约、数据对象和开发模板。
- 合成样例数据，文件名统一带有 `sample`。
- 本地验证脚本和测试用例。
- 平台接入的示例配置，不包含真实授权信息。

本仓库不公开保存：

- 真实 token、refresh token、app secret、Cookie、私钥或本地 `.env`。
- 真实广告账户 ID、后台截图、原始导出报表或 SQLite 运行数据库。
- 客户、学生、家长、供应商、订单、合同、报价、营收、成本、利润等业务原始数据。
- 内部策略文档、未脱敏规划原件、会议记录、聊天记录或 AI 对话原文。
- PDF、Word、Excel、CSV、ZIP、截图、日志等未审核产物。

## 核心工作流

系统的第一版闭环是：

```text
平台只读同步 -> 指标事实 -> 规则诊断 -> 证据解释 -> 建议草稿 -> 人工审批 -> 复盘记录
```

人话理解：

- “指标事实”是一条可追溯的广告数据记录。
- “证据解释”是一包支持诊断结论的材料。
- “建议草稿”是等待人工审批的动作方案，不等于自动执行。
- “复盘记录”用于判断规则和建议是否真的有效。

## 目录结构

- `app/`: 前后端应用骨架。
- `config/examples/`: 可公开的配置模板。
- `data/sample/`: 合成样例数据，只用于契约和测试。
- `docs/`: 公开安全版产品、架构、契约和开发说明。
- `integrations/`: 平台接入适配层。
- `scripts/`: 本地验证、审计和维护脚本。
- `tests/`: 自动化测试。
- `runtime/private/`: 本地运行状态目录，已被 `.gitignore` 排除。
- `config/private/`: 本地真实授权配置目录，已被 `.gitignore` 排除。

## 安全基线

公开前必须通过三件事：

1. 阅读 [安全策略](./SECURITY.md)。
2. 按 [发布检查清单](./docs/publication-checklist.md) 自查。
3. 运行发布审计脚本：

```bash
python3 scripts/publication_audit.py
```

如果脚本报出高风险文件或关键词，先处理风险，再提交或推送。

## 本地运行

安装 Python 依赖：

```bash
python3 -m pip install -r requirements.txt
```

运行测试：

```bash
python3 -m unittest discover -s tests
```

Meta 示例配置从模板复制到私有目录：

```bash
mkdir -p config/private/meta
cp config/examples/meta.env.example config/private/meta/.env
```

然后只在 `config/private/` 中填真实值。不要把真实 `.env` 提交到 Git。

## 远程仓库

GitHub 仓库：

```text
https://github.com/ruansirui0127-glitch/intelligent-ad-system
```

当前仓库是公开仓库，因此默认按“所有内容都会被外部看到”来写文档、样例和提交说明。
