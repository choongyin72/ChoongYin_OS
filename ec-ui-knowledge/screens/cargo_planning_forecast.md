# Screen: Cargo Planning Forecast

- **Type:** Gated OV with PER-FIELD navigator groups (date-effective) + GO.
- **BF_CODE:** CP.0030 - **Treeview:** EC_Transport > Cargo_Planning > Forecast > Cargo Planning Forecast
- **DB view:** `OV_FCST_MNGR_FCST_LIST` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Cargo Planning Forecast` -> `label.tv-link` "Cargo Planning Forecast" |
| Navigator (gated) | PER-FIELD groups `nav:form:G:1..G:4:R:1:C:0:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1 -> P1_CRUDE_STOR (SPECIFIC values) -> GO `#button:form:B` |
| Grid | `fcst:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Cargo Planning Forecast Code*** - **Cargo Planning Forecast Name*** - **Start Date*** (date) + **End Date*** (spans the nav date, e.g. 2026-01-01..2026-12-31) + **Storage Name*** = nav Storage. new_fcst panel + COPY buttons = copy-existing dialog, untouched. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Cargo Planning Forecast Code` (ro) - **`Cargo Planning Forecast Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_FCST_MNGR_FCST_LIST`.

## Automation (code in ec-automation)
- **Playwright:** `py/cargo_planning_forecast_iud.py` (shared engine `ec_object_iud.py` + per-field nav helpers).
- **RF:** T3 `pageobjects/EC_Transport/Cargo_Planning/Forecast/cargo_planning_forecast_page.resource` (**label-driven**) + suite `tests/EC_Transport/Cargo_Planning/Forecast/cargo_planning_forecast_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Gated OV with PER-FIELD navigator groups: every nav group is a SEPARATE mandatory field (not one
  cascade widget) - fill them all before GO or the grid stays empty.
- EC Transport layout: per-field nav G-groups (not the single-row cascade); grid fcst:form:T_data; dual views over base FORECAST (FCST_MNGR_FCST_LIST primary, row also in FORECAST_TRAN_CP).

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
