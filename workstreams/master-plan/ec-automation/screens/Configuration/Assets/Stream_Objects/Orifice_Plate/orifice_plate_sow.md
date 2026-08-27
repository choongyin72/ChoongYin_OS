# SOW — Orifice Plate IUD

_Refreshed 2026-08-28 (lean-waiver retirement backfill, Batch 10 —
`docs/lean-deliverable-backfill-workorder.md`). This bundle predated PR #463's Bank-pattern
conversion (2026-08-23) and still described the OLD generator-scaffolded/label-only build; the
content below is refreshed to describe the CURRENT automation. No automation files were changed
by this refresh — RF/py files are untouched._

## Classification
- **Screen:** Configuration > Assets > Stream_Objects > Orifice Plate (BF_CODE **CO.0089**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`), date-effective, **plain — no
  navigator section**. Full **Bank-pattern** shape (converted via PR #463, Batch 8 of the
  Bank-pattern conversion project, merged 2026-08-23).
- **DB view:** `OV_ORIFICE_PLATE` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_ORIFICE_PLATE` (true delete, no soft-delete flag)
- **Grid id:** `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`)

## Mandatory fields
- **Insert (`objectForm`):** `Orifice Code`, `Orifice Name`, `Start Date` — plus, beyond the plain
  Bank shape, three mandatory extras confirmed via live recon + the pre-existing Playwright driver:
  **Material** (dropdown), **Diameter [mm]**, **Measurement Temp [°R]**.
- **Update (`updateAttributes`):** `Orifice Name` (Code is read-only on update).
- **Delete (`objectdates`):** `End Date` = Start Date.
- Field labels are screen-prefixed (`Orifice Code`/`Orifice Name`), NOT the generic `Code`/`Name`
  Bank/Object List use — the T3 resolves them by label, no hardcoded field ids.

## Test data used
- Fixed test code **`AUTOTEST_ORIFICE_PLATE`** (matches Bank/Berth's convention — confirmed absent
  from `OV_ORIFICE_PLATE` before being wired in, 2026-08-23). Every run must complete TC05 (delete)
  so the code stays free for the next run.
- `${START_DATE}` = 2000-01-01; `${END_DATE}` = `${START_DATE}` (delete). Name updated to
  `AUTOTEST Orifice Plate UPDATED` in TC03, verified against `testdata/orifice_plate_update.properties`.
- Dedicated credentials `ORIFICE_PLATE_EC_USER`/`ORIFICE_PLATE_EC_PASS` (added in PR #463, per the
  owner's 2026-08-22 standing decision that every EC screen gets its own credential pair).

## Dev story (from PR #463's real body)
Orifice Plate had a prior generator-scaffolded/label-driven-only build (2026-07-26) that worked but
predated the Bank/Berth grid-filter and properties-file conventions. PR #463 (Batch 8, merged
2026-08-23) rebuilt it to mirror Bank/Berth exactly: properties-file-driven insert/update/verify
(`Insert Object From Properties And Verify Code` / `Update Object From Properties`), an explicit
`Find/Clear Orifice Plate Row By Filter` wired into Update/Find/Verify-Found/Delete (not into
Verify-Removed/Does-Not-Exist, matching the Bank/Berth convention), the dedicated credential pair,
the fixed test code, and a new TC04 Find test case (the prior suite only had TC01
Verify-Clean-State / TC02 Insert / TC03 Update / TC04 Delete — no Find; the rebuild renumbered
Delete to TC05). No shared T1/T2 keyword changes were made in that round. Screen shape was
confirmed Bank-shaped via live recon (existing driver + `ec-ui-knowledge/screens/orifice_plate.md`
+ a DB column check) before writing new config, not assumed from a similar-looking screen.

## Lessons / known risks
- Optional dropdowns beyond the three mandatory extras are skipped (none of them are mandatory).
- Delete relies on the shared engine's grid-redraw handling — async grid render, not a
  screen-specific quirk.
- The PR flagged its own registry/scorecard rows as **MODIFIED, not added** (replacing the
  2026-07-26 generator-scaffolded build's rows) — relevant if a future merge touches the same
  shared doc files and sees what looks like a duplicate row.
