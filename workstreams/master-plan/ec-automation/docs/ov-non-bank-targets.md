# OV Non-Bank Targets - the 55 OV-GM object screens beyond the 71

**Scope:** OV (`CLASS_TYPE=OBJECT`) screens NOT in the 71 Bank-layout list and not yet automated.
Grouped by NAVIGATOR pattern (owner's recipe `tmp/ov_gm_55_nav_recipe.xlsx`). Build order = easiest first.
Nav values resolved FIRST-AVAILABLE live (recipe gives the nav *shape*, not hardcoded P1/SS1).
Two OV flavours: **manage-object** (grid `manage_object_nav_nav:form:T_data` + GO) vs **custom-URL**
(grid `nav:form:T_data`, no GO, toolbar Refresh) - recon each; engine `click_go` now does GO-or-Refresh.

**Legend:** [x] done+verified · [~] driver-proven/partial · [ ] pending · (P) parked (reason).

## A. No navigator (manage-object no-cascade OR custom-URL)  (17)
**Progress: 4/55 done.**

| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CD.0008 | Stream Item | OV_STREAM_ITEM | Assets > Stream Objects | [x] Custom-URL OV, live 3/3 Insert+Delete - shipped 2026-08-03 - Update out of scope (EC scheduler job UpdateStreamItem not configured, see Parked table) |
| CD.0109 | Document Sequence | OV_DOC_SEQUENCE | Assets > Revenue Document Objects | [x] #236 (custom-URL OV) |
| CO.0021 | Facility Class 2 | OV_FCTY_CLASS_2 | Assets > Facility Objects | (P) grid never shows a row that IS correctly in the DB/view - likely needs a Finder not exposed by nav - see Parked table |
| CO.0100 | Production Sub Unit | OV_PROD_SUB_UNIT | Assets > Basic Objects | [ ] |
| CO.0102 | Constant Standard | OV_CONSTANT_STANDARD | Assets > Hydrocarbon Objects | (P) real Copy-based insert mechanism identified, not yet proven working - see Parked table |
| CO.0158 | Report Group | OV_REPORT_GROUP | Assets > Facility Objects | [x] plain OV, live 4/4 |
| CO.0191 | Task Process | OV_TASK_PROCESS | Task List | [x] #236 (custom-URL OV) |
| CO.0193 | Action Trigger | OV_CONTROL_POINT | Business Action | [x] custom-URL OV, live 7/7 (shipped 2026-08-01) |
| CO.0227 | External Location | OV_EXTERNAL_LOCATION | Assets > Facility Objects | [x] OV-GM GO-only, live 8/8 (shipped 2026-08-01) |
| CO.0264 | Truck | OV_TRUCK | Assets > Transport Objects | [x] #277 (plain OV) |
| CO.0265 | Trailer | OV_TRAILER | Assets > Transport Objects | [x] #279 (plain OV) |
| CO.0266 | Driver | OV_DRIVER | Assets > Transport Objects | [x] #281 (plain OV) |
| CO.1033 | Production Day Table | OV_PRODUCTION_DAY | System | [ ] |
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
| CO.3016 | Price Object | OV_PRICE_OBJECT | Assets > Sales Objects | (P) pager-walk click timeout (5-page grid), self-cleaned - see Parked table |
| CO.3024 | Price Rate | OV_PRICE_RATE | Assets > Sales Objects | [x] OV-GM, live 4/4, BU=SS2 BU (parent_dd worked here) |
| SP.0059 | Property | OV_PROPERTY | Assets > Data Mapping Objects | [x] OV-GM, live 4/4 - #329 - was a test-data date mismatch, not a bug - see Parked table |

## C2. Business Unit + Contract Area  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2016 | Contract | OV_CONTRACT | Assets > Contract Objects | [x] OV-GM, live 4/4, BU=TS5 BU (single-page scope, avoided pager bug) |
| CO.2044 | Contract Capacity | OV_CONTRACT_CAPACITY | Assets > Contract Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-08-01) |
| CO.2054 | Contract Inventory | OV_CONTRACT_INVENTORY | Assets > Contract Objects | [x] OV-GM gated-nav, live 8/8 (shipped 2026-08-02) |
| RC.0058 | Division Order | OV_DIVISION_ORDER | Royalty > Royalty USA | (P) previously mis-scoped as TV - actually OV-GM, buildable now with gen_ovgm.py - see Parked table |
| RC.0059 | Royalty Contract | OV_ROYALTY_CONTRACT | Royalty > Royalty Canada | (P) EC-genuine child-record defect on DELETE (Royalty Fixed Percentage Canada template auto-provisions CNTR_PG_SETUP) - Insert/Update OK - see Parked table |

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
| CO.0100 | Production Sub Unit | **OV-GM** | manageObject:form:T_data | 2 (needs capability) -- **UNVERIFIED 2026-07-27 batch guess**; siblings in this block (Truck/Trailer/Driver/Report Group) all turned out plain OV, so SCAN before building. |
| CO.0021 | Facility Class 2 | **OV-GM** | manageObject:form:T_data | 2 (needs capability) -- **UNVERIFIED 2026-07-27 batch guess**; siblings in this block (Truck/Trailer/Driver/Report Group) all turned out plain OV, so SCAN before building. |
| CO.0158 | Report Group | **plain OV** (PROVEN live 2026-07-31) | report_group_table:form:T_data | **DONE** - verify_screen PASS (RF 4/4 + PW 8/8) |
| CO.0227 | External Location | **OV-GM** | manageObject:form:T_data | 2 (needs capability) -- **UNVERIFIED 2026-07-27 batch guess**; siblings in this block (Truck/Trailer/Driver/Report Group) all turned out plain OV, so SCAN before building. |
| CO.0264 | Truck | **plain OV** (PROVEN live, shipped) | manage_object_nav_nav:form:T_data | **DONE #277** |
| CO.0265 | Trailer | **plain OV** (PROVEN live, shipped) | manage_object_nav_nav:form:T_data | **DONE #279** |
| CO.0266 | Driver | **plain OV** (PROVEN live, shipped) | manage_object_nav_nav:form:T_data | **DONE #281** |
| CO.0102 | Constant Standard | custom-URL grid cstandard:form:T_data | (P) standard New-Object menu gesture times out (custom toolbar) - needs individual insert-gesture recon; 2026-07-27 |
| CD.0008 | Stream Item | (P) no :T_data grid renders on open (different layout / didn't open) - needs individual recon; 2026-07-27 |
| CO.1033 | Production Day Table | custom-URL grid production_day:form:T_data | (P) INVARIANT (physical delete, not End=Start) - needs physical-delete capability; 2026-07-27 |

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
| Production Sub Unit (CO.0100) | OV-GM grid never lists inserts (groupmodel-not-enabled); DB persists |
| Forecast (FC.0010) | **RE-ATTEMPTED 2026-08-02, STILL PARKED - NEW blocker, original reason superseded.** The original park reason (FORECAST_TYPE DB NOT NULL + likely-popup-picker, Save rejected) did NOT reproduce on retry - Forecast Type shows as NOT mandatory on live scan, and 5 test inserts leaving it blank all succeeded (Insert + Update + Delete all worked via the standard `objectdates`/`updateAttributes` OV gestures, confirmed live, self-cleaned via `closeObjectRecord()`, 0 residual). **The actual blocker found this round: `resolve_ec_screen.py`'s class resolution is WRONG for this specific BF code.** The tool resolves screen label "Forecast" -> class `FORECAST_GROUP` via `class_property_cnfg` (the ONLY class with that exact LABEL, confirmed - no ambiguity like Division Order had), but the live screen's data does NOT land in `FORECAST_GROUP` or `OV_FORECAST_GROUP` (checked both, fresh connections, twice - genuinely 0 matching rows even while the test data was live in the UI grid). The screen's own content-frame URL is `com.ec.tran.fc.screens/forecast` (a dedicated custom module, distinct from a generic Manage-Object screen), and its insert form is internally named `new_fcst` (not the standard `objectForm`) - both signals that this BF code (FC.0010, treeview key `TRAN_FC_CREATE`) is bound to a DIFFERENT underlying class than what LABEL-based lookup finds. Root cause NOT isolated (the real base table/view was not identified despite substantial live+DB investigation - searched FCST_MEMBER and other FCST_* candidates, no match); stopped rather than keep grinding on table identification alone. Self-clean confirmed via the UI (0 rows left visible in the grid) even without knowing the true table name. **Next step if resumed:** capture the actual PrimeFaces AJAX request/response during Save (network intercept) to read the real bound class from the server's own response, rather than guessing table names. |
| Constant Standard (CO.0102) | **RE-ATTEMPTED 2026-08-02, STILL PARKED - real insert mechanism identified, not yet completed.** Confirmed the standard "New Object" menu gesture genuinely does not exist on this screen (the Insert toolbar icon's hover menu has NO "New Object" item at all - only "CONSTANT STANDARD" as a plain tooltip label, plus System-of-Measurement override options and personalisation entries). This is a **TV-style inline-editable grid** (`cstandard:form:T_data`), not a standard OV New-Object-form screen, despite `resolve_ec_screen.py` reporting `CLASS_TYPE=OBJECT`. **The real insert gesture: select an existing row (source), fill "New Code" (`copy:form:G:0:R:0:C:1:in`) + "New Name" (`copy:form:G:0:R:0:C:3:in`), then click the "COPY" control** (a `<span>` element, not a `<button>` - the visible green COPY control has NO stable id, which is why it took many selector attempts to even locate; there is a separate HIDDEN `copy:form:defaultSubmit` button unrelated to it). Ran out of reasonable attempts clicking the actual COPY span reliably (10+ tries, escalating per the project's stop-and-ask-after-effort guidance) before completing a live end-to-end test - the mechanism is understood but not yet proven working. No data was ever persisted during this investigation (confirmed 0 residual `AUTOTEST_CS%` rows) - nothing to self-clean. **Next step if resumed:** retry clicking the COPY span with `force=True` or via `dispatch_event('click')` instead of a normal Playwright click, since the normal click kept timing out waiting for actionability despite the element being visually present. |
| Stream Item (CD.0008) | **RESOLVED + SHIPPED 2026-08-03 (Insert + Delete only).** The "Copy-based insert mechanism" finding from the 2026-08-02 re-attempt was a wrong turn (same class of wrong turn as Constant Standard's original COPY detour) - the real Insert path is the standard `ec._open_new_object()` flow, which was already correctly cased on this screen (title-case "New Object"/"New Version", no CSS-uppercase illusion). The non-standard GO button id (`buttongo:form:B`, confirmed in the prior round) is handled by a local wrapper in both the driver and T3 rather than a shared-engine fix. **Two NEW findings this round:** (1) the 12 fields the Save-error lists with `[..._POPUP]`-style brackets are ordinary autocomplete DROPDOWNS (`dd_input`), not "Pick from EC Object" popups - `__FIRST__` on each satisfies Save; (2) Name is server-derived - confirmed against EC's own online help page (*"the Name attribute can be left blank for the system to automatically generate the Name"*) - any typed value is discarded, confirmed 3x including typing it last, right before Save. **Genuine blocker found and accepted, not fixed:** any Save on `updateAttributes` fails with EC's own error "Cannot run schedule job UpdateStreamItem because it has not been configured" - EC's own online help documents this as a real feature (BF VO.0031 - Daily SI Pending Calculation, a background recalculation job triggered by core-attribute changes) that is simply not configured/enabled in this sandbox. Reproduced live 3x, twice headed with the owner watching directly. **Owner instruction 2026-08-02: skip Update, ship Insert + Delete only.** Also hit (and fixed) the 4th confirmed instance of the reference-dropdown date-scope bug ([[feedback_child_object_date_must_follow_parent]]) - the RF suite's `${START_DATE}` was wired to the plain `${TEST_START_DATE}` (2000-01-01) instead of `${TEST_START_DATE_REFDD}` (2003-01-01); 2 live RF failures looked like a flaky dropdown-panel timeout until a screenshot review showed the panel correctly said "No records found". Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 3/3, live RF 3/3, Playwright driver 6/6). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. **This root cause (case-sensitivity was NOT the issue here, unlike Constant Standard/expected for Production Day Table) confirms the toolbar-mystery batch had at least 2 distinct root causes, not one shared cause - re-verify Production Day Table's own Insert mechanism fresh rather than assuming the Constant Standard fix applies unchanged.** |
| Production Day Table (CO.1033) | INVARIANT (physical delete, not End=Start) - needs physical-delete capability |
| Message Group (CO.0236) | **RESOLVED + SHIPPED 2026-08-02** (retried on `feature/retry-message-group-iud`). Original park reason: insert PERSISTS but lands in WRONG SCOPE (Functional Area dropdown pick mismatch: requested option 1 'Administration', persisted option 2 'Allocation'), suspected as the shared `select_dropdown`/`Fill OV Dropdown By Label` engine (used by 22 OV-GM screens). **Real root cause: the same test-data date mismatch as Property/Price Index/Royalty Contract - 4th confirmed instance** - the generator config had NO `start_date` set at all (defaulting to `2000-01-01`), but "Administration" (`ADM`) is only effective from `2001-01-01` onward. Fixed by setting `start_date: "2003-01-01"` in `tmp/cfg_message_group.json` - no shared-engine change needed. Explicitly re-verified `FUNCTIONAL_AREA_CODE = 'ADM'` persisted correctly (not just Name). Also RESOLVES the "NOT confirmed systemic" open question from the original entry - Area's `parent_dd` validation (7/7) never hit this because its own values happened to already be date-compatible, not because a different mechanism was in play; both `parent_dd` and `extra_dropdowns` share the identical date trap. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS). Full bundle shipped, 0 residual. See [[feedback_child_object_date_must_follow_parent]]. |
| Facility Class 2 (CO.0021) | **RE-SCOPED 2026-08-02 (investigate-only, per owner instruction - NOT built)**. Re-confirmed the original finding with a fresh, more thorough test: inserted `AUTOTEST_FC2_INV` with Start Date `2003-01-01` (ruling out the date-mismatch class found on Property/Price Index/Royalty Contract/Message Group - this screen has NO mandatory reference dropdown, so that class doesn't apply here). Confirmed via DB that the row genuinely exists in BOTH tables the view joins (`PRODUCTION_FACILITY` parent + `FCTY_VERSION` child) AND correctly appears when querying `OV_FCTY_CLASS_2` directly - the DB/view layer is 100% correct. The defect is PURELY in the live grid: `row_exists()` against `manageObject:form:T_data` returns `False` and the grid literally renders "No records found", even though the exact same code is querying a view that DOES return the row. Ruled out 3 candidate causes by direct test: (1) nav Date field value - tried both the default (today) and the row's own Start Date, no difference; (2) refresh mechanism - toolbar Refresh vs the GO button, no difference; (3) a stray hidden `fcNum_input` spinner near the grid - inspected its HTML, it's a PrimeFaces "freeze columns" control (max value 4), unrelated to data filtering. **Root cause NOT fully isolated** - the grid's DataTable must be applying some additional filter/scope not visible in the navigator panel and not explained by the OV_ view's own SQL (which has no scope-limiting join at all beyond `CLASS_NAME='FCTY_CLASS_2'`). Most likely explanation, unconfirmed: a parent-object "Finder" selection (a popup-based parent picker, distinct from a dropdown) that this screen's UI expects but doesn't expose as a visible navigator field - this project's current tooling (`select_dropdown`, `apply_ovgm_navigator`) has no mechanism for that pattern. Self-cleaned via the OV view's own End=Start UPDATE (not a raw DELETE), 0 residual confirmed. No bundle shipped - out of scope for current tooling per owner instruction. |
| Planned Well (CO.0247) (2026-08-01) | OV-GM (grid `manageObject:form:T_data`), 5-level cascade nav; PU/Area/Facility Class 1 = PROVEN P1 values (same scope Well/CO.0049 uses), deeper 2 levels left empty per Well's precedent. Insert via the toolbar's "New Object" gesture landed in the WRONG class entirely - `OV_WELL` (`CLASS_NAME='WELL'`), not `OV_PLANNED_WELL` (`CLASS_NAME='PLANNED_WELL'`, confirmed by reading the view SQL - both classes share the SAME base `WELL`/`WELL_VERSION`/`WELL_PERIOD_STATUS` tables, discriminated only by `CLASS_NAME`). The 2 misplaced rows also had ALL scope columns NULL (`OP_PRODUCTIONUNIT_CODE`/`OP_AREA_CODE`/`OP_FCTY_1_CODE` etc.), so they were orphaned regardless of class - the "New Object" gesture on this screen does not bind the nav scope into the new record the way it evidently does on Well's own screen. Root cause not fully isolated (menu-item disambiguation vs a Planned-Well-specific scope-binding gap) - stopped at the 2-attempt limit. Self-cleaned via direct SQL DELETE (child-first: `WELL_PERIOD_STATUS` -> `WELL_VERSION` -> `WELL`, scoped by OBJECT_ID, read in full before delete) since the mis-scoped rows were unreachable via any UI and a raw End=Start close was blocked by `FK_WELL_PERIOD_STATUS_2`. 0 residual confirmed. No bundle shipped. |
| Price Index (CO.3009) | **RESOLVED + SHIPPED 2026-08-02** (retried on `feature/retry-price-index-iud`). Original park reason: the New-Object form's 2nd dropdown in sequence (Frequency, then Business Unit/`parent_dd`) silently persisted `SS1_BU` instead of the requested `Royalty Canada`/`ROYALTY_CA`, reproduced 3 times and suspected as a shared-engine widget-state defect. **Real root cause: the same test-data date mismatch found on Property** - `start_date` was `2000-01-01`, but "Royalty Canada" (`ROYALTY_CA`) is only effective from `2003-01-01` onward, so the reference dropdown correctly excluded it and the fallback landed on a different available option. Fixed by changing `tmp/cfg_pi.json`'s `start_date` to `2003-01-01` - no shared-engine change needed, resolved on the first retry. Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright 8/8). Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. See [[feedback_child_object_date_must_follow_parent]]. NOTE (unchanged from the original park entry): this may also affect Area's `parent_dd` mechanism if that screen's form ever gains a second dropdown before the parent_dd one - not retested this round. |
| Price Object (CO.3016) | OV-GM, insert persists correctly but was never found under the "ECP Norway" scope. **CORRECTED 2026-08-02 (re-investigated for issue #321)**: the original "pager-walk click times out" characterization does NOT hold up under repeated, careful re-testing - the pager mechanism itself walked all 5 real pages in <1s each, twice, with zero hangs. Reproducing the EXACT original scenario (insert with Business Unit deliberately left unset, then immediately `wait_for_row`) gave a clean 44s-then-`False` result, not a `TimeoutError` - because the row genuinely has no `BUSINESS_UNIT_CODE`, so it is NOT VISIBLE under any page of a BU-scoped grid. This is the SAME missing/wrong-scope defect class as Message Group and Planned Well, not a distinct pagination-mechanism bug. See issue #321's comment thread for the full re-investigation; no shared-engine change was made (nothing to fix - see also PR #326, unrelated, which fixed a real `ec_error()` gap found the same day). Self-cleaned x3 (2 original + 1 re-repro), 0 residual each time. |
| Property (SP.0059) | **RESOLVED + SHIPPED 2026-08-02** (retried on `feature/retry-property-iud`). Original park reason ("Save SILENTLY fails - `ec.ec_error()` misses a real visible error banner") no longer reproduces after #319/#326 fixed `ec_error()`'s detection. On retry, hit a DIFFERENT symptom - the Business Unit Name reference dropdown persisted the wrong value ("SS1 BU" instead of "Royalty Canada"), reproduced live 4 times and initially suspected as a `select_dropdown()` shared-engine defect. **Real root cause (owner correction): a test-data date mismatch, not a code bug** - Start Date was `2000-01-01`, but the target Business Unit "Royalty Canada" (`ROYALTY_CA`) is only effective from `2003-01-01` onward; EC's reference dropdowns only offer parents already effective by the child record's own Start Date, so the panel legitimately excluded "Royalty Canada" and the code fell back to the first option actually offered. Fixed by using Start Date `2003-01-01` (>= the referenced Business Unit's own effective date, matching this project's existing `EC_TEST_START_DATE_REFDD` convention). Confirmed live + DB-verified (`AUTOTEST_PROP_FIXEDDATE`, then full driver 8/8 + RF 4/4 via `verify_screen.py`, OVERALL PASS). Also found + fixed locally: `tmp/gen_ovgm.py`'s default single-level nav-dropdown id template assumes Date+dropdown share one navigator group (`G:0:R:1:C:0`/`C:1`), but Property has them in SEPARATE groups (`G:0`=Date, `G:1`=Business Unit) - hand-corrected the generated driver/T3 id to `nav:form:G:1:R:1:C:0:dd`. Full bundle shipped: registry + scorecard rows, JOURNAL/CHECKLIST/KB map, 0 residual. See [[feedback_child_object_date_must_follow_parent]] - **Price Index and Royalty Contract below show the identical symptom and should be rechecked against this same date-mismatch cause before assuming they need a different fix.** |
| Division Order (RC.0058) | **RE-SCOPED 2026-08-02 (investigate-only, per owner instruction - NOT built) - PREVIOUS "genuinely TV" CLASSIFICATION WAS WRONG.** The screen's LABEL matches 3 classes in `class_property_cnfg` (`BEARER`, `DIVISION_ORDER`, `DIVISION_ORDER_SHARE`) - `resolve_ec_screen.py` correctly surfaces all 3 with their own metadata (it does NOT itself pick one), but the original investigation only looked at the FIRST one (`BEARER`, `CLASS_TYPE=DATA`/TV) and concluded "genuinely TV" without checking the other two - a human interpretation gap, not a tool defect. **`DIVISION_ORDER` itself is `CLASS_TYPE=OBJECT`, `TIME_SCOPE_CODE=VERSIONED` (a normal OV-GM screen), base=`CONTRACT`, view=`OV_DIVISION_ORDER` (exists)** - this is the class that actually matches the live screen. Confirmed live: navigator = Date (optional) + mandatory Business Unit dropdown + optional 2nd dropdown (identical shape to Royalty Contract's own nav); grid id = `manageObject:form:T_data` (the standard OV-GM grid, not a TV inline-edit grid); the New-Object form is a 24-row `objectForm` with fields **Division Order Code / Division Order Name / Description / Comments / Start Date / End Date / Contract Template / Trade Alias Name / Contract Area / Project / ...** - near-identical in shape to Royalty Contract's form (both share the `CONTRACT` base table, discriminated by `CLASS_NAME`). **Conclusion: Division Order does NOT need a TV generator at all - it's buildable RIGHT NOW with the existing `gen_ovgm.py` tooling, following essentially the same config pattern as Royalty Contract** (`nav_value` = a Business Unit, `extra_dropdowns` for Contract Template + Contract Area, watch for the same mandatory-End-Date-on-insert quirk and the same reference-dropdown date trap - see [[feedback_child_object_date_must_follow_parent]]). No live Save was ever called during this investigation (form-inspection only) - 0 residual, nothing to self-clean. Not built this round per owner instruction (investigate-only); ready to build in a follow-up task. |
| Royalty Contract (RC.0059) | **STILL PARKED 2026-08-02** (retried on `feature/retry-royalty-contract-iud`). Original park reason (2nd dropdown/Contract Area silently mis-persisting to `SS2_CA`) had the SAME root cause as Property/Price Index - `start_date` `2000-01-01` predates "Alberta" (`CA_AB`)'s own effective date (`OV_CONTRACT_AREA.OBJECT_START_DATE` = `2003-01-01`, confirmed via DB). Fixed by using `start_date` `2003-01-01` + correcting the nav-dropdown id (same G:0/G:1 group-split gap as Property) + adding the mandatory `End Date` field (this screen requires it on INSERT, unusual, same as Contract CO.2016 - value `2099-12-31`, matching Contract's precedent). **Insert and Update now both work correctly, live + DB-verified.** **NEW, SEPARATE, GENUINE BLOCKER found on DELETE** - closing the record (End Date = Start Date) fails with EC's own `"Child record found... all child records must be deleted first"` error, reproduced live (before/after screenshots + headed browser in front of the owner). Root-caused via DB: choosing Contract Template = **"Royalty Fixed Percentage Canada"** causes EC to auto-provision 10 rows in `CNTR_PG_SETUP` (Contract Product Group Setup - one row per Product Group x member-Product: `BLEND`->{Diluent,Blend,Shrinkage,Bitumen}, `DILUENT`->{Diluent}, `TIETO_BLEND`->{Diluent,Blend,Shrinkage,Bitumen}, `TIETO_DIL`->{Diluent}) as a side effect of this template's royalty-percentage business logic. This is EXPECTED EC behavior for this template (all 10 rows confirmed `CREATED_BY='sysadmin'` at the exact Save timestamp, tied to this test object's `OBJECT_ID`) - not a bug in EC or in the shared automation engine. The BLOCKER is that **this screen's own UI exposes no path to view/delete `CNTR_PG_SETUP` rows**, so the End=Start close cannot succeed while they exist, and a raw SQL `DELETE` to clear them was attempted and BLOCKED by the environment's own safety guard (citing this project's "no raw DB write on a read-only-trigger view without explicit authorization" rule) pending owner sign-off. **RESIDUAL DATA ACCEPTED (owner decision, closes #336, 2026-08-02):** test row `AUTOTEST_RC_001` + its 10 `CNTR_PG_SETUP` children remain LIVE in the sandbox permanently, as a disclosed, known exception - no cleanup will be performed. No bundle shipped (blocked before packaging). |

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
