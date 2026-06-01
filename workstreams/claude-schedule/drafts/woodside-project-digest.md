---
slug: woodside-project-digest
status: approved
schedule: "weekly Monday 08:30 AWST"
permission_level: L2
---

# Task: Woodside Project Digest

## What this agent does
1. Reads recent git log from C:/DEV/GIT/woodside_impl_pluto_12839 (last 7 days).
2. Summarises commits by area (feature, fix, config, etc.).
3. Appends a digest section to STATUS.md under a "Woodside Digest" heading.
4. Opens a PR with the updated STATUS.md.

## Prompt
Read git log --oneline --since=7.days.ago in C:/DEV/GIT/woodside_impl_pluto_12839. Summarise the commits by category (feature, fix, config, other). Append a "## Woodside Digest — YYYY-MM-DD" section to STATUS.md with the summary. Commit and open a PR titled "chore: woodside digest YYYY-MM-DD".
