# Session Summary — 4 June 2026

**Date:** 2026-06-04
**Focus:** Issue_1052 Evidence Doc + WHERE_FORMULA fixes + Morning Briefing automation (paused)

---

## Completed Today

### 1. Issue_1052 — Evidence Doc v1.3
- Section 5.3 split into 8 separate TC tables
- TC01/TC02: Component No column added
- WHERE_FORMULA corrected: `<= 0` → `< 0` for TC03/TC04/TC08
- COPS DEV DB updated with correct formulas
- 220/220 unit tests PASS confirmed
- Section 5.3.2 added: correction note documented
- Document History: v1.3 entry

### 2. WHERE_FORMULA Corrections (COPS DEV DB)
| Rule | Before | After |
|---|---|---|
| PHD_STRM_ANALYSIS_DENSITY_VAL1 | `<= 0` | `< 0` |
| PHD_STRM_ANALYSIS_GCV_VAL1 | `<= 0` | `< 0` |
| PHD_TANK_DIP_STD_DENSITY_VAL1 | `<= 0` | `< 0` |
Reason: system initialises to 0.0, waiting for PHD. 0.0 is valid initial state.
Never assume spec conditions — always ask user first.

### 3. Key Learning Saved
- Never make assumptions on spec conditions/thresholds → always ASK first
- Saved to memory: `feedback_no_assumptions.md`

### 4. Morning Briefing Automation — PAUSED
- Azure AD app registered: `Morning Briefing` (client ID: 060468f7-48fa-4203-859e-9c1a7bb86704)
- Admin consent required — IT admin approval request submitted
- Scripts ready at: `C:\Projects\ChoongYin_OS\tools\morning-briefing\`
  - `config.json` — client ID, tenant ID, user email
  - `auth_setup.py` — one-time MSAL auth (run after IT approves)
  - `morning_briefing.py` — daily script: Graph API → HTML email → send to self
  - `smtp_setup.py` — SMTP auth setup (Option B, not used)
  - `morning_briefing_smtp.py` — SMTP version (not used — partial solution rejected)
- **Resume steps when IT approves:**
  1. Run `py auth_setup.py` → login in browser → saves token
  2. Test: `py morning_briefing.py` → verify email received
  3. Add to Task Scheduler at 08:30 AWST daily

---

## Active Pending Tasks

| # | Task | Status |
|---|---|---|
| 1 | Rebase ECPR-31030/31/32/34 | 🟡 Monitor — release team |
| 2 | Verify 1.0.37 in ECaaS TEST | 🔴 Pending |
| 3 | BLP Offtake Report | 🔴 Overdue |
| 4 | Raise ECPR R_BLP_MONTHLY_ALLOC_PLUTO | 🟡 Pending |
| 5 | Merge PRs #603–606 | 🟡 Monitor — release team |
| 6 | Reply to Grant — Issue_1052 | 🔴 Critical blocker for v1.0.38 |
| 7 | Daniel Perez UAT blockers | 🔴 Overdue since 1 Jun |
| 8 | Issue_1052: 6 ECPR drafts A–F | ⏳ Waiting Grant |
| 9 | Morning Briefing automation | ⏳ Waiting IT approval |

---

## Key Files

| File | Location | Status |
|---|---|---|
| Evidence doc | `sql-scripts/Issue1052_Evidence_COPS_DEV.docx` | v1.3 final |
| Evidence generator | `sql-scripts/update_doc_with_screenshots.py` | v1.3 |
| SQL script | `sql-scripts/Issue1052_PHD_Check_Rules.sql` | `< 0` corrected |
| Unit test script | `test-scripts/unit_test_check_rules.py` | 220/220 PASS |
| Morning briefing | `tools/morning-briefing/` | Paused — awaiting IT |

---

## Pluto Project Notes (4 June)
- v1.0.37 deployed to PROD — next version is v1.0.38
- Sandbox kept running out of DB space — COPS increasing storage
- ECaaS DEV PCI Swimlane refresh being discussed — ~4hrs downtime, likely Monday
- Jamilin: raise 2 JIRAs (CI refresh + ECaaS DEV refresh)
- Ricardo: PR #660 (Daily Validation Report template) pending Simon approval
- ECSR-35154 raised — Jean-Pierre looking into it
- Simon: off for the day after 17:57 MY
