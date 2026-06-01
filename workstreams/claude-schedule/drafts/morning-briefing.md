---
slug: morning-briefing
status: approved
schedule: "daily 08:00 AWST"
permission_level: L2
---

# Task: Morning Briefing

## What this agent does
Runs every morning at 08:00 AWST. Sweeps all connected sources for overnight changes, updates workstream context, and flags anything needing Choong-Yin's attention before the day starts.

## Sources to check
1. **Woodside Git** — `C:/DEV/GIT/woodside_impl_pluto_12839`
   - New commits since yesterday 08:00
   - Any uncommitted changes or untracked files
   - Branch status vs remote

2. **EC Web App** — `https://app-plutodev.woodside-pluto.tieto-og.cloud/`
   - Reachability check (HTTP status)
   - Flag if unreachable or returning errors

3. **This OS repo** — `C:/Projects/ChoongYin_OS`
   - Any pending approved specs not yet armed
   - Any open PRs needing review
   - Overdue candidate tasks

4. **STATUS.md**
   - Reconcile: move completed items to Done, clear stale entries

## Attention triggers (always surface these)
- New commits touching core config files (pom.xml, Jenkinsfile, *.properties, *.xml)
- EC Web App unreachable or non-2xx/3xx response
- Any spec stuck in `status: approved` for >1 day (not armed)
- Uncommitted changes in the Woodside repo

## Output
1. Update `STATUS.md` with a `## Morning Briefing — YYYY-MM-DD HH:MM` section summarising:
   - What changed overnight (bullet list per source)
   - **ATTENTION** items highlighted at the top if any triggers fired
2. Update `workstreams/master-plan/drafts/candidates/YYYY-MM-DD.md` with 2-3 suggested tasks for the day based on findings.
3. Open a PR titled `briefing: morning YYYY-MM-DD` with the updates.

## Prompt
You are Choong-Yin's morning briefing agent. Today is {DATE}. Check each source below and produce a briefing.

1. Run `git log --oneline --since="yesterday 08:00" --all` in `C:/DEV/GIT/woodside_impl_pluto_12839`. Note any commits touching pom.xml, Jenkinsfile, *.properties, or *.xml as ATTENTION items.
2. Run `git status` in `C:/DEV/GIT/woodside_impl_pluto_12839`. Flag uncommitted changes.
3. Check reachability of https://app-plutodev.woodside-pluto.tieto-og.cloud/ (HTTP GET, timeout 10s). Flag if not 2xx/3xx.
4. Read `C:/Projects/ChoongYin_OS/STATUS.md`. Find specs stuck on `status: approved` >1 day.
5. Read `C:/Projects/ChoongYin_OS/workstreams/master-plan/drafts/plan.md` for context.

Then:
- Write a `## Morning Briefing — {DATE}` section at the top of STATUS.md. Start with `### ATTENTION` if any triggers fired (bold each item). Follow with `### Changes` (bullet per source). Keep it scannable — max 20 lines.
- Write 2-3 candidate tasks for today to `workstreams/master-plan/drafts/candidates/{DATE}.md`.
- Commit all changes and open a PR titled `briefing: morning {DATE}`.
