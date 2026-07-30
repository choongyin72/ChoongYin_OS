# EC Automation Scorecard
_Last updated: 2026-06-28_

## N-Series Patterns (Production Data Interaction)

| Pattern | Variant | Object Type | Status | Notes | Date |
|---------|---------|-------------|--------|-------|------|
| N1 | Daily status edit-in-place | PWEL (WR.0001) | ✅ Live 3/3 | Reference impl | - |
| N1 | Daily status edit-in-place | STRM (PO.0002) | ✅ Live 3/3 | | - |
| N1 | Daily status edit-in-place | STRM-OIL (PO.0001) | ✅ Live 3/3 | Sibling of gas stream; "Oil"=generic-EC name for Pluto "Daily Liquid Stream Status"; C5=GRS_VOL; scope P1 @ 2023-01-01 (P1 Cond); reuses T2 verbatim (no shared-file change) | 16 Jun |
| N1 | Daily status edit-in-place | STRM-WAT (PO.0003) | ✅ Live 3/3 | Sibling of gas/oil stream; Daily Water Stream Status; C3=GRS_VOL; scope P1 @ 2023-01-01 (P1 S087); reuses T2 verbatim (no shared-file change); stacked on PR #35 | 17 Jun |
| N1 | Daily status edit-in-place | STRM-ELE (PO.0066) | ✅ Live 3/3 | Sibling; Daily Electrical Stream Status; **C2=POWER_CONSUMPTION** (no volume — electrical); scope P1 @ 2011-01-01 (P1 S046); reuses T2 verbatim (no shared-file change); stacked on PR #36 | 17 Jun |
| N1 | Daily status edit-in-place | TANK-VCF (PO.0005.02) | ✅ Live 3/3 | TANK variant; Daily Tank Status - VCF Calc; grid `dip_table:form`; **C4=Liquid Dip → DV_TANK_DAY_DIP_STATUS.LIQUID_DIP_LEVEL** (view, no base table); name is an INPUT (C1) so row-find by C1 value, not textContent; save triggers VCF recalc; OV_TANK; scope P1 @ 2011-01-01 (P1 T006); reuses T2 verbatim (no shared-file change) | 17 Jun |
| N1 | Daily status edit-in-place | IWEL | ✅ Live 3/3 | | - |
| N1 | Daily status edit-in-place | EQPM | ✅ Live 3/3 | Non-iframed; C4=AVG_PRESS | 14 Jun |
| N1 | Sub-daily status edit | PWEL | ✅ Live 3/3 | Datetime-keyed PK; UI↔DB unit conversion (~14.5x pressure) | 14 Jun |
| N1 | Daily status edit-in-place | PFLW (flowline) | ✅ Live 3/3 | Date-range nav (From+To); 4-level cascade; ON_STREAM_HRS unitless | 15 Jun |
| N1 | Sub-daily status edit | STRM | ✅ Live 3/3 | Datetime-keyed PK; GRS_VOL unitless; doc errors fixed (R7) | 15 Jun |
| N1 | Daily status edit (**UPDATE-only**) | IFLW (water inj flowline) | ✅ Live 4/4 | New/Delete toolbar DISABLED (no record insert/delete — business-domain nature); suite edits the value set/change/clear (clear=update-to-null); sibling of PFLW; IFLW_DAY_STATUS; C2=ON_STREAM_HRS; menu-mirrored path; Bank-style bundle | 15 Jun |
| N1 | Daily status edit (**UPDATE-only**) | GIFLW (gas inj flowline) | ✅ Live 4/4 | Sibling of WI (same grid); IFLW_DAY_STATUS INJ_TYPE=GI; P1 F004 GI; set/change/clear; menu-mirrored path; Bank-style bundle; **stacked on PR #24** | 15 Jun |
| N1 | Monthly status edit | PWEL | ⏸ Parked | Sparse data (13 rows), poor target | 14 Jun |
| N3 | Status process P→V | HA.0001 Daily | ✅ Live 2/2 | Dual DB oracle: ROWS_UPDATED + RECORD_STATUS count | 14 Jun |
| N3 | Status process V→A | HA.0001 Daily | ⏸ Parked | STIM_DAY_VALUE empty (0 rows); WELL_FLUID_ANALYSIS needs WHERE vars + data/SME — next: seed data | 15 Jun |
| N3 | Status process V→A | HA.0001 Monthly | 🔵 Build-ready | Thin new T3 for Monthly Data Status Processes screen | 14 Jun |
| N3 | Status process →A (month) | Monthly Data Status Processes (P1_FwdUpdPar1) | 🔵 Built, dryrun-green, live GATED | Screen model verified live (single Date G:0 + Process G:1); target IWEL_DAY_STATUS 19,659 P rows (data EXISTS); suite `monthly_status_process_run.robot` + thin T3; live behind `--variable LIVE_OK:yes` (no-WHERE → large reversible mutation; confirm blast radius + oracle grain on first observed run) | 15 Jun |
| N1 | Composition edit (per-component) | STRM-GAS-COMP (PO.0020) | ✅ Live 3/3 | NEW pattern: per-COMPONENT rows (not object×day); 8-field nav + `go_button:form:B`; grid loads on Analysis Status=Approved + Sampling=*Spot; edit Methane MOL_PCT (COMPONENT_NO=C1) → `DV_STRM_COMP_ANALYSIS`; Ethane(C2) guard proves no normalize-on-save; new append-only DbVerify `component_value_should_be`; target P1 S038_AGA3_1985_AGA8_Y_1 @ 2011-11-01 | 17 Jun |
| N1 | Composition edit (per-component) | STRM-OIL-COMP (PO.0019) | ✅ Live 3/3 | Oil/condensate sibling of PO.0020; edits **WT_PCT** (cell `C2_in`; oil's C1=mol% empty); Facility Class 1=**P1 Facility Allocation** (not P1 Facility 1); target P1 Alloc S001 M OIL @ 2023-06-01; reuses `component_value_should_be` (col=WT_PCT) — no DbVerify change/no canary; Ethane(C2) guard; TC03 reload-before-revert (2nd Save won't re-arm same session); synthetic wt% data (accepted; realistic=later) | 17 Jun |
| N1 | Composition edit (per-component) | WELL-GAS-COMP (WR.0010.01) | ✅ Live 3/3 | Well-level gas-comp sibling of PO.0020; mandatory (yellow) nav only = Date+PU+Area+Facility → GO; **NEW: SELECT the analysis row** in the header grid (lists all date-valid analyses) before components load; edit Methane MOL_PCT (C1, cell `C1_in` like gas) → `DV_WELL_COMP_ANALYSIS` (ANALYSIS_TYPE=WELL_GAS_COMP); Ethane(C2) guard; reuses `component_value_should_be` (no DbVerify change/no canary); name source WELL_VERSION; TC03 reload+RE-SELECT before revert; target P1 W260 GP Comp Gas @ 2025-04-01 (synthetic 0.1) | 17 Jun |
| EVENT | Alarm event-log (gated inline grid) | ALARMS (`FCTY_DAY_ALARM`) | ✅ Live 4/4 (2026-06-19) | **NEW pattern**: gated cascade nav (Date+PU+Area+Facility+GO) + inline-grid INSERT/UPDATE/DELETE; **no object code → unique REASON marker oracle** (`View Count Where DV_ALARMS REASON`); physical delete; reuses T2 `table_class`; full IUD bundle + SOW; treeview EC Production > Production Operations > Event | 19 Jun |

### Key Learnings
- **UI↔DB unit conversion**: UI(psi) ↔ DB(bar), factor ~14.5038. Naive "DB == typed" oracle fails on pressure/rate cols.
- **Sub-daily PK**: PWEL_SUB_DAY_STATUS keyed on (OBJECT_ID, DAYTIME[+time], SUMMER_TIME) — not TRUNC(date). Needs datetime-keyed DbVerify.
- **ec-worker**: Must be running (overlay 12); scheduler STANDBY on front-end nodes. ORA-06569 = empty data scope, not mechanism failure.
- **Data recovery**: Oracle Flashback AS OF TIMESTAMP used successfully for 192-cell restore.

---

## Section Coverage (Screen Automation)

| Section | Screens | Status | Notes |
|---------|---------|--------|-------|
| Basic Objects | 12/12 | ✅ Complete | Reference IUD suite |
| Financial Objects | 15/15 | ✅ Complete | All suites present (validated 2026-06-15) |
| Commercial Objects | ~11 screens | 🟡 Mostly complete | Sub Field parked |
| Account Mapping | 14/14 | ✅ Complete | Financial; unparked after start-date discovery |
| MIME Type Mapping | TV | ✅ Complete | Table-class/TV, both frameworks |
| Equipment | OV | ✅ Complete | 2nd OV screen |
| Language | IUD | ✅ Complete | 2nd Table-class |
| Dispatching Objects — slice 1 | 24/24 | ✅ Complete | 6 BU-gated OV-GM screens |
| Dispatching Objects — slice 2 | Nomination (TV) + Meter (popup) | ✅ Live 4/4 | Pipeline parked |
| Contract Objects | Contract Area (OV-GM, BU-gated) | ✅ Live 4/4 (2026-06-18) | 1st Contract Objects screen; built by ec-object-iud-builder; sibling of Transport System |
| Cargo Objects | Carrier (OV, plain) | ✅ Live 4/4 (2026-06-19) | 1st Cargo Objects screen; built by ec-object-iud-builder; Bank-family grid + mandatory Unit ref dd |
| Laboratory Objects | Analysis Point (OV-GM, 3-level cascade) | ✅ Live 4/4 (2026-06-19) | 1st Laboratory Objects screen; built by ec-object-iud-builder; clean OV-GM (Op PU/Area/Facility settable in form) |
| Royalty Objects | Royalty Owner (OV, plain) — 1/8 | ✅ Live 4/4 (2026-06-25) | 1st of 8 Royalty Objects screens; built by ec-object-iud-builder; straight Bank-family clone (`OV_ROYALTY_OWNER`, no nav dd, End=Start delete); no shared-file edits; DB-verified + self-cleaning |
| Royalty Objects | Royalty Depositor (OV, plain) — 2/8 | ✅ Live 4/4 (2026-06-25) | 2nd of 8 Royalty Objects screens; built by ec-object-iud-builder; Bank-family clone (`OV_ROYALTY_DEPOSITOR`, no nav dd, End=Start delete); no shared-file edits; DB-verified + self-cleaning; stacked on PR #119 |
| Royalty Objects | Product Group (OV, plain) — 3/8 | ✅ Live 4/4 (2026-06-25) | 3rd of 8 Royalty Objects screens; built by ec-object-iud-builder; Bank-family clone (`OV_PRODUCT_GROUP`, no nav dd, End=Start delete); no shared-file edits; DB-verified + self-cleaning; stacked on PR #120 |
| Royalty Objects | Unit Agreement (OV, plain) — 4/8 | ✅ Live 4/4 (2026-06-25) | 4th of 8 Royalty Objects screens; built via `tools/generators/gen_ov_iud_bundle.py` (Bank-family generator); `OV_UNIT_AGR` (view != slug); no shared-file edits; DB-verified + self-cleaning; stacked on PR #121 |
| Royalty Objects | Tract (OV-GM, gated) — 5/8 | ✅ Live 4/4 (2026-06-26) | 5th Royalty Objects screen, 1st OV-GM; gated by Unit Agreement nav dd; clone of Transport System; `OV_TRACT`; 2 OV-GM gotchas solved (date-effective parent 2010 -> form date 2011; lazy-redraw extra Apply Navigator); no shared-file edits; DB-verified + self-cleaning; stacked on PR #122 |
| Royalty Objects | Unit - Well Setup (PC, gated) — 6/8 | ✅ Live 4/4 full I-U-D (2026-06-27) | 6th Royalty Objects screen, 2nd PC (after Object List Setup); gated by Unit Agreement nav dd; clone of Object List Setup; view `DV_UNIT_WELL_SETUP` (count-delta on `PERF_INTERVAL_CODE`); **INSERT + UPDATE (edit COMMENTS `C3_in`, verified via present-in-view) + physical DELETE**; saved-row select via `C0_in` (NEW row calendar vs SAVED text) cost 1 live run then fixed; UPDATE added after user feedback (initial ship was I/D only — IUD requires all three); test pair UNIT_3 (empty) × 108_WB1-1_PF1; no shared-file edits; DB-verified + self-cleaning |
| Royalty Objects | Tract - Well Setup (PC, cascade) — 7/8 | ✅ Live 4/4 full I-U-D (2026-06-27) | 7th Royalty Objects screen, 3rd PC; sibling of Unit - Well Setup (PR #130) over same `WELL_SETUP` base; CASCADE nav (Unit Agreement -> Tract); view `DV_TRACT_WELL_SETUP` (count-delta on `PERF_INTERVAL_CODE` + COMMENTS present-in-view for UPDATE); INSERT+UPDATE+physical DELETE; live 4/4 first run (RC.0050 lessons applied: full I-U-D scope, C0_in saved-row select, pre-flight); no empty Tract -> baseline-0 member under existing Unit 3 Tract 01, existing P1 PI-5/PI-6 verified intact; no shared-file edits; DB-verified + self-cleaning |
| Royalty Objects | Product Group Setup (3-tier, multi-entity) — 8/8 | ✅ Live 10/10 full I-U-D x3 (2026-06-27) | 8th/LAST Royalty Objects screen + most complex (3-tier master->detail->sub-detail, tab-gated, NO nav); ALL 3 sub-entities full I-U-D: Product Group Setup (`DV_PRODUCT_GROUP_SETUP`), Product Group Cost (`DV_PRODUCT_GROUP_COST`), Stream Calc Category (`PRODUCT_STRM_BAL_CAT` — label!=table); COMMENTS-sentinel oracle; 3 gotchas solved (label!=table; silent-reject->fill mandatory cells; 2nd-save-no-rearm->reload before U/D); no shared-file edits; DB-verified + self-cleaning. **Royalty Objects batch COMPLETE 8/8.** |
| Date Objects | Document Date Term (OV, plain) — 1/5 | ✅ Live 4/4 (2026-06-28) | 1st of 5 Date Objects screens; **pilot for the 19-item IUD deliverable standard** (bundle CHECKLIST.md + reviewer gate); built by ec-object-iud-builder; Bank clone + 2 extra mandatory New-Object inputs (METHOD autocomplete dd + numeric OFFSET, filled last); `OV_DOC_DATE_TERM`; reuses T2 `manage_object` + shared `Select EC Dropdown Option`; no shared-file edits; DB-verified + self-cleaning |
| Date Objects | Document Received Term (OV, plain) — 2/5 | ✅ Live 4/4 (2026-06-28) | 2nd of 5 Date Objects screens; sibling of Document Date Term; clone of the CD.0107 pilot (proven METHOD-dd + OFFSET OV pattern); `OV_DOC_RECEIVED_TERM`; reuses T2 `manage_object` + shared `Select EC Dropdown Option`; no shared-file edits; DB-verified + self-cleaning; stacked on PR #141 |
| Date Objects | Payment Term (OV, plain) — 3/5 | ✅ Live 4/4 (2026-06-28) | 3rd of 5 Date Objects screens; richer form than the term screens (recon caught **shifted field rows**: Method R7, mandatory DAY_VALUE R8, optional Calculation dd R9); test 'Fixed number of Days' + 30; `OV_PAYMENT_TERM`; reuses T2 `manage_object` + shared `Select EC Dropdown Option`; no shared-file edits; DB-verified + self-cleaning; stacked on PR #142 |
| Date Objects | Calendar (OV, custom-URL) — 4/5 | ✅ Live 4/4 (2026-06-28) | 4th of 5 Date Objects screens; plainest (Code/Name/Start Date; 7 weekday checkboxes optional); **custom-URL OV gotcha**: grid `nav:form:T_data` + no GO (not `manage_object_nav_`) — wrong-grid-id assumption failed live (insert persisted, UI read failed), diagnosed vs DB + fixed + residuals cleaned; `OV_CALENDAR`; reuses T2 `manage_object` (Refresh fallback); no shared-file edits; DB-verified + self-cleaning; stacked on PR #143 |
| Date Objects | Calendar Collection (OV, custom-URL) — 5/5 | ✅ Live 4/4 (2026-06-28) | 5th/LAST of 5 Date Objects screens; simplest form (Code/Name/Start Date); custom-URL OV (clone of Calendar exemplar, Refresh fallback) — recon-first meant 4/4 first run; member calendars = separate child grid (out of object-IUD scope); `OV_CALENDAR_COLLECTION`; no shared-file edits; DB-verified + self-cleaning; stacked on PR #144. **Date Objects batch COMPLETE 5/5.** |
| ECIS Excel Upload | End-to-end | ✅ Complete | Own interface + schedule, ran live |
| ECIS Excel Upload | Re-runnable SQL + skills + evidence | ✅ Merged (2026-06-22, PR #93) | `workstreams/ecis-excel-upload/`: idempotent create/delete SQL (update-insert, no MERGE), live DB-verified demo (`AVG_BH_PRESS` NULL→210.5/215/220.3 @ 2003-01-10, self-cleaned), page-broken evidence doc, + `ec-sql-script-builder` & `ecis-excel-upload-builder` skills. KNOWN OPEN: automated `upload→RUN NOW` timing flakiness (root cause unconfirmed) |
| Assets | Recon | ✅ Scanned | Registry complete |

---

## Coverage Strategy (Phased Rollout)

| Phase | Scope | Target | Status |
|-------|-------|--------|--------|
| Phase 1 | Configuration screens (objects, lookups, setups) | All Config sections complete | 🟡 In progress |
| Phase 2 | Operation screens (production data, allocations, status processes) | N1/N3/EVENT patterns | 🔵 Next |
| Phase 3 | Transaction screens (contracts, invoices, nominations, liftings) | TBC after Phase 2 | ⏳ Future |

**Runner batch size target:** 25–50 screens/day (current default: 25, raised from 8 per #150). Increase up to 50 via `EC_LEARN_MAX_SCREENS` env var (legacy `EC_LEARN_MAX` still honoured).

**Phase 1 priority order:** Basic Objects → Financial Objects → Commercial Objects → Royalty Objects (✅ 8/8) → Date Objects (✅ 5/5) → remaining config sections (Account Mapping, MIME, Equipment, Language, Dispatching, Contract, Cargo, Laboratory Objects).

**Phase 2 entry criteria:** All Phase 1 config sections ✅ Complete in Section Coverage table above.

---

## Framework Health

| Item | Status | Notes |
|------|--------|-------|
| robocop lint | ✅ Clean | 43→2 warnings after health pass |
| T3 Open-Screen promotion | ✅ Done | Shared keywords adopted |
| Dynamic test data | ✅ Refactored | |
| maximize-browser + expand-screen | ✅ Shared | Adopted across all suites |
| WR.0001 canary | ✅ Running | Used as regression check after each new suite |
| DB restore / teardown | ✅ Pattern established | All suites self-cleaning |
| R16 bundle-credential guard | ✅ Live (2026-06-19) | `scripts/check_bundle_hygiene.py` FAILs on hardcoded creds in `screens/**/playwright/*.py`; wired into ec-object-iud-builder Step-5 verify (PR #77/#78); shared `tmp/scripts/ec_session.py` login helper |
| EC screen-family registry (machine-readable) | ✅ Live (2026-06-19) | `ec_screen_registry.json` (7 IUD families + golden exemplars); `resolve_ec_screen.py` prints CLONE hint; `scan_ec_screen.py` auto-fills gated nav dd + GO (PR #74/#75/#76) |
| EVENT_LOG family (code-less event rows) | ✅ Live (2026-06-20) | New family in `ec_screen_registry.json`; golden exemplar Alarms (`FCTY_DAY_ALARM`/`DV_ALARMS`); marker oracle + physical delete (R19); next clone = Reported Alarms (PR #84) |
| Bundle/recon ASCII hygiene | 🟡 Gap (R20) | All 3 bundles this cycle shipped an em-dash in the FAIL-branch print string; skill template + `check_bundle_hygiene.py` static-ASCII check pending |
| Bundle/recon ASCII hygiene | ✅ Live (2026-06-20) | CLOSES the row above: PR #87 ASCII-normalised 40 bundle/recon `.py` + extended `check_bundle_hygiene.py` with a static non-ASCII gate over `playwright/*.py` + `investigation/*.py` (FAIL on any non-ASCII byte). Reviewer reproduced PASS (R16 + R20) over 48 bundles + 121 recon; 0 non-ASCII in either glob. Wired into skill Step-5 verify |

---

## Parked Items (Resume Backlog)

| Item | Reason | Next step |
|------|--------|-----------|
| N1 Monthly PWEL | Sparse data | Find a month with adequate PWEL_MTH_STATUS rows |
| N3 V→A Daily | STIM_DAY_VALUE empty (0 rows); WELL_FLUID_ANALYSIS needs WHERE_FORMULA var resolution + seeded data | Seed STIM_DAY_VALUE provisional rows or get SME confirmation on Analysis class→physical-table |
| N3 V→A Monthly | Build-ready | Thin new T3 for Monthly Data Status Processes screen |
| Dispatching Pipeline | Not attempted | Resume from slice 2 checkpoint |
| ~~Financial Objects (3 parked)~~ | Closed as stale — all 15 FO suites present (validated 2026-06-15) | — |
| Commercial Sub Field | Not attempted | |
| Disposition Type (OV, CO.0208) | ✅ Done 2026-07-25 — RF 4/4 + Playwright 7/7, DB-verified vs OV_DISPOSITION_TYPE, self-clean; 1st OV-reuse-target on shared py/ec_object_iud.py engine | 34 uncovered OV reuse-targets remain (see docs/ov-reuse-targets.md) |
| Report Area (OV, RP.0017) | ✅ Done 2026-07-25 — RF 4/4 + Playwright 7/7, DB-verified vs OV_REPORT_AREA, self-clean; 2nd OV-reuse-target (simplest OV) | 33 uncovered OV reuse-targets remain (see docs/ov-reuse-targets.md) |
| Choke (OV, CO.0185) | ✅ Done 2026-07-25 — RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CHOKE (Name+Comments), self-clean; 3rd OV-reuse-target | see docs/ov-reuse-targets.md |
| Choke Model (OV, CO.0217) | ✅ Done 2026-07-26 — RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CHOKE_MODEL (Name+Description), self-clean; 4th OV-reuse-target | 31 uncovered OV reuse-targets remain |
| Port (OV, CO.2003) | ✅ Done 2026-07-26 — RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_PORT (Name), self-clean; 5th OV-reuse-target; **first label-driven (zero hardcoded ids)** + shared engine now handles **paginated grids** generically (Bank canary re-run 7/7) | 30 uncovered OV reuse-targets remain |
| Berth (OV, CO.2012) | ✅ Done 2026-07-26 — RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_BERTH (Name), self-clean; 6th OV-reuse-target; label-driven; added generic engine `wait_for_row_absent` (async delete-redraw). Stacked on #203 | 29 uncovered OV reuse-targets remain |
| Canal (OV, CO.2069) | ✅ Done 2026-07-26 — RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CANAL (Name), self-clean; 7th OV-reuse-target; label-driven; **first scaffolded by tmp/gen_ov_screen.py** | 28 uncovered OV reuse-targets remain |
| Revenue Stream Category (OV, CD.0015) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STREAM_CATEGORY (Name), self-clean; 8th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Stream Item Category (OV, CD.0016) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STREAM_ITEM_CATEGORY (Name), self-clean; 9th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Split Item Other (OV, CD.0017) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_SPLIT_ITEM_OTHER (Name), self-clean; 10th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Inventory Area (OV, CD.0115) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_INVENTORY_AREA (Name), self-clean; 11th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Reservoir Block (OV, CO.0133) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_RESV_BLOCK (Name), self-clean; 12th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Reservoir Formation (OV, CO.0135) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_RESV_FORMATION (Name), self-clean; 13th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Blend (OV, CO.0219) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_BLEND (Name), self-clean; 14th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Chemical Transport Tank (OV, CO.0257) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CHEM_TRANS_TANK (Name), self-clean; 15th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Calculation Context (OV, CO.1059) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CALC_CONTEXT (Name), self-clean; 16th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Dummy Tag Event Object (OV, CO.1063) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_DUMMY_TAG_EVENT (Name), self-clean; 17th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Transactional Inventory Layout Set (OV, IN.0033) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_TRANS_INV_TMPL_SET (Name), self-clean; 18th OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Input List (OV, CD.0035) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STREAM_ITEM_COLLECTION (Name), self-clean; 1st mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Input List (OV, CD.0035) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STREAM_ITEM_COLLECTION (Name), self-clean; 1st mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| HCB System (OV, CD.0097) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_BALANCE (Name), self-clean; 2nd mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Input List (OV, CD.0035) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STREAM_ITEM_COLLECTION (Name), self-clean; 1st mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| HCB System (OV, CD.0097) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_BALANCE (Name), self-clean; 2nd mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Config Variable (OV, IN.0031) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CONFIG_VARIABLE (Name), self-clean; 3rd mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Input List (OV, CD.0035) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STREAM_ITEM_COLLECTION (Name), self-clean; 1st mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| HCB System (OV, CD.0097) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_BALANCE (Name), self-clean; 2nd mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Config Variable (OV, IN.0031) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CONFIG_VARIABLE (Name), self-clean; 3rd mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Orifice Plate (OV, CO.0089) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_ORIFICE_PLATE (Name), self-clean; 4th (scanner-driven, extra mandatory fields) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Data Extract Setup (OV, SP.0043) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_SUMMARY_SETUP (Name), self-clean; 5th mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Data Extract Set (OV, SP.0049) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_SUMMARY_SET (Name), self-clean; 6th mandatory-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Meter Run (OV, CO.0091) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_METER_RUN (Name), self-clean; 7th (scanner-driven: 3 dropdowns + 3 extra mandatory) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Document Template (OV, CD.0013) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_DOC_TEMPLATE (Name), self-clean; extra-field (scanner-driven) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Transactional Inventory Properties (OV, IN.0023) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_TRANS_INVENTORY (Name), self-clean; extra-field (scanner-driven) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Storage Flow (OV, CO.2091) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_STORAGE_FLOW (Name), self-clean; cascade-dropdown (first-available) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| UOP Key (OV, CD.0099) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_FIN_UOP_DEPR_KEY (Name), self-clean; cascade-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Process Train (OV, CO.0120) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_PROCESS_TRAIN (Name), self-clean; cascade-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Calculation Group Context (OV, CO.0245) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CALC_GRP_CONTEXT (Name), self-clean; cascade-dropdown OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Deferment Group (OV, CO.0149) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_DEFERMENT_GROUP (Name), self-clean; plain (open-gesture was transient) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| EC Code Object (OV, CD.0135) | ✅ Done 2026-07-26 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_EC_CODE_OBJECT (Name), self-clean; cascade-dropdown (Name is non-mandatory) OV-reuse-target; label-driven, generator-scaffolded | see docs/ov-reuse-targets.md |
| Reservoir Block Formation (OV junction, CO.0137) | 🟡 Driver-proven 2026-07-27 - Playwright multi-object 15/15 (DB-verified vs OV_RESV_BLOCK_FORMATION + parents, self-clean); RF 5-TC suite WIP (2 RF-gesture issues). Full multi-object I-U-D (create Block+Formation -> link -> reverse teardown) | RF suite follow-up |
| Conversion Group (custom-URL OV, CO.1049) | ✅ Done 2026-07-27 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CONVERSION_GROUP (Name), self-clean; 1st custom-URL OV (no navigator GO, toolbar Refresh); label-driven | see docs/ov-non-bank-targets.md |
| Document Sequence (custom-URL OV, CD.0109) | ✅ Done 2026-07-27 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_DOC_SEQUENCE (Name), self-clean; custom-URL OV + mandatory Starting Point field; label-driven | see docs/ov-non-bank-targets.md |
| Calculation Library (custom-URL OV, CO.1060) | ✅ Done 2026-07-27 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_CALC_LIBRARY (Name), self-clean; custom-URL OV; label-driven | see docs/ov-non-bank-targets.md |
| Task Process (custom-URL OV, CO.0191) | ✅ Done 2026-07-27 - RF 4/4 + Playwright 7/7 via verify_screen.py gate (OVERALL PASS), DB-verified vs OV_TASK_PROCESS (Name), self-clean; custom-URL OV; label-driven | see docs/ov-non-bank-targets.md |
| Node (OV-GM, CD.0006) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_NODE (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Chemical Tank (OV-GM, CO.0070) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_CHEM_TANK (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Chemical Injection Point (OV-GM, CO.0212) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_CHEM_INJ_POINT (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Test Separator (OV-GM, CO.0040) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_TESTSEPARATOR (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Production Separator (OV-GM, CO.0042) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_PRODSEPARATOR (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Test Device (OV-GM, CO.0123) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_TEST_DEVICE (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Channel (OV-GM, CO.2077) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_CHANNEL (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Loading Arm (OV-GM, CO.2078) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_LOADING_ARM (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Pilot Boat (OV-GM, CO.2081) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_PILOT_BOAT (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Tug Boat (OV-GM, CO.2080) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_TUG_BOAT (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
| Well Hookup (OV-GM, CO.0108) | OK Done 2026-07-30 - RF 4/4 pass + Playwright 8/8 via verify_screen.py (OVERALL PASS), DB-verified vs OV_WELL_HOOKUP (Name), self-clean; OV-GM gated-navigator; label-driven; Op PU first-available | see docs/ov-non-bank-targets.md |
