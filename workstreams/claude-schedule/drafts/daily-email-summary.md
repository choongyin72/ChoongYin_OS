---
slug: daily-email-summary
status: approved
schedule: "daily 09:00 AWST"
permission_level: L1
---

# Task: Daily Woodside Email Summary

## What this agent does
Every day at 09:00 AWST, reads all Woodside/project-related emails received in the last 24 hours and produces a clean summary.

## Sources
- Outlook inbox — search for: Woodside, Pluto, ECPR, ECaaS, Bitbucket, pull request, woodside_impl_pluto

## What to look for
1. **Bitbucket PR notifications** — new approvals, change requests, merges, comments
2. **Meeting invites/updates** — new, cancelled, or updated Woodside meetings
3. **Project emails** — from Grant, Jamilin, Simon, Kirsten, Tahura, Daniel, Jean-Pierre
4. **External emails** — from Woodside contacts or other external parties on the project

## Output format
Write a `## Daily Email Summary — YYYY-MM-DD` section to STATUS.md with:

### PR Updates
- List any new approvals, change requests, merges or comments on PRs
- Flag if Grant requested changes — these need action

### Meeting Updates
- Any new, cancelled or changed meeting invites

### Other Project Emails
- Any other important project-related emails

### Action Items
- Any emails that require a response or action from Choong-Yin

Commit and open a PR titled `briefing: email summary YYYY-MM-DD`.

## Prompt
Read Outlook emails received in the last 24 hours with subjects or content containing: Woodside, Pluto, ECPR, ECaaS, Bitbucket, pull request, woodside_impl_pluto_12839.

Group into: PR Updates, Meeting Updates, Other Project Emails, Action Items.

For PR Updates, flag clearly if "requested changes" appears — this means action is needed.
For meetings, note if cancelled or new.
For action items, be specific about what response is needed and by when if possible.

Write the summary to STATUS.md under a new `## Daily Email Summary — {DATE}` heading.
Commit and open a PR titled `briefing: email summary {DATE}`.
