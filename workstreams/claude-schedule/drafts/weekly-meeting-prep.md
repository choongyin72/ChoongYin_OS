---
slug: weekly-meeting-prep
status: approved
schedule: "weekly Wednesday 18:30 AWST"
permission_level: L2
---

# Task: Post-Meeting Wrap-Up — Woodside Pluto Weekly Project Meeting

## What this agent does
Every Wednesday at 18:30 AWST (after the 15:00 Woodside Pluto Weekly Project Meeting ends), reads the Teams meeting chat and emails to capture what was discussed, decisions made, and action items for Choong-Yin.

## Sources
1. Teams — Pluto SuperFriends Extended chat (messages from today)
2. Teams — Daily Standup Workstream H chat (messages from today)
3. Outlook — emails received today related to Woodside/project
4. STATUS.md — current task list and open items

## Output
Write a `## Post-Meeting Wrap-Up — YYYY-MM-DD` section to STATUS.md with:

### Key Discussion Points
- What was raised and discussed in today's meeting

### Decisions Made
- Any confirmed decisions or direction changes

### Action Items for Choong-Yin
- Specific tasks assigned or raised for Choong-Yin, with any deadlines

### Watch List
- Items raised by others that may impact Choong-Yin's work

Commit and open a PR titled `docs: post-meeting wrap-up YYYY-MM-DD`.

## Prompt
Read today's messages in Teams (Pluto SuperFriends Extended and Workstream H) and today's Woodside-related emails. Extract: key discussion points, decisions made, action items for Choong-Yin, and anything that impacts the reporting workstream. Write the wrap-up to STATUS.md. Commit and open a PR titled `docs: post-meeting wrap-up {DATE}`.
