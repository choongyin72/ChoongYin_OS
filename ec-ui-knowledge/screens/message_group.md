# Screen: Message Group

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0236 - **Treeview:** Configuration > Messaging > Message Group
- **DB view:** `OV_MESSAGE_GROUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, `FUNCTIONAL_AREA_CODE`)
- **Last verified:** 2026-08-02 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Message Group` -> `label.tv-link` "Message Group" |
| Navigator | Date + Functional Area dropdown, SAME group `nav:form:G:0:R:1:C:1:dd` (MANDATORY) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until Functional Area + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Message Group Code*** - **Start Date*** (date) - End Date - **Name*** - **Functional Area***
(reference dropdown, `parent_dd` - must equal nav scope). (`*` mandatory per live scan.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Message Group Code` (ro) - **`Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_MESSAGE_GROUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/message_group_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator` first-available).
- **RF:** T3 `pageobjects/Configuration/Messaging/message_group_page.resource` (**label-driven**) + suite `tests/Configuration/Messaging/message_group_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- **Same reference-dropdown date trap as Property/Price Index/Royalty Contract** (see
  `ec-ui-knowledge/screens/property.md`): the Functional Area dropdown only offers Functional Areas
  already effective as of the record's own Start Date. "Administration" (`ADM`) is only valid from
  `2001-01-01` onward - with the plain default `2000-01-01`, it wasn't in the option list and the
  code fell back to "Allocation" (effective since 1900) instead. Fix: use Start Date `>= 2003-01-01`
  for ANY screen with a reference dropdown. See memory `feedback_child_object_date_must_follow_parent`.
- This screen uses the `parent_dd` binding mechanism (form field must equal the navigator's captured
  top-parent), not `extra_dropdowns` - confirms the date trap applies to both mechanisms equally.
