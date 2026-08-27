# SOW - Reservoir Block IUD

## Classification
- **Screen:** Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block (BF_CODE **CO.0133**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; **plain Bank-pattern**
  (no navigator/mandatory dropdowns) - converted to the FULL Bank-pattern shape in Batch 9
  (PR #466, merged 2026-08-23): properties-file-driven Insert/Update/Verify + explicit grid-filter
  wiring, same shape as `bank_page.resource`/`berth_page.resource`.
- **DB view:** `OV_RESV_BLOCK` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_RESV_BLOCK`
- **Grid id:** `${RESERVOIR_BLOCK_TABLE}` = shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`
  (= `manage_object_nav_nav:form:T_data`).

## Nav / grid / cells
- **Open:** menu search "Reservoir Block" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}`, wired with **explicit grid-filter** keywords
  (`Find Reservoir Block Row By Filter` / `Clear Reservoir Block Row Filter` -> shared T2
  `Find/Clear Object Row By Filter`) rather than relying only on the implicit 3s-timeout fallback in
  `Select Object Row` - matches Bank/Berth/Account/State's convention (owner, 2026-08-22).
- **NO hardcoded field ids** - resolved BY LABEL via the shared T2 `Fill OV * By Label` / `OV Field Id
  By Label`, with the screen's own prefixed labels (`@{RESERVOIR_BLOCK_FORM_LABELS}` = `Reservoir Block
  Code`, `Reservoir Block Name` - NOT the generic "Code"/"Name" Bank/Object List use):
  - **Insert (objectForm):** `Reservoir Block Code`, `Reservoir Block Name`, `Start Date` (mandatory).
    Optional dropdowns skipped (IUD fills only needed fields).
  - **Update (updateAttributes):** `Reservoir Block Name` only (Code read-only; Start Date is
    Insert-only, not present in `updateAttributes` - same as Bank/Berth).
  - **Delete (objectdates):** `End Date` (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`) = Start Date.
- **Test data driven from properties files** (`testdata/reservoir_block_{insert,update,form_verify,
  grid_verify}.properties`), not hardcoded in the T3/suite.

## Test data
- Fixed test code `AUTOTEST_RESVB` (matching Bank/Berth's convention - confirmed absent from
  `OV_RESV_BLOCK` before being wired in). Start/End = `2000-01-01`. Per-TC login/logout using
  Reservoir Block's own dedicated credentials (`RESERVOIR_BLOCK_EC_USER`/`RESERVOIR_BLOCK_EC_PASS`).
  Never touch real rows.

## Dev story
Originally built 2026-07-26 as a partial, label-driven-only implementation (RF 4/4, no properties
files, no grid-filter wiring) - see the JOURNAL's 2026-07-26 entry for that earlier build. Upgraded in
**Batch 9 of the Bank-pattern conversion project (PR #466, merged 2026-08-23)** to the full Bank/Berth
shape: properties-file-driven Insert/Update/Verify plus explicit grid-filter wiring
(`Find/Clear Reservoir Block Row By Filter`, wired into Update/Find/Verify-Found/Delete), reusing the
shared T1/T2 keywords as-is (zero shared-keyword changes). Suite expanded from 4 TCs to the full 5-TC
shape (TC01 clean-state / TC02 insert / TC03 update / TC04 find / TC05 delete), fixed test code
`AUTOTEST_RESVB`, per-TC login/logout with dedicated credentials. **Real gotcha from the PR:** the
Batch 9 ground-rules doc assumed the "Batch 9 additions (pending)" checklist-doc section header was
already merged to master via PR #464 - but at branch-clone time PR #464 was still open, so PR #466 had
to re-add the identical header text verbatim, flagging (not silently resolving) the small header-
duplication conflict for whichever of the two PRs merged second.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete uses the shared engine's async-redraw-aware
  row-absent wait.
- robocop on the rebuilt T3+suite: exit 1, but the same 9 baseline issues (8x DOC02 missing test-case
  documentation, 1x VAR02 unused variable) as the accepted `berth_iud.robot` exemplar - parity, not a
  regression.
