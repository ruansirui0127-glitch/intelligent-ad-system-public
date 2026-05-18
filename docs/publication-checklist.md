# 发布检查清单

本清单用于公开、分享、交付或合并到主分支前自查。

## 业务问题

要解决的问题：确认仓库只包含可以公开的代码、文档、模板和脱敏样例，避免把真实授权、真实广告数据或内部业务材料发布出去。

做到什么算完成：

- 没有真实密钥和授权文件。
- 没有真实广告账户、原始报表、客户或订单数据。
- 样例数据能说明接口形状，但不能还原真实业务。
- README、PR 和安全策略都写清楚公开边界。

## 文件检查

- [ ] 没有 `.env`、`.env.*`、token、secret、key、pem、p12、pfx 文件。
- [ ] 没有 SQLite、日志、缓存、运行态数据库。
- [ ] 没有真实 Excel、CSV、PDF、Word、ZIP、截图或录屏。
- [ ] `data/raw/`、`outputs/`、`exports/`、`downloads/` 中没有被 Git 跟踪的业务产物。
- [ ] `config/private/` 和 `runtime/private/` 没有被 Git 跟踪。

## 内容检查

- [ ] 文档没有真实广告账户 ID、真实账户名称或后台截图。
- [ ] 文档没有客户、学生、家长、供应商、合同、报价、订单、营收、成本、利润等原始业务信息。
- [ ] 示例数据只使用 `sample`、`demo`、`synthetic`、`Region A`、`Campaign Sample` 这类占位信息。
- [ ] 业务规则只保留产品逻辑，不暴露真实阈值、预算线或内部策略。
- [ ] README 说明了仓库公开范围和禁止公开内容。

## 命令检查

```bash
git status --short
python3 scripts/publication_audit.py
python3 -m unittest discover -s tests
```

如果审计脚本提示风险，不要用“这是示例”直接跳过；先确认是否真的脱敏，再决定保留、改写或移除。
