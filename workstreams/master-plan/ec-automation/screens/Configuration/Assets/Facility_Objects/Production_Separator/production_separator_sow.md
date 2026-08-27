# SOW - Production Separator IUD (Configuration > Assets > Facility_Objects)

_Backfilled 2026-08-27 under `docs/lean-deliverable-backfill-workorder.md` (Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) to reflect the Area-pattern conversion in PR #551, merged
2026-08-26 - the prior version of this SOW predated that conversion and still described the OLD
4-TC/first-available-navigator shape._

## 1. Classification
- **Screen:** Production Separator   **BF:** CO.0042   **View:** `OV_PRODSEPARATOR` (versioned)   **Base:** `SEPARATOR`
- **Type:** OV-GM (groupmodel manage-object; grid `manageObject:form:T_data`), navigator-GATED,
  date-effective. Pattern: **Area-pattern** (full 5-TC/per-TC-login/properties-file-driven
  structure - owner's 2026-08-26 standing rule that any navigator screen matching Area's layout
  gets Area's full pattern, the same status Bank holds for non-navigator screens).

## 2. Navigator / grid / cell shape
- **Navigator:** genuine 3-level, same-row-increasing-column cascade - Production Unit (`nav:form:
  G:0:R:1:C:1:dd`) -> Area (`C:2:dd`) -> Facility Class 1 (`C:3:dd`), no 4th level (`C:4` absent,
  confirmed live 2026-08-26). Filled via the shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`), driven by `testdata/production_separator_navigator.properties`
  with explicit values (Op Production Unit=`AS1 EC Exploration Norway`, Op Area=`AS1_Area`, Op
  Facility Class 1=`AS1_Facility_01`) - the same values the screen's prior first-available cascade
  already resolved to live, captured explicitly rather than re-invented.
- **Grid columns** (confirmed live, `manageObject:form:T_head`): Production Separator Code /
  Production Separator Name / Start Date / End Date - same 4-column shape as Area/Facility Class 1.
- **Field labels are screen-prefixed:** "Production Separator Code" / "Production Separator Name"
  (like Area's "Area Code"/"Area Name"), not the generic "Code"/"Name" Bank/Object List use.
- **Delete End Date field** is hardcoded (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`),
  not label-driven - Start Date (C:1) and End Date (C:3) share a row with the End Date label at
  C:2, a shape the one-field-per-row label scan cannot safely resolve (same rationale as Area's/
  Bank's own `${..._DEL_ENDDATE}` constant).

## 3. Mandatory fields / test data
- **Insert (mandatory):** Production Separator Code, Production Separator Name, Start Date, Op
  Production Unit. Op Production Unit is a date-effective reference dropdown filtered by the
  form's OWN Start Date; the exact-value approach (`AS1 EC Exploration Norway`, the alphabetically-
  first option pre-Start-Date) reproducibly timed out live once Start Date=2000-01-01 was filled,
  because the version-filtered post-Start-Date list differs from the pre-filter list. Fixed by
  using the shared T2's `__FIRST__` literal instead (`Fill OV Dropdown By Label` / `Select First EC
  Dropdown Option`) - the SAME mechanism the pre-existing Playwright driver
  (`py/production_separator_iud.py`) already used successfully (`insert_fields: {"label": "Op
  Production Unit", "value": "__FIRST__"}`). This is the same class of "Op Production Unit dropdown
  filtered / doesn't include the exact nav value" issue also hit and fixed identically on Chemical
  Tank and Chemical Injection Point.
- **Update (mandatory):** Production Separator Name only - Production Separator Code is read-only
  in `updateAttributes`.
- **Test data:** fixed test code `AUTOTEST_PSEP` (not generated/timestamped, unlike the old
  pre-conversion `AUTOTEST_PSEP_<timestamp>`) - confirmed absent from `OV_PRODSEPARATOR` before
  wiring it in; every run must complete TC05 (delete) so the code is free for the next run.
- Extra objectForm fields exist (Sort Order, Meter Frequency, Op Area/Op Facility Class 1, Cp
  Production Unit, Geo Area/Geo Field, etc.) but the proven driver leaves them blank and inserts
  successfully under this scope - trusted, not hunted for as an unstated requirement.

## 4. Dev story (real, from PR #551, merged 2026-08-26)
Converted Production Separator's existing RF automation from the old shape (4 TCs, suite-level
login, `Apply OV-GM Navigator First Available` cascade, inline DB-verify calls) to Area's full
pattern: 5 TCs, per-TC login/logout, the shared T2 `Apply Navigator From Properties` keyword driven
by explicit values for the genuine 3-level Production Unit -> Area -> Facility Class 1 navigator
cascade, properties-file-driven insert/update/verify, explicit grid-filter wiring, and zero inline
DB-verify calls (all screen verification delegates to shared T2 keywords). No shared T1/T2 files
(`resources/manage_object.resource`, `resources/table.resource`, `resources/common.resource`) were
touched - the existing `Apply Navigator From Properties` keyword already supported this screen's
3-level same-row cascade shape as-is. The one real gotcha: the form's Op Production Unit dropdown
is a date-effective reference filtered by the form's own Start Date, so requesting the EXACT
alphabetically-first value after Start Date was filled reproducibly timed out live (2 attempts,
`tmp/wt-prodsep-live/output.xml`, TC02) - resolved by reusing the pre-existing driver's proven
`__FIRST__` mechanism instead of a fixed string, matching the same fix already applied to Chemical
Tank and Chemical Injection Point for the identical class of issue.

## 5. Deliverables
- Driver (pre-existing, unchanged, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`): `py/production_separator_iud.py`.
- T3: `pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource`.
- Suite: `tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot` (5 TCs).
- Testdata: `testdata/production_separator_{navigator,insert,update,form_verify,grid_verify}.properties`.
- This SOW, `README.md`, `JOURNAL.md`, `CHECKLIST.md`, `evidence/`,
  `ec-ui-knowledge/screens/production_separator.md` (this backfill, 2026-08-27).
