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

## Batch 7 (2026-08-23) — new round, additions beyond the closed 37/37 pool

The 37/37 pool above (original 23-screen Bank-pattern conversion program, Batches 2-6)
is CLOSED — not reopened here. This is a separate, later round (owner-directed:
sort by screen LAYOUT similarity to Bank, regardless of prior automation history),
5 screens (Berth/Blend/Calculation Context/Calculation Group Context/Canal),
tracked in `tmp/batch7_shared_findings.md`. Each screen already had SOME existing
automation from an earlier approach (label-driven but missing properties-file-driven
insert + explicit grid-filter wiring) - this batch brings them the rest of the way.

| Screen | Explicit filter wired? | Notes |
|---|---|---|
| Berth | ✅ DONE (2026-08-23, Batch 7) | Manage-object OV, single-page grid (11 rows, Transport Objects). Screen-prefixed labels ("Berth Code"/"Berth Name") confirmed via ec-ui-knowledge/screens/berth.md + proven py/berth_iud.py (Code/Name/Start Date mandatory only, all dropdowns optional). Fixed test code `AUTOTEST_BERTH`. Wired in via this batch (prior page object already had label-driven fields but no properties-file-driven insert/update or explicit filter). Live 5/5, filter keyword confirmed fired 15x via output.xml grep for `Find Berth Row By Filter`. Dryrun 753/753. No shared T1/T2 edits. DB self-clean confirmed via fresh oracledb connection. |

**Batch 7 addition (2026-08-23, NEW round beyond the closed 37/37 pool above):**
Calculation Group Context (Configuration > Assets > Calculation_Objects) got the
same explicit `Find/Clear Calculation Group Context Row By Filter` wrapper
delegating to the shared T2 `Find/Clear Object Row By Filter` — wired into
Update/Find/Verify-Found/Delete, not Verify-Removed/Does-Not-Exist. Small/
single-page grid today. Live 5/5, filter confirmed fired via output.xml grep
(23 hits). See `docs/ec_screen_registry.md`'s Calculation Group Context row for
full detail — the closed 37-screen table above is not reopened for this entry.
## Batch 7 additions (NEW round, beyond the closed 37/37 pool above)

The 37/37 pool above is closed and not reopened. Batch 7 is a separate, later round
(owner-directed: sort by screen LAYOUT similarity to Bank, regardless of prior
automation history) adding MORE screens on top of that closed pool. Tracked here,
append-only, same as the closed table above.

| Screen | Status | Notes |
|---|---|---|
| Calculation Context | ✅ DONE (2026-08-23, batch-7) | Manage-object OV (`OV_CALC_CONTEXT`), already partially on the label-driven pattern (`Fill OV Field By Label`) from an earlier build - this round added the missing properties-file-driven Insert/Update (`testdata/calculation_context_*.properties`) and explicit `Find/Clear Calculation Context Row By Filter` grid-filter wiring (wired into Update/Find/Verify-Found/Delete, matching Bank/Account). Live-recon confirmed Bank-pattern shape: objectForm = Calc Context Code/Name/Start Date (mandatory)/End Date/Description/Comments; updateAttributes = Calc Context Code (read-only)/Name/Description/Comments (no Start/End Date there, matching Bank); no mandatory navigator dropdown beyond the universal GO bar. Fixed test code `AUTOTEST_CALCCTX` (confirmed free live). Live 5/5, robocop clean, dryrun 753/753, DB self-clean 0 residual (fresh oracledb connection), filter keyword confirmed fired (12x `Find Calculation Context Row By Filter` / 8x `Filter Grid Text Column By Value` via output.xml grep). No shared T1/T2 (`manage_object.resource`/`common.resource`) changes needed - reused every consolidated T2 keyword as-is. |
## Batch 7 additions (beyond the closed 37/37 pool, 2026-08-23)

The 37/37 pool above is closed and not reopened. Batch 7 is a NEW round, sorted by
LAYOUT similarity to Bank rather than prior automation history (owner direction).
Screens land here as they're completed, appended, not merged into the closed table.

| Screen | Explicit filter wired? | Notes |
|---|---|---|
| Blend | ✅ DONE (2026-08-23, batch-7) | Manage-object OV (Hydrocarbon Objects), small grid (3 rows). Had a PARTIAL prior label-driven build (`Fill OV Field By Label`, 2026-07-26) missing properties-file-driven insert/update and explicit grid-filter wiring - upgraded to the full Bank pattern. Screen-prefixed labels confirmed live ("Blend Code"/"Blend Name", like State's own precedent) - NOT the generic "Code"/"Name" Bank/Customer use, so `code_label=Blend Code` is threaded through Insert/Update/Find. Only Blend Code/Blend Name/Start Date mandatory (MandatoryCellStyle confirmed via a fresh per-row class dump); Master System Code/Name, Sort Order, End Date left optional/out of scope. Description is optional but exercised (never populated on any real production Blend row - 0 non-null DESCRIPTION rows confirmed live). Wired in from the start. Live 5/5, filter keyword confirmed fired 50 hits total (Find+Clear across TC02-05) via output.xml grep. DB self-clean confirmed 0 residual `AUTOTEST_BLEND` rows via a fresh oracledb connection. |

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

## How to update this doc

When a new screen's T3 gets rebuilt to the Bank pattern, add it to the eligible
table above as "⬜ NOT YET DONE". When a screen gets the explicit filter wrapper
added (following the exact pattern in `bank_page.resource`/`account_page.resource`
— `Find <Screen> Row By Filter`/`Clear <Screen> Row Filter` wired into
Update/Find/Verify-Found/Delete, NOT into Removed/Does-Not-Exist), flip it to
"✅ DONE (date)" with a one-line note. Append-only in spirit — don't delete rows for
screens that get superseded/retired, just note it.
