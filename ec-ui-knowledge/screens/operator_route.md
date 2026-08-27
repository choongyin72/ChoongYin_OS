# Screen: Operator Route

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
  Converted to the **Area-pattern** RF structure 2026-08-26 (PR #533) - remains OV-GM, its genuine
  2-level Production Unit -> Area cascade is unchanged; this was a structural RF conversion only.
- **BF_CODE:** CO.0244 - **Treeview:** Configuration > Assets > Facility_Objects > Operator Route
- **DB view:** `OV_OPERATOR_ROUTE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox (`localhost:1521/ORCL`) - live RF
  5/5 pass (fresh headless re-run in an isolated worktree, `docs/lean-deliverable-backfill-
  workorder.md` backfill session). Base-build gate (`verify_screen.py` OVERALL PASS, RF 4/4 +
  Playwright 8/8) was 2026-08-01, before the RF suite grew to 5 TCs.

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Operator Route` -> `label.tv-link` "Operator Route" |
| Navigator | genuine mandatory 2-level SAME-ROW cascade `nav:form:G:0:R:1:C:1:dd` (Production Unit) then `nav:form:G:0:R:1:C:2:dd` (Area) -> GO `#button:form:B`. PROVEN explicit values `P3 Production Unit` / `P3 Area` (not first-available - `scripts/find_populated_scope.py` confirmed the first-available option is not guaranteed to have data underneath it). RF fill delegates to the shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/operator_route_navigator.properties`. |
| Grid | `manageObject:form:T_data` (empty until cascade + GO). RF filters explicitly on the Code column via the shared T2 `Find/Clear Object Row Filter`, wired into Update/Find/Verify-Found/Delete (`Find/Clear Operator Route Row By Filter` wrapper) - 15 `Find Object Row By Filter` hits confirmed live in `output.xml`. |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded deliberately, not label-driven - the row packs Start Date C:1 + End Date C:3 with the label at C:2, same documented rationale as Area's/Bank's/Facility Class 1's own del-enddate constant) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Operator Route Code*** - **Operator Route Name*** - **Start Date*** (date). (`*` mandatory,
yellow when empty)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Operator Route Code` (read-only after creation) - **`Operator Route Name`** (editable). Delete:
**`End Date`** = Start Date -> object fully removed from `OV_OPERATOR_ROUTE` (true delete,
DB-verified).

## Automation (code in ec-automation)
- **Playwright:** `py/operator_route_iud.py` (shared engine `ec_object_iud.py` + explicit
  `select_dropdown` with PROVEN values, not `apply_ovgm_navigator`). Frozen at its 2026-08-01
  state - not kept in sync with the RF conversion; the Universal Screen Engine is the owner-decided
  replacement for hand-written Playwright drivers going forward (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- **RF (current, post-conversion, 5 TCs):** T3
  `pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource`
  (properties-driven, **label-driven**, no hardcoded ids except the documented del-enddate
  constant) + suite `tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot`
  (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete - per-TC
  Login/Logout, pure-screen verification only, zero inline DB-verify calls in the `.robot` file).
  Fixed test code `AUTOTEST_OR` (was a generated `AUTOTEST_OR_<timestamp>` pre-conversion).
  `testdata/operator_route_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Gate:** base build `verify_screen.py` -> OVERALL PASS (2026-08-01, 4-TC gates). Post-conversion
  gates re-run manually 2026-08-27: dryrun 5/5, full-tree dryrun 883/883 (0 collisions), live
  headless 5/5, robocop 7 issues (5x DOC02 + 2x VAR02, parity with Area's reference files), hygiene
  PASS, DB self-clean 0/0 (fresh oracledb connection before/after).

## Quirks
- OV-GM: nav cascade uses PROVEN explicit values from `scripts/find_populated_scope.py` (not
  first-available) - the alphabetically/positionally-first option is NOT guaranteed to have data
  underneath it; see ov-gm-navigator-capability.md.
- The RF suite and the Playwright driver are DELIBERATELY out of sync post-2026-08-26: RF moved to
  5 TCs / fixed code / explicit filter wiring; Playwright stays on the 2026-08-01 8-step/generated-
  code shape. This is an accepted, owner-approved split (Section H waiver), not a documentation gap.
