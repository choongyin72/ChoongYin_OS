---
slug: daily-status-reconcile
status: approved
schedule: "daily 08:00 AWST"
permission_level: L2
---

# Task: Daily Status Reconcile

## What this agent does
1. Reads STATUS.md and the last 7 days of git log in this repo.
2. Updates STATUS.md — moves completed items to Done, clears stale queue entries.
3. Proposes 2-3 candidate tasks for the day and appends them to workstreams/master-plan/drafts/candidates/YYYY-MM-DD.md.
4. Opens a PR with the updates.

## Prompt
Read STATUS.md and git log --oneline --since=7.days.ago. Reconcile the status page: move done items to Done, remove stale queue entries. Then propose 2-3 candidate tasks for today based on the master plan (workstreams/master-plan/drafts/plan.md). Write the candidates to workstreams/master-plan/drafts/candidates/$(date +%Y-%m-%d).md. Commit and open a PR titled "chore: daily status reconcile YYYY-MM-DD".
