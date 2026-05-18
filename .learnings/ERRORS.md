# Errors

Command failures, API/tool failures, integration gotchas, and recovery notes captured while building the intelligent advertising system.

Use this file when:
- a Meta/Xiaohongshu/Tencent/Google platform integration step fails
- auth, token, SDK, scraper, browser, publishing, or dashboard verification breaks
- a workaround is found that should be reused

Do not store real tokens, app secrets, refresh tokens, account IDs with sensitive context, or raw private ad data here. Use short redacted excerpts.

## Entry Template

```markdown
## ERR-YYYYMMDD-001 - short-title

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | fixed | accepted-risk
**Area**: meta | xiaohongshu | auth | sdk | scrape | publish | frontend | data | infra

### Symptom
What failed, including the shortest useful redacted error excerpt.

### Cause
Known or suspected root cause.

### Fix / Workaround
What worked, including commands only when safe to store.

### Metadata
- Tool:
- Related Files:
- Tags:
```

