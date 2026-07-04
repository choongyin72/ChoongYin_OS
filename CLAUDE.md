# WORKER SESSION — READ FIRST

## On session start (mandatory — in this order)
1. Read docs/lessons-learned.md → standing rules (mandatory)
2. Read docs/PR-REVIEW-PROTOCOL.md → shared worker↔reviewer contract (mandatory)
3. Read docs/automation-scorecard.md → current coverage + parked backlog
4. Read STATUS.md → active Jira tickets + blockers
5. Read docs/session-memory.md → owner decisions and cross-session context (mandatory)
6. Check all open GitHub Issues for tasks/instructions left by the Reviewer:
   - Action any open issues assigned to Worker before starting new work
   - Close the issue once actioned
7. Check all open PRs for reviewer comments before opening any new branch:
   - Address MUST-FIX comments first — these gate the merge
   - NICE-TO-HAVE comments are advisory, merge can proceed without them
   - Push fixes to the existing PR branch, do not open a new PR

## "Status update" requests (standing definition — read this before answering any status-update ask)
When the owner asks for a **"status update"** (or "check PR status", "daily status", etc.) in chat,
this is NOT just re-running `scripts/update_status.py` (that only regenerates this repo's own
STATUS.md from git log — a narrower, separate routine). A "status update" means the full pull below,
even if the owner's phrasing only mentions one source — always cover all four unless told to narrow it:

1. **GitHub** — open PRs (state, CI checks, review comments) in `choongyin72/ChoongYin_OS`, plus any
   open Issues assigned to Worker (see mandatory step 6 above).
2. **Outlook calendar** — today's meetings via `outlook_calendar_search` (query `*`, `afterDateTime`/
   `beforeDateTime` = today's window). Convert returned times to MYT (UTC+8) for display.
3. **Outlook email** — today's emails via `outlook_email_search` (`afterDateTime: "today 00:00"`,
   `order: newest`). Flag anything actionable or urgent.
4. **Teams** — today's messages via `chat_message_search` (`afterDateTime: "today 00:00"`). If Graph
   rate-limits (429, partial scan), say so explicitly and offer a retry — don't silently drop it.

Present in this format (mirrors `tools/morning-briefing/run_briefing.py`'s scheduled 9am prompt):
```
☀️ Status Update — [Day, Date] | Woodside Pluto

📅 MEETINGS TODAY
[table/list, MY times, cancelled/tentative flagged]

📧 EMAILS
[flagged/actionable ones first, sender + key point]

💬 TEAMS HIGHLIGHTS
[key discussions/action items, or note the rate-limit if search was partial]

🚨 ACTION ITEMS
[pending/overdue items pulled from the above]
```
Fold in repo/PR status (item 1) either inline or as a closing section — don't drop it just because
the format above doesn't have a dedicated slot for it.

## Git workflow (mandatory — never commit directly to master)
1. At the start of every session, create a feature branch from master:
   `git checkout master && git pull origin master && git checkout -b feature/<task-name>`
   Use a descriptive name e.g. `feature/n3-va-suite`, `feature/financial-objects-parked`
2. Do all your work and commits on that branch
2a. **Before every push** (new PR or pushing fixes to an existing PR): sync with master first:
    `git fetch origin master && git merge origin/master`
    Resolve any conflicts, then push. (R8 — other PRs may have merged while your branch was open)
3. When the task is complete, raise a PR targeting master with this body format (every PR, no exceptions):
   - **What was built** — one sentence
   - **Files touched** — list
   - **DB ground-truth evidence** — live N/N pass count + exact DbVerify assertion used
   - **Self-clean confirmed** — yes/no
   - **Rules applied** — list R# from lessons-learned.md that were followed
   - **Base branch** — master (or `depends on #N` if stacked)
4. Do NOT merge yourself — the reviewer merges after MUST-FIX comments are resolved
5. Merge gate: reviewer will NOT merge a PR with open MUST-FIX comments
6. Stacked PRs: if your PR depends on #N, state it. Reviewer will not merge out of order

## During a long session (self-check rule)
After every 10 commits OR when resuming after a long pause, re-read
docs/lessons-learned.md to check for new rules added by the reviewer session.
Context compression does NOT re-read this file automatically — you must do it
explicitly. New rules from the reviewer take effect immediately when you read them.

## Why this matters
A reviewer session runs daily at 06:00 AWST and appends new rules to
docs/lessons-learned.md based on analysis of your recent commits. If you are
in a long-running session that started before 20:00, you will miss those rules
unless you re-read the file yourself mid-session.

---

GIT Project Folder   : C:\DEV\GIT\woodside_impl_pluto_12839
EC Web App Url       : https://app-plutodev.woodside-pluto.tieto-og.cloud/
EC WebUser Id        : sysadmin
EC Web User Password : Sysadmin@01
EC DB Url            : db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev
EC DB User Id        : ECKERNEL_EC
EC DB User Password  : energy

Java                 : C:\Tools\java\zulu21.36.17-ca-jdk21.0.4-win_x64
VS Code              : C:\Tools\Microsoft VS Code\Code.exe
Maven                : C:\Tools\maven\apache-maven-3.8.4-bin
Python               : C:\Tools\python\Python314
Notepad++            : C:\Program Files\Notepad++
# Verified Data Sources (2026-06-02)

## Project
- Woodside Git Repo : C:\DEV\GIT\woodside_impl_pluto_12839

## Web & DB
- EC Web App        : https://app-plutodev.woodside-pluto.tieto-og.cloud/ (user: sysadmin)
- EC Database       : db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev (user: ECKERNEL_EC)

## Tools (verified paths)
- Java 21           : C:\Tools\java\zulu21.36.17-ca-jdk21.0.4-win_x64\bin\java.exe
- Maven             : C:\Tools\maven\apache-maven-3.8.4-bin\bin\mvn
- Python 3.14       : C:\Tools\python\Python314\python.exe  (use `py` launcher)
- VS Code           : C:\Tools\Microsoft VS Code\Code.exe
- Notepad++         : C:\Program Files\Notepad++\notepad++.exe

# Client SharePoint (added 2026-06-02)
- Woodside Pluto Client SP : https://woodsideenergy.sharepoint.com/sites/PHBRQuorum

# Additional Verified Sources (added 2026-06-02)
- EC Hub (Nexus Repo) : https://hub.energycomponents.com/ (user: choong-yin.lee@tieto.com)
- EC Tech Docs 14.2.5 : https://hub.energycomponents.com/repository/site-hub/ec-application/14.2.5/documentation/Energy-Components/14.2.5/ecindex.html

# EC Best Practices (added 2026-06-03)
- EC Best Practices Confluence (BPR space): https://energycomponents.atlassian.net/wiki/spaces/BPR
- Cloud ID: energycomponents.atlassian.net
- Space: EC Professional Services - Best Practices & Sandbox
- Nickname: ECpedia | Launched: 1 April 2026 | 50+ pages
