# Grid column-filter standardization — screen tracking checklist

_Created 2026-08-23. Tracks which EC screens have had the Account/Bank-style grid
column-filter row-locate feature applied, so future sessions don't redo work on a
screen that's already done, and know exactly which are still pending._

## Background

Account's IUD suite (PR #422, 2026-08-22) originally hit a live failure because
`OV_FIN_ACCOUNT` has 110+ rows across a 20-row/page grid, and the test code sorted
onto a page beyond page 1 — the shared T1/T2 row-select/check keywords only ever
looked at the currently-rendered page. The fix used EC's own grid hamburger-menu
column filter (`resources/grid_menu.resource`, a server-side "contains" search
across the FULL dataset in one call) instead of walking pages.

Per owner direction ("can other screens (e.g. bank, list_object) also use filter
too... standardise it" → "same to other ec screens"), this was generalized in two
layers, both in **PR #423** (`feature/ov-grid-filter-standardize`):

1. **Implicit fallback (applies automatically, zero code change per screen)** —
   `resources/manage_object.resource`'s `Select Object Row` / `OV Row Should Exist` /
   `OV Row Should Not Exist` try the fast direct-click/current-page path first, and
   only fall back to filtering if the row isn't found within 3s (or, for absence
   checks, always prefer the filter-based full-dataset check when the grid supports
   it). **This already applies to every OV screen using `manage_object.resource`,
   whether or not it appears in the "explicit" table below.**
2. **Explicit `Find <Screen> Row By Filter` / `Clear <Screen> Row Filter` wrappers**
   — thin T3 keywords calling the shared T2 `Find Object Row By Filter` /
   `Clear Object Row Filter`, wired directly into Update/Find/Verify-Found/Delete so
   the filter fires deliberately, not just as a fallback. This is what the table
   below tracks — it only applies to screens already rebuilt to the label-driven,
   T2-consolidated pattern (the "Bank pattern"), since that's the shape these
   wrapper keywords slot into.

**Deliberately NOT wired into `Verify <Screen> Record Removed`/`Does Not Exist`** on
any screen — those already get a filter-based full-dataset absence check for free
via the shared T2 `OV Row Should Not Exist` (layer 1 above), so an outer explicit
wrap there would be pure redundant duplication with no behavior change.

## Screens eligible for the explicit wrapper (rebuilt to the Bank-pattern T2-consolidated shape)

| Screen | Explicit filter wired? | Notes |
|---|---|---|
| Bank | ✅ DONE (2026-08-23) | Small/single-page grid — filter fires but narrows to 1 row instantly either way. Verified live 5/5, filter keywords confirmed fired via output.xml. |
| State | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Object List | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Account | ✅ DONE (2026-08-22, PR #422 + #423) | The original screen this fix was built for — 110+ rows/6 pages, genuinely needs it. `Find/Clear Account Row By Filter` were the FIRST version of this pattern, later promoted into shared T2 and Account's own T3 updated to delegate to the promoted keywords (commit a9a36cd9). |
| Cost Centre | ✅ DONE (2026-08-23) | Custom-URL OV, small grid. Live 5/5, filter confirmed fired. |
| Revenue Order | ✅ DONE (2026-08-23) | Custom-URL OV, small grid. Live 5/5, filter confirmed fired. |
| WBS | ✅ DONE (2026-08-23) | Custom-URL OV, small grid. Live 5/5, filter confirmed fired. |
| Payment Scheme | ✅ DONE (2026-08-23) | Manage-object OV. Live 5/5, filter confirmed fired. |
| Exchange Rate Source | ✅ DONE (2026-08-23) | Manage-object OV. Live 5/5, filter confirmed fired. |
| Region | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired (output.xml). |
| Functional Area | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Business Unit | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Production Unit | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Company | ✅ DONE (2026-08-23) | Large PAGINATED grid (8 pages, hundreds of rows) with a prior non-reproducible TC05 flake on its first-ever live build - the strongest real candidate in this whole set for actually needing the filter, not just consistency. Live 5/5 clean on this run (no flake), filter confirmed fired. |
| Country | ✅ DONE (2026-08-23) | Small grid (20 rows). Batch-2 rebuild, filter wiring included from the start (not deferred as a follow-up). Live 5/5, filter confirmed fired exactly 5 times via output.xml grep (Update/Find/Verify-Insert-Exists/Verify-Found/Delete). |
| County | ✅ DONE (2026-08-23) | Manage-object OV, small grid (batch-2 conversion, parallel worker clone). Live 5/5, filter confirmed fired (5 hits for `Find County Row By Filter` in output.xml). |
| Currency | ✅ DONE (2026-08-23) | Manage-object OV, small grid. Batch-2 5-screen Bank-pattern conversion (Country/County/Regulatory Permits/Currency/VAT Code). Live 5/5, filter confirmed fired (5 hits in output.xml for `Find Currency Row By Filter`). Also confirmed live: the registry-flagged mandatory "Active" checkbox (`MandatoryCellStyleWhite` class) is NOT actually save-blocking - a checkbox has no "empty" state, so it's omitted from the insert properties (see currency_insert.properties). |
| VAT Code | ✅ DONE (2026-08-23, PR #431) | Manage-object OV, small/single-page grid (15 rows). Wired in from the start (batch-2, not a follow-up). Live 5/5, filter keyword confirmed fired 7x via output.xml grep. |
| Regulatory Permits | ✅ DONE (2026-08-23, batch-2) | Custom-URL OV (grid `nav:form:T_data`, WITH a GO button unlike Account/Cost Centre - confirmed live, a shape not seen elsewhere). Small grid, currently 0 rows on this sandbox. Live 5/5, filter confirmed fired (7 hits in output.xml). |
| Field Group | ✅ DONE (2026-08-23, batch-3) | Manage-object OV, small grid (plain navigator, no mandatory nav scope - confirmed live). Batch-3 5-screen Bank-pattern conversion (Customer/Field Group/Licence/MMS Lease/Operator Lease), parallel worker clone. Live 5/5, filter wiring included from the start, confirmed fired (5 hits for `Find Field Group Row By Filter` in output.xml). |
| Customer | ✅ DONE (2026-08-23, batch-3) | Manage-object OV, small grid (Commercial Objects). Batch-3 5-screen Bank-pattern conversion (Customer/Field Group/Licence/MMS Lease/Operator Lease, parallel isolated clones). Wired in from the start. Live 5/5, filter keyword confirmed fired 5x via output.xml grep. |
| Operator Lease | ✅ DONE (2026-08-23, batch-3) | Manage-object OV, empty grid (0 rows on this sandbox). Batch-3 5-screen Bank-pattern conversion (Customer/Field Group/Licence/MMS Lease/Operator Lease). Wired in from the start. Live 5/5, filter confirmed fired (5 hits in output.xml for `Find Operator Lease Row By Filter`). |
| MMS Lease | ✅ DONE (2026-08-23, batch-3) | Manage-object OV, small/empty grid (0 rows before this suite's own TC02). Batch-3 5-screen Bank-pattern conversion (Customer/Field Group/Licence/MMS Lease/Operator Lease). Wired in from the start. Live 5/5, filter confirmed fired (5 hits each for `Find MMS Lease Row By Filter`/`Clear MMS Lease Row Filter` in output.xml). |
| Licence | ✅ DONE (2026-08-23, batch-3) | Manage-object OV, small grid (12 rows). Batch-3 5-screen Bank-pattern conversion (Customer/Field Group/Licence/MMS Lease/Operator Lease, parallel isolated clones). Wired in from the start. Live 5/5, filter keyword confirmed fired exactly 5 times via output.xml grep. |
| Vendor | ✅ DONE (2026-08-23, batch-4) | Manage-object OV, small grid (20 rows, Commercial Objects). Batch-4 conversion (State Lease/Vendor/Cost Object Mapping/DOA Credit Limit/Product Description, parallel isolated clones). Wired in from the start. Live 5/5, filter keyword confirmed fired 5x via output.xml grep. |
| State Lease | ✅ DONE (2026-08-23, batch-4) | Manage-object OV, empty grid (0 rows on this sandbox). Batch-4 5-screen Bank-pattern conversion (State Lease/Vendor/Cost Object Mapping/DOA Credit Limit/Product Description, parallel isolated clones). Wired in from the start. Live 5/5, filter confirmed fired (5 hits in output.xml for `Find State Lease Row By Filter`). |
| Product Description | ✅ DONE (2026-08-23, batch-4) | Manage-object OV, 20-row grid (Financial Objects), screen-prefixed Code label ("Product Node Item Code") + 3 mandatory reference dropdowns (Product/Node/Financial Code). Batch-4 5-screen Bank-pattern conversion (State Lease/Vendor/Cost Object Mapping/DOA Credit Limit/Product Description, parallel isolated clones, see `tmp/batch4_shared_findings.md`). Wired in from the start. Live 5/5, filter keyword confirmed fired exactly 5 times via output.xml grep. |
| Cost Object Mapping | ✅ DONE (2026-08-23, batch-4) | Manage-object OV, small grid (90 rows, Financial Objects). Batch-4 5-screen Bank-pattern conversion (State Lease/Vendor/Cost Object Mapping/DOA Credit Limit/Product Description, parallel isolated clones). Confirmed NOT a scope mismatch despite the "Mapping" name - genuine Code/Name manage-object OV with 4 mandatory reference dropdowns (one is a Start-Date/Object-Type cascade). Wired in from the start. Live 5/5, filter keyword confirmed fired 5x via output.xml grep. |
| DOA Credit Limit | ✅ DONE (2026-08-23, batch-4) | Manage-object OV, small grid (3 rows). Batch-4 5-screen Bank-pattern conversion (State Lease/Vendor/Cost Object Mapping/DOA Credit Limit/Product Description, parallel isolated clones). Wired in from the start. Live 5/5 (after fixing a real conditional-mandatory Currency business rule and excluding Role Name from the live-DOM round-trip - see docs/ec_screen_registry.md), filter keyword confirmed fired 7x via output.xml grep. |
| Sales Order | ✅ DONE (2026-08-23, batch-5) | Manage-object OV, 20+ row grid (Financial Objects), screen-prefixed Code label ("Product Sales Order Code") + 2 mandatory reference dropdowns (Company/Field, neither a cascade). Confirmed NOT a scope mismatch despite the "Order" name (genuine Code/Name manage-object OV, no nav dropdown, no document-header-plus-lines shape) - batch-5 shared-findings naming concern resolved live. Wired in from the start. Live 5/5, filter keyword confirmed fired 5x via output.xml grep. |
| Product Group | ✅ DONE (2026-08-23, batch-5) | Manage-object OV, 19-row grid (Royalty Objects), screen-prefixed labels ("Product Group Code"/"Product Group Name") like State — NOT the generic "Code"/"Name" Bank/Object List use. Only Start Date is CSS-mandatory beyond Code/Name; Sort Order/Product Group Type (dropdown)/Comments are optional and left out of the IUD flow (fill-only-needed-fields convention). Batch-5 5-screen Bank-pattern conversion (Sales Order/Product Group/Royalty Depositor/Royalty Owner/Unit Agreement, parallel isolated clones). Wired in from the start. Live 5/5, filter keyword confirmed fired exactly 5 times via output.xml grep. |
| Unit Agreement | ✅ DONE (2026-08-23, batch-5) | Manage-object OV, small grid (4 rows, Royalty Objects). Batch-5 conversion from the older hardcoded-field-id generator build to the Bank pattern; screen-prefixed Code label ("Unit Agreement Code") + an optional Comments field + an objectForm-level End Date field (left unset at insert). Wired in from the start. Live 5/5, filter keyword confirmed fired 5x via output.xml grep. |
| Royalty Owner | ✅ DONE (2026-08-23, batch-5) | Manage-object OV, small grid (Royalty Objects), screen-prefixed Code/Name labels ("Royalty Owner Code"/"Royalty Owner Name"). Batch-5 Bank-pattern conversion (Sales Order/Product Group/Royalty Depositor/Royalty Owner/Unit Agreement, parallel isolated clones, see `tmp/batch5_shared_findings.md`). Wired in from the start. Live 5/5, filter keyword confirmed fired exactly 5 times via output.xml grep. |
| Royalty Depositor | ✅ DONE (2026-08-23, batch-5) | Manage-object OV, small grid (2 rows). Batch-5 conversion (Sales Order/Product Group/Royalty Depositor/Royalty Owner/Unit Agreement, parallel isolated clones). Screen-prefixed labels confirmed live ("Royalty Depositor Code"/"Royalty Depositor Name"), matching State's precedent. Only Code/Name/Start Date mandatory - kept the same minimal field scope as the already-proven prior driver (no scope expansion). Wired in from the start. Live 5/5 after one retry (first live run hit a transient shared-sandbox account lockout + cross-session "unsaved changes" artifact from a concurrent Batch-5 agent sharing the same sysadmin login - not a defect in this screen's automation; confirmed clear on retry after a leftover test row was cleaned up), filter keyword confirmed fired 5x via output.xml grep for `Find Royalty Depositor Row By Filter`. |
| Calendar Collection | ✅ DONE (2026-08-23, batch-6) | Custom-URL OV (grid `nav:form:T_data`, NO GO button - confirmed live, matching Account/Cost Centre's shape). Batch-6 (FINAL batch) conversion from the older hardcoded-field-id pattern. Generic Code/Name labels (not screen-prefixed) confirmed live via a New Object form field-label scan (8 ECCell labels; no weekday-indicator checkboxes on this EC build, contrary to the pre-existing page object's stale docstring). Wired in from the start. Live 5/5, filter keyword confirmed fired exactly 5 times via output.xml grep for `Find Calendar Collection Row By Filter`. |
| Account Mapping | ✅ DONE (2026-08-23, batch-6, FINAL) | Manage-object OV, 75-row custom grid (Financial Objects) with 13 grid columns (Code, Name, Product, Line Item Type, Financial Code, Company Category, Company, Status, Debit / Credit, Debit PK, Credit PK, Account Category, Financial Account) and NO Start Date column - grid-verify only checks Code/Name. Confirmed NOT a scope mismatch despite the "Mapping" name (genuine Code/Name manage-object OV, same outcome as Cost Object Mapping in Batch 4). Reused the screen's own already-proven reference combination (`JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT`, confirmed still free live) across EIGHT mandatory reference dropdowns + one cascade-dependency field. Wired in from the start. Live 5/5 after one retry (Line Item Type re-renders as short code `ALL` after reload - excluded from the live-DOM round-trip form check, same DOA Credit Limit Role Name gotcha), filter keyword confirmed fired 5x via output.xml grep for `Find Account Mapping Row By Filter`. |

| Calendar | ✅ DONE (2026-08-23, batch-6, final batch) | Custom-URL OV (grid `nav:form:T_data`, NO navigator/GO button - confirmed live, matching Account/Cost Centre's shape). Screen-prefixed labels confirmed live ("Calendar Code"/"Calendar Name"). Only Code/Name/Start Date mandatory - 7 weekday-indicator checkboxes + Description/Comments left optional/out of scope, matching the prior driver's own field scope (no expansion). Wired in from the start. Live 5/5, filter keyword confirmed fired exactly 5 times via output.xml grep for `Find Calendar Row By Filter`. DB self-clean confirmed 0 residual rows via a fresh oracledb connection. |
| Canal | ✅ DONE (2026-08-23, batch-7, NEW round beyond the closed 37/37 pool) | Manage-object OV (Transport Objects, CO.2069), small grid (2 real rows: SUEZ/PANAMA). Screen-prefixed labels confirmed live via the already-proven Playwright driver's source (`py/ec_object_iud.py`/`py/canal_iud.py`, 7/7 live) - "Canal Code"/"Canal Name" (`code_label=Canal Code` threaded through T2, matching State's precedent). Rebuilt from the OLDER argument-driven page object (`Insert Canal Record`/`Update Canal Name`/`Delete Canal`, no properties files, no filter wiring) up to the full Bank pattern - properties-file-driven insert/update/verify + `Find Canal Row By Filter`/`Clear Canal Row Filter` wired into Update/Find/Verify-Found/Delete. Only Canal Code/Canal Name/Start Date mandatory (Time Zone dropdown optional, skipped - matches the prior driver's own field scope, no expansion). Fixed test code `CANAL_KIEL` (confirmed free live). Wired in from the start. Live 5/5, filter keyword confirmed fired 15x via output.xml grep for `Find Canal Row By Filter`/`Clear Canal Row Filter`/`Find Object Row By Filter`/`Clear Object Row Filter`. DB self-clean confirmed 0 residual rows via a fresh oracledb connection (only SUEZ/PANAMA remain). |

**37 of 37 done. ALL 23 BANK-PATTERN SCREENS NOW HAVE EXPLICIT GRID-FILTER
WIRING.** All 5 batch-2 screens (Country, County, Currency, VAT Code,
Regulatory Permits), all 5 batch-3 screens (Field Group, Customer, Operator
Lease, MMS Lease, Licence), all 5 batch-4 screens (Vendor, State Lease,
Product Description, Cost Object Mapping, DOA Credit Limit), all 5
batch-5 screens (Sales Order, Product Group, Unit Agreement, Royalty Owner,
Royalty Depositor), and all 3 batch-6 screens (Calendar Collection, Account
Mapping, Calendar) are in — plus the original 14 pre-existing Bank-pattern
screens (Bank, State, Object List, Account, Cost Centre, Revenue Order, WBS,
Payment Scheme, Exchange Rate Source, Region, Functional Area, Business Unit,
Production Unit, Company). Every screen rebuilt to the Bank-pattern
T2-consolidated shape now has the explicit filter wiring. Any FUTURE screen
rebuilt to this pattern should get the same treatment as part of its own
build (see "How to update this doc" below).

## Batch 7 additions (2026-08-23) — consolidated

_Section consolidated by the reviewer at the Batch 8 merge: the parallel per-screen
PRs each appended their own "Batch 7" section header; rows below are the union, each
screen exactly once, content unchanged._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Berth | ✅ DONE (2026-08-23, Batch 7) | Manage-object OV, single-page grid (11 rows, Transport Objects). Screen-prefixed labels ("Berth Code"/"Berth Name") confirmed via ec-ui-knowledge/screens/berth.md + proven py/berth_iud.py (Code/Name/Start Date mandatory only, all dropdowns optional). Fixed test code `AUTOTEST_BERTH`. Wired in via this batch (prior page object already had label-driven fields but no properties-file-driven insert/update or explicit filter). Live 5/5, filter keyword confirmed fired 15x via output.xml grep for `Find Berth Row By Filter`. Dryrun 753/753. No shared T1/T2 edits. DB self-clean confirmed via fresh oracledb connection. |
| Blend | ✅ DONE (2026-08-23, batch-7) | Manage-object OV (Hydrocarbon Objects), small grid (3 rows). Had a PARTIAL prior label-driven build (`Fill OV Field By Label`, 2026-07-26) missing properties-file-driven insert/update and explicit grid-filter wiring - upgraded to the full Bank pattern. Screen-prefixed labels confirmed live ("Blend Code"/"Blend Name", like State's own precedent) - NOT the generic "Code"/"Name" Bank/Customer use, so `code_label=Blend Code` is threaded through Insert/Update/Find. Only Blend Code/Blend Name/Start Date mandatory (MandatoryCellStyle confirmed via a fresh per-row class dump); Master System Code/Name, Sort Order, End Date left optional/out of scope. Description is optional but exercised (never populated on any real production Blend row - 0 non-null DESCRIPTION rows confirmed live). Wired in from the start. Live 5/5, filter keyword confirmed fired 50 hits total (Find+Clear across TC02-05) via output.xml grep. DB self-clean confirmed 0 residual `AUTOTEST_BLEND` rows via a fresh oracledb connection. |

## Batch 8 additions (2026-08-23) — consolidated

_Section consolidated by the reviewer at the Batch 8 merge: the parallel per-screen
PRs each appended their own "Batch 8" section header; rows below are the union, each
screen exactly once, content unchanged._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Orifice Plate | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV, single-page grid (Stream Objects). Screen-prefixed labels ("Orifice Code"/"Orifice Name") confirmed via ec-ui-knowledge/screens/orifice_plate.md + proven py/orifice_plate_iud.py. Mandatory beyond Code/Name/Start Date: Material (dropdown), Diameter [mm], Measurement Temp [°R] (all confirmed mandatory, not optional-skippable). Fixed test code `AUTOTEST_ORIFICE_PLATE` (confirmed free live). Wired in via this batch (prior page object already had label-driven fields but no properties-file-driven insert/update or explicit filter, and only had TC01-04, no TC04 Find). Live 5/5, filter keyword confirmed fired 13x via output.xml grep for `Find Orifice Plate Row By Filter`. Dryrun 758/758. No shared T1/T2 edits. DB self-clean confirmed via fresh oracledb connection. |
| Calculation Context | ✅ DONE (2026-08-23, batch-7) | Manage-object OV (`OV_CALC_CONTEXT`), already partially on the label-driven pattern (`Fill OV Field By Label`) from an earlier build - this round added the missing properties-file-driven Insert/Update (`testdata/calculation_context_*.properties`) and explicit `Find/Clear Calculation Context Row By Filter` grid-filter wiring (wired into Update/Find/Verify-Found/Delete, matching Bank/Account). Live-recon confirmed Bank-pattern shape: objectForm = Calc Context Code/Name/Start Date (mandatory)/End Date/Description/Comments; updateAttributes = Calc Context Code (read-only)/Name/Description/Comments (no Start/End Date there, matching Bank); no mandatory navigator dropdown beyond the universal GO bar. Fixed test code `AUTOTEST_CALCCTX` (confirmed free live). Live 5/5, robocop clean, dryrun 753/753, DB self-clean 0 residual (fresh oracledb connection), filter keyword confirmed fired (12x `Find Calculation Context Row By Filter` / 8x `Filter Grid Text Column By Value` via output.xml grep). No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed - reused every consolidated T2 keyword as-is. |
| Inventory Area | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV (Inventory Objects, CD.0115). Had a PARTIAL prior label-driven build (`Fill OV Field By Label`, 2026-07-26) missing properties-file-driven insert/update and explicit grid-filter wiring - upgraded to the full Bank/Berth pattern. Screen-prefixed labels confirmed live ("Inventory Area Code"/"Inventory Area Name") via the pre-existing page object + proven `py/inventory_area_iud.py`, re-confirmed via a fresh live Playwright run 2026-08-23. Only Inventory Area Code/Inventory Area Name/Start Date mandatory - no other fields on this screen's insert form. Fixed test code `AUTOTEST_INVA` (confirmed free live via fresh oracledb connection, both before and after the live RF run). Live 5/5, filter keyword confirmed fired 11x (`Find Inventory Area Row By Filter`) via output.xml grep. Dryrun 758/758. No shared T1/T2 (`manage_object.resource`/`common.resource`) edits - reused every consolidated T2 keyword as-is. DB self-clean confirmed 0 residual `AUTOTEST_INVA`/`AUTOTEST%` rows via a fresh oracledb connection. |
| Meter Run | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV (Stream Objects, CO.0091). Screen-prefixed labels ("Meter Run Code"/"Meter Run Name") confirmed via the proven py/meter_run_iud.py + the prior live-tested page object. Mandatory: Meter Run Code/Meter Run Name/Start Date + Type of Taps/Pipe Material/Location of Taps dropdowns + Pipe Diameter (temp uncorrected) [mm]/Diameter Meas Temp [°R]/All Calibration Factor (all confirmed mandatory live via the existing driver - Save is rejected without them, unlike Bank/Berth's Code/Name/Start-Date-only set). Fixed test code `AUTOTEST_METER_RUN` (confirmed free live). Wired in via this batch (prior page object already had label-driven fields but no properties-file-driven insert/update or explicit filter). Live 5/5, filter keyword confirmed fired 15x via output.xml grep for `Find Meter Run Row By Filter`. Dryrun 758/758. No shared T1/T2 edits. DB self-clean confirmed 0 residual `AUTOTEST_METER_RUN` rows via a fresh oracledb connection. Delete End Date field id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` confirmed live via read-only recon on an existing row (never saved). |
| Chemical Transport Tank | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV (`OV_CHEM_TRANS_TANK`, Chemical Objects). Already partially on the label-driven pattern (`Fill OV Field By Label`) from an earlier build (2026-07-26) - this round added the missing properties-file-driven Insert/Update (`testdata/chemical_transport_tank_*.properties`) and explicit `Find/Clear Chemical Transport Tank Row By Filter` grid-filter wiring (wired into Update/Find/Verify-Found/Delete, matching Bank/Berth). Field labels are screen-prefixed ("Transport Tank Code"/"Transport Tank Name") - confirmed via the already-proven Playwright driver `py/chemical_transport_tank_iud.py`, not re-scanned live. Only Transport Tank Code/Transport Tank Name/Start Date mandatory. Fixed test code `AUTOTEST_CTT` (confirmed free via a fresh oracledb connection before the build). Live 5/5, dryrun 758/758, DB self-clean 0 residual (fresh oracledb connection), filter keyword confirmed fired 7x (`Find Chemical Transport Tank Row By Filter` via output.xml grep). No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed - reused every consolidated T2 keyword as-is. |
| Deferment Group | ✅ DONE (built 2026-08-23 Batch 8, BLOCKED then, merged 2026-08-23 after owner fixed a role-access gate) | Manage-object OV (`OV_DEFERMENT_GROUP`, Facility Objects, CO.0149). Explicit `Find/Clear Deferment Group Row By Filter` grid-filter wiring built same as the rest of Batch 8 (wired into Update/Find/Verify-Found/Delete), but the screen itself was UNREACHABLE at build time - `TV_T_BASIS_ACCESS` had `LEVEL_ID=0` ("No access") for all 5 roles, so the menu-search link couldn't even be found, let alone tested live. Left uncommitted in an isolated clone (`Workplaces/deferment_group`) pending an access fix rather than merged untested. Owner granted sysadmin-role access 2026-08-23; re-verified live access first (login + menu search now opens the screen), then ran the full gate: live 5/5, filter keyword confirmed fired 15x (`Find Deferment Group Row By Filter` via output.xml grep), dryrun 774/774, DB self-clean 0 residual `AUTOTEST_DEFERMENT_GROUP` rows via a fresh independent oracledb connection. No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed. |

## Batch 9 additions (2026-08-23) — consolidated

_Header pre-created via PR #464 per the Batch-8 lesson; two parallel PRs raced it
and self-added their own headers (honestly flagged in their bodies) - consolidated
by the reviewer at merge, rows unioned by key, content unchanged._

| Screen | Status | Notes |
|---|---|---|
| Port | ✅ DONE (2026-08-23, Batch 9) | Manage-object OV, **paginated grid (2 pages)** (Transport Objects, CO.2003). Screen-prefixed labels ("Port Code"/"Port Name") confirmed via the pre-existing page object + proven `py/port_iud.py`. Only Port Code/Port Name/Start Date mandatory - Country/Canal/Time Zone/Carrier dropdowns all optional and skipped. Wired in via this batch (prior page object already had label-driven fields but no properties-file-driven insert/update or explicit filter). Live 5/5, filter keyword confirmed fired 15x via output.xml grep for `Find Port Row By Filter`. Dryrun 762/762. Confirmed the shared T2 filter/row-locate keywords still walk both pager pages correctly - no engine change needed. No shared T1/T2 edits. DB self-clean confirmed 0 residual `AUTOTEST_PORT` rows via a fresh oracledb connection. |
| Reservoir Block | ✅ DONE (2026-08-23, Batch 9) | Manage-object OV (`OV_RESV_BLOCK`, Well_and_Reservoir_Objects, CO.0133). Already partially on the label-driven pattern (`Fill OV Field By Label`) from an earlier build (2026-07-26) - this round added the missing properties-file-driven Insert/Update (`testdata/reservoir_block_*.properties`) and explicit `Find/Clear Reservoir Block Row By Filter` grid-filter wiring (wired into Update/Find/Verify-Found/Delete, matching Bank/Berth). Field labels are screen-prefixed ("Reservoir Block Code"/"Reservoir Block Name") - confirmed via the already-proven Playwright driver `py/reservoir_block_iud.py`, not re-scanned live. Only Reservoir Block Code/Reservoir Block Name/Start Date mandatory. Fixed test code `AUTOTEST_RESVB` (confirmed free via a fresh oracledb connection before the build). Live 5/5, dryrun 762/762, DB self-clean 0 residual (fresh oracledb connection), filter keyword confirmed fired 13x (`Find Reservoir Block Row By Filter` via output.xml grep). No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed - reused every consolidated T2 keyword as-is. NOTE: at clone time PR #464 (pre-created this section header) was still OPEN, not merged into master - this PR re-adds the identical header text verbatim so it converges cleanly with #464 whichever merges first; flag this to the reviewer. |
| Reservoir Formation | ✅ DONE (2026-08-23, Batch 9) | Manage-object OV (`OV_RESV_FORMATION`, Well_and_Reservoir_Objects, CO.0135). Already partially on the label-driven pattern (`Fill OV Field By Label`) from an earlier build (2026-07-26) - this round added the missing properties-file-driven Insert/Update (`testdata/reservoir_formation_*.properties`) and explicit `Find/Clear Reservoir Formation Row By Filter` grid-filter wiring (wired into Update/Find/Verify-Found/Delete, matching Bank/Berth). Field labels are screen-prefixed ("Reservoir Formation Code"/"Reservoir Formation Name") - confirmed via ec-ui-knowledge/screens/reservoir_formation.md + the already-proven Playwright driver `py/reservoir_formation_iud.py`. Only Reservoir Formation Code/Reservoir Formation Name/Start Date mandatory. Fixed test code `AUTOTEST_RESVF` (confirmed free via a fresh oracledb connection before AND after the live run). Live 5/5, dryrun 762/762, DB self-clean 0 residual (fresh oracledb connection), filter keyword confirmed fired 7x (`Find Reservoir Formation Row By Filter` via output.xml grep). No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed - reused every consolidated T2 keyword as-is. |
| Report Area | ✅ DONE (2026-08-23, Batch 9) | Manage-object OV (Reporting > Report Area, RP.0017, top-level Reporting menu). Had a PARTIAL prior label-driven build (`Fill OV Field By Label`) missing properties-file-driven insert/update and explicit grid-filter wiring - upgraded to the full Bank/Berth pattern. Screen-prefixed labels confirmed via the pre-existing page object + proven `py/report_area_iud.py` ("Report Area Code"/"Report Area Name"). Date label is **"Start date"** (lowercase "date") - confirmed live via a 30s locator-timeout reproduction with "Start Date" (capital D), then fixed. Only Report Area Code/Report Area Name/Start date mandatory - simplest OV, no Description/dropdowns. Fixed test code `AUTOTEST_RPTA` (confirmed free via fresh oracledb connection, before and after the live run). Live 5/5, filter keyword confirmed fired 28x (`Find Object Row By Filter`) via output.xml grep. Dryrun 762/762. No shared T1/T2 (`manage_object.resource`/`common.resource`) edits - reused every consolidated T2 keyword as-is. DB self-clean confirmed 0 residual `AUTOTEST_RPTA`/`AUTOTEST%` rows via a fresh oracledb connection. |
| Process Train | ✅ DONE (2026-08-23, Batch 9) | Manage-object OV (Configuration > Assets > Facility_Objects, CO.0120). Had a PARTIAL prior label-driven build (`Fill OV Field By Label`) missing properties-file-driven insert/update and explicit grid-filter wiring - upgraded to the full Bank/Berth pattern with `Find/Clear Process Train Row By Filter` wired into Update/Find/Verify-Found/Delete. **CORRECTION found live**: the KB doc's "no mandatory dropdowns" claim was wrong for persistence - Insert with only Process Train Code/Process Train Name/Start Date clicked Save successfully but the row never reached `OV_PROCESS_TRAIN` and left EC's own unsaved-changes confirmation modal open, stalling the suite; re-running the already-proven `py/process_train_iud.py` unmodified (which fills **Production Facility Class 1** = `__FIRST__`) passed 7/7 cleanly, so that dropdown is now in `testdata/process_train_insert.properties` too (excluded from the round-trip form-label compare list since `__FIRST__` never matches the resolved literal text on reload). Fixed test code `AUTOTEST_PT` (confirmed free via fresh oracledb connection, before and after the live run). Live 5/5, dryrun 762/762, DB self-clean 0 residual (fresh oracledb connection), filter keyword confirmed fired via output.xml grep. No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed - reused every consolidated T2 keyword as-is. |

## Screens NOT yet eligible (still on the older pre-Bank-pattern shape)

The ~80 other OV/OV-GM screens listed in `docs/ec_screen_registry.md` have not been
rebuilt to the label-driven, T2-consolidated pattern yet (they predate this
session's Bank-pattern conversion work). They don't have `Find/Clear Object Row By
Filter`-compatible T3 wrapper keywords to wire this into — that would require
rebuilding them to the Bank pattern FIRST (a separate, larger task), not just
retrofitting the filter. **Do not attempt to add filter wiring to a screen still on
the old pattern without rebuilding it first** — check this doc's "eligible" table
above before starting, and check `docs/ec_screen_registry.md` for the screen's
current pattern if it's not listed here at all.

## Batch 10 additions (pending) — Split Item Other, Storage Flow, Stream Item Category, Data Extract Set, Trailer

_Section header pre-created on master before fan-out. Each screen's PR appends
only its own ROW here — no per-PR section header._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Split Item Other (Configuration > Assets > Revenue_Split_Keys, CD.0017) | ✅ DONE (2026-08-23) | `Find/Clear Split Item Other Row By Filter` wired into Update/Find/Verify-Found/Delete, matching `bank_page.resource`/`berth_page.resource` exactly. Filter keyword confirmed fired 30x via output.xml grep (live 5/5 run). |
| Storage Flow (Configuration > Assets > Tank_and_Storage_Objects, CO.2091) | ✅ Wired (2026-08-23, Batch 10) | `Find/Clear Storage Flow Row By Filter` added to `storage_flow_page.resource`, wired into Update/Find/Verify-Found/Delete (T2 `Find Object Row By Filter`/`Clear Object Row Filter`, resources/manage_object.resource - unchanged). Confirmed fired 15x via output.xml grep on the live 5/5 run. |
| Stream Item Category | ✅ DONE (2026-08-23) | `Find Stream Item Category Row By Filter`/`Clear Stream Item Category Row Filter` added, wired into Update/Find/Verify-Found/Delete (NOT Verify-Removed/Does-Not-Exist), matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired live via output.xml grep (filter 24x, clear 20x). |
| Data Extract Set | ✅ DONE (2026-08-23) | `Find/Clear Data Extract Set Row By Filter` (delegating to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `data_extract_set_page.resource`, matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired 13x via output.xml grep on the live 5/5 run. |
| Trailer | ✅ Wired (2026-08-23, Batch 10) | `Find/Clear Trailer Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete, matching Bank/Berth. Filter keyword confirmed fired 23x via output.xml grep on the live 5/5 run. |

## Batch 11 additions (pending) — Bank Account, Carrier

_Section header pre-created on master before fan-out. Each screen's PR appends
only its own ROW here — no per-PR section header. Note: both screens are on the
OLD hardcoded (`Fill New Object Form`) pattern, a bigger lift than Batch 7-10's
label-driven upgrades; Carrier's nav-free status also needs live recon before
committing to a full conversion (see `tmp/batch11_shared_findings.md`)._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Carrier (Configuration > Assets > Cargo_Objects) | ✅ DONE (2026-08-23) | `Find/Clear Carrier Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `carrier_page.resource`, matching `bank_page.resource`/`berth_page.resource`/`port_page.resource` exactly. Confirmed fired 14x via output.xml grep on the live 5/5 run. |
| Bank Account (Configuration > Assets > Financial_Objects) | ✅ DONE (2026-08-23, Batch 11) | `Find/Clear Bank Account Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `bank_account_page.resource`, matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired 15x / cleared 15x via output.xml grep on the live 5/5 run. |

## Phase 3 additions (pending) — Chemical Product, Product, Document Template

_Section header pre-created on master before fan-out. Phase 3 = first batch out
of the Phase 2 recon (19 reconciled unknown screens); these 3 are the only ones
confirmed genuinely Bank-shaped with no navigator-column entry. Each screen's
PR appends only its own ROW here — no per-PR section header._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Document Template (Configuration > Assets > Revenue_Document_Objects, CD.0013) | ✅ DONE (2026-08-24) | `Find/Clear Document Template Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `document_template_page.resource`, matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired 15x via output.xml grep on the live 5/5 run. |
| Product (Configuration > Assets > Hydrocarbon_Objects, CO.0007) | ✅ DONE (2026-08-24) | `Find/Clear Product Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `product_page.resource`, matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired 15x via output.xml grep on the live 5/5 run (brand-new build, zero prior automation). |
| Chemical Product (Configuration > Assets > Chemical Objects, CO.0072) | ✅ DONE (2026-08-24) | `Find/Clear Chemical Product Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `chemical_product_page.resource`, matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired 26x via output.xml grep on the live 5/5 run. |

## Disposition Type addition (2026-08-24)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Disposition Type (Configuration > Assets > Hydrocarbon_Objects, CO.0208) | ✅ DONE (2026-08-24) | `Find/Clear Disposition Type Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `disposition_type_page.resource`, matching `bank_page.resource`/`berth_page.resource` exactly. Confirmed fired 15x via output.xml grep on the live 5/5 run. Upgraded from an OLD hardcoded-field-id build with no filter wiring at all - see `docs/bank-pattern-conversion-checklist.md` for the full conversion detail. |

## EC Code Object conversion (2026-08-24)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| EC Code Object | ✅ DONE (2026-08-24) | `Find/Clear EC Code Object Row By Filter` (delegating to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `ec_code_object_page.resource` (PR #494), matching Bank/Berth. Confirmed fired 15x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge._ |

## Report Group addition (2026-08-24)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Report Group (Configuration > Assets > Facility_Objects, CO.0158) | ✅ DONE (2026-08-24) | `Find/Clear Report Group Row By Filter` (delegates to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `report_group_page.resource`, matching `bank_page.resource`/`disposition_type_page.resource` exactly. Confirmed fired 15x via output.xml grep on the live 5/5 run. Upgraded from a PARTIAL label-driven build with no filter wiring - see `docs/bank-pattern-conversion-checklist.md` for the full conversion detail. |

## Choke Model + Choke conversions (2026-08-24)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Choke Model | DONE (2026-08-24) | `Find/Clear Choke Model Row By Filter` (delegating to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `choke_model_page.resource` (PR #497), matching Bank/Berth. Confirmed fired 15x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge - PR omitted this checklist (R38)._ |
| Choke | DONE (2026-08-24) | `Find/Clear Choke Row By Filter` (delegating to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `choke_page.resource` (PR #498), matching Bank/Berth. Confirmed fired 15x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge - PR omitted this checklist (R38)._ |

## Document Sequence conversion (2026-08-25)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Document Sequence | DONE (2026-08-25) | `Find/Clear Document Sequence Row By Filter` (delegating to shared T2 `Find/Clear Object Row By Filter`) wired into Update/Find/Verify-Found/Delete in `document_sequence_page.resource` (PR #506). Confirmed fired 15x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |

## Revenue Lists + Data Extract Setup conversions (2026-08-25)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Input List | DONE (2026-08-25) | `Find/Clear Input List Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete in `input_list_page.resource` (PR #515). Confirmed fired 15x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| UOP Key | DONE (2026-08-25) | `Find/Clear UOP Key Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete in `uop_key_page.resource` (PR #516). Confirmed fired 15x/14x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| HCB System | DONE (2026-08-25) | `Find/Clear HCB System Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete in `hcb_system_page.resource` (PR #517). Confirmed fired 30x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Data Extract Setup | DONE (2026-08-25) | `Find/Clear Data Extract Setup Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete in `data_extract_setup_page.resource` (PR #518). Confirmed fired 13x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |

## Area - owner-directed OV-GM exception (2026-08-25)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Area | DONE (2026-08-25, owner-directed OV-GM exception) | `Find/Clear Area Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete in `area_page.resource` (PR #521), after the mandatory Production Unit navigator + GO populates the grid. Confirmed fired 29x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ **2026-08-26 (PR #523):** navigator fill now delegates to the shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`, additive-only shared-file change with R12 canaries: well 4/4 + test_separator 4/4 live, dryrun 846/846), driven by `testdata/area_navigator.properties` - same id/value as the previous inline fill. |

## OV-GM Area-parity conversions (2026-08-26)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| External Location | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear External Location Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete (#528), after the navigator populates the grid. Confirmed fired 15x/12x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Field | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Field Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete (#529), after the navigator populates the grid. Confirmed fired 29x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Facility Class 1 | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Facility Class 1 Row By Filter` (delegating to shared T2) wired into Update/Find/Verify-Found/Delete (#530), after the navigator populates the grid. Confirmed fired 26x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |

## OV-GM Area-parity batch (2026-08-26)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Operator Route | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Operator Route Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#533); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Price Rate | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Price Rate Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#534); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Contract Capacity | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Contract Capacity Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#535); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Price Object | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Price Object Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#536); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Storage | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Storage Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#537); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Sub Area | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Sub Area Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#538); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Well Hookup | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Well Hookup Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#539); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Well | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Well Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#540); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Collection Point | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Collection Point Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#541); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Contract Area | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Contract Area Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#542); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Well Hole | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Well Hole Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#543); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Chemical Stream Hookup | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Chemical Stream Hookup Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#544); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Chemical Stream | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Chemical Stream Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#545); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Contract | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Contract Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#546); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Shift | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Shift Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#547); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Chemical Tank | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Chemical Tank Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#549); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Chem Injection Point (Chemical Injection Point) | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Chemical Injection Point Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#550); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Production Separator | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Production Separator Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#551); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |
| Service | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Service Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (#552); confirmed fired via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |

## Meter Area-parity conversion (2026-08-26)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Meter | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Meter Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (PR #554); confirmed fired 15x via output.xml grep on the live 5/5 run. _Row added by the reviewer at merge (R38)._ |

## Tract Area-parity conversion (2026-08-26 - corrects PR #555's original "does not fit" conclusion)

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Tract | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Tract Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (PR #555); confirmed fired 15x via output.xml grep on the live 5/5 run. |
## Property Area-parity conversion (2026-08-26)

## Pipeline Segment Area-parity conversion (2026-08-26)

| Pipeline Segment | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Pipeline Segment Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete; confirmed fired 15x via output.xml grep on the live 5/5 run. |

## Contract Inventory Area-parity conversion (2026-08-26)

| Contract Inventory | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Contract Inventory Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete; confirmed fired 26x via output.xml grep on the live 5/5 run. |
| Property | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Property Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete; confirmed fired 15x via output.xml grep on the live 5/5 run. |
## Transport Zone Area-parity conversion (2026-08-26)

| Transport Zone | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Transport Zone Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete; confirmed fired 15x via output.xml grep on the live 5/5 run. |


## Pilot Area-parity conversion (2026-08-26)

| Pilot | DONE (2026-08-26, OV-GM Area-parity) | `Find/Clear Pilot Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (feature/pilot-area-pattern, PR #560); confirmed fired 15x via output.xml grep on the live 5/5 run. |

## Well Bore Area-parity conversion (2026-08-27)

| Well Bore | DONE (2026-08-27, OV-GM Area-parity) | `Find/Clear Well Bore Row By Filter` (shared T2 delegation) wired into Update/Find/Verify-Found/Delete (feature/well-bore-area-pattern); confirmed fired 14x via output.xml grep on the live 5/5 run. First Area-parity conversion whose navigator does NOT fit the shared `Apply Navigator From Properties` shape (PER-FIELD groups G:1-G:5, not a same-row cascade) - a bespoke screen-local navigator keyword was added instead; this filter wrapper itself is still the standard shared-T2 delegation pattern, unaffected by that navigator difference. |

## How to update this doc

When a new screen's T3 gets rebuilt to the Bank pattern, add it to the eligible
table above as "⬜ NOT YET DONE". When a screen gets the explicit filter wrapper
added (following the exact pattern in `bank_page.resource`/`account_page.resource`
— `Find <Screen> Row By Filter`/`Clear <Screen> Row Filter` wired into
Update/Find/Verify-Found/Delete, NOT into Removed/Does-Not-Exist), flip it to
"✅ DONE (date)" with a one-line note. Append-only in spirit — don't delete rows for
screens that get superseded/retired, just note it.

