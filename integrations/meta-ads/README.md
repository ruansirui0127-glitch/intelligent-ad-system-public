# Meta Ads 接入

## 私有配置

真实 System User Token 只放在：

`config/private/meta/.env`

模板在：

`config/examples/meta.env.example`

不要把真实 token 写入 README、文档、代码或 Git 提交。

## 只读验证

如果还没确定广告账号，先列出 token 可访问的账号：

```bash
.venv/bin/python scripts/meta_list_accounts.py --env config/private/meta/.env
```

推荐先用官方 SDK 验证：

```bash
.venv/bin/python scripts/meta_sdk_verify.py --env config/private/meta/.env
```

如果 SDK 返回不清楚，再用 raw Graph API 对照：

```bash
.venv/bin/python scripts/meta_verify.py --env config/private/meta/.env
```

验证范围：

- `/me`
- Ad Account
- Campaigns
- Ad Sets
- Ads
- Campaign-level Insights

脚本只打印 token 的首尾少量字符，不打印完整 token。

## 安装 SDK

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

当前使用官方 `facebook-business==25.0.1`。
