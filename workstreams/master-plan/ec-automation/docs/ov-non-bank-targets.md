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
| CD.0008 | Stream Item | OV_STREAM_ITEM | Assets > Stream Objects | [ ] |
| CD.0109 | Document Sequence | OV_DOC_SEQUENCE | Assets > Revenue Document Objects | [x] #236 (custom-URL OV) |
| CO.0021 | Facility Class 2 | OV_FCTY_CLASS_2 | Assets > Facility Objects | [ ] |
| CO.0100 | Production Sub Unit | OV_PROD_SUB_UNIT | Assets > Basic Objects | [ ] |
| CO.0102 | Constant Standard | OV_CONSTANT_STANDARD | Assets > Hydrocarbon Objects | [ ] |
| CO.0158 | Report Group | OV_REPORT_GROUP | Assets > Facility Objects | [x] plain OV, live 4/4 |
| CO.0191 | Task Process | OV_TASK_PROCESS | Task List | [x] #236 (custom-URL OV) |
| CO.0193 | Action Trigger | OV_CONTROL_POINT | Business Action | [ ] |
| CO.0227 | External Location | OV_EXTERNAL_LOCATION | Assets > Facility Objects | [ ] |
| CO.0264 | Truck | OV_TRUCK | Assets > Transport Objects | [x] #277 (plain OV) |
| CO.0265 | Trailer | OV_TRAILER | Assets > Transport Objects | [x] #279 (plain OV) |
| CO.0266 | Driver | OV_DRIVER | Assets > Transport Objects | [x] #281 (plain OV) |
| CO.1033 | Production Day Table | OV_PRODUCTION_DAY | System | [ ] |
| CO.1049 | Conversion Group | OV_CONVERSION_GROUP | System > Units | [x] #236 (custom-URL OV) |
| CO.1060 | Calculation Library | OV_CALC_LIBRARY | Assets > Calculation Objects | [x] #236 (custom-URL OV) |
| CO.2038 | Contract Area Setup | OV_CONTRACT_AREA_SETUP | Assets > Contract Objects | [ ] |
| FC.0010 | Forecast | OV_FORECAST_GROUP | Forecasting | [ ] |

## B. Production Unit + Area + Facility Class 1  (20)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CD.0006 | Node | OV_NODE | Assets > Calculation Objects | [ ] |
| CO.0034 | Storage | OV_STORAGE | Assets > Tank and Storage Objects | [ ] |
| CO.0040 | Test Separator | OV_TESTSEPARATOR | Assets > Facility Objects | [ ] |
| CO.0042 | Production Separator | OV_PRODSEPARATOR | Assets > Facility Objects | [ ] |
| CO.0049 | Well | OV_WELL | Assets > Well and Reservoir Objects | [ ] |
| CO.0051 | Well Hole | OV_WELL_HOLE | Assets > Well and Reservoir Objects | [ ] |
| CO.0070 | Chemical Tank | OV_CHEM_TANK | Assets > Chemical Objects | [ ] |
| CO.0108 | Well Hookup | OV_WELL_HOOKUP | Assets > Facility Objects | [ ] |
| CO.0123 | Test Device | OV_TEST_DEVICE | Assets > Equipment Objects | [ ] |
| CO.0212 | Chemical Injection Point | OV_CHEM_INJ_POINT | Assets > Chemical Objects | [ ] |
| CO.0224 | Shift | OV_SHIFT | Assets > Facility Objects | [ ] |
| CO.0258 | Chemical Stream | OV_CHEM_STREAM | Assets > Chemical Objects | [ ] |
| CO.0260 | Chemical Stream Hookup | OV_CHEM_STRM_HOOKUP | Assets > Chemical Objects | [x] OV-GM, live 4/4, mandatory-field gate |
| CO.2004 | Lifting Account | OV_LIFTING_ACCOUNT | Assets > Transport Objects | [ ] |
| CO.2077 | Channel | OV_CHANNEL | Assets > Transport Objects | [ ] |
| CO.2078 | Loading Arm | OV_LOADING_ARM | Assets > Transport Objects | [ ] |
| CO.2079 | Pilot | OV_PILOT | Assets > Transport Objects | [ ] |
| CO.2080 | Tug Boat | OV_TUG_BOAT | Assets > Transport Objects | [ ] |
| CO.2081 | Pilot Boat | OV_PILOT_BOAT | Assets > Transport Objects | [ ] |
| CP.0030 | Cargo Planning Forecast | OV_FCST_MNGR_FCST_LIST | Cargo Planning > Forecast | [ ] |

## C1. Business Unit only  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2103 | Service | OV_SERVICE | Assets > Service Objects | [ ] |
| CO.3009 | Price Index | OV_PRICE_INDEX | Assets > Sales Objects | [ ] |
| CO.3016 | Price Object | OV_PRICE_OBJECT | Assets > Sales Objects | [ ] |
| CO.3024 | Price Rate | OV_PRICE_RATE | Assets > Sales Objects | [x] OV-GM, live 4/4, BU=SS2 BU (parent_dd worked here) |
| SP.0059 | Property | OV_PROPERTY | Assets > Data Mapping Objects | [ ] |

## C2. Business Unit + Contract Area  (5)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.2016 | Contract | OV_CONTRACT | Assets > Contract Objects | [x] OV-GM, live 4/4, BU=TS5 BU (single-page scope, avoided pager bug) |
| CO.2044 | Contract Capacity | OV_CONTRACT_CAPACITY | Assets > Contract Objects | [ ] |
| CO.2054 | Contract Inventory | OV_CONTRACT_INVENTORY | Assets > Contract Objects | [x] OV-GM, live 4/4, PROVEN chain TS5 BU->TS5 Contract Area->TS5 Shipper C |
| RC.0058 | Division Order | OV_DIVISION_ORDER | Royalty > Royalty USA | [ ] |
| RC.0059 | Royalty Contract | OV_ROYALTY_CONTRACT | Royalty > Royalty Canada | [ ] |

## D. Production Unit + Area  (3)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0019 | Facility Class 1 | OV_XFCTY_CLASS_1 | Assets > Facility Objects | [ ] |
| CO.0205 | Collection Point | OV_COLLECTION_POINT | Assets > Facility Objects | [ ] |
| CO.0244 | Operator Route | OV_OPERATOR_ROUTE | Assets > Facility Objects | [x] OV-GM, live 4/4, PROVEN nav (P3 PU/Area) |

## E. Well hierarchy  (2)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0054 | Well Bore | OV_WELL_BORE | Assets > Well and Reservoir Objects | [ ] |
| CO.0247 | Planned Well | OV_PLANNED_WELL | Assets > Well and Reservoir Objects | (P) wrong-class insert, self-cleaned - see Parked table |

## E3. Well hierarchy (deepest)  (2)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0057 | Well Bore Interval | OV_WELL_BORE_INTERVAL | Assets > Well and Reservoir Objects | [ ] |
| CO.0153 | Perforation Interval | OV_PERF_INTERVAL | Assets > Well and Reservoir Objects | [ ] |

## F. Functional Area  (1)
| BF | Screen | OV_ view | Folder | Status |
|---|---|---|---|---|
| CO.0236 | Message Group | OV_MESSAGE_GROUP | Messaging | [ ] |

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
| Forecast (FC.0010) | FORECAST_TYPE (DB NOT NULL) mandatory + likely popup-picker; Save rejected after 2 attempts |
| Constant Standard (CO.0102) | custom toolbar - standard New-Object menu gesture times out |
| Stream Item (CD.0008) | no :T_data grid renders on open |
| Production Day Table (CO.1033) | INVARIANT (physical delete, not End=Start) - needs physical-delete capability |
| Message Group (CO.0236) (2026-07-31, recovered 2026-08-01) | OV-GM, insert PERSISTS but lands in WRONG SCOPE (Functional Area dropdown pick mismatch: requested option 1 'Administration', persisted option 2 'Allocation') - grid never lists it. Suspect code is the SHARED `select_dropdown`/`Fill OV Dropdown By Label` engine used by 22 OV-GM screens; stopped at the 2-attempt limit rather than touching shared code without the shared-file protocol. Self-cleaned (DB End=Start). NOT confirmed systemic - a later PR (Area, 2026-08-01) validated the same `parent_dd` binding mechanism 7/7, so this may be screen-specific (Functional Area's panel), not universal - still unresolved either way. Originally parked on an unmerged branch (`feature/message-group-iud`); recovered here so the finding is not lost. |
| Facility Class 2 (CO.0021) (2026-08-01) | OV-GM (grid `manageObject:form:T_data`), nav = single OPTIONAL date field + GO (`nav_mode=go_only`), no mandatory dropdown at all. Insert PERSISTS correctly (`PRODUCTION_FACILITY.CLASS_NAME='FCTY_CLASS_2'` confirmed, `OV_FCTY_CLASS_2` view has no RECORD_STATUS/scope filter), but the grid shows "No records found" regardless of nav date (tried today's date and the row's own Start Date 2000-01-01 - both empty). Only one grid id exists in the DOM (`manageObject:form:T_data`); no hidden second grid. Likely needs a parent-scope/Finder selection this screen's navigator panel doesn't expose - not yet supported by current tooling. Self-cleaned (DB End=Start, 0 residual). No bundle shipped (deleted before commit). |
| Planned Well (CO.0247) (2026-08-01) | OV-GM (grid `manageObject:form:T_data`), 5-level cascade nav; PU/Area/Facility Class 1 = PROVEN P1 values (same scope Well/CO.0049 uses), deeper 2 levels left empty per Well's precedent. Insert via the toolbar's "New Object" gesture landed in the WRONG class entirely - `OV_WELL` (`CLASS_NAME='WELL'`), not `OV_PLANNED_WELL` (`CLASS_NAME='PLANNED_WELL'`, confirmed by reading the view SQL - both classes share the SAME base `WELL`/`WELL_VERSION`/`WELL_PERIOD_STATUS` tables, discriminated only by `CLASS_NAME`). The 2 misplaced rows also had ALL scope columns NULL (`OP_PRODUCTIONUNIT_CODE`/`OP_AREA_CODE`/`OP_FCTY_1_CODE` etc.), so they were orphaned regardless of class - the "New Object" gesture on this screen does not bind the nav scope into the new record the way it evidently does on Well's own screen. Root cause not fully isolated (menu-item disambiguation vs a Planned-Well-specific scope-binding gap) - stopped at the 2-attempt limit. Self-cleaned via direct SQL DELETE (child-first: `WELL_PERIOD_STATUS` -> `WELL_VERSION` -> `WELL`, scoped by OBJECT_ID, read in full before delete) since the mis-scoped rows were unreachable via any UI and a raw End=Start close was blocked by `FK_WELL_PERIOD_STATUS_2`. 0 residual confirmed. No bundle shipped. |
