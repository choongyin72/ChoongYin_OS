# Screen: Operator Lease

- **Type:** OV (EC Object Configuration, date-effective) — manage-object, **plain, no navigator**.
- **Treeview:** Configuration > Assets > Commercial Objects > Operator Lease
- **DB view:** `OV_OPERATOR_LEASE` (generic `CODE` column per `libraries/DbVerify.py`; also
  `NAME`, `DESCRIPTION`, `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 — EC 14.2.4 — local sandbox — RF dryrun 5/5 PASS + full-tree
  dryrun 883/883 PASS + live headless 5/5 PASS (TC01-TC05, first attempt, no retry needed),
  fresh-connection DB self-clean 0 residual before+after, `check_bundle_hygiene.py` PASS (backfill
  re-run of PR #436's Bank-pattern conversion, merged 2026-08-23)

## Selectors

| Purpose | Selector |
|---|---|
| Open | search `Operator Lease` -> `label.tv-link` "Operator Lease" |
| Grid | `manage_object_nav_nav:form:T_data` (reused via T2's `${OV_MANAGE_OBJECT_TABLE}` constant, not re-hardcoded per screen) |
| Nav-free confirmation | grid loads without any navigator dropdown; the top "Date" field + GO button is the same universal as-at-date filter Bank also has — pre-filled, auto-queries on page load, confirmed NOT a mandatory nav requirement via a direct side-by-side screenshot compare against the live Bank screen |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` — matching Bank/State/Country/Account's already-proven row layout (Start Date `C:1`, End Date label `C:2`, End Date input `C:3`), not independently re-verified per the batch's ground rules |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL)
Field labels are **screen-prefixed**: **Operator Lease Code***, **Operator Lease Name***,
**Start Date*** (mandatory, `MandatoryCellStyle`), plus Description and End Date (optional). 7
`ECCell` labels total. NOT the generic "Code"/"Name" Bank/Object List use — same screen-prefixed
convention as Country/State/Licence. (`*` = mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Operator Lease Code` (read-only guard) — **`Operator Lease Name`*** (mandatory) — Description
(optional). 3 `ECCell` labels total; no Start/End Date present here (lives only in `objectdates`).
Delete: **`End Date`** = Start Date (zero-length window) -> true delete, row leaves
`OV_OPERATOR_LEASE`.

### Grid columns (confirmed live)
Operator Lease Code / Operator Lease Name / Start Date / End Date.

## Recon gotcha (2026-08-23, PR #436)
The grid held **0 real Operator Lease rows** in this sandbox at conversion time, so
`updateAttributes` labels could not be read off an existing row (the normal recon method). Resolved
via a live throwaway Insert+Delete round-trip (`RECON_OL_TMP`), self-cleaned and DB re-verified
empty afterward — not assumed from a similar-looking screen's field set.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource`
  (label-driven, 2026-08-23 Bank-pattern conversion, PR #436) + suite
  `tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code
  `AUTOTEST_OPERATOR_LEASE`).
- **Playwright (historical reference only, NOT maintained):**
  `playwright/ec_iud_operator_lease.py` inside this screen's bundle — original 2026-06-12 build
  over the shared `ec_object_iud.py` engine, preserved unchanged; no new Playwright bundle is
  built for Bank-pattern work (owner decision 2026-08-27, Universal Screen Engine replaces this
  role).
- **Test data:** `testdata/operator_lease_{insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `OPERATOR_LEASE_EC_USER`/`OPERATOR_LEASE_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- Plain manage-object OV, genuinely nav-free — do not confuse the pre-filled Date+GO bar with a
  mandatory navigator; that pattern is shared with Bank and every other plain-OV screen in this
  batch series.
- Field labels are screen-prefixed ("Operator Lease Code"/"Operator Lease Name"), unlike Bank's
  generic "Code"/"Name" — check the live label set before assuming either convention for a new
  screen.
- Grid can be genuinely empty of real rows in this sandbox; don't assume an existing row is always
  available for label recon — a throwaway Insert+Delete round-trip is the fallback, self-cleaned
  and DB-reverified.
- DB self-clean checks against `OV_OPERATOR_LEASE` must use the generic `CODE` column, not a
  screen-specific column.
- Distinct from sibling Commercial Objects screens converted in the same PR #436 batch — Customer
  (`OV_CUSTOMER`), Field Group (`OV_FIELD_GROUP`), Licence (`OV_LICENCE`), MMS Lease
  (`OV_MMS_LEASE`) — do not confuse when grepping/searching this batch's shared findings.
