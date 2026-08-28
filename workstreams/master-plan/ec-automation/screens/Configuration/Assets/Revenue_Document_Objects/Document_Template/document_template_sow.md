# SOW - Document Template IUD

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md`
Batch 12) to reflect the 2026-08-24 Bank-pattern conversion (PR #484). The 2026-07-26 original
build's classification/test-data facts are unchanged and carried forward below; only the RF
shape described has changed._

## Classification
- **Screen:** Configuration > Assets > Revenue_Document_Objects > Document Template (BF_CODE **CD.0013**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective, plain (no mandatory
  navigator cascade). **Bank-pattern conversion DONE (2026-08-24, Phase 3)**, via
  `ec-bank-pattern-converter` - upgraded from the original label-driven-only RF shape.
- **DB view:** `OV_DOC_TEMPLATE` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_DOC_TEMPLATE`

## Nav / grid / cells
- **Open:** menu search "Document Template" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`).
- **NO hardcoded field ids** - resolved BY LABEL via T2, now via the Bank-pattern properties-file
  keywords rather than the original per-field `Fill OV Field By Label` calls:
  - **Insert (objectForm):** `Code`, `Name`, `Start Date` (mandatory) + `Document Title`
    (de-facto mandatory - Save silently fails to persist without it, per the already-proven
    Playwright driver's own field set, trusted over the Phase-3 static scanner's "no mandatory
    dropdowns" note). Optional dropdowns skipped. Driven by
    `testdata/document_template_insert.properties` via `Insert Object From Properties And Verify
    Code`.
  - **Update (updateAttributes):** `Name` (Code read-only). Driven by
    `testdata/document_template_update.properties` via `Update Object From Properties`.
  - **Find/verify:** explicit `Find/Clear Document Template Row By Filter` wired into
    Update/Find/Verify-Found/Delete, matching Bank/Berth's own explicit grid-filter usage.
    Verification against `testdata/document_template_{form,grid}_verify.properties`.
  - **Delete (objectdates):** `End Date` = Start Date, field id resolved BY LABEL at runtime
    (`OV Field Id By Label`), not hardcoded.

## Test data
- Fixed test code **`AUTOTEST_DOCUMENT_TEMPLATE`** (changed from the original build's per-run
  `AUTOTEST_DT_<timestamp>` by the 2026-08-24 conversion, matching the fixed-code convention used
  by every other Bank-pattern-converted screen); Start/End = `2000-01-01`. Never touch real rows.
  Own dedicated login: `DOCUMENT_TEMPLATE_EC_USER`/`DOCUMENT_TEMPLATE_EC_PASS`
  (`resources/credentials.py`, added additively by PR #484).

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` => OV; live form) found a plain Bank-layout OV, no mandatory
navigator, only Code/Name/Start Date form-mandatory. Original 2026-07-26 build was label-driven
on the shared engine + T2 (zero engine changes): Playwright driver 7/7, RF T3+suite live 4/4.
The 2026-08-24 Bank-pattern conversion (PR #484, Phase 3 of the wider Bank-pattern conversion
project) classified the existing RF as **PARTIAL** (had `Fill OV Field By Label` but neither
`Insert Object From Properties` nor `Find <Screen> Row By Filter`) and rebuilt the T3 + suite to
the full properties-file-driven, explicit-grid-filter shape - TC01-05 (added TC04 Find), 4 new
`.properties` files, dedicated screen credentials, fixed test code. A 2026-08-25 alignment fix
then removed 2 leftover inline DB-verify keywords from the suite that violated Bank's
pure-screen-only verification convention. `py/document_template_iud.py` (Playwright) stayed
untouched throughout, still 7/7 from 2026-07-26.

## Lessons / known risks
- `Document Title` is de-facto mandatory even though the static scanner does not flag it (Save
  silently fails to persist without it) - trust the proven driver's field set over a static scan.
- Delete's `objectdates` End Date field id is resolved BY LABEL at runtime, not hardcoded - no
  live row-shape scan of `objectdates` has been run to safely hardcode an id the way Bank's own
  documented precedent does.
- This backfill's own contribution: the bundle's SOW/README/JOURNAL/CHECKLIST previously still
  described the pre-conversion 4-TC shape after PR #484 shipped the 5-TC Bank-pattern shape - this
  refresh corrects that drift, per the retired lean-waiver work order.
