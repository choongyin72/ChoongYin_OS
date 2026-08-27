# Screen: Facility Class 1

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
  Converted 2026-08-26 to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (PR #526 +
  PR #530) - remains OV-GM; the conversion is structural, not a reclassification.
- **BF_CODE:** CO.0019 - **Treeview:** Configuration > Assets > Facility_Objects > Facility Class 1
- **DB view:** `OV_FCTY_CLASS_1` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - live RF run 5/5 pass, DB-verified
  (fresh-connection self-clean = 0 residual), robocop 7 issues (2 VAR02 + 5 DOC02, same non-regression
  baseline as Area), hygiene PASS.

## Selectors
| Purpose | Selector |
|---|---|
| Open | `Open EC Screen` -> "Facility Class 1" (T1 treeview keyword) |
| Navigator (gated, 2-level same-row cascade) | `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `nav:form:G:0:R:1:C:2:dd` (Area) - C:3 absent; filled via shared T2 `Apply Navigator From Properties` from `testdata/facility_class_1_navigator.properties` (EXPLICIT values, not first-available, since PR #526) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Grid filter | `Find/Clear Facility Class 1 Row By Filter` (T3 wrapper -> shared T2 `Find/Clear Object Row By Filter`, filters the Code column) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" (via shared T2 `Insert Object From Properties And Verify Code`) |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded deliberately - not label-driven, same rationale as Area/Bank's own del-enddate constant) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, screen-prefixed)
**Facility Class 1 Code*** - **Facility Class 1 Name*** - **Start Date*** (date). (`*` mandatory)
objectForm DOES also expose "Op Production Unit"/"Op Area" fields (confirmed live 2026-08-26 -
broader than the original 2026-07-30 build's "no Op PU field" note) but the proven driver/suite
inserts successfully leaving them blank - not filled, per the repo's standing rule against hunting
unstated requirements.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Facility Class 1 Code` (ro) - **`Facility Class 1 Name`**. Delete: **`End Date`** = Start Date ->
leaves `OV_FCTY_CLASS_1` (true delete).

### Grid columns (confirmed live 2026-08-26, `manageObject:form:T_head` scan)
Facility Class 1 Code / Facility Class 1 Name / Start Date / End Date - same 4-column shape as Area.

## Test data
Fixed test code **`AUTOTEST_FC1`** (confirmed free in `OV_FCTY_CLASS_1` via a fresh oracledb
connection before use, since PR #530 - replaced the earlier generated `AUTOTEST_FC1_<timestamp>`
code). Navigator scope: `Op Production Unit=AS1 EC Exploration Norway`, `Op Area=AS1_Area`
(`testdata/facility_class_1_navigator.properties`).

## Automation (code in ec-automation)
- **Playwright:** `py/facility_class_1_iud.py` (shared engine `ec_object_iud.py` +
  `apply_ovgm_navigator`) - built 2026-07-30, RETAINED as-is (still passing); NOT rebuilt as part of
  the 2026-08-26 conversion or this backfill - Playwright bundles are waived for Bank-/Area-pattern
  work (owner decision 2026-08-27, Universal Screen Engine is the forward replacement).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource`
  (label-driven, `code_label=Facility Class 1 Code`) + suite
  `tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot` (5 TCs: Verify Clean
  State/Insert/Update/Find/Delete, per-TC Login/Logout on one Suite-Setup-opened browser).
- **Properties files:** `testdata/facility_class_1_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Gate (2026-08-27 backfill re-run):** dryrun 5/5, live headless 5/5, robocop 7 issues
  (non-regression baseline), hygiene PASS, DB self-clean 0 residual (see
  `screens/Configuration/Assets/Facility_Objects/Facility_Class_1/VERIFY-REPORT.md`).

## Quirks
- OV-GM navigator-gated: grid empty until the 2-level Production Unit -> Area cascade + GO is
  applied. This screen was the FIRST to exercise the shared `Apply Navigator From Properties`
  keyword's multi-column same-row cascade addressing (`C:1`/`C:2` in one row) - Area itself only has
  a single navigator dropdown and never exercised that shape. No shared-file change was needed; the
  existing flat 0.7s sleep in the shared keyword was already sufficient.
- Field labels are screen-prefixed ("Facility Class 1 Code"/"Facility Class 1 Name"), like
  Area/Sub Area - not the generic "Code"/"Name" Bank/Object List use.
- objectForm DOES have Op Production Unit/Op Area fields (see above) but they are NOT required for a
  successful insert - don't add them to test data without a stated reason to.
- Delete = End Date = Start Date via the `objectdates` tab's hardcoded field id (not label-driven,
  documented rationale above).
