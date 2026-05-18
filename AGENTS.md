# Codex 工作原则

## 项目定位

本仓库是「智能投放系统」主仓库。Codex 在本项目中应默认围绕智能投放系统推进，第一阶段以 Meta 平台为主线。

## 规划使用方式

- 公开 main 只保留脱敏后的规划模板和安全说明；原始 PRD、业务画像、账户口径和导出材料不进入公开仓库。
- 理解产品方向时，优先读取 README、`docs/product-vision.md`、`docs/architecture.md`、`docs/data-model.md`、`docs/integration-plan.md` 和 `docs/api-contracts.md`。
- README、`docs/product-vision.md`、`docs/architecture.md`、`docs/data-model.md`、`docs/integration-plan.md` 是当前可执行口径。
- Meta 是第一阶段广告数据和投放诊断主线；小红书、Google、抖音、腾讯广告是后续扩展平台。
- 不要引入额外的离线表格作为平台或数据源。

## 敏感配置

- 真实 token、refresh token、app secret、授权状态文件只能保存在 `config/private/`、`runtime/private/` 或其他 `.gitignore` 排除的私有目录。
- 不允许提交真实 token、真实广告数据、SQLite 运行数据库、日志或本地 `.env`。
- 不允许提交未审核的 Word、PDF、Excel、CSV、ZIP、截图、后台导出、抓包和原始业务材料。
- 对外只提交 `config/examples/` 下的模板。
- 最终回复和文档中不要打印真实 token 内容。

## 开发规则

- 所有新功能必须服务于智能投放系统目标：广告投放管理、跨平台数据接入、诊断、优化建议、预算和创意辅助。
- 改动前先判断属于哪个模块：`app/`、`integrations/`、`intelligence/`、`config/`、`runtime/`、`data/` 或 `docs/`。
- 后续开发按 Git 分支进行，默认从 `dev` 拉功能分支。
- 重要产品决策、数据模型变化、平台接入约束必须沉淀到 `docs/`。

## 沟通输出规则

- 默认把项目输出写给「非技术、非投放团队」也能听懂的人看。
- 涉及技术对象、数据模型、API、Agent、Meta 字段或投放诊断时，先用中文人话解释业务含义，再补充系统对象或字段名。
- 不要只输出 `MetricFact`、`EvidenceObject`、`ContextPackage`、`ActionIntent` 这类术语；必须同时说明它们分别对应「一条指标事实」「一包判断证据」「给 Agent 的限定材料」「等待人工审批的动作草稿」。
- 给团队分工、会议议程、验收标准和开发任务时，先说“要解决什么业务问题、谁要提供什么输入、做到什么算完成”，再说文件路径、JSON、validator 或测试命令。
