# Screen: Division Order

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** RC.0058 - **Treeview:** EC Revenue > Royalty > Royalty USA > Division Order
- **DB view:** `OV_DIVISION_ORDER` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, `CONTRACT_AREA_CODE`)
- **Last verified:** 2026-08-02 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Division Order` -> `label.tv-link` "Division Order" |
| Navigator | Date `nav:form:G:0:R:1:C:0:da_input` (NOT mandatory) + Business Unit `nav:form:G:1:R:1:C:0:dd` (MANDATORY, own group, not C:1 inside G:0) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until Business Unit + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Division Order Code*** - **Division Order Name*** - Description - Comments - **Start Date***
(not flagged mandatory but functionally required) - **End Date** (NOT flagged yellow, but Save
REJECTS without it - value `2099-12-31` used) - Contract Template - Trade Alias Name - Contract Area
(must match nav Business Unit scope) - Project - Calculation Approval Check - Pricing/Booking
Currency - UOM 1-4 Template - Revenue Accountant (+ Name/Phone/E-mail) - Business Contact - Contract
Stage Code - Processable Code. (`*` mandatory per live yellow-highlight scan.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Division Order Code` (ro) - **`Division Order Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_DIVISION_ORDER`.

## Automation (code in ec-automation)
- **Playwright:** `py/division_order_iud.py` (shared engine `ec_object_iud.py` + explicit `select_dropdown` - PROVEN value, not `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/EC_Revenue/Royalty/Royalty_USA/division_order_page.resource` (**label-driven**) + suite `tests/EC_Revenue/Royalty/Royalty_USA/division_order_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- **This screen's LABEL is ambiguous in `class_property_cnfg`** - matches 3 classes (`BEARER`,
  `DIVISION_ORDER`, `DIVISION_ORDER_SHARE`). The real class for this BF code (RC.0058) is
  `DIVISION_ORDER` (`OBJECT`/`VERSIONED`, base=`CONTRACT` - the SAME base table as Royalty Contract).
  A prior investigation checked only the first alphabetically-listed class and wrongly concluded
  "genuinely TV, needs a different generator" - always check ALL candidate classes returned for an
  ambiguous label before concluding a screen needs different tooling.
- Same navigator-group-split gap as Property/Royalty Contract: Date and the mandatory Business Unit
  dropdown are in SEPARATE navigator groups (`G:0`/`G:1`), not one shared group.
- Same "End Date functionally mandatory despite not flagged yellow" quirk as Royalty Contract/Contract.
- Real populated scope: Business Unit "Royalty USA" (`ROYALTY_US`) -> Contract Area "Louisiana North"
  (`US_LOUISIANA_NORTH`), both effective `2003-01-01`.
