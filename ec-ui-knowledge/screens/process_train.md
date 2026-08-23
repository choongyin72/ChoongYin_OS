# Screen: Process Train

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`)
- **BF_CODE:** CO.0120 - **Treeview:** Configuration > Assets > Facility_Objects > Process Train _(DB treeview JSON)_
- **DB view:** `OV_PROCESS_TRAIN` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-23 - EC 14.2.4 - local sandbox - Batch 9 Bank-pattern conversion, live RF 5/5
- ⚠️ **CORRECTION (2026-08-23):** the earlier "plain (optional dropdowns only, none mandatory)"
  note below is WRONG for actually persisting the record. Live repro: Insert with only Code/
  Name/Start Date clicked Save successfully (button enabled, click succeeded) but the row
  never reached `OV_PROCESS_TRAIN` (0 rows) and left EC's own unsaved-changes confirmation
  modal (`#confirmationForm:confirmation_modal`) open, stalling every later click. Re-running
  the already-proven `py/process_train_iud.py` unmodified (which fills **Production Facility
  Class 1** = `__FIRST__`) passed 7/7 cleanly. So Production Facility Class 1 IS effectively
  required for Save to actually commit, even though it isn't CSS-flagged mandatory - a
  business-rule-level requirement invisible to a static field-inventory scan.

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Process Train` -> `label.tv-link` "Process Train" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Process Train Code*** - **Process Train Name*** - **Start Date*** (date) - **Production Facility
Class 1*** (dropdown, `__FIRST__` proven live) - End Date - other optional dropdowns. (`*`
required to actually persist - see CORRECTION above; Production Facility Class 1 is not
CSS-flagged mandatory but Save silently fails to commit without it.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Process Train Code` (ro) - **`Process Train Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_PROCESS_TRAIN`.

## Automation (code in ec-automation)
- **Playwright:** `py/process_train_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource` -
  rebuilt 2026-08-23 (Batch 9) to the Bank/Berth label-driven, properties-file-driven,
  T2-consolidated, grid-filter-wired pattern (`Find/Clear Process Train Row By Filter`) + suite
  `tests/.../process_train_iud.robot` -> live 5/5 (TC01 clean-state/TC02 insert/TC03 update/
  TC04 find/TC05 delete, fixed code `AUTOTEST_PT`).
- Insert properties (`testdata/process_train_insert.properties`) fill Code/Name/Start Date +
  Production Facility Class 1=`__FIRST__`; that dropdown is deliberately EXCLUDED from the
  round-trip form-label compare list (`__FIRST__` never matches the resolved literal text on
  reload).

## Quirks
- Bank-family OV, but NOT fully "plain": Production Facility Class 1 is a de-facto mandatory
  dropdown for Save to actually commit (see CORRECTION above) despite no CSS mandatory-flag.
  Generic engine handles appear/absent/pagination for the rest.
