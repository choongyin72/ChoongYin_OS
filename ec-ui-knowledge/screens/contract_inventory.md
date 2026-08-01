# Screen: Contract Inventory

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.2054 - **Treeview:** Configuration > Assets > Contract_Objects > Contract Inventory
- **DB view:** `OV_CONTRACT_INVENTORY` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-02 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Contract Inventory` -> `label.tv-link` "Contract Inventory" |
| Navigator | cascade `nav:form:G:0:R:1:C:1..N:dd` (PROVEN explicit values, not first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Inventory Code*** - **Contract Inventory Name*** - **Start Date*** (date) + dropdowns Contract name=TS5 Shipper C. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Inventory Code` (ro) - **`Contract Inventory Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CONTRACT_INVENTORY`.

## Automation (code in ec-automation)
- **Playwright:** `py/contract_inventory_iud.py` (shared engine `ec_object_iud.py` + explicit `select_dropdown` (PROVEN values, not `apply_ovgm_navigator`)).
- **RF:** T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM: nav cascade uses PROVEN explicit values from `scripts/find_populated_scope.py` (not first-available) - the alphabetically/positionally-first option is NOT guaranteed to have data underneath it; see ov-gm-navigator-capability.md.
