---
name: project-learnings
description: Use when a project-local correction, recurring platform failure, missing capability, or reusable advertising-system workflow lesson should be recorded without changing global memory immediately.
---

# Project Learnings

This skill keeps lightweight, project-local learning records in `.learnings/` before anything is promoted to long-term memory or a reusable global skill.

## When to Use

Use this skill when:
- the user corrects a mistaken assumption about platform priority, KPI meaning, scope, ranking, wording, or workflow
- a Meta Ads, Xiaohongshu, SDK, auth, scraper, browser, dashboard, or publishing step fails
- a missing capability should become a backlog item
- a lesson is specific to the intelligent advertising system and should not become global memory yet

Do not use it for secrets, tokens, full transcripts, raw private ad data, or full config files. Store short summaries and redacted error excerpts.

## Files

- `.learnings/LEARNINGS.md`: corrections, insights, knowledge gaps, best practices
- `.learnings/ERRORS.md`: failures, causes, workarounds, recovery commands
- `.learnings/FEATURE_REQUESTS.md`: requested capabilities and backlog ideas

## Logging Rule

Append one compact entry. Prefer:
- what changed
- why it matters next time
- the smallest useful evidence
- the next concrete action

If a lesson becomes broadly useful across projects, suggest promoting it to a reusable skill, project `AGENTS.md`, or Codex memory.

