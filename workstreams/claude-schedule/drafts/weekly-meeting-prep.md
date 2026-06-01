---
slug: weekly-meeting-prep
status: approved
schedule: "weekly Tuesday 14:00 AWST"
permission_level: L2
---

# Task: Weekly Meeting Prep — Woodside Pluto Project Meeting

## What this agent does
Every Tuesday at 14:00 AWST (day before the Wednesday 15:00 AWST Woodside Pluto Weekly Project Meeting), prepares a structured meeting input document.

## Sources to check
1. Git log in `C:/DEV/GIT/woodside_impl_pluto_12839` — commits since last Wednesday
2. Open branches and PR status (from STATUS.md + workstreams/features-in-flight/context.md)
3. Teams — Pluto SuperFriends Extended + Workstream H chats (last 7 days)
4. STATUS.md — current ATTENTION items and task list
5. workstreams/master-plan/drafts/project-summary.md — project context

## Output
Write a meeting input file to `workstreams/master-plan/drafts/meeting-input-YYYY-MM-DD.md` containing:
- Completed since last meeting
- In progress
- Blockers / risks
- Planned this week
- Questions to raise in the meeting

Commit and open a PR titled `docs: meeting input YYYY-MM-DD`.
