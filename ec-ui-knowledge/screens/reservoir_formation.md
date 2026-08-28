# Screen: Reservoir Formation

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain
  (optional dropdowns only, none mandatory) - **full Bank-pattern conversion (Batch 9, PR #467, merged
  2026-08-23)**
- **BF_CODE:** CO.0135 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Reservoir
  Formation _(DB treeview JSON)_
- **DB view:** `OV_RESV_FORMATION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live RF 5/5 (TC01-05), dryrun 5/5
  (screen-scoped), fresh-connection DB self-clean 0 residual `AUTOTEST_RESVF` rows, hygiene PASS
  (backfill re-run of the Batch 9 build; automation itself unchanged since 2026-08-23)

## Selectors `[from screens/x.md, refreshed 2026-08-28 against PR #467's build]`
| Purpose | Selector |
|---|---|
| Open | search `Reservoir Formation` -> `label.tv-link` "Reservoir Formation" |
| Grid | `manage_object_nav_nav:form:T_data` (T3 constant `${RESERVOIR_FORMATION_TABLE}`; needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter (Batch 9) | `Find Reservoir Formation Row By Filter <code>` / `Clear Reservoir Formation Row Filter` -> shared T2 `Find/Clear Object Row By Filter` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, properties-file-driven since Batch 9)
**Reservoir Formation Code*** - **Reservoir Formation Name*** - **Start Date*** (date) - End Date -
optional dropdowns (skipped, none mandatory). (`*` mandatory-and-empty on a pristine Insert row)
Insert data source: `testdata/reservoir_formation_insert.properties`.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Reservoir Formation Code` (read-only) - **`Reservoir Formation Name`** (only field in
`testdata/reservoir_formation_update.properties`). Delete: **`End Date`** = Start Date -> leaves
`OV_RESV_FORMATION`.

## Test code / credentials
- Fixed test code `AUTOTEST_RESVF` (Batch 9 changed this from a timestamp-suffixed unique code) -
  confirmed free via a fresh oracledb connection before each verified run.
- Dedicated credentials: `RESERVOIR_FORMATION_EC_USER`/`RESERVOIR_FORMATION_EC_PASS`
  (`resources/credentials.py`, falls back to `EC_USER`/`EC_PASS` then `sysadmin`/`sysadmin`).

## Automation (code in ec-automation)
- **Playwright:** `py/reservoir_formation_iud.py` -> last verified 7/7 (2026-07-26). **Unchanged since**
  - permanently waived from further Playwright-bundle work per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H (superseded by the Universal Screen Engine).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_page.resource`
  (properties-file-driven, explicit grid-filter wiring, NO hardcoded field ids) + suite
  `tests/.../reservoir_formation_iud.robot` (TC01-05: clean-state/insert/update/find/delete) -> live 5/5.
- **Gate (this backfill):** dryrun 5/5, live 5/5, robocop 11 issues (VAR02/DOC02 style, same class as
  Berth's own exemplar, no new-pattern delta), hygiene PASS, DB self-clean 0 residual (fresh connection).

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
- Grid filter (`Find/Clear Reservoir Formation Row By Filter`) is used explicitly before/after
  Update/Find/Verify-Found/Delete (Batch 9 standardization, matching Account/Bank/Berth/State), rather
  than relying only on the implicit 3s-timeout fallback in `Select Object Row`.
- Fixed AUTOTEST code only stays reusable across runs if TC05 (delete) actually completes each time -
  EC never lets a deleted code be reused if the delete didn't run.
