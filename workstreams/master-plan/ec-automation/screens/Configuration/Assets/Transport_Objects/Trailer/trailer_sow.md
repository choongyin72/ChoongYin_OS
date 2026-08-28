# SOW - Trailer IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Trailer   **BF:** CO.0265   **View:** `OV_TRAILER` (0 rows on the sandbox - our AUTOTEST row is the first)   **Base:** `TRAILER`
- **Type:** PLAIN OV (Bank family) with a **CUSTOM grid id `trailer_object:form:T_data`** and an
  **EMPTY navigator** (no nav fields at all - GO alone populates the grid). Sibling of Truck (CO.0264).
- **Mandatory set (live-scan verified):** Trailer Code / Trailer Name / Start Date +
  **Licence Plate No** (text) + **Trailer Type**, **UOM**, **Transport Company** (dropdowns,
  first-available). Lighter than Truck: no quantity fields are mandatory here.
- Start Date 2000-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_TR_<timestamp>` per run;
  self-cleaning.
- Built by the audited plain-OV generator `tmp/gen_ov.py` - **8/8 driver and 5/5 gates on the FIRST
  run**, no per-screen debugging needed (the 6 defects that generator audit fixed on Truck paid off).

## Known risks
- Mandatory set is screen-specific; if EC config changes, re-derive from EC's save-time
  "Required fields are empty" message.

## Addendum (2026-08-23, PR #475) — Batch 10 Bank-pattern conversion

Trailer's RF page object/suite (`trailer_page.resource`/`trailer_iud.robot`) was rebuilt to the full
Bank-pattern shape — properties-file-driven insert/update/verify + explicit grid-filter wiring —
matching `bank_page.resource`/`berth_page.resource` exactly. Part of Batch 10's 5-screen expanded-scope
conversion round.

- **What changed:** suite moved from label-driven-but-hardcoded-arguments to label-driven +
  properties-file-driven (`testdata/trailer_{insert,update,form_verify,grid_verify}.properties`),
  T2-consolidated, per-TC Login/Logout, with explicit `Find/Clear Trailer Row By Filter` grid-filter
  wiring delegated to the shared T2 `Find/Clear Object Row By Filter` (matches Account/Bank/Berth/
  State's convention per owner 2026-08-22: "others (Bank, State, List_Object) should follow
  Account... utilise same filter feature").
- **Grid id kept, not switched:** `trailer_object:form:T_data` is Trailer's OWN grid id, confirmed via
  the pre-existing proven Playwright driver's `GRID_DATA_ID` — NOT the shared
  `manage_object_nav_nav:form:T_data` constant most manage-object screens use. Kept unchanged rather
  than assumed to match Bank/Berth's shared constant — a real, documented quirk of this screen.
  Ground rule: no shared `manage_object.resource`/`common.resource` changes for this conversion.
- **Mandatory field set carried over unchanged:** Licence Plate No + Trailer Type/UOM/Transport
  Company (first-available) — the proven driver's field set was trusted over a static label/CSS scan
  (Process Train Batch-9 lesson): Licence Plate No was kept rather than dropped, since a field can be
  de-facto mandatory even when not CSS-flagged.
- **Test data:** fixed code `AUTOTEST_TRAILER` (matching Bank/Berth's convention), confirmed absent
  from `OV_TRAILER` before being wired in. Start Date 2000-01-01; DELETE = End Date = Start Date.
- **Live evidence at merge (PR #475):** `EC_HEADLESS=true` run 5/5 pass; fresh `oracledb` connection
  (`SELECT CODE FROM OV_TRAILER WHERE CODE LIKE 'AUTOTEST%'`) returned 0 rows both before and after;
  `robot --dryrun` on the full `tests/` tree 767/767 pass; `py -m robocop check` on both changed files
  9 issues (4 VAR02 + 5 DOC02) — same count/type as the already-merged `berth_iud.robot` baseline,
  advisory only, exit=0; filter keyword confirmed firing 23x via `output.xml` grep. Self-clean
  confirmed (0 residual `AUTOTEST_TRAILER`/`AUTOTEST%` rows).
- This addendum documents the conversion for `docs/lean-deliverable-backfill-workorder.md` (Batch 11,
  2026-08-27/28) — the RF automation itself was NOT touched to produce this SOW update.
