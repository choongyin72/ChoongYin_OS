# SOW — Well Hole IUD (Configuration > Assets > Well_and_Reservoir_Objects)

_Refreshed 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 4) for the Area-pattern
STRUCTURE conversion (PR #543, merged 2026-08-26). The original 2026-07-31 SOW text below described
the OLD 4-TC "Apply OV-GM Navigator First Available" shape and is now superseded by the section
above it; it is retained further down for historical reference, not deleted._

## Classification
- **Screen:** Well Hole   **BF:** CO.0051   **View:** `OV_WELL_HOLE` (versioned)   **Base:** `WELL_HOLE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED,
  date-effective. Converted to Area's full RF pattern (PR #543, 2026-08-26): 5-TC/per-TC-login/
  pure-screen-verify structure, properties-file-driven insert/update/verify, explicit grid-filter
  wiring, zero inline DB-verify calls.

## Navigator / grid / cell shape
- **Navigator:** genuine 3-level SAME-ROW cascade — Op Production Unit (`nav:form:G:0:R:1:C:1:dd`)
  -> Op Area (`C:2`) -> Op Facility Class 1 (`C:3`) — mandatory before the grid loads any rows.
- **Scope used:** SPECIFIC "P1 Production Unit / P1 Area / P1 Facility 1" — the SAME scope already
  proven live by the sibling Well screen (`well_page.resource`, owner screenshot ground truth
  2026-07-30), NOT first-available. Confirmed live 2026-08-26 that this scope also lists 20 real
  rows in `OV_WELL_HOLE` and that "P1 Production Unit" is a valid Insert-form Op Production Unit
  option.
- Navigator fill delegates to the shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`), driven by `testdata/well_hole_navigator.properties`.
- **Grid:** `manageObject:form:T_data`, filtered explicitly via `Find/Clear Well Hole Row By
  Filter` (shared T2 `Find/Clear Object Row By Filter` on the Code column).
- **Cell labels:** SCREEN-PREFIXED — "Well Hole Code" / "Well Hole Name" (like Area's "Area
  Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use.

## Mandatory fields
- **Insert (`objectForm`):** Well Hole Code*, Well Hole Name*, Start Date* (mandatory); Op
  Production Unit must equal the navigator's own PU value (`P1 Production Unit`) or the inserted
  row is invisible under the filtered grid scope.
- **Update (`updateAttributes`):** Well Hole Name only — Well Hole Code is read-only;
  `OV_WELL_HOLE` has no Description column.
- **Delete (`objectdates`):** End Date = Start Date (zero-length window => true delete), field id
  `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — same rationale
  as Area's `${AREA_DEL_ENDDATE}`: End Date label sits at C:2, Start Date at C:1).

## Test data
- Fixed test code `AUTOTEST_WELL_HOLE` (not a generated/unique code) — confirmed absent from
  `OV_WELL_HOLE` before PR #543 wired it in; every run must complete TC05 (delete) so the code is
  free for the next run.
- `testdata/well_hole_{insert,update,form_verify,grid_verify,navigator}.properties`.

## Dev story (from PR #543's real body)
PR #543 converted Well Hole's RF automation from the OLD pattern (4 TCs, `Apply OV-GM Navigator
First Available`, single suite-level login, generated timestamp code) to Area's full pattern (5
TCs, per-TC login/logout, properties-file-driven insert/update/verify, explicit grid-filter wiring,
zero inline DB-verify calls). The real gotcha: the OLD build used a first-available navigator scope
that was sparse/unreliable for this screen; the conversion instead reused the sibling Well screen's
already-proven SPECIFIC "P1" scope, confirming live (2026-08-26) that the same scope also lists real
`OV_WELL_HOLE` rows before committing to it — i.e. copy-adapt-verify against a sibling, not a fresh
guess. No shared-file regression risk: `resources/manage_object.resource`'s `Apply Navigator From
Properties` keyword already existed (added on PR #521/#523). Well Hole's Playwright bundle
(`py/well_hole_iud.py`, live 8/8, 2026-07-31) was left untouched by the conversion, and stays
permanently waived from further build per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (the
Universal Screen Engine replaces that role going forward).

## Deliverables
- Driver `py/well_hole_iud.py` (unchanged, historical Playwright reference — waived from rebuild).
- T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource`.
- Suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot` (5 TCs).
- This SOW, `README.md`, `JOURNAL.md`, `evidence/`, `CHECKLIST.md` (all refreshed/added by this
  backfill, 2026-08-28), plus the pre-existing `VERIFY-REPORT.md` (kept as a historical record of
  the 2026-07-31 base build, not re-generated — it predates and does not describe the current 5-TC
  structure) and `investigation/` (pre-existing, left untouched).
- KB selector map `ec-ui-knowledge/screens/well_hole.md` (refreshed this backfill).

---

## Historical (superseded) — original 2026-07-31 SOW text
- **Screen:** Well Hole   **BF:** CO.0051   **View:** `OV_WELL_HOLE`   **Base:** `WELL_HOLE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_WHL_<timestamp>`; self-clean = absent in OV_WELL_HOLE.
- Deliverables (original): driver `py/well_hole_iud.py`, T3
  `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource`, suite
  `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot`, this SOW,
  `VERIFY-REPORT.md` (auto-generated).
