# Screen: Property

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** SP.0059 - **Treeview:** Configuration > Assets > Data Mapping Objects > Property
- **DB view:** `OV_PROPERTY` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, `BUSINESS_UNIT_CODE`)
- **Last verified:** 2026-08-02 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Property` -> `label.tv-link` "Property" |
| Navigator | Date `nav:form:G:0:R:1:C:0:da_input` (NOT mandatory) + Business Unit `nav:form:G:1:R:1:C:0:dd` (MANDATORY, own group, not C:1 inside G:0) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until Business Unit + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Property Code*** - **Property Name*** - **Start Date*** (date) - End Date - Comments -
**Business Unit Name** (reference dropdown, must equal nav scope) - Use as Property (checkbox).
(`*` mandatory per live scan; Business Unit Name is not flagged yellow but MUST be set to match the
navigator's Business Unit or the row won't list correctly under that scope.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Property Code` (ro) - **`Property Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_PROPERTY`
(raw SQL UPDATE is REJECTED - `ORA-20299: ... PROPERTY class is a read-only class`; cleanup MUST go
through the live UI's own End=Start gesture, same as `OV_ROYALTY_CONTRACT`).

## Automation (code in ec-automation)
- **Playwright:** `py/property_iud.py` (shared engine `ec_object_iud.py` + explicit `select_dropdown` - PROVEN value, not `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- **Reference-dropdown date trap (the real root cause of the earlier park + a false "shared-engine
  bug" chase):** the Business Unit Name dropdown only offers Business Units already effective as of
  the record's own Start Date. "Royalty Canada" (`ROYALTY_CA`) is only valid from `2003-01-01` onward.
  Using the plain default test date (`2000-01-01`) causes one of two failures depending on approach:
  leaving the field's navigator-inherited label untouched -> Save rejects with "Object not found";
  explicitly re-selecting it -> the dropdown panel silently only offers Business Units that ARE valid
  at that date (e.g. SS1 BU/SS2 BU/TS5 BU), and the code falls back to the first one instead of the
  requested-but-absent option. **Fix: use Start Date >= 2003-01-01** (this project's
  `EC_TEST_START_DATE_REFDD` constant in `resources/environment.py`) for ANY screen with a reference
  dropdown, not just the plain `TEST_START_DATE` (2000-01-01). See memory
  `feedback_child_object_date_must_follow_parent`.
- Navigator layout gotcha: Date and Business Unit are in TWO SEPARATE navigator groups (`G:0` and
  `G:1`), not one group with Date at C:0 and the dropdown at C:1. `tmp/gen_ovgm.py`'s default
  single-level nav-dropdown id template assumes the latter and needs manual correction on screens
  shaped like this one.
