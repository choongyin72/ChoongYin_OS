# Bank-pattern conversion — screen tracking checklist

_Created 2026-08-23. Tracks which EC screens (with an EXISTING IUD suite already built,
just on the older hardcoded-field-id pattern) have been converted to the label-driven,
properties-file-driven, T2-consolidated "Bank pattern" — so future sessions know exactly
which screens are done, which are queued, and which are out of scope, without redoing the
survey each time._

## Background

Bank/State/Object List/Account/Cost Centre/etc. were rebuilt (2026-08-22/23) from an older
per-screen hand-coded pattern (hardcoded `objectForm`/`updateAttributes` field ids, bespoke
per-screen keywords, no properties files) to a shared, label-driven, T2-consolidated pattern
(`resources/manage_object.resource` keywords: `Insert/Update/Find/Verify Object *`,
`Delete Object Via End Date`), including the explicit grid column-filter row-locate wiring
(see `docs/grid-filter-standardization-checklist.md`). A full-repo survey (2026-08-23)
found **129 OV/OV-GM screens still on the old pattern with an existing IUD suite** already
built, split into:

- **48 "Tier 0" screens** — genuinely old pattern (hardcoded field ids in
  `objectForm`/`updateAttributes`) — **these are the real candidates for conversion**,
  tracked below.
- **80 "Tier 1" screens** — already label-driven via a SEPARATE Playwright/generator
  pipeline (`verify_screen.py`-gated, built in an earlier session) — structurally modern
  already, just not the RF Bank-pattern shape. Lower priority / arguably optional; NOT
  tracked in this checklist (a different, already-adequate pattern).
- **56 OV-GM screens** (gated navigator) — bigger lift than a straight Bank-pattern
  conversion, needs a nav-cascade design decision first. NOT tracked here.

Of the 48 Tier-0 screens, a further live-verified filter (checking each screen's actual
documented navigator requirement in `docs/ec_screen_registry.md`, not just its OV/OV-GM
label) found:
- **23 screens are genuinely nav-free** (plain manage-object with no mandatory
  dropdown/date before GO, OR custom-URL with no navigator at all) — same shape as
  Bank/Account. **These are what this checklist tracks and batches.**
- **20 screens have a real navigator requirement** (mandatory single date+GO, or a
  mandatory dropdown/cascade) — SKIP per owner instruction ("if the ec screen is not same
  as bank... SKIP it for next target screen"). Listed in "Excluded" below for the record.
- **5 screens were unclear/not in the registry** at survey time — need live recon before
  they can be classified either way.

## Batch tracking (23 nav-free Tier-0 candidates)

| Screen | Folder | Status | PR |
|---|---|---|---|
| Country | Basic Objects | ✅ DONE (2026-08-23, Batch 2) | #428 |
| County | Basic Objects | ✅ DONE (2026-08-23, Batch 2) | #429 |
| Regulatory Permits | Basic Objects | ✅ DONE (2026-08-23, Batch 2) | #432 |
| Currency | Financial Objects | ✅ DONE (2026-08-23, Batch 2) | #430 |
| VAT Code | Financial Objects | ✅ DONE (2026-08-23, Batch 2) | #431 |
| Customer | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #435 |
| Field Group | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #434 |
| Licence | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #438 |
| MMS Lease | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #437 |
| Operator Lease | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #436 |
| State Lease | Commercial Objects | ✅ DONE (2026-08-23, Batch 4) | #440 |
| Vendor | Commercial Objects | ✅ DONE (2026-08-23, Batch 4) | #439 |
| Cost Object Mapping | Financial Objects | ✅ DONE (2026-08-23, Batch 4) | #442 |
| DOA Credit Limit | Financial Objects | ✅ DONE (2026-08-23, Batch 4) | #443 |
| Product Description | Financial Objects | ✅ DONE (2026-08-23, Batch 4) | #441 |
| Sales Order | Financial Objects | ✅ DONE (2026-08-23, Batch 5) | #444 |
| Product Group | Royalty Objects | ✅ DONE (2026-08-23, Batch 5) | #445 |
| Royalty Depositor | Royalty Objects | ✅ DONE (2026-08-23, Batch 5) | #448 |
| Royalty Owner | Royalty Objects | ✅ DONE (2026-08-23, Batch 5) | #447 |
| Unit Agreement | Royalty Objects | ✅ DONE (2026-08-23, Batch 5) | #446 |
| Calendar Collection | Date Objects | ✅ DONE (2026-08-23, Batch 6) | #449 |
| Calendar | Date Objects | ✅ DONE (2026-08-23, Batch 6) | #451 |
| Account Mapping | Financial Objects | ✅ DONE (2026-08-23, Batch 6, FINAL) | #450 |

**23 of 23 done. ALL SCREENS IN THE ORIGINAL CANDIDATE POOL CONVERTED.** Batch 2
(Country #428, County #429, Regulatory Permits #432, Currency #430, VAT Code
#431), Batch 3 (Customer #435, Field Group #434, Licence #438, MMS Lease #437,
Operator Lease #436), Batch 4 (State Lease #440, Vendor #439, Cost Object
Mapping #442, DOA Credit Limit #443, Product Description #441), Batch 5 (Sales
Order #444, Product Group #445, Royalty Depositor #448, Royalty Owner #447,
Unit Agreement #446), and Batch 6 (Calendar Collection #449, Calendar #451,
Account Mapping #450) — all 23 nav-free Tier-0 screens are now on the
label-driven, properties-file-driven, T2-consolidated Bank pattern, with
explicit grid-filter wiring included. This checklist's "Batch tracking" table
is now complete; any future Bank-pattern conversion work (Tier 1/OV-GM
screens, or newly-registered screens) should get its own new tracking table
rather than reusing this one.

Note: once a screen from this table is converted, it should ALSO be added to
`docs/grid-filter-standardization-checklist.md`'s "done" table in the same PR (per the
owner's standing instruction to include the filter wiring from day one, not as a
follow-up pass).

## Excluded — has a real navigator requirement (per owner: SKIP if not same as Bank)

| Screen | Reason |
|---|---|
| Document Date Term, Payment Term, Choke, Choke Model, Disposition Type | Mandatory single date + GO before grid loads |
| Field, Contract Area, Delivery Point, Delivery Stream, Nomination Point, Pipeline Segment, Transport Zone | Mandatory Business Unit/Area dropdown + GO |
| Sub Area | Cascading PU→Area + GO |
| Equipment | 5-field cascading navigator |
| Analysis Point | 3-level cascade (PU→Area→Facility Class) + GO |
| Tract | Gated: mandatory date + mandatory Unit Agreement dropdown + GO |

## Unclear at survey time — needs live recon before batching either way

Sub Field, Pipeline, Meter, Transport System, Commercial Entity, Company Contact,
Carrier — not found in `docs/ec_screen_registry.md`'s navigator column at survey time,
or registry text was ambiguous (e.g. "optional" dropdown/date). Do NOT assume nav-free;
recon live before adding to a batch.

## Out of scope (Tier 1 — different, already-adequate pattern)

The 80 Tier-1 screens (generator-scaffolded, `verify_screen.py`-gated, Playwright-driven,
already label-driven via a different mechanism) are NOT tracked in this checklist. They
are not "old pattern" in the sense this doc cares about — converting them to the RF
Bank-pattern would be a consistency change, not a functional uplift, and is lower
priority. If ever prioritized, treat as a separate initiative, not an extension of this
checklist.

## Batch 7 additions (2026-08-23) — consolidated

_Section consolidated by the reviewer at the Batch 8 merge: the parallel per-screen
PRs each appended their own "Batch 7" section header; rows below are the union, each
screen exactly once, content unchanged._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Berth | ✅ DONE (2026-08-23, Batch 7) | Manage-object OV (Bank family), single-page grid (11 rows). Screen-prefixed labels "Berth Code"/"Berth Name" confirmed via ec-ui-knowledge/screens/berth.md + proven py/berth_iud.py (only Code/Name/Start Date mandatory, dropdowns optional). Rebuilt berth_page.resource/berth_iud.robot to mirror bank_page.resource/state_page.resource exactly: properties-file-driven insert ("Insert Object From Properties And Verify Code"), update, form/grid verify, explicit `Find/Clear Berth Row By Filter` wired into Update/Find/Verify-Found/Delete. Fixed test code `AUTOTEST_BERTH` (confirmed free live). Live 5/5, dryrun 753/753, filter fired 15x (output.xml grep), DB self-clean confirmed via fresh oracledb connection. No shared T1/T2 file changes. |
| Calculation Group Context (Configuration > Assets > Calculation_Objects, CO.0245) | ✅ DONE (2026-08-23) — brought to full Bank-pattern shape: `Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/Removed/Does Not Exist`, explicit `Find/Clear Calculation Group Context Row By Filter`, dedicated `CALCULATION_GROUP_CONTEXT_EC_USER/PASS`, fixed test code `AUTOTEST_CGC_BANK`. Live 5/5 RF, robocop parity with `bank_iud.robot`'s baseline, dryrun 753/753, DB self-clean (fresh connection) 0 residual, filter fired 23x per output.xml. See `docs/ec_screen_registry.md` and `docs/grid-filter-standardization-checklist.md` for full detail. |

## Batch 8 additions (2026-08-23) — consolidated

_Section consolidated by the reviewer at the Batch 8 merge: the parallel per-screen
PRs each appended their own "Batch 8" section header; rows below are the union, each
screen exactly once, content unchanged._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Inventory Area | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV (Inventory Objects, CD.0115), single-page grid. Screen-prefixed labels "Inventory Area Code"/"Inventory Area Name" confirmed via the pre-existing page object + proven py/inventory_area_iud.py (only Code/Name/Start Date mandatory, no other fields), re-confirmed via a fresh live Playwright run 2026-08-23. Rebuilt inventory_area_page.resource/inventory_area_iud.robot to mirror bank_page.resource/berth_page.resource exactly: properties-file-driven insert ("Insert Object From Properties And Verify Code"), update, form/grid verify, explicit `Find/Clear Inventory Area Row By Filter` wired into Update/Find/Verify-Found/Delete. Fixed test code `AUTOTEST_INVA` (confirmed free live via fresh oracledb connection, before and after the live RF run). Live 5/5, dryrun 758/758, filter fired 11x (output.xml grep), DB self-clean confirmed via fresh oracledb connection. No shared T1/T2 file changes. |
| Meter Run (Configuration > Assets > Stream_Objects, CO.0091) | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV (Bank family), single-page grid (20 rows). Screen-prefixed labels "Meter Run Code"/"Meter Run Name" confirmed via the proven py/meter_run_iud.py + the prior live-tested page object (only that driver, not a fresh guess). Rebuilt meter_run_page.resource/meter_run_iud.robot to mirror bank_page.resource/berth_page.resource exactly: properties-file-driven insert (`Insert Object From Properties And Verify Code`), update, form/grid verify, explicit `Find/Clear Meter Run Row By Filter` wired into Update/Find/Verify-Found/Delete. Fixed test code `AUTOTEST_METER_RUN` (confirmed free live via a fresh oracledb query). Mandatory set is WIDER than Bank/Berth - besides Code/Name/Start Date, Type of Taps/Pipe Material/Location of Taps dropdowns and Pipe Diameter/Diameter Meas Temp/All Calibration Factor are also mandatory (per the existing driver, unchanged from before this batch). Live 5/5, dryrun 758/758, filter fired 15x (output.xml grep), DB self-clean confirmed 0 residual via a fresh oracledb connection. No shared T1/T2 file changes. |
| Orifice Plate (Configuration > Assets > Stream_Objects, CO.0089) | ✅ DONE (2026-08-23, Batch 8) — brought to full Bank-pattern shape: rebuilt `orifice_plate_page.resource`/`orifice_plate_iud.robot` to mirror `bank_page.resource`/`berth_page.resource` exactly — properties-file-driven insert (`Insert Object From Properties And Verify Code`), update, form/grid verify, explicit `Find/Clear Orifice Plate Row By Filter` wired into Update/Find/Verify-Found/Delete, dedicated `ORIFICE_PLATE_EC_USER/PASS`, fixed test code `AUTOTEST_ORIFICE_PLATE` (confirmed free live), added TC04 Find (prior suite only had TC01-04 Verify/Insert/Update/Delete, no Find). Mandatory fields beyond Code/Name/Start Date: Material (dropdown), Diameter [mm], Measurement Temp [°R] — all confirmed mandatory via ec-ui-knowledge/screens/orifice_plate.md + proven py/orifice_plate_iud.py, included in the insert properties file. Live 5/5, dryrun 758/758, filter fired 13x (output.xml grep), DB self-clean confirmed via fresh oracledb connection. No shared T1/T2 file changes. This MODIFIES the screen's existing `docs/ec_screen_registry.md` / `docs/automation-scorecard.md` rows (from the 2026-07-26 generator-scaffolded build) — not a new row. |
| Chemical Transport Tank | ✅ DONE (2026-08-23, Batch 8) | Manage-object OV, single-page grid (Chemical Objects). Screen-prefixed labels "Transport Tank Code"/"Transport Tank Name" confirmed via the already-proven Playwright driver py/chemical_transport_tank_iud.py (only Code/Name/Start Date mandatory, dropdowns optional). Rebuilt chemical_transport_tank_page.resource/chemical_transport_tank_iud.robot to mirror bank_page.resource/berth_page.resource exactly: properties-file-driven insert (`Insert Object From Properties And Verify Code`), update, form/grid verify, explicit `Find/Clear Chemical Transport Tank Row By Filter`. Fixed test code `AUTOTEST_CTT` (confirmed free live via fresh oracledb connection). Live 5/5, dryrun 758/758, filter fired 7x (output.xml grep), DB self-clean confirmed via fresh oracledb connection. No shared T1/T2 file changes. |

## Batch 9 additions (2026-08-23) — Port, Process Train, Report Area, Reservoir Block, Reservoir Formation

_Note: PR #464 (pre-creating this section header on master ahead of fan-out) was still OPEN,
not yet merged, when this row was authored - this clone was branched off origin/master
BEFORE that header existed there. This header+row is added here so the row has a home;
if PR #464 merges first, the reviewer/merge step should dedupe to a single header per the
Batch-8 lesson (keep one header, keep every row, verify by-key row set is unchanged)._

| Screen | Explicit filter wired? / Status | Notes |
|---|---|---|
| Reservoir Formation | ✅ DONE (2026-08-23, Batch 9) — brought to full Bank-pattern shape: rebuilt `reservoir_formation_page.resource`/`reservoir_formation_iud.robot` to mirror `bank_page.resource`/`berth_page.resource` exactly — properties-file-driven insert (`Insert Object From Properties And Verify Code`), update, form/grid verify, explicit `Find/Clear Reservoir Formation Row By Filter` wired into Update/Find/Verify-Found/Delete, dedicated `RESERVOIR_FORMATION_EC_USER/PASS`, fixed test code `AUTOTEST_RESVF` (confirmed free live via fresh oracledb connection, before and after). Mandatory fields: Reservoir Formation Code/Reservoir Formation Name/Start Date only (no other mandatory fields, confirmed via ec-ui-knowledge/screens/reservoir_formation.md + proven py/reservoir_formation_iud.py). Live 5/5, dryrun 762/762, filter fired 7x (output.xml grep), DB self-clean confirmed via fresh oracledb connection. No shared T1/T2 file changes. This MODIFIES the screen's existing `docs/ec_screen_registry.md` / `docs/automation-scorecard.md` rows (from the 2026-07-26 generator-scaffolded build) — not a new row. |

## How to update this doc

When a new batch of screens from the "Batch tracking" table gets converted, flip each to
"✅ DONE (date, BatchN)" with its PR number. If a screen turns out to have an
undocumented navigator requirement once recon'd live (contradicts its "nav-free" premise
here), move it to the "Excluded" table instead of force-fitting it — this happened for
zero screens in Batch 2, but is a real possibility for any future batch. Append-only in
spirit for the "Excluded"/"Unclear" tables; the "Batch tracking" table's rows should only
ever flip status, not be deleted.

