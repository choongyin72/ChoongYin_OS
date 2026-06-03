# Full Session Summary & Backup — 2026-06-02
_All analysis, findings and summaries from today's Claude Code session_

---

## 1. Personal-OS Setup
- GitHub repo: https://github.com/choongyin72/ChoongYin_OS
- gh CLI v2.93.0 installed, authenticated as choongyin72
- Personal-OS scaffolded: STATUS.md, workstreams, scripts, scheduled tasks
- 4 workstreams: features-in-flight, reporting, production-stability, platform-ops
- Scheduled tasks: morning briefing (08:00), daily email summary (09:00), weekly meeting wrap-up (Wed 18:30), Monday digest (08:30)
- M365 connector active — Teams, SharePoint, Outlook, Calendar
- Oracle DB connected (ECKERNEL_EC), EC Hub connected

---

## 2. Project Status Summary
**File:** `workstreams/master-plan/drafts/project-summary.md`

- **Delivery confidence: RED**
- Calculations: 64% vs 82% target | Reports: 51% vs 80% target
- **1 July go-live AT RISK** — mid-July firm (Wave03 UAT 7 Jul, Wave04 UAT 16 Jul)
- Critical path: Onshore Monthly Commercial Allocation (29%) blocks 8+ reports
- CR28 active — Woodside retaining current team post go-live
- Dev complete: 22 June | Wave03 release ~9 June | Wave04 release ~23 June
- Co-location: Cato Perth 15 Jun–3 Jul, Shivani/Azila 14–24 Jun, JP 12–25 Jul

---

## 3. Today's Teams Activity (2 June 2026)
| Time AWST | Who | Update |
|-----------|-----|--------|
| 08:14 | Simon Lee | No CY + Grant this week. Release team unavailable. |
| 10:42 | Dinesh Agarwala | CI broken — extensions failing, asked Jamilin to fix |
| 12:01 | Ricardo | Asked Simon to approve PR #648 (scheduler changes) |
| 12:01 | Simon | Praised Ricardo, noted As-Built schedules tab not updated |
| 12:03 | Ricardo | Updated AsBuilt-01 Schedules tab |
| **13:15** | **Kirsten** | **NEW BLOCKER ECSR-35153 raised — tagged JP Dessart** |
| 18:18 | Joey Koh | Flagged ALLOC_F... issue needing attention |
| 19:09 | Dinesh | New PR #650 raised, asked Simon to review |
| 19:09 | JP Dessart | Agreed ALLOC_F... needs updating |

**KL public holiday today. Cato Johansen sick (2nd day).**

---

## 4. Your Task List
| # | Task | Status |
|---|------|--------|
| 1 | Rebase email notification branches to PCI_Release | Pending |
| 2 | Verify changes in 1.0.37-RC1 ECaaS TEST | Pending |
| 3 | Check BLP Offtake Report (0% dev, due 5 Jun) | Pending |
| 4 | Raise ECPR for R_BLP_MONTHLY_ALLOC_PLUTO arch fix | Pending |
| 5 | Merge PRs #603–606 (check Grant change requests first) | Pending |
| 6 | Issue_1052: Reply to Grant — ST vs UAT approach | Pending |
| 7 | Check 2 open UAT blockers (Daniel, 1 Jun) | Pending |
| 8 | Meeting input Wed 3 Jun | Done |

---

## 5. Issue_1052 — PHD Tag Validation Full Analysis

### Validation Status (661 active PHD tags since 1 Dec 2025)
| Category | Tags | % |
|----------|------|---|
| BOTH (Class Val + Check Rule) | 81 | 12% |
| Check Rule ONLY | 449 | 68% |
| Class Val ONLY | 0 | 0% |
| **NEITHER** | **131** | **20%** |

### 131 Unvalidated Tags by Class
| Class | Attribute | Count | Risk | Streams Affected |
|-------|-----------|-------|------|-----------------|
| STRM_COMP_ANALYSIS | MOL_PCT | 78 | CRITICAL | DBNGP Pipeline Export, HP/MP Fuel Gas GT4001-4004, 1C1401 to E1405A/B, Pluto Feed Ref, Train 1 HP N2 Vent |
| STRM_COMP_ANALYSIS | WT_PCT | 24 | CRITICAL | 1C1401 to E1405A/B, Flare Pilot A, Pluto-NWS Interconnector Export |
| STRM_ANALYSIS | GCV | 9 | HIGH | HP/MP Fuel Gas GT4001-4004, Flare Pilots A/B, Train 1 RTO |
| STRM_ANALYSIS | DENSITY | 6 | HIGH | HP/MP Fuel Gas GT4001-4004 |
| TANK_DAY_DIP_STATUS | AVG_TEMP/GRS_VOL/MEAS_STD_DENSITY/ZWP_GRS_MASS | 14 | MEDIUM | LNG T3101/T3102, Condensate T3301/T3302/T3303 |
| PWEL_DAY_STATUS | AVG_CHOKE_SIZE | 12 | LOW | Wells PLA01-08, PYA01, XNA01/02 |
| PWEL_DAY_STATUS | AVG_GAS_RATE | 9 | LOW | SCA wells 01-11 |
| STRM_DAY_STREAM_MEAS_WAT | ZWT_OILINWAT | 1 | LOW | Water Overboard |

### DB Findings (read-only Oracle query)
- ZWT_OILINWAT (PRP.00AI02631XR24.DACA.PV): FROM_UNIT = NULL, zero check rules
- N2 MOL_PCT (PGP.114QI207_FWA.DACA.PV): LAST_TRANSFER stuck 31-DEC-2025, no data received
- STRM_COMP_ANALYSIS: As-Built 05 specifies STRM_GAS_COMPONENT but DB uses STRM_COMP_ANALYSIS — different class, rules never fire

### 6 ECPR Drafts (File: ecpr-drafts-phd-validation.md)
| Draft | Focus | Priority |
|-------|-------|----------|
| A | STRM_COMP_ANALYSIS MOL_PCT + WT_PCT — add check rules | CRITICAL |
| B | STRM_ANALYSIS GCV + DENSITY — fix ZWP_PostPHDImport double-write | HIGH |
| C | TANK_DAY_DIP_STATUS — add check rules, update As-Built | MEDIUM |
| D | AVG_GAS_RATE — document + validate | MEDIUM |
| E | AVG_CHOKE_SIZE — add 0-100% range rule | LOW |
| F | ZWT_OILINWAT — set FROM_UNIT=mg/L, add rules | LOW |

### Reply to Grant Draft (Task 6)
- ST: verify config (tag mapping, check rules, unit conversion)
- UAT: verify actual PHD data quality (values in range, sums correct)
- Flag 4 DB issues found: NULL units, zero check rules, wrong class, N2 stuck
- CRITICAL caveat: EC 14.1.5.1 has check rule log bug (ECPD-166168) — Validation Overview unreliable

---

## 6. EC Hub Analysis (New Data Source)
- URL: https://hub.energycomponents.com/
- Credentials: choong-yin.lee@tieto.com / Xinyee!20090330
- Contains: EC documentation, release notes, ECIS technical docs, artifact repo

### Woodside EC Version: 14.1.5.1 (CONFIRMED)
Source: `extensions/extensions.properties` — `ec_version = 14.1.5.1`

### Missing Fixes — 14.1.6 (not installed)
| Fix | Description | Impact |
|-----|-------------|--------|
| ECSR-32880 ECIS timeout | API calls less likely to time out | PHD import reliability — may explain stuck N2 tag |
| ECPD-112165 | CALC_COLLECTION_DAILY class fix | Onshore allocation calculations |
| Security | Critical patches | Recommended |

### Missing Fixes — 14.1.7 (Dec 2025, not installed)
| Fix | Description | Impact |
|-----|-------------|--------|
| **ECPD-166168** | **Check rule log for child groups NOT updated when re-running validation** | **CRITICAL — Validation Overview screen unreliable. Affects Issue_1052 testing directly.** |
| ECIS memory | ec-messaging memory calculation improved | PHD daily job stability |
| Deferment rounding | Forecast using wrong date for rounding | Allocation accuracy |
| Security | Critical patches | Recommended |

### EC 14.2.5 (Latest — May 2026, 2 major versions ahead)
Notable features Woodside doesn't have:
- **Fitness Functions** — automated health checks (could replace manual Issue_1052 validation work)
- **REST API precision change** — full precision instead of 5dp fallback (risk if upgrading pre-go-live)
- **Client-side Data Validation for Stream Items** — relevant to STRM_COMP_ANALYSIS gap
- **Deprecation framework** — for custom ZWP_* classes

### My Recommendations
1. **Tell Grant:** EC 14.1.5.1 has known check rule child group bug. Validation Overview unreliable. Use DB queries to verify check rules (as we did).
2. **The N2 stuck LAST_TRANSFER may be ECIS timeout** (fixed in 14.1.6), not a missing tag. Check ECIS logs.
3. **Raise with team:** Should Woodside upgrade to 14.1.7 before go-live? Risk vs benefit discussion.
4. **Post go-live CR28:** EC upgrade to 14.2.x will be needed — plan for it.

---

## 7. Wednesday 3 June Meeting Prep
**File:** `workstreams/master-plan/drafts/meeting-input-2026-06-03.md`
**Meeting:** 15:00 AWST, Woodside Pluto Weekly Project Meeting (Kirsten organises)

Items to raise:
1. BLP Offtake Report — was 0% dev with 5 June target — status?
2. PCI branch rebase scope — which ECPRs go through PCI swimlane?
3. Wave 03 test data (SCA + T2) — ready from Cato/Simon?
4. UAT blockers — any new ones affecting reporting?
5. New blocker ECSR-35153 (Kirsten, today) — impact on Workstream H?

---

## 8. All Files Created Today
| File | Description |
|------|-------------|
| `workstreams/production-stability/issue-1052-phd-validation-analysis.md` | Gap analysis vs As-Built |
| `workstreams/production-stability/issue-1052-validation-status-table.md` | Structured table per category |
| `workstreams/production-stability/issue-1052-tag-list-full.md` | 661 tags individually listed (692 lines) |
| `workstreams/production-stability/issue-1052-tag-list.csv` | Excel-ready CSV |
| `workstreams/production-stability/ecpr-drafts-phd-validation.md` | 6 ECPR drafts |
| `workstreams/master-plan/drafts/meeting-input-2026-06-03.md` | Wed meeting prep |
| `workstreams/master-plan/drafts/project-summary.md` | Full project milestones |
| `workstreams/master-plan/drafts/session-summary-2026-06-02.md` | Earlier partial summary |
| `workstreams/master-plan/drafts/session-summary-2026-06-02-full.md` | This file — full backup |

---
_Session: 2026-06-02 | Claude Code Sonnet 4.6 | choong-yin.lee@quorumsoftware.com_

---

## UPDATE — 2026-06-03: Issue_1052 Deep Retrospective

### What Was Done
| Step | Done |
|------|------|
| Read defects image — understood scope | Done |
| DB analysis (661 PHD tags since 1 Dec 2025, read-only) | Done |
| Cross-referenced As-Built 09 (Validations) + As-Built 05 (Interfaces) | Done |
| Categorised 661 tags: BOTH/CR_ONLY/CV_ONLY/NEITHER | Done |
| Identified 131 NEITHER tags with object names and PHD tag IDs | Done |
| Found RV_ view column names for WHERE formula | Done |
| Wrote SQL migration script (3 code review iterations) | Done |
| Produced validation summary table, CSV, full tag list (692 lines) | Done |
| Drafted 6 ECPRs (A-F) | Done |

### What Was Learned
1. STRM_COMP_ANALYSIS != STRM_GAS_COMPONENT — As-Built 05 specifies STRM_GAS_COMPONENT but DB uses STRM_COMP_ANALYSIS. Mismatch between spec and implementation — check rules on STRM_GAS_COMPONENT never fire.
2. EC 14.1.5.1 bug (ECPD-166168) — Validation Overview screen unreliable for child group check rules. Must verify via DB query, not UI screen.
3. ZWP_PostPHDImport double-write risk — STRM_ANALYSIS DENSITY/GCV written by both schedule and PHD direct import. Conflict not yet resolved.
4. N2 MOL_PCT stuck (PGP.114QI207_FWA.DACA.PV) — LAST_TRANSFER stuck at 31-DEC-2025. Could be ECIS timeout bug (fixed in 14.1.6).
5. FROM_UNIT NULL matters — REST API precision change in EC 14.2.5 means untyped tags could produce inconsistent values post-upgrade.
6. RV_ view columns != attribute names — e.g. attribute GCV maps to GCV_MJPERSM3 in the view. Must use view column name in WHERE formula.
7. Simon Lee's standard — DELETE then INSERT OR UPDATE then INSERT — scripts must be re-runnable. Not MERGE.
8. REV_TEXT is mandatory — all Woodside extension scripts must reference ECPR ticket number (e.g. 'ECPR-31012').

### What Was Done WRONGLY
| Mistake | Fix Applied |
|---------|------------|
| Hardcoded CHECK_ID = 1142 — fails on different DB instances | Changed to SELECT NVL(MAX(CHECK_ID),0)+1 FROM CTRL_CHECK_RULES |
| INSERT only — not re-runnable, fails on duplicate key | Changed to UPDATE then if SQL%ROWCOUNT=0 then INSERT |
| Used MERGE — not Woodside style | Removed, replaced with pure UPDATE-then-INSERT |
| DBMS_OUTPUT.PUT_LINE included | Removed entirely |
| Missing REV_TEXT column | Added c_rev_text constant 'ECPR-Issue1052' (placeholder) |
| CV_ONLY = 0 but presented as if it existed | Should have stated upfront: no PHD tag has CV without CR |
| ECPR placeholder not a valid JIRA ticket | Needs real ECPR number before deploy |

### What Is NOT Covered / Still Open
| Gap | ECPR | Priority |
|-----|------|----------|
| Sum check 98-102% for MOL_PCT + WT_PCT | ECPR-A | CRITICAL |
| Frozen value check for new tags | ECPR-A | HIGH |
| ZWT_OILINWAT FROM_UNIT fix | ECPR-F | LOW (deferred) |
| STRM_ANALYSIS double-write investigation | ECPR-B | HIGH |
| AVG_CHOKE_SIZE check rule (12 tags) | ECPR-E | LOW |
| AVG_GAS_RATE doc + check rule (9 tags) | ECPR-D | LOW |
| SQL script NOT tested on dev DB yet | Task 9 | Next |
| Script NOT moved to Woodside project | Awaiting permission | Next |
| Proper Flyway filename (V1.0.37.xxxx__ECPR-XXXXX.sql) | After ECPR raised | Next |
| REV_TEXT still placeholder 'ECPR-Issue1052' | After ECPR raised | Next |
| Task 6 — Reply to Grant still not sent | Task 6 | Urgent |
| 6 ECPR drafts not raised in JIRA | Task 9 | Pending Grant |

### Priority Order — What's Next
1. Reply to Grant (Task 6) — unblock decision
2. Get real ECPR number — update c_rev_text in SQL
3. Test SQL on dev DB (write access)
4. Rename SQL file with proper Flyway version
5. Get permission before moving to Woodside project
6. Raise ECPR-A (sum check — 102 tags, most critical)
7. Investigate STRM_ANALYSIS double-write (ECPR-B)
