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

### 3. ECpedia Index Scan — COMPLETE

**158 pages** fully scanned and mapped to all 9 EC deep dive sessions.

Key ECpedia findings:
- Launched April 1, 2026 — only 2 months old, some pages not yet "Verified"
- ⚠️ Only use pages marked **"Verified"** — others may be outdated
- 5 mandatory training sessions for PS team (EC SaaS, Extensions, Integrations, Scorecard)
- **EC SaaS Scorecard** — mandatory for all EC projects, 60+ items, blocking scores prevent go-live
- **TRAP process** — all customisations must follow Technical Review and Approval Process
- Sandbox environments: EC Upstream (Polar Bear) + EC Midstream — for hands-on learning
- Rich calculation engine pages (Library Calcs, Naming Conventions, Equation Blocks — all relevant for Session G)

### 4. ectestautomation Deep Dive — COMPLETE

**File saved:** `workstreams/master-plan/drafts/ectestautomation-deep-dive.md`

**Rating: 7.5/10** — 21 areas below 9/10 scheduled for sessions ET-A to ET-E

Key findings:
- Java 11 / Arquillian / Graphene / Cucumber — production-grade BDD framework
- 96 feature files, 90+ step classes, 113 page objects, 20+ test runners
- **CheckRulePage.java + ValidationOverviewPage.java** — Java constants confirm our DOM scan 100%
- `runAllButton` in `groups:form:runAllButton` ✅ confirmed working in production
- Wait values for EC: GUI=10s, AJAX=30s, Model=60s — proven in production
- Confirmation dialogs after every Save — must handle in Robot Framework Phase 2
- 9 test users configured for multi-user workflow testing
- Multi-user workflow pattern (User1 creates → User2 verifies → User3 approves)

**ectestautomation deep dive sessions (ET-A to ET-E) added to todo list**

---

## Key Files

| File | Location | Status |
|---|---|---|
| EC deep dive notes | `workstreams/master-plan/drafts/ec-application-deep-dive.md` | ✅ Complete |
| Phase 2 explore scripts | `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest\tests\validation\explore_*.py` | Reference only |
| DOM screenshots | `.../screenshots/issue_1052/` | Reference |
| EC Technical Docs raw | `ec_doc_p01-p10_*.txt` | In project root |

---

## Session F — Architecture and Database (2026-06-05, second run)

**Status:** COMPLETE — 4 items, all 7→9/10

### Items Covered

| # | Item | Before | After | Sources |
|---|---|---|---|---|
| 9 | JSF/PrimeFaces rendering | 7/10 | 9/10 | EC source: frmw-pf-jsf module |
| 10 | Screen template structure | 7/10 | 9/10 | EC source: ec-web/xhtml/screen/ |
| 11 | Flyway migrations deep | 7/10 | 9/10 | EC Tech Docs + ec-db-migration-oc-0 source |
| 12 | Journal tables _JN mechanics | 7/10 | 9/10 | EC source: ECDP_GENERATE + migration SQL |

### Key Learnings

**#9 JSF/PrimeFaces:**
- `OnAjaxReqListener` tracks all 6 JSF lifecycle phases for every AJAX request
- `EventDispatcher` is the central hub: `ECEvent → ECEventType → handler service`
- Three notification channels: AJAX partial re-render (immediate), polling (periodic, `ECPoll`), WebSocket push (`RemoteScreenNotifierService` → `f:websocket`)
- Dynamic `jsChannel` / `styleChannel` output panels allow server to push JS/CSS via AJAX

**#10 Screen Templates:**
- 5-file hierarchy: `screen_template.xhtml` → `screen.xhtml` → toolbar + notification + status_area
- `statusarea_tab:tabPanel:_sa_revisionInfo:form:T:0:C13_in` = REV_TEXT field (confirmed for Issue_1052)
- Confirmation dialog (modal `p:dialog`) is shared across all screens — reusable via `Confirmations` stack
- `p:remoteCommand` handlers: `postServerSideEvent`, `ecFocus`, `hotKeyPressed` are standard across all screens

**#11 Flyway:**
- V prefix = versioned (runs once), R prefix = repeatable (runs on checksum change)
- `owner_context_0` = core product; `flwy_schema_history_0` = migration audit table
- Naming: `V<version>.<date>__<ticket>_<description>.sql`
- `cleanDisabled=true` always — Flyway never drops production objects
- Custom resolvers support XML class definitions and JSON migrations
- PreUpgrade/PostUpgrade callbacks wrap every migration run

**#12 Journal _JN Triggers:**
- JN trigger fires ONLY when `rev_no` changes OR on DELETE (not every update)
- Class IUD trigger decides when to increment rev_no (per class journal rule)
- `ECDP_GENERATE.generate('TABLE', EcDp_Generate.JN_TRIGGERS)` auto-creates trigger
- `JN_NOTES` session parameter carries REV_TEXT into journal — must be set before DML
- EXT_JOIN extension tables must also have `_JN` table + trigger (often missed)

### Practical Impact on Woodside Work
- **Issue_1052 SQL**: When writing `REV_TEXT = 'ECPR-Issue1052'`, also set `JN_NOTES` via `EcDp_User_Session` for proper audit trail
- **Robot Framework**: `statusarea_tab` REV_TEXT locator confirmed from both source code and screen template structure
- **Flyway extensions**: Woodside's `R__XXXXX_CLASSNAME.xml` files follow standard EC Flyway repeatable pattern
- **EC source navigation**: `ec-db-migration-oc-0` is the right place to read migration history and trigger generation code
