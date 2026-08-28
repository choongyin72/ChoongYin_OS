# SOW - Chemical Transport Tank IUD

_Updated 2026-08-28 (lean-deliverable backfill, Batch 9) - reflects the Batch 8 full
Bank-pattern conversion (PR #461, merged 2026-08-23), which superseded the original
2026-07-26 partial label-driven build referenced by the prior version of this file._

## Classification
- **Screen:** Configuration > Assets > Chemical_Objects > Chemical Transport Tank (BF_CODE **CO.0257**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`), plain Bank-pattern - date-effective,
  **no navigator/mandatory dropdowns** (plain single Date+GO nav). Full Bank-pattern conversion via
  `ec-bank-pattern-converter` (Batch 8, 2026-08-23) - properties-file-driven insert/update/verify,
  explicit grid-filter wiring, matches `bank_page.resource`/`berth_page.resource` shape exactly.
- **DB view:** `OV_CHEM_TRANS_TANK` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_CHEM_TRANS_TANK`

## Nav / grid / cells
- **Open:** menu search "Chemical Transport Tank" -> `label.tv-link`. Navigator = single **Date + GO**;
  grid needs GO to populate (no default rows on open).
- **Grid:** shared T2 constant `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`).
- **Grid filter:** explicit Code-column filter via shared T2 `Find Object Row By Filter`/
  `Clear Object Row Filter`, wrapped as `Find Chemical Transport Tank Row By Filter`/
  `Clear Chemical Transport Tank Row Filter` - matches Bank/Berth/State's own filter usage
  (owner, 2026-08-22).
- **NO hardcoded field ids** - resolved BY LABEL via T2, properties-file-driven:
  - **Insert (objectForm):** `Transport Tank Code`, `Transport Tank Name`, `Start Date` (mandatory,
    via `testdata/chemical_transport_tank_insert.properties`). Optional dropdowns deliberately
    skipped (IUD fills only needed fields).
  - **Update (updateAttributes):** `Transport Tank Name` only (via
    `testdata/chemical_transport_tank_update.properties`) - Code is read-only, Start Date lives
    only in objectdates (same pattern as Bank/Berth/State).
  - **Delete (objectdates):** `End Date` field id
    `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (framework-invariant, same id confirmed
    live on Bank/State/Berth) = Start Date.

## Test data
- **Fixed test code** `AUTOTEST_CTT` (confirmed absent from `OV_CHEM_TRANS_TANK` before Batch 8 wired
  it in) - matches Bank/Berth's convention rather than a generated-unique code. Every run must
  complete TC05 (delete) so the code is free for the next run.
- Name: `AUTOTEST Chemical Transport Tank` (insert) / `AUTOTEST Chemical Transport Tank UPDATED`
  (update). Start/End = `2000-01-01`. Never touches real rows.

## Dev story (from PR #461's real body)
Brought Chemical Transport Tank up to the same full Bank-pattern shape as
`bank_page.resource`/`berth_page.resource` on top of the screen's existing partial label-driven
build (2026-07-26): properties-file-driven insert/update/verify + explicit grid-filter wiring.
Field labels/mandatory set were trusted from the already-proven, live-tested Playwright driver
`py/chemical_transport_tank_iud.py` rather than re-scanned live (rule: check the real driver first
before writing new test config). Fixed test code, per-TC Login/Logout, and dedicated per-screen
credentials (`CHEMICAL_TRANSPORT_TANK_EC_USER`/`CHEMICAL_TRANSPORT_TANK_EC_PASS`) follow the
standing Bank/Berth conventions. Registry/scorecard rows were explicitly replaced in place (not
duplicated) to avoid the Batch 7 merge-conflict defect seen on PR #458/#459. No shared T1/T2
(`resources/manage_object.resource`/`resources/common.resource`) files were changed - every
consolidated T2 keyword was reused as-is.

## Verified (PR #461, merged 2026-08-23T12:07:19Z)
- Live RF suite (`EC_HEADLESS=true`): **5/5 pass** (TC01 clean-state, TC02 insert, TC03 update,
  TC04 find, TC05 delete).
- `robot --dryrun` on the full `tests/` tree: **758/758 pass**.
- DB self-clean: fresh `oracledb` connection queried
  `SELECT COUNT(*) FROM OV_CHEM_TRANS_TANK WHERE UPPER(CODE) LIKE 'AUTOTEST%'` -> **0** residual rows.
- Grid filter fired: `output.xml` grep for `Find Chemical Transport Tank Row By Filter` -> **7 hits**.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete uses engine `wait_for_row_absent` (async redraw).
- The original 2026-07-26 build's bundle (SOW/README/JOURNAL/CHECKLIST/KB map) was left stale after
  the Batch 8 conversion landed - this backfill (2026-08-28) is what brings it back in sync with the
  real, currently-merged automation.
