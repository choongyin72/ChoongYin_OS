# Screen: Carrier

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain
  (one mandatory reference dropdown, otherwise not gated)
- **Treeview:** Configuration > Assets > Cargo Objects > Carrier
- **DB view:** `OV_CARRIER` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, plus Unit/Carrier Group/
  Carrier Type/Capacity/Dead Weight/Nationality/Rating/Product Group/Speed columns)
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox (Woodside Pluto ECaaS) — live RF 5/5
  PASS, DB self-clean 0 residual (this backfill's re-run); RF layer converted to the Bank pattern
  in PR #477 (Batch 11, merged 2026-08-23).
- **Distinct from:** "Contract Carrier" — a different, unrelated sibling screen. Do not confuse
  file paths (`carrier_page.resource`/`carrier_iud.robot` vs. `contract_carrier_*`).

## Selectors `[from carrier_page.resource Variables section, fresh confirm 2026-08-28]`
| Purpose | Selector / value |
|---|---|
| Open | Open EC Screen `Carrier` (T1 `common.resource`), treeview title = "Carrier" |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` (shared T2 constant = `manage_object_nav_nav:form:T_data`) — Bank-family, first column = Carrier Code |
| Navigator | one optional date field + GO — NOT gated (no mandatory dropdown/cascade); grid loads on open |
| Grid-filter keywords | `Find Carrier Row By Filter` / `Clear Carrier Row Filter` (wrap shared T2 `Find/Clear Object Row By Filter`) |
| Delete field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (`${CARRIER_DEL_ENDDATE}`) — End Date, set = Start Date |
| Login | `Login To EC Application` → `Login To EC Screen ${CARRIER_EC_USER} ${CARRIER_EC_PASS}` (own dedicated creds in `resources/credentials.py`) |

## Insert / Update / Verify (properties-file-driven, T2-consolidated)
- **Insert** — `testdata/carrier_insert.properties`, via T2 `Insert Object From Properties And
  Verify Code` (`code_label=Carrier Code`):
  - **Carrier Code** — mandatory
  - **Carrier Name** — mandatory
  - **Start Date** — mandatory (Insert-only; not present in `updateAttributes`)
  - **Unit** — mandatory reference dropdown, filled `__FIRST__` (throwaway value)
  - Carrier Group / Carrier Type / End Date / Capacity Volume/Mass / Dead Weight / Nationality /
    Rating / Product Group / Speed / etc. — optional, not filled
- **Update** — `testdata/carrier_update.properties`, via T2 `Update Object From Properties`:
  only **Carrier Name** (Code is read-only in `updateAttributes`; Start Date lives only in
  `objectdates`).
- **Verify** — `@{CARRIER_FORM_LABELS}` = `Carrier Code`, `Carrier Name` ONLY. **Unit is
  deliberately EXCLUDED** from this list — a mandatory dropdown filled `__FIRST__` fails
  round-trip verify if included (Batch 2 VAT Code gotcha). `testdata/carrier_form_verify.properties`
  and `testdata/carrier_grid_verify.properties` hold the expected post-update state for TC04.
- **Find** — T2 `Find Object Record` (`code_label=Carrier Code`).
- **Delete** — T2 `Delete Object Via End Date` on `${CARRIER_DEL_ENDDATE}`, End Date = Start Date
  (true delete from `OV_CARRIER`, not a soft-close).

## Mandatory-yellow fields (Insert form)
Carrier Code · Carrier Name · Start Date · Unit (reference dropdown). All others optional.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource` (label-driven,
  properties-file-driven, T2-consolidated — mirrors Bank/Berth/Port) + suite
  `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` (5 TCs, per-TC login/logout, fixed
  test code `AUTOTEST_CARRIER`) → live 5/5.
- **Playwright:** `screens/Configuration/Assets/Cargo_Objects/Carrier/playwright/ec_iud_carrier.py`
  — pre-existing (2026-06-19), UNCHANGED by the Bank-pattern conversion; not rebuilt going forward
  (Universal Screen Engine is the owner-decided replacement, Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).

## Quirks
- **`Unit` mandatory-dropdown-excluded-from-verify pattern.** Same gotcha as Batch 2's VAT Code:
  a mandatory reference dropdown filled `__FIRST__` at Insert must be excluded from the
  form-label verify list, or the round-trip compare fails (the DOM shows the resolved dropdown
  text, not the literal `__FIRST__` sentinel).
- **Fixed test code, not generated-unique.** `AUTOTEST_CARRIER` is reused every run (post-PR #477
  convention, matching Bank/Berth/Port) — every run MUST complete TC05 (delete) or the code stays
  "used" and blocks the next run (EC never lets a deleted code be reused, but only if delete
  actually ran).
- **Plain OV, no OV-GM lazy-redraw risk.** Navigator has no mandatory dropdown, so the grid loads
  immediately on open — none of the paginated-grid or gated-navigator gotchas that apply to
  screens like Port apply here.
- **Do not confuse with "Contract Carrier".** Different screen, different file paths, different
  class. Grep for `carrier_page.resource` and exclude anything matching `contract_carrier` to stay
  on the right file.
