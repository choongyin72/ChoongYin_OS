# Screen: Well Hookup

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  navigator-GATED.
- **BF_CODE:** CO.0108 - **Treeview:** Configuration > Assets > Facility_Objects > Well Hookup
- **DB view:** `OV_WELL_HOOKUP` (versioned; key `CODE`; also `NAME`, `OBJECT_START_DATE`,
  `OBJECT_END_DATE`)
- **Last verified:** 2026-08-27 - EC **14.2.4** - local sandbox
  (`localhost:1521/ORCL`, `ECKERNEL_EC`) - live RF 5/5 PASS, DB self-clean 0 residual `AUTOTEST%`
  rows, grid-filter wiring fired 15x. (Superseding the 2026-07-30 entry below this file previously
  held, which covered the pre-conversion 4-TC build.)
- **Pattern:** Area's full pattern (converted PR #539, merged 2026-08-26) - 5 TCs, per-TC
  Login/Logout, fixed test code, properties-file-driven fields, explicit grid-filter wiring, zero
  inline DB-verify calls in the `.robot` file (DB check lives only in shared T2
  `Verify Object Removed`).

## Selectors `[from pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource Variables]`

| Purpose | Selector |
|---|---|
| Open screen | menu search "Well Hookup" -> treeview link |
| Grid (rows) | `manageObject:form:T_data` |
| Navigator (mandatory, gated) | `nav:form:G:0:R:1:C:1:dd` (Op Production Unit) -> `C:2:dd` (Op Area) -> `C:3:dd` (Op Facility Class 1) -> GO `button:form:B`. Same row, increasing column, 3-level cascade; C:4 absent. Grid stays EMPTY until this cascade is set + GO clicked. |
| Insert (+) | hover insert icon -> "New Object" (standard OV-GM insert gesture) |
| Save | standard `//a[@title='Save [Ctrl+s]' and not(...disabled)]` |
| Delete (End Date) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded id - Start Date is C:1, End Date label sits at C:2, End Date input at C:3; one-field-per-row label scan cannot safely resolve this row, same documented rationale as Area's/Facility Class 1's own del-enddate constant) |

### Navigator values (EXPLICIT since PR #539, `testdata/well_hookup_navigator.properties` - was
first-available before the conversion)
```
Op Production Unit=AS1 EC Exploration Norway
Op Area=AS1_Area
Op Facility Class 1=AS1_Facility_01
```
Captured live via a read-only recon script (`tmp/recon_well_hookup_navigator_cascade.py`,
2026-08-26) against this repo's local sandbox EC - the same values the screen's original
first-available cascade resolution already used successfully (2026-07-30 base build).

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, screen-prefixed)
**Well Hookup Code*** - **Well Hookup Name*** - **Start Date*** (in `objectdates`, not
`objectForm`/`updateAttributes`) - **Op Production Unit*** (dropdown; filled `__FIRST__` - a fill
directive, NOT a comparable screen value, so deliberately excluded from the form-verify label set).
(`*` = mandatory, per the already-proven driver `py/well_hookup_iud.py`.)

Grid columns (confirmed live 2026-08-26, `manageObject:form:T_head` scan): Well Hookup Code / Well
Hookup Name / Start Date / End Date.

### Update (`updateAttributes`) - Code read-only
Only **Well Hookup Name** is updatable per this task's mandatory scope
(`testdata/well_hookup_update.properties`).

### Delete (`objectdates`)
Set End Date = Start Date (true delete for `OV_WELL_HOOKUP`, versioned groupmodel) -> Save. Grid
redraws lazily after delete; the shared T2 `Save And Refresh List` re-applies the navigator before
the removal assertion reads the list.

## Quirks
- **Genuine 3-level navigator cascade** (Production Unit -> Area -> Facility Class 1) - unlike
  Facility Class 1 (2-level, no Op PU/Op Area fields on `objectForm`) or Well Bore (per-field
  `nav:form:G:<n>` groups, NOT the same-row/increasing-column shape) - Well Hookup fits the shared
  T2 `Apply Navigator From Properties` keyword's supported shape directly, confirmed live via DOM
  recon 2026-08-26.
- **Op Production Unit is mandatory on `objectForm` at Insert** (filled first, `__FIRST__`) - this
  is a genuine screen field, unlike some sibling OV-GM screens where the equivalent field is
  optional/out-of-scope. Excluded from `@WH_FORM_LABELS`'s verify list because its inserted value is
  a fill directive, not a comparable static value.
- Screen-prefixed field labels ("Well Hookup Code"/"Well Hookup Name"), not the generic
  "Code"/"Name" Bank/Object List use - every T2 call passes `code_label=Well Hookup Code`.
- Del-end-date field id is hardcoded (not label-driven) - same documented exception as Area's/
  Facility Class 1's own constant, because the date row packs Start Date + End Date together with
  the label sitting between them.
- (Historical, pre-2026-08-26) first-available nav PU was a sparse test scope and not necessarily a
  valid option in every panel - resolved by the conversion's move to EXPLICIT navigator values.

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource` (5-TC
  Area pattern, label-driven, no hardcoded ids except the documented del-enddate exception) + suite
  `tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot`. Test code `AUTOTEST_WH`
  (fixed, confirmed absent from `OV_WELL_HOOKUP` before use each run). Live 5/5 PASS.
- **Legacy Playwright driver** (unchanged, not the current delivery path):
  `py/well_hookup_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`) - the
  Universal Screen Engine supersedes this role going forward per owner decision 2026-08-27; not
  rebuilt or refreshed by this backfill.
- **Bundle:** `ec-automation/screens/Configuration/Assets/Facility_Objects/Well_Hookup/` - SOW,
  README, JOURNAL, evidence, CHECKLIST.md.
