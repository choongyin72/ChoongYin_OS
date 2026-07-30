# Screen: Lifting Account

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.2004 - **Treeview:** Configuration > Assets > Transport_Objects > Lifting Account
- **DB view:** `OV_LIFTING_ACCOUNT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Lifting Account` -> `label.tv-link` "Lifting Account" |
| Navigator (gated, 4-LEVEL) | cascade `nav:form:G:0:R:1:C:1..3:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1, PLUS Storage on 2ND ROW `nav:form:G:0:R:3:C:0:dd` = P1_CRUDE_STOR (SPECIFIC values - Storage level EMPTY under first-available AS1) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Lifting Account Code*** - **Lifting Account Name*** - **Start Date*** (date, 2020-01-01) + **Company Name*** (first-available) + **Storage Name*** = nav Storage P1_CRUDE_STOR (parent-matching - row never lists otherwise). NO Op Production Unit field. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Lifting Account Code` (ro) - **`Lifting Account Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_LIFTING_ACCOUNT`.

## Automation (code in ec-automation)
- **Playwright:** `py/lifting_account_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/lifting_account_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Transport_Objects/lifting_account_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  navigator needs SPECIFIC P1 values (Storage 2nd-row level empty under first-available AS1 - the original park reason); form Storage Name must equal nav Storage.
