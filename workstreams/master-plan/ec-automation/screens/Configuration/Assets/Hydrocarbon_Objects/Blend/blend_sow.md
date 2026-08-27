# SOW - Blend IUD

## Classification
- **Screen:** Configuration > Assets > Hydrocarbon_Objects > Blend (BF_CODE **CO.0219**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain (no navigator, no mandatory
  dropdowns) - **Bank family**, FULL Bank-pattern (properties-file-driven, grid-filter-wired, T2-consolidated,
  5-TC) as of the Batch 7 conversion (PR #457, merged 2026-08-23)
- **DB view:** `OV_BLEND` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_BLEND`

## Nav / grid / cells
- **Open:** menu search "Blend" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`); explicit
  grid-filter wiring via `Find Blend Row By Filter` / `Clear Blend Row Filter` (delegates to shared T2
  `Find/Clear Object Row By Filter`) rather than relying only on `Select Object Row`'s implicit
  3s-timeout fallback (owner, 2026-08-22: "others... should follow Account... utilise same filter feature").
- **NO hardcoded field ids** for the form fields - resolved BY LABEL via T2's properties-file-driven
  keywords (`Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found`):
  - **Insert (objectForm):** `Blend Code`*, `Blend Name`*, `Start Date`* (mandatory, confirmed live via
    `MandatoryCellStyle` on the data cells 2026-08-23). Optional: `End Date`, `Sort Order`, `Description`,
    `Master System Code`, `Master System Name` - skipped.
  - **Update (updateAttributes):** same set minus the two Date fields; `Blend Code` read-only there.
  - **Delete (objectdates):** hardcoded `${BLEND_DEL_ENDDATE}` (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`)
    - deliberately NOT label-driven, same documented shape as Bank's/Customer's own delete-field ids
    (objectdates row packs Start Date C:1 / End Date C:3, label at C:2 - confirmed live 2026-08-23).
  - Blend's Code/Name fields are screen-prefixed ("Blend Code"/"Blend Name", matching State's own
    "State Code"/"State Name" precedent) - NOT the generic "Code"/"Name" Bank/Customer use.
    `${BLEND_CODE_LABEL}` = `Blend Code` is threaded through every T2 call that resolves the Code
    field by label.

## Test data
- Fixed test code `AUTOTEST_BLEND` (not a per-run generated unique code) - confirmed absent from
  `OV_BLEND` before use; every run must complete TC05 (delete) so the code stays reusable, since EC
  never lets a deleted code be reused otherwise.
- `testdata/blend_insert.properties`, `blend_update.properties`, `blend_form_verify.properties`,
  `blend_grid_verify.properties` drive the 5 TCs. Start/End = `${TEST_START_DATE}`/`2000-01-01`.
  Never touches real production rows.

## Dev story
Built 2026-07-26 via `ec-object-iud-builder`: recon-first (DB `CLASS_TYPE=OBJECT` => OV; live form
scan) found a plain Bank-layout OV with no mandatory dropdowns; delivered as a label-driven RF T3 +
suite (4 TCs: insert/update/delete/cleanup) plus a thin Playwright driver, both green (RF 4/4,
Playwright 7/7) on the shared engine + T2 with zero engine changes.

Upgraded 2026-08-23 (Batch 7 of the Bank-pattern conversion project, PR #457): the PARTIAL
label-driven RF build was rebuilt into the FULL properties-file-driven, grid-filter-wired "Bank
pattern" matching `bank_page.resource`/`customer_page.resource`/`state_page.resource` - added
`Find/Clear Blend Row By Filter` (delegating to shared T2), converted Insert/Update/Verify to the
properties-file-driven keywords (`Insert/Update Object From Properties`, `Verify Object Insert
Exists/Form Record/Found`), threaded `code_label=Blend Code` through since Blend's Code field is
screen-prefixed (matching State's precedent), and converted the suite to the 5-TC pattern (TC01
clean-state / TC02 insert / TC03 update / TC04 find / TC05 delete) with a fixed test code
`AUTOTEST_BLEND` and per-TC Login/Logout. No shared T1/T2 file was touched - every needed keyword
already existed. Live run: 5/5 first attempt; DB self-clean confirmed via a fresh connection (0
residual `AUTOTEST_BLEND` rows in `OV_BLEND`); full-tree dryrun 753/753.

This backfill (2026-08-28, `docs/lean-deliverable-backfill-workorder.md` Batch 9) refreshes this
SOW/README/JOURNAL/CHECKLIST/evidence/KB-map bundle - which had been left describing the 2026-07-26
partial 4-TC build - to reflect the 2026-08-23 Bank-pattern conversion that superseded it. **No RF
automation file was touched or re-verified from scratch** by this backfill; the suite was re-run once
live (5/5, first attempt) purely to capture current-state evidence.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory).
- Delete field id is hardcoded by design (not label-driven) - documented, same shape as Bank/Customer.
- Registry (`docs/ec_screen_registry.md` row) and scorecard (`docs/automation-scorecard.md` row) were
  already updated at the PR #457 merge and needed no changes in this backfill - only the bundle docs
  (SOW/README/JOURNAL/CHECKLIST/evidence) and `VERIFY-REPORT.md`/KB map were stale.
