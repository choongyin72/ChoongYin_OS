# OV Non-Bank Targets - the 55 OV-GM object screens beyond the 71

**Scope:** OV (`CLASS_TYPE=OBJECT`) screens NOT in the 71 Bank-layout list and not yet automated.
Grouped by NAVIGATOR pattern (owner's recipe `tmp/ov_gm_55_nav_recipe.xlsx`). Build order = easiest first.
Nav values resolved FIRST-AVAILABLE live (recipe gives the nav *shape*, not hardcoded P1/SS1).
Two OV flavours: **manage-object** (grid `manage_object_nav_nav:form:T_data` + GO) vs **custom-URL**
(grid `nav:form:T_data`, no GO, toolbar Refresh) - recon each; engine `click_go` now does GO-or-Refresh.

**Legend:** [x] done+verified · [~] driver-proven/partial · [ ] pending · (P) parked (reason) · (E) excluded (verified not buildable, permanent).

## A. No navigator (manage-object no-cascade OR custom-URL)  (17)
**Progress: 4/55 done.**

| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CD.0008 | Stream Item | OV_STREAM_ITEM | Assets > Stream Objects | [x] Custom-URL OV, live 3/3 Insert+Delete - shipped 2026-08-03 - Update out of scope (EC scheduler job UpdateStreamItem not configured, see Parked table) |
| CD.0109 | Document Sequence | OV_DOC_SEQUENCE | Assets > Revenue Document Objects | [x] #236 (custom-URL OV) |
| CO.0021 | Facility Class 2 | OV_FCTY_CLASS_2 | Assets > Facility Objects | (P) PERMANENT - sandbox config gap (owner-confirmed 2026-08-03: feature not enabled in this environment) - see Parked table |
| CO.0100 | Production Sub Unit | OV_PROD_SUB_UNIT | Assets > Basic Objects | (E) EXCLUDED 2026-08-03 - OV-GM groupmodel not enabled; insert persists in DB but grid never lists it (verified 2026-07-27, see Parked table + [[reference_ec_groupmodel_not_enabled]]) - cannot verify via UI, permanently excluded |
| CO.0102 | Constant Standard | OV_CONSTANT_STANDARD | Assets > Hydrocarbon Objects | [x] TV-style, live 4/4 - shipped 2026-08-02 - was a menu-text case-sensitivity bug, not a real gesture gap - see Parked table |
| CO.0158 | Report Group | OV_REPORT_GROUP | Assets > Facility Objects | [x] plain OV, live 4/4 |
| CO.0191 | Task Process | OV_TASK_PROCESS | Task List | [x] #236 (custom-URL OV) |
| CO.0193 | Action Trigger | OV_CONTROL_POINT | Business Action | [x] custom-URL OV, live 7/7 (shipped 2026-08-01) |
| CO.0227 | External Location | OV_EXTERNAL_LOCATION | Assets > Facility Objects | [x] OV-GM GO-only, live 8/8 (shipped 2026-08-01) |
| CO.0264 | Truck | OV_TRUCK | Assets > Transport Objects | [x] #277 (plain OV) |
| CO.0265 | Trailer | OV_TRAILER | Assets > Transport Objects | [x] #279 (plain OV) |
| CO.0266 | Driver | OV_DRIVER | Assets > Transport Objects | [x] #281 (plain OV) |
| CO.1033 | Production Day Table | OV_PRODUCTION_DAY | System | [x] TV-style grid, live 1/1 Insert-only - shipped 2026-08-03 - Delete does not exist by design (owner-confirmed, see Parked table) |
| CO.1049 | Conversion Group | OV_CONVERSION_GROUP | System > Units | [x] #236 (custom-URL OV) |
| CO.1060 | Calculation Library | OV_CALC_LIBRARY | Assets > Calculation Objects | [x] #236 (custom-URL OV) |
| CO.2038 | Contract Area Setup | OV_CONTRACT_AREA_SETUP | Assets > Contract Objects | [x] custom-URL OV, live 7/7 (shipped 2026-07-30) |
| FC.0010 | Forecast | OV_FORECAST_GROUP (UNCONFIRMED - see Parked table, likely wrong) | Forecasting | (P) class resolution mismatch, self-cleaned via UI - see Parked table |

## B. Production Unit + Area + Facility Class 1  (20)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CD.0006 | Node | OV_NODE | Assets > Calculation Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0034 | Storage | OV_STORAGE | Assets > Tank and Storage Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0040 | Test Separator | OV_TESTSEPARATOR | Assets > Facility Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0042 | Production Separator | OV_PRODSEPARATOR | Assets > Facility Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0049 | Well | OV_WELL | Assets > Well and Reservoir Objects | [x] OV-GM SPECIFIC-P1 nav, live 8/8 (shipped 2026-07-30) |
| CO.0051 | Well Hole | OV_WELL_HOLE | Assets > Well and Reservoir Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-31) |
| CO.0070 | Chemical Tank | OV_CHEM_TANK | Assets > Chemical Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0108 | Well Hookup | OV_WELL_HOOKUP | Assets > Facility Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0123 | Test Device | OV_TEST_DEVICE | Assets > Equipment Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0212 | Chemical Injection Point | OV_CHEM_INJ_POINT | Assets > Chemical Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0224 | Shift | OV_SHIFT | Assets > Facility Objects | [x] OV-GM + mandatory free-text Start Time, live 8/8 (shipped 2026-07-31) |
| CO.0258 | Chemical Stream | OV_CHEM_STREAM | Assets > Chemical Objects | [x] OV-GM + From Connection POPUP, live 8/8 (shipped 2026-07-30) |
| CO.0260 | Chemical Stream Hookup | OV_CHEM_STRM_HOOKUP | Assets > Chemical Objects | [x] OV-GM, live 4/4, mandatory-field gate |
| CO.2004 | Lifting Account | OV_LIFTING_ACCOUNT | Assets > Transport Objects | [x] OV-GM 4-level nav, live 8/8 (shipped 2026-07-30) |
| CO.2077 | Channel | OV_CHANNEL | Assets > Transport Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.2078 | Loading Arm | OV_LOADING_ARM | Assets > Transport Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.2079 | Pilot | OV_PILOT | Assets > Transport Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-31) |
| CO.2080 | Tug Boat | OV_TUG_BOAT | Assets > Transport Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.2081 | Pilot Boat | OV_PILOT_BOAT | Assets > Transport Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CP.0030 | Cargo Planning Forecast | OV_FCST_MNGR_FCST_LIST | Cargo Planning > Forecast | [x] custom forecast-manager OV, live 8/8 (shipped 2026-07-31) |

## C1. Business Unit only  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2103 | Service | OV_SERVICE | Assets > Service Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-08-01) |
| CO.3009 | Price Index | OV_PRICE_INDEX | Assets > Sales Objects | [x] OV-GM, live 4/4 - was a test-data date mismatch, not a bug - see Parked table |
| CO.3016 | Price Object | OV_PRICE_OBJECT | Assets > Sales Objects | [x] OV-GM, live 4/4 full I-U-D - shipped 2026-08-03 - was a missing Business Unit scope binding, not a pager bug - see Parked table |
| CO.3024 | Price Rate | OV_PRICE_RATE | Assets > Sales Objects | [x] OV-GM, live 4/4, BU=SS2 BU (parent_dd worked here) |
| SP.0059 | Property | OV_PROPERTY | Assets > Data Mapping Objects | [x] OV-GM, live 4/4 - #329 - was a test-data date mismatch, not a bug - see Parked table |

## C2. Business Unit + Contract Area  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2016 | Contract | OV_CONTRACT | Assets > Contract Objects | [x] OV-GM, live 4/4, BU=TS5 BU (single-page scope, avoided pager bug) |
| CO.2044 | Contract Capacity | OV_CONTRACT_CAPACITY | Assets > Contract Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-08-01) |
| CO.2054 | Contract Inventory | OV_CONTRACT_INVENTORY | Assets > Contract Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-08-02) |
| RC.0058 | Division Order | OV_DIVISION_ORDER | Royalty > Royalty USA | [x] OV-GM, live 4/4 - shipped 2026-08-02 - was previously misclassified as TV - see Parked table |
| RC.0059 | Royalty Contract | OV_ROYALTY_CONTRACT | Royalty > Royalty Canada | [x] OV-GM gated-nav, live 3/3 RF + 7/7 Playwright - shipped 2026-08-15, **Insert+Update only** (Delete permanently out of scope, EC-genuine child-record defect, closes Issue #336) - see Parked table |

## D. Production Unit + Area  (3)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0019 | Facility Class 1 | OV_XFCTY_CLASS_1 | Assets > Facility Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-07-30) |
| CO.0205 | Collection Point | OV_COLLECTION_POINT | Assets > Facility Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-08-01) |
| CO.0244 | Operator Route | OV_OPERATOR_ROUTE | Assets > Facility Objects | [x] OV-GM, live 4/4, PROVEN nav (P3 PU/Area) |

## E. Well hierarchy  (2)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0054 | Well Bore | OV_WELL_BORE | Assets > Well and Reservoir Objects | [x] OV-GM per-field nav + Well POPUP, live 8/8 (shipped 2026-07-31) |
| CO.0247 | Planned Well | OV_PLANNED_WELL | Assets > Well and Reservoir Objects | (P) wrong-class insert, self-cleaned - see Parked table |

## E3. Well hierarchy (deepest)  (2)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0057 | Well Bore Interval | OV_WELL_BORE_INTERVAL | Assets > Well and Reservoir Objects | [x] OV-GM 6-group nav + Well Bore POPUP, live 8/8 (shipped 2026-07-31) |
| CO.0153 | Perforation Interval | OV_PERF_INTERVAL | Assets > Well and Reservoir Objects | [x] OV-GM 7-group nav + POPUP + dd, live 8/8 (shipped 2026-07-31) |

## F. Functional Area  (1)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0236 | Message Group | OV_MESSAGE_GROUP | Messaging | [x] OV-GM, live 4/4 - was a test-data date mismatch, not a bug - see Parked table |

## Group A live flavour classification (2026-07-27, read-only grid probe + verify)
**CORRECTED after a live build attempt** (Production Sub Unit): the initial batch probe only checked two
grid ids (`manage_object_nav_nav:form:T_data`, `nav:form:T_data`). Screens showing `grid=? go=True` are
actually **OV-GM** with a THIRD grid id `manageObject:form:T_data` (navigator-scoped, GO reload, lazy
redraw). Proof: Production Sub Unit inserted OK (row persisted in `OV_PROD_SUB_UNIT`) but the grid re-check
failed; a follow-up probe found grid = `manageObject:form:T_data`, and `select_row` could not find the row
(navigator-scoped). So **"no navigator" in the recipe != plain manage-object.** OV-GM screens -> **Phase 2**
(need grid_id=`manageObject:form:T_data` + GO reload + lazy-redraw wait R17 + insert parent-dd = nav scope).
Only the **custom-URL** ones build with current tooling.

> WARNING: the 'Flavour' column below started as a 2026-07-27 BATCH GUESS. Four rows
> (Truck/Trailer/Driver/Report Group) were labelled OV-GM and proved to be plain OV on
> contact - issue #278 came from trusting it. Treat any row without 'PROVEN' as a
> hypothesis and SCAN the screen first.

| BF | Screen | Flavour | grid_id | Phase |
|---|---|---|---|---|
| CO.1049 | Conversion Group | custom-URL | nav:form:T_data | **DONE #236** |
| CO.1060 | Calculation Library | custom-URL | nav:form:T_data | **DONE #236** |
| CO.2038 | Contract Area Setup | custom-URL | nav:form:T_data | 1 (buildable now) |
| CD.0109 | Document Sequence | custom-URL | nav:form:T_data | **DONE #236** |
| CO.0193 | Action Trigger | custom-URL (POPUP refs) | nav:form:T_data | (P) popup-picker capability (AT_TYPE_POPUP/TRIGGER_TYPE_POPUP mandatory) |
| CO.0191 | Task Process | custom-URL | nav:form:T_data | **DONE #236** |
| FC.0010 | Forecast | custom-URL | nav:form:T_data | (P) end-date-on-insert ADDED to generator, but FORECAST_TYPE (DB NOT NULL) also mandatory; filling Forecast Type first-available still rejected at Save (likely popup-picker, not dropdown) - 2 attempts, parked 2026-07-27 |
| CO.0100 | Production Sub Unit | **OV-GM, groupmodel NOT enabled** (VERIFIED 2026-07-27, not a batch guess) | manageObject:form:T_data | (E) EXCLUDED - insert persists in `OV_PROD_SUB_UNIT` but grid never lists it; cannot verify via UI - see Parked table |
| CO.0021 | Facility Class 2 | plain OV (single Date nav, no cascade/dropdown/popup - the 2026-07-27 OV-GM guess was WRONG) | manageObject:form:T_data | (P) PERMANENT - sandbox config gap, owner-confirmed 2026-08-03, not buildable in this environment regardless of navigator family - see Parked table |
| CO.0158 | Report Group | **plain OV** (PROVEN live 2026-07-31) | report_group_table:form:T_data | **DONE** - verify_screen PASS (RF 4/4 + PW 8/8) |
| CO.0227 | External Location | **OV-GM** | manageObject:form:T_data | 2 (needs capability) -- **UNVERIFIED 2026-07-27 batch guess**; siblings in this block (Truck/Trailer/Driver/Report Group) all turned out plain OV, so SCAN before building. |
| CO.0264 | Truck | **plain OV** (PROVEN live, shipped) | manage_object_nav_nav:form:T_data | **DONE #277** |
| CO.0265 | Trailer | **plain OV** (PROVEN live, shipped) | manage_object_nav_nav:form:T_data | **DONE #279** |
| CO.0266 | Driver | **plain OV** (PROVEN live, shipped) | manage_object_nav_nav:form:T_data | **DONE #281** |
| CO.0102 | Constant Standard | custom-URL grid cstandard:form:T_data | (P) standard New-Object menu gesture times out (custom toolbar) - needs individual insert-gesture recon; 2026-07-27 |
| CD.0008 | Stream Item | (P) no :T_data grid renders on open (different layout / didn't open) - needs individual recon; 2026-07-27 |
| CO.1033 | Production Day Table | custom-URL grid production_day:form:T_data | [x] Insert-only, shipped 2026-08-03 - no physical delete exists on this screen by design (owner-confirmed) |

## OV-GM batch investigation (2026-07-27) - grid-never-lists blocker
Attempted the OV-GM capability starting with the simplest case, **Production Sub Unit (CO.0100)**:
- Navigator = **Date + GO only** (no BU/PU/Area cascade) - so it's a date-scoped OV-GM, grid `manageObject:form:T_data`.
- Insert **persists** in `OV_PROD_SUB_UNIT` (DB-verified) and `insertObjectRecord` runs GO after Save, BUT the
  grid shows **"No records found" at every nav Date** (tested today + 2005). The row never lists.
- This matches the known EC behavior [[reference_ec_groupmodel_not_enabled]]: an OV-GM screen with the group
  model NOT enabled accepts inserts but the grid never lists them -> **cannot verify via the grid; exclude**.
- Self-cleaned all AUTOTEST_PSU rows via End=Start (DB-verified 0 residual).

**Implication for the OV-GM batch (Groups A-OVGM 7, B 20, C 10, D 3, F 1 = ~41):** each needs a per-screen check
of whether its group model is enabled (grid lists inserts) BEFORE building - do NOT assume. Gated ones (B/C/D)
additionally need the BU/PU/Area/Facility cascade filled + parent-dd = nav scope. This is genuine capability
R&D, not a quick build. **PARKED pending a dedicated OV-GM capability session.**

### Parked this session (2026-07-27, verified reasons - skip-and-park)
| Screen | Reason |
|---|---|
| Production Sub Unit (CO.0100) | **MARKED EXCLUDED 2026-08-03 (owner-directed) - not re-investigated, same verified finding stands.** OV-GM grid never lists inserts (groupmodel-not-enabled); DB persists. This was already correctly diagnosed and self-cleaned on 2026-07-27 (matches the documented EC behavior [[reference_ec_groupmodel_not_enabled]]: an OV-GM screen with the group model NOT enabled accepts inserts but the grid never lists them - cannot verify via the grid). The two summary-table rows (Group A + Group A live-flavour classification) had gone stale, still showing `[ ]` pending / "UNVERIFIED batch guess - SCAN before building" despite this screen's actual status having been settled weeks earlier - corrected both to the `(E) excluded` marker introduced in this pass. No live testing repeated; this is a doc-accuracy fix only. |
| Forecast (FC.0010) | **RE-ATTEMPTED 2026-08-02, STILL PARKED - NEW blocker, original reason superseded.** The original park reason (FORECAST_TYPE DB NOT NULL + likely-popup-picker, Save rejected) did NOT reproduce on retry - Forecast Type shows as NOT mandatory on live scan, and 5 test inserts leaving it blank all succeeded (Insert + Update + Delete all worked via the standard `objectdates`/`updateAttributes` OV gestures, confirmed live, self-cleaned via `closeObjectRecord()`, 0 residual). **The actual blocker found this round: `resolve_ec_screen.py`'s class resolution is WRONG for this specific BF code.** The tool resolves screen label "Forecast" -> class `FORECAST_GROUP` via `class_property_cnfg` (the ONLY class with that exact LABEL, confirmed - no ambiguity like Division Order had), but the live screen's data does NOT land in `FORECAST_GROUP` or `OV_FORECAST_GROUP` (checked both, fresh connections, twice - genuinely 0 matching rows even while the test data was live in the UI grid). The screen's own content-frame URL is `com.ec.tran.fc.screens/forecast` (a dedicated custom module, distinct from a generic Manage-Object screen), and its insert form is internally named `new_fcst` (not the standard `objectForm`) - both signals that this BF code (FC.0010, treeview key `TRAN_FC_CREATE`) is bound to a DIFFERENT underlying class than what LABEL-based lookup finds. Root cause NOT isolated (the real base table/view was not identified despite substantial live+DB investigation - searched FCST_MEMBER and other FCST_* candidates, no match); stopped rather than keep grinding on table identification alone. Self-clean confirmed via the UI (0 rows left visible in the grid) even without knowing the true table name. **Next step if resumed:** capture the actual PrimeFaces AJAX request/response during Save (network intercept) to read the real bound class from the server's own response, rather than guessing table names. |
| Constant Standard (CO.0102) | **RESOLVED + SHIPPED 2026-08-02.** The "COPY control unreachable" finding from the prior attempt was a wrong turn - the COPY mechanism is a SEPARATE secondary feature, not the real Insert path. **Real root cause: the Insert menu item's VISIBLE text ("CONSTANT STANDARD", all caps) is NOT its real DOM text - the actual text is "Constant Standard" (title case), the all-caps rendering is pure CSS `text-transform`.** Every earlier attempt (including the original 2026-07-27 park and the same-day COPY-mechanism detour) searched for the all-caps string and silently failed to match. Also found: both the Insert AND Delete icons have an identically-worded submenu item - must scope the xpath to the specific icon's own `<li class="ui-menu-parent">` ancestor (this project's own `table_class.resource` already documents this exact gap). Confirmed this IS a genuine TV-style inline-editable grid (`cstandard:form:T_data`) with a proven blank-row insert (fill Standard Code/Standard Name/Start Date/**Daytime** - a separate mandatory field) and a date-effective close (`End Date = Start Date` in the inline C3 cell, NOT the toolbar Delete button - this class IS `VERSIONED` despite the TV-looking grid). Built a bespoke driver (doesn't fit `gen_ovgm.py`) + T3 reusing shared T1 keywords. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright 7/7). Full bundle shipped, 0 residual. **This root cause (case-sensitivity + wrong-<li>-scope) is expected to directly unblock Stream Item and Production Day Table too, which share the identical toolbar shape and symptom.** |
| Stream Item (CD.0008) | **RESOLVED + SHIPPED 2026-08-03 (Insert + Delete only).** The "Copy-based insert mechanism" finding from the 2026-08-02 re-attempt was a wrong turn (same class of wrong turn as Constant Standard's original COPY detour) - the real Insert path is the standard `ec._open_new_object()` flow, which was already correctly cased on this screen (title-case "New Object"/"New Version", no CSS-uppercase illusion). The non-standard GO button id (`buttongo:form:B`, confirmed in the prior round) is handled by a local wrapper in both the driver and T3 rather than a shared-engine fix. **Two NEW findings this round:** (1) the 12 fields the Save-error lists with `[..._POPUP]`-style brackets are ordinary autocomplete DROPDOWNS (`dd_input`), not "Pick from EC Object" popups - `__FIRST__` on each satisfies Save; (2) Name is server-derived - confirmed against EC's own online help page (*"the Name attribute can be left blank for the system to automatically generate the Name"*) - any typed value is discarded, confirmed 3x including typing it last, right before Save. **Genuine blocker found and accepted, not fixed:** any Save on `updateAttributes` fails with EC's own error "Cannot run schedule job UpdateStreamItem because it has not been configured" - EC's own online help documents this as a real feature (BF VO.0031 - Daily SI Pending Calculation, a background recalculation job triggered by core-attribute changes) that is simply not configured/enabled in this sandbox. Reproduced live 3x, twice headed with the owner watching directly. **Owner instruction 2026-08-02: skip Update, ship Insert + Delete only.** Also hit (and fixed) the 4th confirmed instance of the reference-dropdown date-scope bug ([[feedback_child_object_date_must_follow_parent]]) - the RF suite's `${START_DATE}` was wired to the plain `${TEST_START_DATE}` (2000-01-01) instead of `${TEST_START_DATE_REFDD}` (2003-01-01); 2 live RF failures looked like a flaky dropdown-panel timeout until a screenshot review showed the panel correctly said "No records found". Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 3/3, live RF 3/3, Playwright driver 6/6). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. **This root cause (case-sensitivity was NOT the issue here, unlike Constant Standard/expected for Production Day Table) confirms the toolbar-mystery batch had at least 2 distinct root causes, not one shared cause - re-verify Production Day Table's own Insert mechanism fresh rather than assuming the Constant Standard fix applies unchanged.** |
| Production Day Table (CO.1033) | **RESOLVED + SHIPPED 2026-08-03 (Insert only, permanently).** The "Insert toolbar icon does nothing" finding from the 2026-08-02 re-attempt was a wrong turn (a stale/incomplete recon - the menu item "Production Days" IS clickable and already correctly title-cased on this screen, confirmed via raw `onclick`/`textContent`; no CSS-uppercase illusion, unlike Constant Standard). Deliberately did NOT assume Constant Standard's/Stream Item's fixes applied here (per Stream Item's own JOURNAL note) - correct call, since this screen's real blockers were 3 entirely distinct issues: (1) filling Object Code via `.fill()`/synthetic-set silently breaks the NEXT cell's autocomplete dropdown from ever rendering - fixed with real keystrokes+Tab (`Type Cell By Id`, this project's own established inline-grid convention); (2) DB commit visibility measured ~8s slower than every other screen built so far (timed test: not visible at t+0/1/2/3/5s, visible at t+8s) - the driver/T3 use a generous 10s post-Save wait; (3) RF's `Evaluate JavaScript` trailing-argument form silently passes `undefined` into the JS function on this project's setup - fixed by inlining the value via `${VARIABLE}` string substitution into the JS source (matching `allocation_run.resource`/`popup.resource`'s own established pattern), after a full live RF failure ("No blank row after Insert" on a row that genuinely existed). **DELETE DOES NOT EXIST ON THIS SCREEN - confirmed by the owner directly, live, 2026-08-03**: "no deletion is allow in Production Day Table screen... Production Day Table set object end date its not trigger delete record as its implementation are different than other objects implementation." Independently exhausted 6+ distinct row-selection gestures first (cell/td/tr/edge click, fresh-reload-then-click, tested on 3+ pre-existing real rows not just test data) - toolbar Delete never enabled regardless; End Date = Start Date does NOT remove a row from `OV_PRODUCTION_DAY` either (confirmed via DB - no date-range filter, consistent with `TIME_SCOPE_CODE=INVARIANT`). **Self-clean is impossible by design** - owner decision 2026-08-03: accept permanent test residual (same precedent as Royalty Contract's `CNTR_PG_SETUP` rows) rather than skip the screen or restrict to a single-ever run; 8 `AUTOTEST_PDT_*` rows permanently live in the sandbox as of this build (2 from pre-confirmation diagnostics, 6 from driver/suite proof runs). Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 1/1, live RF 1/1, Playwright driver 5/5). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map. **Confirms the "toolbar mystery" batch (Constant Standard/Stream Item/Production Day Table) had 3 DIFFERENT root causes across 3 screens, not one shared cause - a lesson worth remembering for any future "these screens look similar so the same fix should work" assumption.** |
| Message Group (CO.0236) | **RESOLVED + SHIPPED 2026-08-02** (retried on `feature/retry-message-group-iud`). Original park reason: insert PERSISTS but lands in WRONG SCOPE (Functional Area dropdown pick mismatch: requested option 1 'Administration', persisted option 2 'Allocation'), suspected as the shared `select_dropdown`/`Fill OV Dropdown By Label` engine (used by 22 OV-GM screens). **Real root cause: the same test-data date mismatch as Property/Price Index/Royalty Contract - 4th confirmed instance** - the generator config had NO `start_date` set at all (defaulting to `2000-01-01`), but "Administration" (`ADM`) is only effective from `2001-01-01` onward. Fixed by setting `start_date: "2003-01-01"` in `tmp/cfg_message_group.json` - no shared-engine change needed. Explicitly re-verified `FUNCTIONAL_AREA_CODE = 'ADM'` persisted correctly (not just Name). Also RESOLVES the "NOT confirmed systemic" open question from the original entry - Area's `parent_dd` validation (7/7) never hit this because its own values happened to already be date-compatible, not because a different mechanism was in play; both `parent_dd` and `extra_dropdowns` share the identical date trap. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS). Full bundle shipped, 0 residual. See [[feedback_child_object_date_must_follow_parent]]. |
| Facility Class 2 (CO.0021) | **ROOT CAUSE CONFIRMED 2026-08-03 (owner) - genuine sandbox configuration gap, NOT built.** Re-investigated a 3rd time (fresh recon, no assumptions carried over from the 2026-08-02 investigate-only round): confirmed the navigator is a PLAIN single Date field (`nav:form:G:0:R:1:C:0:da_input`) with no dropdown, no popup/pin field, and no "Finder" button anywhere on the page - the "Finder" hypothesis from the prior round does not hold up; there simply is no such control on this screen. Reproduced the exact same defect live (headed, owner-observed twice): Insert succeeds with no error banner, the row genuinely persists in `OV_FCTY_CLASS_2` with the correct date, but the grid's own server-side widget config reports `rowCount: 0` (confirmed via `PrimeFaces.widgets['manageObject_wv'].cfg.paginator`) - this is a genuine server-side query mismatch, not a client rendering bug. Ruled out a 4th candidate cause this round (RECORD_STATUS/approval state - the test row's `RECORD_STATUS='P'` is identical to every other screen's rows, including working ones like Bank - not the differentiator). **Owner confirmed the real root cause directly**: "its configuration issue. to turn on FCTY_CLASS_2 usage its need some special setting to be set. but this sandbox is not ready for it" (verified via `SELECT OBJECT_ID FROM OV_FCTY_CLASS_2` returning legitimate rows that the UI still can't list). This class requires a sandbox-level enablement setting that isn't configured here - not a code defect, not a missing capability, not fixable from the automation side at all. Self-cleaned all 4 `AUTOTEST_FC2_*` rows accumulated across this investigation via the OV view's own End=Start UPDATE (owner-authorized explicitly, since the UI cannot select an invisible row to close it normally) - confirmed 0 residual via the owner's own query. **No bundle shipped - permanently out of scope until the sandbox's FCTY_CLASS_2 feature is enabled at the environment level (owner/EC-admin action, not an automation task).** |
| Planned Well (CO.0247) (2026-08-01) | OV-GM (grid `manageObject:form:T_data`), 5-level cascade nav; PU/Area/Facility Class 1 = PROVEN P1 values (same scope Well/CO.0049 uses), deeper 2 levels left empty per Well's precedent. Insert via the toolbar's "New Object" gesture landed in the WRONG class entirely - `OV_WELL` (`CLASS_NAME='WELL'`), not `OV_PLANNED_WELL` (`CLASS_NAME='PLANNED_WELL'`, confirmed by reading the view SQL - both classes share the SAME base `WELL`/`WELL_VERSION`/`WELL_PERIOD_STATUS` tables, discriminated only by `CLASS_NAME`). The 2 misplaced rows also had ALL scope columns NULL (`OP_PRODUCTIONUNIT_CODE`/`OP_AREA_CODE`/`OP_FCTY_1_CODE` etc.), so they were orphaned regardless of class - the "New Object" gesture on this screen does not bind the nav scope into the new record the way it evidently does on Well's own screen. Root cause not fully isolated (menu-item disambiguation vs a Planned-Well-specific scope-binding gap) - stopped at the 2-attempt limit. Self-cleaned via direct SQL DELETE (child-first: `WELL_PERIOD_STATUS` -> `WELL_VERSION` -> `WELL`, scoped by OBJECT_ID, read in full before delete) since the mis-scoped rows were unreachable via any UI and a raw End=Start close was blocked by `FK_WELL_PERIOD_STATUS_2`. 0 residual confirmed. No bundle shipped. |
| Price Index (CO.3009) | **RESOLVED + SHIPPED 2026-08-02** (retried on `feature/retry-price-index-iud`). Original park reason: the New-Object form's 2nd dropdown in sequence (Frequency, then Business Unit/`parent_dd`) silently persisted `SS1_BU` instead of the requested `Royalty Canada`/`ROYALTY_CA`, reproduced 3 times and suspected as a shared-engine widget-state defect. **Real root cause: the same test-data date mismatch found on Property** - `start_date` was `2000-01-01`, but "Royalty Canada" (`ROYALTY_CA`) is only effective from `2003-01-01` onward, so the reference dropdown correctly excluded it and the fallback landed on a different available option. Fixed by changing `tmp/cfg_pi.json`'s `start_date` to `2003-01-01` - no shared-engine change needed, resolved on the first retry. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright 8/8). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. See [[feedback_child_object_date_must_follow_parent]]. NOTE (unchanged from the original park entry): this may also affect Area's `parent_dd` mechanism if that screen's form ever gains a second dropdown before the parent_dd one - not retested this round. |
| Price Object (CO.3016) | **RESOLVED + SHIPPED 2026-08-03 (full I-U-D).** OV-GM, insert persists correctly but was never found under the "ECP Norway" scope. **CORRECTED 2026-08-02 (re-investigated for issue #321)**: the original "pager-walk click times out" characterization does NOT hold up under repeated, careful re-testing - the pager mechanism itself walked all 5 real pages in <1s each, twice, with zero hangs. Reproducing the EXACT original scenario (insert with Business Unit deliberately left unset, then immediately `wait_for_row`) gave a clean 44s-then-`False` result, not a `TimeoutError` - because the row genuinely has no `BUSINESS_UNIT_CODE`, so it is NOT VISIBLE under any page of a BU-scoped grid. This is the SAME missing/wrong-scope defect class as Message Group and Planned Well, not a distinct pagination-mechanism bug. See issue #321's comment thread for the full re-investigation; no shared-engine change was made (nothing to fix - see also PR #326, unrelated, which fixed a real `ec_error()` gap found the same day). Self-cleaned x3 (2 original + 1 re-repro), 0 residual each time. **2026-08-03: built the actual fix** using `gen_ovgm.py`'s `parent_dd="Business Unit"` mechanism to bind the navigator's captured top-parent into the insert form's own Business Unit dropdown. Found + hand-fixed a related generator gap in passing: `nav_levels` (a config key that caps the navigator cascade, already used to solve this exact symptom on Service/CO.2103) only affects the generated PYTHON driver - it does NOT thread into the generated RF T3, which still calls the shared multi-level cascade keyword and times out on this screen's 2 unrelated optional filter columns. Fixed locally (no shared-file change) by bypassing the shared keyword with a direct single-dropdown fill on the T3's own `${NAV_DD}` variable, matching Service's own established precedent exactly. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright driver 8/8). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. |
| Property (SP.0059) | **RESOLVED + SHIPPED 2026-08-02** (retried on `feature/retry-property-iud`). Original park reason ("Save SILENTLY fails - `ec.ec_error()` misses a real visible error banner") no longer reproduces after #319/#326 fixed `ec_error()`'s detection. On retry, hit a DIFFERENT symptom - the Business Unit Name reference dropdown persisted the wrong value ("SS1 BU" instead of "Royalty Canada"), reproduced live 4 times and initially suspected as a `select_dropdown()` shared-engine defect. **Real root cause (owner correction): a test-data date mismatch, not a code bug** - Start Date was `2000-01-01`, but the target Business Unit "Royalty Canada" (`ROYALTY_CA`) is only effective from `2003-01-01` onward; EC's reference dropdowns only offer parents already effective by the child record's own Start Date, so the panel legitimately excluded "Royalty Canada" and the code fell back to the first option actually offered. Fixed by using Start Date `2003-01-01` (>= the referenced Business Unit's own effective date, matching this project's existing `EC_TEST_START_DATE_REFDD` convention). Confirmed live + DB-verified (`AUTOTEST_PROP_FIXEDDATE`, then full driver 8/8 + RF 4/4 via `verify_screen.py`, OVERALL PASS). Also found + fixed locally: `tmp/gen_ovgm.py`'s default single-level nav-dropdown id template assumes Date+dropdown share one navigator group (`G:0:R:1:C:0`/`C:1`), but Property has them in SEPARATE groups (`G:0`=Date, `G:1`=Business Unit) - hand-corrected the generated driver/T3 id to `nav:form:G:1:R:1:C:0:dd`. Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. See [[feedback_child_object_date_must_follow_parent]] - **Price Index and Royalty Contract below show the identical symptom and should be rechecked against this same date-mismatch cause before assuming they need a different fix.** |
| Division Order (RC.0058) | **RESOLVED + SHIPPED 2026-08-02.** Originally parked as "genuinely TV, needs a different generator" - WRONG classification, corrected in an earlier investigate-only pass the same day: the screen's LABEL matches 3 classes in `class_property_cnfg` (`BEARER`, `DIVISION_ORDER`, `DIVISION_ORDER_SHARE`), and the real class for this BF code is `DIVISION_ORDER` (`OBJECT`/`VERSIONED`, base=`CONTRACT` - the SAME base table as Royalty Contract). Built with `gen_ovgm.py` using the same config pattern as Royalty Contract: `nav_value="Royalty USA"` (real populated Business Unit, resolved from the 2 existing rows), `extra_dropdowns` for Contract Template (first-available) + Contract Area ("Louisiana North", matching the nav scope). Two already-known fixes applied immediately (both previously seen on Property/Royalty Contract): (1) nav-dropdown id correction for the G:0/G:1 group-split gap, (2) `INSERT_END_DATE="2099-12-31"` since End Date is functionally mandatory on Save despite not being flagged yellow. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright 8/8). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. |
| Royalty Contract (RC.0059) | **STILL PARKED 2026-08-02** (retried on `feature/retry-royalty-contract-iud`). Original park reason (2nd dropdown/Contract Area silently mis-persisting to `SS2_CA`) had the SAME root cause as Property/Price Index - `start_date` `2000-01-01` predates "Alberta" (`CA_AB`)'s own effective date (`OV_CONTRACT_AREA.OBJECT_START_DATE` = `2003-01-01`, confirmed via DB). Fixed by using `start_date` `2003-01-01` + correcting the nav-dropdown id (same G:0/G:1 group-split gap as Property) + adding the mandatory `End Date` field (this screen requires it on INSERT, unusual, same as Contract CO.2016 - value `2099-12-31`, matching Contract's precedent). **Insert and Update now both work correctly, live + DB-verified.** **NEW, SEPARATE, GENUINE BLOCKER found on DELETE** - closing the record (End Date = Start Date) fails with EC's own `"Child record found... all child records must be deleted first"` error, reproduced live (before/after screenshots + headed browser in front of the owner). Root-caused via DB: choosing Contract Template = **"Royalty Fixed Percentage Canada"** causes EC to auto-provision 10 rows in `CNTR_PG_SETUP` (Contract Product Group Setup - one row per Product Group x member-Product: `BLEND`->{Diluent,Blend,Shrinkage,Bitumen}, `DILUENT`->{Diluent}, `TIETO_BLEND`->{Diluent,Blend,Shrinkage,Bitumen}, `TIETO_DIL`->{Diluent}) as a side effect of this template's royalty-percentage business logic. This is EXPECTED EC behavior for this template (all 10 rows confirmed `CREATED_BY='sysadmin'` at the exact Save timestamp, tied to this test object's `OBJECT_ID`) - not a bug in EC or in the shared automation engine. The BLOCKER is that **this screen's own UI exposes no path to view/delete `CNTR_PG_SETUP` rows**, so the End=Start close cannot succeed while they exist, and a raw SQL `DELETE` to clear them was attempted and BLOCKED by the environment's own safety guard (citing this project's "no raw DB write on a read-only-trigger view without explicit authorization" rule) pending owner sign-off. **RESIDUAL DATA ACCEPTED (owner decision, closes #336, 2026-08-02):** test row `AUTOTEST_RC_001` + its 10 `CNTR_PG_SETUP` children remain LIVE in the sandbox permanently, as a disclosed, known exception - no cleanup will be performed. No bundle shipped (blocked before packaging). **RESOLVED + SHIPPED 2026-08-15** (owner confirmed: "marked parked... its product defect... cant delete due to PC relationship. only work for Insert and update process") - packaged as an **Insert+Update-only bundle**, same precedent as Production Day Table (CO.1033): reused the existing SOW/T3/suite/driver from this investigation, bumped the driver's default test code to `AUTOTEST_RC_003` (since `AUTOTEST_RC_002` was already taken by a same-day recon run), removed the Delete test case (TC04) and pre-clean-via-close logic, confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 3/3, live RF 3/3, Playwright driver 7/7). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map (`ec-ui-knowledge/screens/royalty-contract.md`), root-cause record (`investigation/ROOT_CAUSE_delete_blocked.md`). Self-clean remains impossible by design - 5 `AUTOTEST_RC_*` rows permanently residual as of this PR (up from 1), disclosed plainly per the same accepted precedent. |

### Backlog classification audit (2026-08-02, closes Issue #320)
Ran a batch `class_property_cnfg`/`class_cnfg` check across all 55 backlog rows (label -> class_name ->
`CLASS_TYPE`), plus a targeted re-check of the 5 screens parked on 2026-07-27 (Production Sub Unit,
Forecast, Constant Standard, Stream Item, Production Day Table) in case any of THOSE were also secretly
TV-not-OV rather than genuinely blocked for their stated reason.

**Result: Division Order (RC.0058) was the ONLY genuine TV-vs-OV misclassification in the entire backlog.**
- The 5 earlier-parked screens all confirmed `CLASS_TYPE=OBJECT` at the class_cnfg level - their park
  reasons (groupmodel-not-enabled, toolbar timeout, INVARIANT physical-delete, mandatory FORECAST_TYPE)
  stand as genuinely OV-specific blockers, not misclassification.
- The batch check's label-match heuristic flagged 4 screens as "candidate mismatch" (Well, Test Device,
  Contract Capacity, Division Order) because their display label text also matches unrelated
  child/lookup/interface classes (e.g. `FORECAST_WELL`, `ACTIVE_INJ_RESULT_DEVICE`,
  `CAPACITY_REL_CNTR_CAP`) that happen to share the same LABEL property value. Well/Test Device/Contract
  Capacity are all proven-working, correctly-classified OV screens (shipped this session with live
  RF+Playwright PASS) - those 3 flags were false positives from label-collision noise, not real
  misclassifications. Only Division Order's flag was real (confirmed independently by the live
  `scan_ec_screen.py` DOM-open scan showing `CLASS_TYPE=DATA`, which is authoritative over a DB label-match
  heuristic alone).
- No other screen in the 55-row backlog needs reclassification.

### Contract Area Setup (CO.2038) - Bank-pattern sweep evaluation, NOT eligible (2026-08-25)
**Identity resolved live, distinct from "Contract Area" (a different screen/class already used elsewhere as
a navigator scope, e.g. Royalty Contract/Division Order's C2 group).** `SCREEN="contract area setup" py
tmp/scripts/resolve_ec_screen.py` (label lookup against `class_property_cnfg`, DB read-only, local sandbox)
resolves ONE unambiguous class: `CLASS_NAME=CONTRACT_AREA_SETUP` (`CLASS_TYPE=OBJECT`,
`TIME_SCOPE_CODE=VERSIONED`, base table `CONTRACT_AREA_SETUP`, view `OV_CONTRACT_AREA_SETUP` - exists).
Re-running the same tool with `SCREEN="contract area"` resolves a DIFFERENT class entirely
(`CLASS_NAME=CONTRACT_AREA`, base `CONTRACT_AREA`, view `OV_CONTRACT_AREA`) - confirms these are two
genuinely separate screens/classes, not a label variant of the same one.

**Bank-pattern eligibility: NO - structural, not a gap to fix.** The same resolver's own family-hint
classifier places `contract area setup` in family **`OV_CUSTOM_URL`** (clone exemplar: Account
`account_page.resource`), explicitly BECAUSE "no navigator GO button; grid `nav:form:T_data` (or
`manageObject:form:T_data`); Save And Refresh List falls back to toolbar Refresh" - not family `OV` (clone
Bank), which requires "grid id `manage_object_nav_nav:form:T_data`" (manage-object controller + GO). This
matches the screen's own already-verified metadata in `ec-ui-knowledge/screens/contract_area_setup.md` and
this doc's own row above (section A): "CUSTOM-URL OV - NO navigator, NO GO button", grid `nav:form:T_data`.
Cross-checked against every screen already converted to the Bank pattern this project
(`grep -l "manage_object_nav\|Insert/Update Object From Properties" pageobjects/**/*.resource`, 73 files) -
**zero** are custom-URL-flavour screens; every custom-URL OV built so far (Stream Item CD.0008, Document
Sequence CD.0109, Task Process CO.0191, Action Trigger CO.0193, Conversion Group CO.1049, Calculation
Library CO.1060, Production Day Table CO.1033, Contract Area Setup itself) uses the older label-driven
T3/driver shape instead, consistent with this class of screen never having had the Bank T2 keywords
(`Insert/Update Object From Properties`, `Find/Clear <Screen> Row By Filter`) apply to it.

**Already-done status unaffected.** This screen already has full automation, shipped and verified
2026-07-30 (`verify_screen.py` OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright 7/7),
registry + scorecard rows already present. No rebuild performed this session - the Bank-pattern sweep
evaluation confirms this screen correctly sits OUTSIDE the sweep's scope (custom-URL flavour, no navigator/
GO, different grid id/controller than Bank's `manage_object_nav`), not that it needs conversion. No code
change beyond this note; no PR content beyond documentation.


**Reviewer correction at merge (2026-08-25):** the OUTCOME above stands - Contract Area Setup needs no
rebuild (its own automation is complete and verify_screen-PASSED 2026-07-30) - but the STRUCTURAL claim
("custom-URL family => Bank T2 keywords don't apply") is wrong as a general rule. Report Context (RP.0007,
PR #487, merged 2026-08-24) is a custom-URL OV (grid `nav:form:T_data`, NO navigator/GO) built to the FULL
Bank pattern - `Insert/Update Object From Properties` + `Find/Clear <Screen> Row By Filter` - and passed
live 5/5 with the filter confirmed fired 15x. The T2 keywords take the grid id as an argument and do not
depend on the manage-object controller. The "73 converted page objects, zero custom-URL" cross-check above
also mis-measured: its grep used the literal string `Insert/Update Object From Properties`, which matches
NEITHER real keyword name, so it silently found nothing to contradict the claim. Correct decision rule for
the sweep: a custom-URL OV with existing working automation = SKIP (nothing to gain, like this screen); a
custom-URL OV needing NEW automation = ELIGIBLE, use the Report Context shape (Open keyword without Apply
Navigator, screen's own grid id).

### Well Mode (CO.0256) - FALSE POSITIVE correction (2026-08-24)
**NOT the same screen as Well (CO.0049) above, and NOT eligible for the Bank-pattern skills - EXCLUDED.**
The full-product deep-dive's "already known" filtering matched Well Mode (CO.0256) against this doc's own
CO.0049 `Well`/`OV_WELL` row via a plain substring match on the view name `OV_WELL` - both the deep-dive
note `DeepDiveLearnings/ec-screens/notes/CO.0256.md` and this row list `OV_WELL` as Well Mode's DB binding
(metadata-resolved purely from its URL path token `object_mode/OBJECT_TYPE/WELL` -> class `WELL`), but that
metadata resolution is misleading for this screen: **Well Mode's own data does not live in `OV_WELL` at
all.** Live recon (2026-08-24) confirmed its real storage is `OBJECT_MODE`, a generic EAV
(entity-attribute-value) table shared across object types (`MODE_TYPE='WELL'` + `MODE_CODE`/`ATTRIBUTE`/
`VALUE` rows) - this is TABLE-shaped data, not a proper date-effective `CLASS_TYPE=OBJECT` record like
Bank/Well/Stream-All. Insert is done via a "New Mode" gesture (not `objectForm`/New Object), Update targets
a `modeDetail:form` container (not `updateAttributes`), and Delete is a plain toolbar Delete + Save (not the
End Date = Start Date date-effective close Bank-family screens use). None of the standard `manage_object.
resource` (T2) OV helpers apply. **Correctly excluded from this round's plain Bank-pattern skills** - would
need a bespoke EAV-table driver, not a conversion. Self-cleaned during investigation (`OBJECT_MODE` rows for
`AUTOTEST_WELL_MODE` = 0, DB-verified fresh connection). No bundle shipped; no PR raised.

### Carrier (CO.0098) - single-BF_CODE, dual menu placement (2026-08-25)
Live sandbox menu search for "Carrier" returns TWO exact-label treeview hits with different breadcrumbs -
`Configuration > Assets > Cargo Objects > Carrier` and `Configuration > Assets > Transport Objects > Carrier`
- which could look like two separate screens (and does in the flat `docs/EC/ec_full_tree_inventory.json`
export, which carries no folder-header rows to disambiguate). **Confirmed to be the SAME screen, menu-linked
into two folders** - both hits load the identical URL (`manage_object_nav/CLASS_NAME/CARRIER?tran`), same
`screenLabel`, near-identical form HTML; `BUSINESS_FUNCTION` DB table has exactly one row with `NAME =
'Carrier'` (`BF_CODE = CO.0098`). Already fully Bank-pattern converted (registry row, Batch 11 2026-08-23) -
no second screen exists to build. Do not re-investigate this as a build gap in a future session.

### Document Sequence (CD.0109) - Bank-pattern conversion, verification-purity fix (2026-08-25)
Re-checked against the row above (marked `[x] #236 (custom-URL OV)`) - the classification (custom-URL OV,
grid `nav:form:T_data`, no navigator/GO, toolbar Refresh) re-confirmed accurate live (existing driver
`py/document_sequence_iud.py` re-run headless this session: PASS 5/5 steps, DB self-clean 0 residual).

However, reading the FULL `.robot` file content (not just re-running it) found the same class of deviation
already caught on DOA Credit Limit this session: THREE inline DB-verify keyword calls sitting directly in
the test cases (`Document Sequence Should Exist In DB`, `Field Should Equal In View OV_DOC_SEQUENCE ...`,
`Document Sequence Should Not Exist In DB`), violating the owner's 2026-08-18 pure-screen-verification
convention. Also found: not properties-file-driven (raw `Fill OV Field By Label` calls), no explicit
`Find/Clear Document Sequence Row By Filter` grid-filter wiring, a timestamped/generated test code
(`AUTOTEST_DS_<timestamp>`) instead of a fixed one, single Suite-level Login/Logout instead of per-TC, and
only 4 TCs (missing an explicit TC04 Find).

Per the reviewer's 2026-08-25 correction on Contract Area Setup (same doc, above): the T2 Bank-pattern
keywords (`Insert/Update Object From Properties`, `Find/Clear <Screen> Row By Filter`) take the grid id as
an argument and do not depend on the manage-object controller - they apply to custom-URL OV screens too, as
proven live on Report Context (RP.0007, PR #487). Converted Document Sequence to the same shape as Report
Context: 4 new `testdata/document_sequence_{insert,update,form_verify,grid_verify}.properties` files, a
`DOCUMENT_SEQUENCE_EC_USER`/`_EC_PASS` credential pair (additive-only in `resources/credentials.py`), full
T3 rewrite (`document_sequence_page.resource`) and T3 test-suite rewrite (`document_sequence_iud.robot`) -
fixed test code `AUTOTEST_DOCUMENT_SEQUENCE` (confirmed absent from `OV_DOC_SEQUENCE` before use, fresh
connection), per-TC Login/Logout, explicit grid-filter wiring, zero inline DB-verify calls in the .robot
file, 5 TCs (added TC04 Find). Starting Point (a mandatory extra text field, DB column `STARTING_POINT`)
kept in the insert properties file (still filled on Insert, matching the screen's own prior driver) but
excluded from the form-verify label list - it was never previously round-trip-verified in `updateAttributes`,
same precedent as Bank/Report Context excluding their own Insert-only fields from that list.

No shared T1/T2 file changes. Verified: robocop parity (9 issues, identical count/category to Report
Context's own 9 - not a regression), full-tree dryrun 811/811, live RF 5/5 (`results/_live_ds/`), filter
keyword fired 15x (`grep -c "Find Object Row By Filter" output.xml`), DB self-clean 0 residual `AUTOTEST%`
rows in `OV_DOC_SEQUENCE` via a fresh `oracledb` connection after the live run. Playwright driver
(`py/document_sequence_iud.py`) left unchanged - already properties-free/label-driven and still passes;
no defect found in it. Registry (`docs/ec_screen_registry.md`) and scorecard
(`docs/automation-scorecard.md`) rows updated in place (modifying the existing row, not adding a new one).
### The 6 "* Split Key" screens - blanket `split_key`-URL exclusion was UNVERIFIED, corrected (2026-08-25)
A prior filtering pass excluded any screen whose URL contains `split_key` from Bank-pattern consideration,
on the assumption "split-key percentage-share screens (different UI shape)" - **that exclusion was never
live-verified on any specific screen; it was a blanket guess from the URL substring alone.** Investigated
fresh (deep-dive notes + live DB query + live browser recon, no build) on all 6 base "Split Key" screens:
Product Split Key (CD.0036), Company Split Key (CD.0044), Field Split Key (CD.0095), Stream Item Category
Split Key (CD.0042), Other Split Key (CD.0046), Stream Item Split Key (CD.0156).

**Finding: all 6 are Bank-shaped and should be treated as ELIGIBLE, not excluded.** All 6 share ONE
underlying class (`SPLIT_KEY`, `OBJECT`/`VERSIONED`, base table `SPLIT_KEY`, view `OV_SPLIT_KEY`) and ONE
generic controller URL `manage_object_split_key/CLASS_NAME/SPLIT_KEY/SPLIT_TYPE/<TYPE>` - the 6 BF_CODEs are
the SAME parametrized OV template with a different `SPLIT_TYPE` path segment (`PRODUCT`/`COMPANY`/`FIELD`/
`STREAM_ITEM_CATEGORY`/`SPLIT_ITEM_OTHER`/`STREAM_ITEM_SPLIT`), confirmed via `class_property_cnfg`
(`SPLIT_KEY`'s only LABEL is generic "Split Key" - the per-screen titles come from the URL parameter, not a
per-class label) and live `page.url` capture after GO (`.../manage_object_split_key/CLASS_NAME/SPLIT_KEY/
SPLIT_TYPE/PRODUCT`). Live recon (headless, read-only, no insert/update/delete) opened all 6 via the
treeview search and confirmed **pixel-identical layout to Bank (CD.0021)**: single `Date`+`GO` navigator (no
mandatory dropdowns), a grid with an explicit column-filter row (`Split Key Code`/`Split Key Name`/`Start
Date`/`End Date`), a "NEW VERSION" tab with `Start Date`/`End Date` + object fields (`Split Key Code`,
`Split Key Name`, `Description`, `Comments`, `Value Method`, `Shares add to 100%`, `Rounding Rule`, `Number
of Rounding Decimals`, `Number Display Format`), and the same "Daytime" mirror sub-grid Bank itself has
(this is a standard Bank-pattern element, not something unique to Split Key). Stream Item Category Split Key
(CD.0042) showed the same shape live (Value Method/Rounding fields present), matching the other 5 exactly -
all 6 are structurally identical to each other, not just to Bank. Toolbar Save/New/Delete all present and
enabled on every screen. This is a plain master-data OV screen, NOT a percentage-allocation grid or a
parent-object-selection screen - the actual percentage-share data lives in the SEPARATE, already-distinct
"* Split Key Shares" screens (CD.0037/CD.0045/CD.0096/CD.0047/CD.0157, classes `PRODUCT`/`COMPANY`/`FIELD`/
`SPLIT_ITEM_OTHER`/`STREAM_ITEM_SPLIT`) - those Shares screens were NOT investigated this round and their
own eligibility remains unassessed; do not assume this note covers them.

**Reviewer note at merge (2026-08-25):** the six builds this note green-lit (PRs #508-#513, merged the same
day) each re-recon'd their own screen, and their navigator findings DIVERGE from the shared description
above: Product/Company/Other/Stream-Item-Category builds report NO navigator at all (grid renders
immediately on open), while Field/Stream-Item builds report a GO button (`navButton:form:B`) present. All
six passed live 5/5 with their own shape, so treat EACH SCREEN'S OWN page object as the operative truth for
its gestures, not this note's shared "single Date+GO" description. The eligibility conclusion (all 6
Bank-shaped, ELIGIBLE) is unaffected either way.


**No existing automation found for any of the 6.** The only "Split Key"-family automation in the repo
(`py/split_item_other_iud.py` + `pageobjects/.../split_item_other_page.resource` +
`tests/.../split_item_other_iud.robot`, already full Bank-pattern, built Batch 10 2026-08-23) targets a
DIFFERENT screen - **Split Item Other (CD.0017)**, a standalone menu entry on class `SPLIT_ITEM_OTHER` via
the plain `manage_object_nav` controller (not `manage_object_split_key`), which happens to share the same
underlying class as "Other Split Key Shares" (CD.0047) but is NOT one of the 6 screens in this note and NOT
"Other Split Key" (CD.0046, one of the 6 - class `SPLIT_KEY`). Do not confuse the two when picking this up
for a build.

Verdict: all 6 CONVERT/BUILD candidates, same shape as the plain Bank-pattern new-screen build (5 mandatory
fields shared across all 6: `Split Key Code`, `Split Key Name`, `Start Date` on Insert; `Split Key Name` on
Update - `Description`/`Comments`/`Value Method`/`Shares add to 100%`/`Rounding Rule`/`Number of Rounding
Decimals`/`Number Display Format` all appeared populated/optional on existing rows, not confirmed mandatory
this round). All 6 write to the SAME table (`SPLIT_KEY`) - each build must use its own distinct fixed test
code (no cross-screen collision) same as any other shared-table screen. No build/convert/PR performed this
round - investigation only, per instruction; a build can be dispatched from this note.
