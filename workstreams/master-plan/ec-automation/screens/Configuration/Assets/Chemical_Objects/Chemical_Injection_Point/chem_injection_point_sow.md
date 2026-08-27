# SOW - Chemical Injection Point IUD (Configuration > Assets > Chemical Objects)

## 1. Identity
- **Screen:** Chemical Injection Point   **BF:** CO.0212   **View:** `OV_CHEM_INJ_POINT`   **Base:** `CHEM_INJ_POINT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED.
- **Date-effective:** YES (VERSIONED) -> DELETE = End Date = Start Date.

## 2. Navigator (gated, genuine 3-level cascade)
`nav:form:G:0:R:1:C:1..3:dd` = Production Unit -> Area -> Facility Class 1, same-row increasing
column (C:1/C:2/C:3 present, C:4 absent - confirmed live 2026-08-26); first-available + GO. Driven
via the shared T2 `Apply Navigator From Properties` keyword
(`testdata/chem_injection_point_navigator.properties`).

## 3. New-Object form (BY LABEL, screen-prefixed)
| Field | Label | Mandatory | Kind |
|---|---|---|---|
| Code | Chem Inj Point Code | yes | text |
| Name | Chem Inj Point Name | yes | text |
| Start Date | Start Date | yes | date |
| Op Production Unit | Op Production Unit | no | dropdown - `__FIRST__` (see gotcha below) |

## 4. IUD plan
5-TC structure (TC01 clean state, TC02 insert, TC03 update, TC04 find, TC05 delete). Fixed test
code `AUTOTEST_CIP` (not timestamp-generated); self-clean = absent in `OV_CHEM_INJ_POINT`, 0
residual re-read via a fresh DB connection.

## 5. Deliverables
T3 `pageobjects/Configuration/Assets/Chemical_Objects/chem_injection_point_page.resource`; suite
`tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot`; testdata
`testdata/chem_injection_point_{navigator,insert,update,form_verify,grid_verify}.properties`;
legacy Playwright driver `py/chem_injection_point_iud.py` retained for reference only (waived per
Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` - not rebuilt); this SOW; `README.md`;
`JOURNAL.md`; `CHECKLIST.md`; `evidence/`.

## 6. Dev story (2026-08-26, PR #550) - Area-pattern full conversion

_This SOW was backfilled 2026-08-27 under `docs/lean-deliverable-backfill-workorder.md` (Batch 2).
The RF automation described here was already built and merged in PR #550 on 2026-08-26; this
section narrates what that PR's own body recorded - it is not a new build, and no automation file
was touched to produce this backfill._

PR #550 converted Chemical Injection Point from the OLD 4-TC/suite-level-login shape to Area's
full pattern: 5 TCs, per-TC login/logout, a fixed test code (`AUTOTEST_CIP`),
properties-file-driven insert/update/verify, explicit grid-filter wiring, and the shared T2
`Apply Navigator From Properties` keyword driving the screen's genuine 3-level Production Unit ->
Area -> Facility Class 1 navigator cascade. The screen stayed classified OV-GM throughout - this
was a structural conversion, not a reclassification as plain Bank-shaped.

**Live gotcha found and fixed during the conversion (Op Production Unit / `__FIRST__`):** the
Insert form's own "Op Production Unit" `objectForm` field (distinct from the mandatory navigator
cascade) is a long (~25-row) autocomplete that renders only a small (~5-row) MRU/default subset
before its full reference list finishes loading. A hardcoded exact-label wait for the navigator's
own picked value (`AS1 EC Exploration Norway`) was flaky against that subset - the requested label
could be absent from whichever partial subset happened to render within the click-wait window
(diagnosed live via `tmp/recon_cip_pu_scroll_diagnosis.py`, which confirmed the DOM held only 5
`<tr>` rows at that moment). The fix reverted that ONE field to `__FIRST__` in
`chem_injection_point_insert.properties`, matching the exact tolerant mechanism the
already-proven, currently-passing legacy driver (`py/chem_injection_point_iud.py`, `verify_screen`
PASS 2026-07-30) already used for this field - not a new invention. The resulting row still shows
under the navigator scope regardless of which specific Op Production Unit value gets picked, so
this field is not actually required to match the nav scope for grid visibility on this screen
(confirmed by the proven driver's own passing behavior, unlike the Area/Facility Class 1 rationale
for their own Op-PU-must-match-nav convention, which does not hold here). Re-ran live after the
fix: 5/5 PASS.

## 7. Lessons
- Explicit dropdown values (label match) are the right default for navigator/reference fields that
  render their full option list promptly; `__FIRST__` remains the correct, tolerant choice for a
  field whose autocomplete only exposes a partial MRU subset at click time - don't force an exact
  label onto a field a proven driver already handles with `__FIRST__`.
- The 3-level Production Unit -> Area -> Facility Class 1 cascade fits the shared T2 `Apply
  Navigator From Properties` keyword's supported same-row C:1..C:N shape without any new plumbing.
