# SOW - Stream Item Category IUD

## Classification
- **Screen:** Configuration > Assets > Stream_Objects > Stream Item Category (BF_CODE **CD.0016**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain Bank family
  (no navigator mandatory-value shape beyond Date+GO, no mandatory dropdowns). Full "Bank
  pattern" (properties-file-driven insert/update/verify + explicit grid-filter wiring, T2-
  consolidated) since PR #473 (2026-08-23, Batch 10 of the Bank-pattern conversion project).
  **NOT** the same screen as "Stream Item Category Split Key" (CD.0042, class `SPLIT_KEY`,
  shared view `OV_SPLIT_KEY`) - a sibling screen built separately; confirm real file paths before
  editing either.
- **DB view:** `OV_STREAM_ITEM_CATEGORY` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_STREAM_ITEM_CATEGORY`

## Nav / grid / cells
- **Open:** menu search "Stream Item Category" -> `label.tv-link`. Navigator = single **Date +
  GO**; grid needs GO to populate (no default rows on open).
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`), same
  constant Bank/Berth use.
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By
  Label`:
  - **Insert (objectForm):** `Code`, `Name`, `Start Date` (mandatory, GENERIC labels not
    screen-prefixed). Optional dropdowns skipped.
  - **Update (updateAttributes):** `Name` only (Code read-only; Start Date lives only in
    objectForm at Insert time, not present in updateAttributes).
  - **Delete (objectdates):** `End Date` = Start Date. Field id
    `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (kept hardcoded per Bank/Berth's own
    documented precedent, same framework-invariant objectdates row shape).
- **Grid-filter wiring (added PR #473):** `Find Stream Item Category Row By Filter` / `Clear
  Stream Item Category Row Filter`, thin wrappers around the shared T2 `Find Object Row By
  Filter` / `Clear Object Row Filter`, wired into Update/Find/Verify-Found/Delete.

## Test data
- Fixed test code `AUTOTEST_SIC` (not a generated/timestamped code - PR #473 moved this screen
  off the original generated-code convention to match Bank's fixed-code convention). Confirmed
  free in `OV_STREAM_ITEM_CATEGORY` before each run; every run completes TC05 (delete) so the
  code stays free for the next run. Start/End = 2000-01-01. Never touch real rows.

## Dev story
Original build (2026-07-26): recon-first (DB `CLASS_TYPE=OBJECT` -> OV; live form) -> plain
Bank-layout OV, no mandatory dropdowns; label-driven T3 on the shared engine + T2; Playwright
driver 7/7, RF T3+suite live 4/4, generated/timestamped test code, no grid-filter wiring.

PR #473 (2026-08-23, Batch 10): brought this screen up to the SAME full shape as
`bank_page.resource`/`berth_page.resource` - added properties-file-driven insert/update/verify
and explicit grid-filter wiring (both missing before), rebuilt the suite from 4-TC to 5-TC
(clean-state/insert/update/find/delete) with per-TC login/logout and the fixed test code
`AUTOTEST_SIC`. Confirmed the mandatory field set (Code/Name/Start Date only) against the
already-proven Playwright driver `py/stream_item_category_iud.py` rather than re-deriving it.
Registry/scorecard rows were MODIFIED (not duplicated) since this screen already had a row from
the 2026-07-26 build. One real LEN32 robocop hit (2 variable names 43/40 chars) fixed by
shortening `*_PROPERTIES` -> `*_PROPS`. A 2026-08-25 alignment fix then removed 3 direct
DB-verification calls from the `.robot` file's TC02/TC03/TC05 that violated Bank's pure-
screen-only verification convention.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory).
- Delete uses the shared T2's grid-redraw-aware verification.
- Disambiguation risk is real: 6 sibling "* Split Key" screens (including "Stream Item Category
  Split Key") share the view `OV_SPLIT_KEY` and can be confused with this plain screen by name
  alone - always confirm the real `_page.resource` file path, not just the screen title.
