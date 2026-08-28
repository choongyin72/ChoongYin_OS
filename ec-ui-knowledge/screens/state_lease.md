# Screen: State Lease

- **Type:** OV (EC Object Configuration, date-effective), Manage Object — plain, no mandatory
  navigator/cascade dropdown (confirmed live 2026-08-23: only the universal as-at-date + GO bar).
- **Treeview path:** Configuration > Assets > Commercial Objects > State Lease
- **DB view (ground truth):** `OV_STATE_LEASE` (key `CODE`; also `NAME`, `DESCRIPTION`,
  `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 · EC **14.2.4** · local sandbox · live RF 5/5 PASS, DB self-clean
  confirmed via fresh connection
- **Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated) — converted via
  PR #440, merged 2026-08-23 (Batch 4)

## Selectors `[from state_lease_page.resource Variables section]`

| Purpose | Selector / value |
|---|---|
| Grid id | `manage_object_nav_nav:form:T_data` (shared `${OV_MANAGE_OBJECT_TABLE}` T2 constant) |
| Code label | `State Lease Code` (screen-prefixed, NOT generic "Code" — same precedent as "State Code") |
| Delete (End Date) field id | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded — row packs Start Date C:1 / End Date label C:2 / End Date input C:3, same documented shape as Bank/Customer's DEL_ENDDATE) |
| Form label set (insert/find verify) | `State Lease Code`, `State Lease Name`, `Description` (`@{STATE_LEASE_FORM_LABELS}`) |
| Update label set | `State Lease Name`, `Description` only |

Insert/Update/Find/Delete/grid-filter mechanics are NOT re-implemented per screen — this T3 is a
thin wrapper delegating to the shared T2 `resources/manage_object.resource` keywords
(`Insert Object From Properties And Verify Code`, `Update Object From Properties`,
`Verify Object Form Record`, `Verify Object Found`, `Delete Object Via End Date`,
`Find/Clear Object Row Filter`) plus T1 `resources/common.resource` for login/navigate/logout.

## Mandatory-yellow fields `[from PR #440 body / state_lease_sow.md]`
- `objectForm` (Insert): **State Lease Code\***, **State Lease Name\***, **Start Date\*** (yellow,
  mandatory) — Description and End Date present but optional.
- `updateAttributes` (Update): only State Lease Code (read-only), State Lease Name, Description —
  Start Date and End Date are NOT present in updateAttributes at all (they live only in
  `objectForm` and `objectdates`), so they cannot be verified via `Verify Object Form Record`
  (which always reads updateAttributes).
- No mandatory reference dropdowns on this screen — no `__FIRST__`/literal-value resolution needed.

## Quirks
- Screen-prefixed labels ("State Lease Code"/"State Lease Name") rather than Bank/Customer's
  generic "Code"/"Name" — confirmed via a live field-inventory scan 2026-08-23, matching the
  existing "State Code" precedent already documented in `manage_object.resource`.
- Delete field id is deliberately hardcoded (not label-resolved) — same documented shape as
  Bank's/Customer's own `DEL_ENDDATE`; confirmed round-tripping a live insert+delete during recon.
- Test code is fixed (`AUTOTEST_STL`), not timestamp-suffixed — every run must complete TC05
  (delete) so the code is free for the next run; EC never lets a deleted code be reused.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (current, maintained):** T3
  `ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/state_lease_page.resource` +
  suite `ec-automation/tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot`
  (T2 `manage_object.resource` + T1 `common.resource` + `libraries/DbVerify.py` +
  `libraries/PropertiesReader.py`). Validated live 5/5 (PR #440, 2026-08-23; re-confirmed 5/5 in
  this backfill, 2026-08-28).
  Run: `EC_HEADLESS=true robot tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot`
- **Playwright (historical only, NOT maintained):**
  `ec-automation/screens/Configuration/Assets/Commercial_Objects/State_Lease/playwright/ec_iud_state_lease.py`
  — built 2026-06-12, predates the Bank-pattern conversion. Per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, no new Playwright driver is built for Bank-pattern
  screens going forward (Universal Screen Engine replaces that role).
- Full bundle (SOW/README/JOURNAL/CHECKLIST/evidence):
  `ec-automation/screens/Configuration/Assets/Commercial_Objects/State_Lease/`
