# SOW - Data Extract Set IUD

## Classification
- **Screen:** Configuration > Assets > Data_Mapping_Objects > Data Extract Set (BF_CODE **SP.0049**)
- **Type/pattern:** OV (Bank family, `manage_object_nav`) - plain manage-object, no navigator cascade,
  date-effective. Rebuilt to the **FULL Bank-pattern** shape (`bank_page.resource`/`berth_page.resource`)
  via PR #474 (2026-08-23, Batch 10 of the Bank-pattern conversion project): properties-file-driven
  insert/update/verify + explicit grid-filter wiring, on top of the pre-existing label-driven T3.
- **DB view:** `OV_SUMMARY_SET` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_SUMMARY_SET`

## Nav / grid / cells
- **Open:** menu search "Data Extract Set" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`), aliased locally
  as `${DATA_EXTRACT_SET_TABLE}`.
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`,
  driven by properties files (`testdata/data_extract_set_{insert,update,form_verify,grid_verify}.properties`):
  - **Insert (objectForm):** `Code`, `Name`, `Start Date`, **`Owner Class` (dropdown, MANDATORY - corrected
    2026-08-23 per this SOW; the 2026-07-26 build's "optional dropdowns skipped" note was factually wrong)**
    = `All`.
  - **Update (updateAttributes):** `Name` only - Owner Class is Insert-only (objectForm), not present in
    `updateAttributes`; Code is read-only.
  - **Delete (objectdates):** `End Date` = Start Date, field id
    `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (not label-scannable per-row, same convention as
    Bank/Berth).
- **Grid filter:** explicit `Find/Clear Data Extract Set Row By Filter` (T2 `Find/Clear Object Row By
  Filter`) wired into Update/Find/Verify-Found/Delete, matching Account/Bank/Berth's filter usage
  (owner, 2026-08-22 standardisation) rather than relying on `Select Object Row`'s implicit fallback.

## Test data
- Fixed test code **`AUTOTEST_DXT`** (changed from the earlier `AUTOTEST_DXT_<timestamp>` pattern to match
  Bank/Berth's fixed-code convention) - confirmed absent from `OV_SUMMARY_SET` before use each run.
  Start/End = `2000-01-01`. Never touches real rows.

## Dev story
Originally built 2026-07-26 as a generic-engine, label-driven OV screen (RF live 4/4, Playwright 7/7).
Rebuilt 2026-08-23 (PR #474, Batch 10) to the FULL Bank-pattern shape: properties-file-driven
insert/update/verify, explicit grid-filter wiring, dedicated credential pair
(`DATA_EXTRACT_SET_EC_USER/PASS`), fixed test code `AUTOTEST_DXT`, and a corrected field
classification - Owner Class is a **mandatory** dropdown per the screen's own SOW, not an optional
field that can be skipped, as the original 2026-07-26 build had assumed. Suite is now 5 TCs
(clean-state / insert / update / find / delete), each with its own Login/Logout on one browser
opened in Suite Setup, matching Bank/Berth's convention. No shared T1/T2 keyword changes were
needed - all required T2 keywords already existed. Sibling screen `Data Extract Setup` (SP.0043,
`data_extract_setup_page.resource`) is a DIFFERENT screen and was explicitly untouched by PR #474.

## Lessons / known risks
- The 2026-07-26 build's classification of Owner Class as an optional/skippable dropdown was WRONG -
  corrected 2026-08-23 after re-checking the live form; this SOW is the source of truth now.
- Delete relies on the fixed test code (`AUTOTEST_DXT`) being freed by TC05 every run - EC never lets a
  deleted code be reused, so a failed/aborted run leaves the code stuck until manually cleaned.
