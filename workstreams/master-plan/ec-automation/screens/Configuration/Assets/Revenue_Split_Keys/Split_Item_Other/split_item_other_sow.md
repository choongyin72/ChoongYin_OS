# SOW - Split Item Other IUD

## Classification
- **Screen:** Configuration > Assets > Revenue_Split_Keys > Split Item Other (BF_CODE **CD.0017**)
- **Type/pattern:** OV (Manage-Object, controller `manage_object_nav`) - date-effective; **plain
  Bank-pattern OV** (no mandatory navigator, no mandatory dropdowns). Class `SPLIT_ITEM_OTHER`,
  view `OV_SPLIT_ITEM_OTHER`. NOT the same screen as the 6 sibling "* Split Key" screens
  (Product/Company/Field/Stream Item Category/Other/Stream Item Split Key), which share a
  DIFFERENT class `SPLIT_KEY` and view `OV_SPLIT_KEY` via the `manage_object_split_key`
  controller - confirmed by direct file-path/class inspection, not assumed from name similarity.
- **DB view:** `OV_SPLIT_ITEM_OTHER` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_SPLIT_ITEM_OTHER`
- **Grid id:** `manage_object_nav_nav:form:T_data` (shared T2 `${OV_MANAGE_OBJECT_TABLE}` constant)

## Nav / grid / cells
- **Open:** menu search "Split Item Other" -> `label.tv-link`. Navigator = single **Date + GO**
  (not mandatory - no navigator scope value required); grid needs GO to load.
- **Insert (objectForm), mandatory fields:** `Split Item Code` (screen-prefixed) / GENERIC `Name`
  (NOT screen-prefixed - confirmed via direct grep of the live form) / `Start Date`. No mandatory
  optional dropdowns.
- **Update (updateAttributes):** `Name` only (`Split Item Code` read-only in this form; `Start
  Date` lives only in Insert, not in updateAttributes - same convention as Bank/Berth).
- **Delete (objectdates):** `End Date` = Start Date, field id
  `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.

## Test data
- Fixed test code `AUTOTEST_SIO` (matching Bank/Berth's convention, not a generated-unique code -
  confirmed absent from `OV_SPLIT_ITEM_OTHER` before use). Name `AUTOTEST Split Item Other` ->
  updated to `AUTOTEST Split Item Other UPDATED`. Start/End = `2000-01-01`. Never touches real
  rows.

## Dev story (real history, pulled from the original PRs)
Built 2026-07-26 as the 10th OV-reuse-target: DB `CLASS_TYPE=OBJECT` recon confirmed OV shape;
label-driven T3 (no hardcoded field ids) on the shared engine + T2, verified via
`verify_screen.py` (RF 4/4 + Playwright 7/7, OVERALL PASS). Rebuilt **2026-08-23 via PR #471**
(Batch 10 of the Bank-pattern conversion project) to upgrade from that partial label-driven build
to the full Bank/Berth pattern: properties-file-driven insert/update/verify
(`Insert Object From Properties And Verify Code`, `Update Object From Properties`,
`Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object Found`) plus explicit
grid-filter wiring (`Find/Clear Split Item Other Row By Filter` -> shared T2 `Find/Clear Object
Row By Filter`) wired into Update/Find/Verify-Found/Delete. Rebuilt to the 5-TC business
narrative (TC01 Verify Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete) with
per-TC Login/Logout on one Suite-Setup browser, matching Bank/Berth's convention. Confirmed the
live field set (mandatory Code/Name/Start Date, no mandatory dropdowns) from the existing page
object plus the already-proven Playwright driver `py/split_item_other_iud.py` - no CSS/label
guessing needed.

## Lessons / known risks (from PR #471)
- No shared T1/T2 (`manage_object.resource`/`common.resource`) edits were needed - the Bank
  pattern's grid-filter helper already existed generically in T2.
- The filter keyword firing was confirmed live (not assumed): `grep -c "Find Object Row By
  Filter" output.xml` = 30 hits across the 5-TC run.
- Optional dropdowns confirmed not mandatory (none skipped by omission - verified against the
  live form, not inferred from a sibling screen).
- This backfill (2026-08-28) added SOW/README/JOURNAL/evidence/CHECKLIST refresh only - the RF
  automation itself (page object + suite + testdata) was NOT touched; re-ran the existing suite
  once (dryrun 5/5, live 5/5) purely to capture fresh evidence, per the backfill work order.
