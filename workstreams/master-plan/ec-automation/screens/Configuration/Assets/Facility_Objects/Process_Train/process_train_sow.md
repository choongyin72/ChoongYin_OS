# SOW - Process Train IUD

_Backfilled 2026-08-28 (docs/lean-deliverable-backfill-workorder.md, Batch 10) - this SOW predates
the Batch 9 Bank-pattern rebuild (PR #469, merged 2026-08-23) and is refreshed here, not recreated,
per the Batch 1 precedent ("several screens had pre-existing bundles predating the lean rule that
needed refreshing, not fresh creation")._

## Classification
- **Screen:** Configuration > Assets > Facility_Objects > Process Train (BF_CODE **CO.0120**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective. Converted to the full
  **Bank/Berth pattern** (Batch 9 of the Bank-pattern conversion program, PR #469) - properties-file-driven
  insert/update/verify, T2-consolidated, explicit grid-filter wiring (`Find/Clear Process Train Row By Filter`).
  Plain OV, **no navigator/mandatory dropdown cascade** in the sense of Area's OV-GM screens - but see the
  live correction below, it is not a "zero mandatory fields beyond Code/Name/Start Date" screen either.
- **DB view:** `OV_PROCESS_TRAIN` (versioned); key `CODE`
- **Grid id:** `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`), shared T2 constant.
- **Delete:** End Date = Start Date -> row leaves `OV_PROCESS_TRAIN`.

## Nav / grid / cells
- **Open:** menu search "Process Train" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **NO hardcoded field ids** - resolved BY LABEL via shared T2 `manage_object.resource` keywords, matching
  Bank/Berth exactly:
  - **Insert (objectForm):** `Process Train Code`, `Process Train Name`, `Start Date`, and
    **`Production Facility Class 1` (`__FIRST__`)** - see "Mandatory fields" below, this dropdown is
    de-facto required to persist even though it carries no CSS mandatory flag.
  - **Update (updateAttributes):** `Process Train Name` only (Code read-only; Start Date lives only in
    objectdates, not updateAttributes - same as Bank/Berth).
  - **Delete (objectdates):** `End Date` = Start Date.

## Mandatory fields (live-confirmed, PR #469)
`Process Train Code` / `Process Train Name` / `Start Date` / **`Production Facility Class 1`**. The
KB doc's original 2026-07-26 scan called all dropdowns optional; a live RF attempt in Batch 9 with only
Code/Name/Start Date clicked Save successfully (button enabled, click succeeded) but the row never
reached `OV_PROCESS_TRAIN` (0 rows) and left EC's own unsaved-changes confirmation modal
(`#confirmationForm:confirmation_modal`) open, stalling every subsequent click (4/5 fail that attempt).
Re-running the already-proven, unmodified `py/process_train_iud.py` (which fills Production Facility
Class 1 = `__FIRST__`) passed 7/7 cleanly, confirming that dropdown is required for Save to actually
commit - a business-rule-level requirement invisible to a static field/CSS scan.

## Test data
- Fixed test code `AUTOTEST_PT` (not a per-run unique code) - matching Bank/Berth's convention, confirmed
  absent from `OV_PROCESS_TRAIN` before being wired in. Every run must complete TC05 (delete) so the code
  is free for the next run. Start/End = `2000-01-01`.

## Dev story
Originally built 2026-07-26 as a plain label-driven OV on the shared engine + T2 (Playwright 7/7, RF live
4/4) with optional dropdowns skipped as non-mandatory. Rebuilt in Batch 9 (PR #469, merged 2026-08-23) to
the full Bank/Berth pattern - properties-file-driven testdata, T2-consolidated helpers, and explicit
`Find/Clear Process Train Row By Filter` grid-filter wiring (owner, 2026-08-22: other screens should
follow Account's explicit-filter convention). During that rebuild a live RF run surfaced the
Production-Facility-Class-1 gotcha above; the fix and the KB correction were shipped in the same PR
(write-after). Live RF suite passed 5/5 post-fix (TC01 clean-state / TC02 insert / TC03 update / TC04
find / TC05 delete). No shared T1/T2 (`manage_object.resource`/`common.resource`) files were changed -
every consolidated T2 keyword was reused as-is.

## Lessons / known risks
- `Production Facility Class 1 = __FIRST__` is deliberately EXCLUDED from the round-trip form-label
  compare list (`@{PROCESS_TRAIN_FORM_LABELS}` in the T3) because `__FIRST__` never matches the resolved
  literal text on reload - a documented Batch 9 gotcha shared by other screens using the same convention.
- Robocop baseline: 9 issues (4 VAR02 + 5 DOC02), identical in kind/count to Bank/Berth/Port's established
  baseline - not a new defect class.
