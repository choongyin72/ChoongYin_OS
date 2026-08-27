# SOW - Inventory Area IUD

## Classification
- **Screen:** Configuration > Assets > Inventory_Objects > Inventory Area (BF_CODE **CD.0115**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain (no mandatory dropdowns)
- **DB view:** `OV_INVENTORY_AREA` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_INVENTORY_AREA`

## Nav / grid / cells
- **Open:** menu search "Inventory Area" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`).
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Inventory Area Code`, `Inventory Area Name`, `Start Date` (mandatory). Optional dropdowns skipped.
  - **Update (updateAttributes):** `Inventory Area Name` (Code read-only; loaded-check via `OV Field Id By Label` on `Inventory Area Code`).
  - **Delete (objectdates):** `End Date` = Start Date.

## Test data
- Fixed code `AUTOTEST_INVA` (Bank/Berth convention as of the Batch 8 rebuild, not the original
  per-run generated code) - confirmed absent from `OV_INVENTORY_AREA` before being wired in
  (2026-08-23). Start/End = `2000-01-01`. Update name -> `AUTOTEST Inventory Area UPDATED`. Never
  touch real rows.

## Dev story
Original build (2026-07-26): recon-first (DB `CLASS_TYPE=OBJECT` => OV; live form) -> plain
Bank-layout OV, no mandatory dropdowns. Built label-driven on the shared engine + T2 (zero engine
changes). Playwright driver 7/7; RF T3+suite label-driven -> live 4/4.

**Rebuilt 2026-08-23 (Batch 8, PR #460)** from that partial label-driven build to the FULL
Bank/Berth-pattern shape: `inventory_area_page.resource` and `inventory_area_iud.robot` were rebuilt
to mirror `berth_page.resource`/`berth_iud.robot` exactly - properties-file-driven insert/update/verify
(`testdata/inventory_area_{insert,update,form_verify,grid_verify}.properties`), explicit grid-filter
wiring (`Find Inventory Area Row By Filter`/`Clear Inventory Area Row Filter` -> shared T2's
`Find Object Row By Filter`, per the owner's 2026-08-22 "others should follow Account" standing
instruction), dedicated per-screen credentials (`INVENTORY_AREA_EC_USER`/`INVENTORY_AREA_EC_PASS` in
`resources/credentials.py`), and expanded the suite from 4 to 5 TCs (added TC01 Verify Clean State)
with per-TC login/logout, matching Bank/Berth's convention. No changes to shared T1/T2 files
(`manage_object.resource`/`common.resource`) - every consolidated keyword reused as-is.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete relies on async grid redraw after delete+GO;
  RF's Browser auto-wait tolerates it (no screen-specific tuning needed).
- Batch 7's lesson carried into this build: `ec_screen_registry.md`/`automation-scorecard.md` rows
  must be a clean REPLACEMENT of the old row, not left alongside stale text (both confirmed MODIFIED,
  not duplicated, in PR #460).
