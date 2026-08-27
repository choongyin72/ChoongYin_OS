# Screen: Well

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0049 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well
- **DB view:** `OV_WELL` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 (this backfill's live re-run) - EC 14.2.4 - local sandbox
  (`localhost:1521/ORCL`, `ECKERNEL_EC`). Base build verified 2026-07-30 (`verify_screen.py`
  OVERALL PASS, RF 4/4 + Playwright 8/8); RF suite converted to the Area-pattern 5-TC structure by
  PR #540 (2026-08-26), re-confirmed live 5/5 by this backfill without any automation changes.

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Well` -> `label.tv-link` "Well" |
| Navigator (gated) | cascade `nav:form:C:1` (Production Unit) / `C:2` (Area) / `C:3` (Facility Class 1), same-row - SPECIFIC values `P1 Production Unit` -> `P1 Area` -> `P1 Facility 1` (AS1 first-available leaves a deeper level empty) -> GO `go_button:form:B`; 2nd-row Well & Well Hookup / Well dds = optional filters, leave EMPTY |
| Grid | `manageObject:form:T_data` (empty until cascade + GO); grid-filter via `Find Well Row By Filter` / `Clear Well Row Filter` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `go_button:form:B` |
| Delete End Date cell | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - documented rationale, same as Area/Bank) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Well Code*** - **Well Name*** - **Start Date*** (date) + **Well Type*** (first-available, via
`__FIRST__` sentinel). NO Op Production Unit field. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Well Code` (ro) - **`Well Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_WELL`.

## Navigator fill mechanism (RF)
`Open Well Screen With Navigator Values Populated` (T3, `well_page.resource`) calls `Open EC
Screen` then the SHARED T2 `Apply Navigator From Properties` (`resources/manage_object.resource`),
driven by `testdata/well_navigator.properties`. This replaced the screen's own earlier bespoke
`Apply Well Navigator` T3 keyword (base build, on T1 `Select EC Dropdown Option` + `Apply
Navigator`) during the Area-pattern conversion (PR #540, 2026-08-26) - no changes were made to
`resources/manage_object.resource` by PR #540 itself; Well's cascade was already documented there
as a proven same-row 3-level case.

**Regression-canary history:** before PR #540 touched Well's own navigator logic, Well - still on
its OLD bespoke keyword, UNCHANGED - was one of 2 screens (with Test Separator) re-run live to
prove the shared `Apply Navigator From Properties` keyword's addition (made for the Area
conversion) caused zero regression to screens not yet migrated onto it (source:
`docs/automation-scorecard.md`'s Area/CO.0003 row).

## Automation (code in ec-automation)
- **Playwright:** `py/well_iud.py` (shared engine `ec_object_iud.py` + screen-local
  `apply_well_navigator`) - unchanged by PR #540 (RF-only structural conversion).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_page.resource`
  (**label-driven**, navigator via shared T2) + suite
  `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_iud.robot` (5 TCs: Verify Clean
  State / Insert / Update / Find / Delete; per-TC login/logout; fixed test code `AUTOTEST_WELL`;
  zero inline DB-verify calls - DB check lives in shared T2 `Verify Object Removed`).
- **Gate history:** base build `verify_screen.py` -> OVERALL PASS (2026-07-30); PR #540's own
  re-run -> live 5/5, full-tree dryrun 850/850, robocop 7 issues (parity w/ Area's baseline), DB
  self-clean 0 residual; this backfill's 2026-08-27 re-run -> live 5/5, dryrun 5/5, full-tree
  dryrun 883/883, hygiene PASS, robocop 7 issues (unchanged), DB self-clean 0 residual.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. Navigator needs SPECIFIC P1 values - the
  first-available AS1 scope leaves a deeper nav level empty (the original park reason, see
  OV_SWEEP_PARKED). 2nd-row Well filter dds are optional - leave empty. No form parent field needed
  (rows list under the nav scope without an Op Production Unit field, like Facility Class 1).
- Well Type (mandatory first-available dropdown) and Start Date/End Date are deliberately excluded
  from the round-trip form-label comparison (`WELL_FORM_LABELS` = Well Code, Well Name only) -
  first-available dropdowns can re-render different display text after reload, and Start/End Date
  live only in `objectdates`, not the `objectForm`/`updateAttributes` fill-once trio.
- Well's bespoke navigator-keyword NAMING precedent (`Apply Well Navigator`, pre-PR-#540) was later
  reused, in name shape only, for Well Bore's own bespoke per-field-group keyword
  (`Apply Well Bore Navigator From Properties`) once that sibling screen's DOM turned out NOT to
  fit the shared same-row-cascade keyword Well itself now uses.
