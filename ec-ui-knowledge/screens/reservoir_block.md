# Screen: Reservoir Block

- **Type:** OV (EC Object Configuration, date-effective) - **full Bank-pattern** (`manage_object_nav`);
  plain (no mandatory navigator/dropdowns) - upgraded from a partial label-driven build to the full
  Bank/Berth shape in Batch 9 of the Bank-pattern conversion project (PR #466, merged 2026-08-23).
- **BF_CODE:** CO.0133 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block _(DB treeview JSON)_
- **DB view:** `OV_RESV_BLOCK` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Grid id:** `${RESERVOIR_BLOCK_TABLE}` = shared T2 constant `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data`
- **Last verified:** 2026-08-28 (this KB entry refreshed during the deliverable backfill) - EC 14.2.4 -
  local sandbox - dryrun 5/5, LIVE RF 5/5, fresh-connection DB self-clean (0 residual `AUTOTEST%` rows
  in `OV_RESV_BLOCK`), hygiene PASS. RF automation itself was last changed 2026-08-23 (PR #466); not
  modified by this KB refresh.

## Selectors `[from PR #466 / reservoir_block_page.resource Variables section, confirmed live 2026-08-28]`
| Purpose | Selector |
|---|---|
| Open | search `Reservoir Block` -> `label.tv-link` "Reservoir Block" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter (Code column) | `Find Object Row By Filter`/`Clear Object Row By Filter` (shared T2), wrapped by this screen's own `Find Reservoir Block Row By Filter`/`Clear Reservoir Block Row Filter` |
| Delete field id | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, no hardcoded ids)
**Reservoir Block Code*** (mandatory-yellow) - **Reservoir Block Name*** (mandatory-yellow) -
**Start Date*** (mandatory-yellow, date) - End Date - optional dropdowns (skipped, none mandatory).
(`*` = mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Reservoir Block Code` (read-only) - **`Reservoir Block Name`** (only field updated). Delete:
**`End Date`** = Start Date -> row leaves `OV_RESV_BLOCK`.

### Test data (properties-file-driven, not hardcoded)
- `testdata/reservoir_block_insert.properties` - Code/Name/Start Date.
- `testdata/reservoir_block_update.properties` - Name only.
- `testdata/reservoir_block_form_verify.properties` / `reservoir_block_grid_verify.properties` -
  expected post-update state for TC04 Find/Verify.
- Fixed test code: `AUTOTEST_RESVB`.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_page.resource`
  (label-driven, NO hardcoded ids, properties-file-driven, explicit grid-filter wiring) + suite
  `tests/.../reservoir_block_iud.robot` (5 TCs: clean-state/insert/update/find/delete, per-TC
  login/logout with dedicated credentials `RESERVOIR_BLOCK_EC_USER`/`RESERVOIR_BLOCK_EC_PASS`) ->
  live 5/5.
- **Playwright:** `py/reservoir_block_iud.py` - predates the Bank-pattern conversion (built
  2026-07-26, 7/7 live at that time); left unchanged by PR #466 and by this backfill. The Universal
  Screen Engine is the owner-decided replacement for hand-written Playwright drivers going forward
  (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`) - not rebuilt.
- **Gates (2026-08-28 backfill re-run):** robocop exit 1 (9 baseline issues, parity with
  `berth_iud.robot`) - dryrun 5/5 - LIVE RF 5/5 - DB ground-truth + self-clean confirmed via fresh
  `oracledb` connection - hygiene PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Delete uses async-redraw-aware row-absent handling in the shared engine.
- Field labels are screen-prefixed (`Reservoir Block Code`/`Reservoir Block Name`), NOT the generic
  `Code`/`Name` that Bank/Object List use - confirmed via the Playwright driver's `INSERT_FIELDS` and
  the T3's own `@{RESERVOIR_BLOCK_FORM_LABELS}`.
- Sibling screen **Reservoir Block Formation** (CO.0137) is a DIFFERENT, multi-object junction screen
  (`OV_RESV_BLOCK_FORMATION` + parents) with a dependent-dropdown cascade - do not confuse the two;
  see `ec-ui-knowledge/screens/reservoir_block_formation.md` / `reservoir_formation.md` separately.
