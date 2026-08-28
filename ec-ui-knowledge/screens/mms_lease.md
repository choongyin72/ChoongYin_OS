# Screen: MMS Lease

- **Type:** OV (EC Object Configuration / Manage Object, date-effective)
- **Treeview path:** Configuration > Assets > Commercial Objects > MMS Lease
- **Open via:** menu search / treeview
- **DB view (ground truth):** `OV_MMS_LEASE` (key `CODE`; also `NAME`, `DESCRIPTION`, `OPERATOR`, `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 · EC **14.2.4** · local sandbox · dryrun 5/5 + live RF 5/5, DB-verified (re-run of PR #437's suite, merged 2026-08-23)
- **Pattern:** Bank pattern (`ec-bank-pattern-converter`) — plain manage-object OV, **no mandatory navigator scope**

## Selectors `[from pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource Variables section]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`) |
| Navigator | none mandatory — `manage_object_nav` GO button count = 0, confirmed live 2026-08-23 |
| Row filter | `Find Object Row By Filter` / `Clear Object Row Filter` (T2 `resources/manage_object.resource`), wrapped as `Find MMS Lease Row By Filter` / `Clear MMS Lease Row Filter` |
| Delete (End Date input) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |
| Login credentials | `MMS_LEASE_EC_USER` / `MMS_LEASE_EC_PASS` (own dedicated pair in `resources/credentials.py`) |

## Form fields (labels are SCREEN-PREFIXED, not generic "Code"/"Name")

### Insert (`objectForm`) — 6 ECCell labels
`MMS Lease Code`* , `MMS Lease Name`* , `Description`, `Start Date`* (date), `End Date` (date), `Operator`.
(`*` = mandatory, `MandatoryCellStyle`-confirmed — 3 mandatory total: Code/Name/Start Date.)

### Update (`updateAttributes`) — 4 ECCell labels
`MMS Lease Code` (read-only guard), `MMS Lease Name`* , `Description`, `Operator`.
(2 mandatory: Code/Name. No Start/End Date here — same as Bank/State/Country.)

### Grid columns
MMS Lease Code / MMS Lease Name / Start Date / End Date (4 columns).

## Mandatory-yellow fields (Insert)
MMS Lease Code, MMS Lease Name, Start Date.

## Test data (fixed code convention)
`AUTOTEST_MMS_LEASE` / `AUTOTEST MMS Lease` → `AUTOTEST MMS Lease UPDATED` / Start=End `2000-01-01`.
Description/Operator confirmed optional and omitted (IUD-fill-only-needed-fields convention).

## Quirks
- Field labels are screen-prefixed ("MMS Lease Code"/"MMS Lease Name"), unlike sibling
  Field Group which uses the generic "Code"/"Name" — do not assume the sibling's label
  convention carries over; confirm live per screen.
- No mandatory navigator dropdown/date before the grid loads (`manage_object_nav` GO count
  = 0) — plain manage-object OV, same navigator-free shape as Bank.
- objectdates row layout (Start Date C:1, End Date label C:2, End Date input C:3) matches
  Bank/State/Country's already-proven, framework-invariant pattern.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (primary, maintained):** T3
  `ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot`
  (T2 `manage_object.resource` + `DbVerify.py`). Rebuilt to the Bank pattern in PR #437
  (merged 2026-08-23). Validated live 5/5 (re-confirmed 2026-08-28).
  Run: `EC_HEADLESS=true robot tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot`
- **Playwright (legacy, waived, kept for reference only):**
  `ec-automation/screens/Configuration/Assets/Commercial_Objects/MMS_Lease/playwright/ec_iud_mms_lease.py`
  — predates the Bank-pattern conversion (built 2026-06-12); superseded by the Universal
  Screen Engine per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`. Not maintained.
