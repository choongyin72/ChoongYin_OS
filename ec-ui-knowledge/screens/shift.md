# Screen: Shift

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0224 - **Treeview:** Configuration > Assets > Facility_Objects > Shift
- **DB view:** `OV_SHIFT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Shift` -> `label.tv-link` "Shift" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..3:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1 (SPECIFIC values) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Shift Code*** - **Shift Name*** - **Start Date*** (date) + **Start Time (HH:MI)*** FREE TEXT ('07:00' - format from the existing P1 S001 row) + Op Production Unit = nav PU. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Shift Code` (ro) - **`Shift Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_SHIFT`.

## Automation (code in ec-automation)
- **Playwright:** `py/shift_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/shift_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Facility_Objects/shift_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  mandatory free-text Start Time (HH:MI) - generator-unfillable field class, hand-built; field formats read from the existing P1 S001 row (scan-existing-row technique).
