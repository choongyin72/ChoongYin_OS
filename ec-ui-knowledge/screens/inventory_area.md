# Screen: Inventory Area

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CD.0115 - **Treeview:** Configuration > Assets > Inventory_Objects > Inventory Area _(DB treeview JSON)_
- **DB view:** `OV_INVENTORY_AREA` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live RF **5/5 PASS** re-confirmed this
  backfill; underlying Bank-pattern conversion verified 2026-08-23 (PR #460): dryrun 758/758
  (full tree), live RF 5/5, DB self-clean 0 residual (fresh connection, before/after).

## Selectors `[from pageobjects/.../inventory_area_page.resource Variables section, 2026-08-23 rebuild]`
| Purpose | Selector / value |
|---|---|
| Open | search `Inventory Area` -> `label.tv-link` "Inventory Area" |
| Grid id | `${INVENTORY_AREA_TABLE}` = `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`; needs GO to load) |
| Grid filter (Code col) | `Find Inventory Area Row By Filter` -> T2 `Find Object Row By Filter(${INVENTORY_AREA_TABLE}, ${code})`; cleared via `Clear Inventory Area Row Filter` -> T2 `Clear Object Row Filter` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" (T2 `Insert Object From Properties And Verify Code`, driven by `testdata/inventory_area_insert.properties`) |
| Update | T2 `Update Object From Properties`, driven by `testdata/inventory_area_update.properties` |
| Delete field id | `${INVENTORY_AREA_DEL_ENDDATE}` = `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (objectdates tab, End Date) |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Credentials | `${INVENTORY_AREA_EC_USER}` / `${INVENTORY_AREA_EC_PASS}` (own dedicated pair, `resources/credentials.py`) |

### Form labels (T3 resolves BY LABEL, `@{INVENTORY_AREA_FORM_LABELS}`)
**Inventory Area Code*** (mandatory-yellow when empty) - **Inventory Area Name*** (mandatory-yellow
when empty) - **Start Date*** (mandatory-yellow when empty; insert-only, NOT present in
`updateAttributes`) - End Date - optional dropdowns (none mandatory).

### Update (`updateAttributes`) / Delete (`objectdates`)
`Inventory Area Code` (read-only on update; used as the loaded-check via `OV Field Id By Label`) -
**`Inventory Area Name`** (the only field TC03 updates). Delete: **`End Date`** = Start Date ->
row leaves `OV_INVENTORY_AREA` (true delete, no soft-delete flag).

### Test data (fixed code, matches Bank/Berth convention)
`AUTOTEST_INVA` / name `AUTOTEST Inventory Area` -> updated name `AUTOTEST Inventory Area UPDATED`;
Start/End = `2000-01-01`. Every run must complete TC05 (delete) so the fixed code stays reusable -
EC never lets a deleted code be reused mid-run otherwise.

## Automation (code in ec-automation)
- **Playwright:** `py/inventory_area_iud.py` -> 7/7 (update Name). **Unchanged since 2026-07-26** -
  not rebuilt for the Batch 8 RF conversion; the Universal Screen Engine is the owner-decided
  replacement for hand-written Playwright drivers going forward (owner decision 2026-08-27).
- **RF:** T3 `pageobjects/Configuration/Assets/Inventory_Objects/inventory_area_page.resource`
  (**properties-file-driven, explicit grid-filter wiring, NO hardcoded field ids** - rebuilt
  2026-08-23/PR #460 to mirror `berth_page.resource` exactly) + suite `tests/.../inventory_area_iud.robot`
  (5 TCs: Verify Clean State / Insert / Update / Find / Delete, per-TC login/logout) -> live 5/5.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine/T2 handles appear/absent/pagination with zero
  screen-specific tuning.
- Superseded a partial 2026-07-26 build (4-TC, no grid-filter wiring, per-run generated test code,
  shared generic credentials) - if cross-referencing anything dated before 2026-08-23, it describes
  the OLD shape, not the current one.
