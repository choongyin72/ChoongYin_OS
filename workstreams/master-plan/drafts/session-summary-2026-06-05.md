# Session Summary — 5 June 2026

**Date:** 2026-06-05
**Focus:** Phase 2 exploration + EC Application deep dive learning

---

## Completed Today

### 1. Phase 2 — EC Web App System Test Exploration (IN PROGRESS)

**Status:** DOM scan and screen exploration done. Waiting for user confirmation on PHD check group name in Validation Overview before building Robot Framework suite.

**What was explored:**
- Correct screen name: `Check Rule` (not Check Rules, not Maintain Check Rules)
- Navigation: sidebar search `menu:searchForm:searchTxt` + `label.tv-link` click
- Correct selectors confirmed from ec_keywords.robot keyword files
- Confirmed login: `#username`, `#password`, `#kc-login` (Keycloak)

**DOM findings from live screen capture:**
- Check Rule grid on page 7 shows all our 8 PHD rules (1143-1149)
- Rule 1142 (MOL_PCT) is on page 6
- WHERE_FORMULA is directly readable in grid column C4
- REV_TEXT in REVISION INFO tab: `statusarea_tab:tabPanel:_sa_revisionInfo:form:T:0:C13_in`
- Filter already ON for sysadmin — `check_rules:form:T:sfilter1_ft_filter`

**Validation Overview (CO.0203) — confirmed:**
- Screen name: `Validation Overview` ✅
- Date range: `nav:form:G:0:R:1:C:0:da_input` (From) / `nav:form:G:0:R:1:C:1:da_input` (To)
- Groups table: `groups:form:T`
- Logs table: `logs:form:T`
- **Run All button: `groups:form:runAllButton`** = "Run Selected Groups"
- Currently shows: 0 Errors, 0 Warnings for all groups on 2026-06-01 to 2026-06-06
- ECPD-166168 bug confirmed — CO.0203 unreliable for child group check rules

**Source code confirmed (ec-application repo):**
- `maintain_check_rules.xhtml` → `check_rules`, `variables`, `function_param`, `sub_query_var`
- `validation_overview.xhtml` → `groups`, `logs`, `runAllButton`, `nav`, `navButton`
- `CheckRulePage.java` → screen URL key: `CTRL_CHECK_RULES`
- `ValidationOverviewPage.java` → componentId: `DATA_VALIDATION_TTV`

**BLOCKED ON:** Which check group in Validation Overview contains PHD rules (STRM_COMP_ANALYSIS, STRM_ANALYSIS, TANK_DAY_DIP_STATUS). User checking.

**Phase 2 Test Cases (final plan):**
| TC | Action | Evidence |
|---|---|---|
| TC_UI_01 | Login verification | Screenshot: Dashboard |
| TC_UI_02 | EC version check | Screenshot: version |
| TC_UI_03 | Open Check Rule screen | Screenshot: screen loaded |
| TC_UI_04 | Page 6 — rule 1142 | Screenshot |
| TC_UI_05 | Page 7 — rules 1143-1149 | Screenshot |
| TC_UI_06 | Click all 8 rules — verify detail | Screenshot × 8 |
| TC_UI_07 | All 8 rules visible (filter PHD_) | Screenshot |
| TC_UI_08 | CO.0203 — set date 2026-05-26, Run All, screenshot errors | Screenshot |

**Screenshots saved:** `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest\tests\validation\screenshots\issue_1052\`

---

### 2. EC Application Deep Dive — COMPLETE

**Files saved:**
- `workstreams/master-plan/drafts/ec-application-deep-dive.md` — comprehensive learning notes

**Sources used:**
1. `C:\DEV\GIT\ec-application` — EC source code (XHTML, Java, SQL)
2. `https://hub.energycomponents.com/repository/site-hub/ec-application/14.2.5/documentation/` — Official EC Technical Docs 14.2.5

**Key learnings — from source code:**
- Architecture: Screenlet-Service-Model triangle
- 25+ screenlet types (Form, Table, Button, Chart, Network, etc.)
- Element ID pattern: `{screenletId}:form:{elementId}` — deterministic across all screens
- Check Rules: `CTRL_CHECK_RULES` + `CTRL_CHECK_RULE_VARIABLE` + `pck_gen_check`
- Events: `ECEvent` → `EventDispatcher` → service handlers → AJAX re-render
- Technology: JSF/PrimeFaces 15, WildFly 39, Keycloak 26, Oracle, Flyway 12, jBPM 7.74

**Key learnings — from official documentation:**

**Check Rules:**
- WHERE formula returns rows when validation FAILS
- `${variable}` = Constant / Attribute / Function call / Sub query
- Connected to screens via CO.0079 Check Group + CO.0080 Rule Group Combination
- `runAllButton` executes all rules in connected group

**Class Model (4 types):**
- Object = static physical entities (Well, Tank, Facility)
- Data = measurements owned by objects (daily readings)
- Interface = abstraction over multiple object classes
- Table = like Data but less framework support

**View Types (auto-generated from class definitions):**
- `OV_` = Object views (no delete)
- `DV_` = Data views (full DML)
- `IV_` = Interface views (UNION ALL)
- `TV_` = Table views
- `RV_` = Reporting views (READ ONLY — what we query in SQL)
- `IUD_` = Instead-of triggers

**ECIS (PHD integration) pipeline:**
```
PI Historian (PHD tags)
    ↓ PI Web API / PI JDBC Adapter
SOURCE STAGE: read tags → aggregate → DTOs
    ↓ JMS queue (800MB)
TARGET STAGE: map to EC class → UOM convert → INSERT/UPDATE
    ↓
RV_STRM_COMP_ANALYSIS, RV_STRM_ANALYSIS, RV_TANK_DAY_DIP_STATUS
```
- `LAST_TRANSFER` = last timestamp written; move to re-read history
- NULL values = PHD tag never sent data OR ECIS mapping not configured

**Data Model Standards:**
- Every table has 11 mandatory columns (RECORD_STATUS, CREATED_BY, REV_NO, **REV_TEXT**, REC_ID, etc.)
- `REV_TEXT` = where `ECPR-Issue1052` goes
- Sub-daily timestamps: DAYTIME + SUMMER_TIME + UTC_DAYTIME + PRODUCTION_DAY

**Extension naming rules (explains Woodside patterns):**
- `ZWP_` prefix = Woodside Pluto extension (hard-enforced by EC extension rules)
- `ZWT_` = another Woodside extension
- All extension DB objects, attributes, relations must use extension prefix

**EC knowledge rating: 8.5/10** (upgraded from 7/10)

---

## Pending Tasks (EOD 5 June 2026)

| # | Task | Status |
|---|---|---|
| Phase 2 RF tests | Build Robot Framework suite | 🔲 BLOCKED — waiting for PHD check group |
| 1 | Rebase ECPR-31030/31/32/34 | 🟡 Monitor — release team |
| 2 | Verify 1.0.37 in ECaaS TEST | 🔴 Pending |
| 3 | BLP Offtake Report | 🔴 Overdue |
| 4 | Raise ECPR R_BLP_MONTHLY_ALLOC_PLUTO | 🟡 Pending |
| 5 | Merge PRs #603–606 | 🟡 Monitor — release team |
| 6 | Reply to Grant — Issue_1052 | 🔴 Critical blocker |
| 7 | Daniel Perez UAT blockers | 🔴 Overdue |
| 8 | Issue_1052: 6 ECPR drafts A–F | ⏳ Waiting Grant |
| 9 | Morning Briefing automation | ⏳ Waiting IT admin approval |

---

## Key Files

| File | Location | Status |
|---|---|---|
| EC deep dive notes | `workstreams/master-plan/drafts/ec-application-deep-dive.md` | ✅ Complete |
| Phase 2 explore scripts | `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest\tests\validation\explore_*.py` | Reference only |
| DOM screenshots | `.../screenshots/issue_1052/` | Reference |
| EC Technical Docs raw | `ec_doc_p01-p10_*.txt` | In project root |
