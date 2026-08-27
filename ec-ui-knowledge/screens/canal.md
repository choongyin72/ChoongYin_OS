# Screen: Canal

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`);
  plain OV, no navigator/mandatory dropdown cascade. Full Bank-pattern conversion (PR #458,
  Batch 7, 2026-08-23) — properties-file-driven insert/update/verify + explicit grid-filter
  wiring, superseding the earlier argument-driven 4-TC build this KB entry originally described.
- **BF_CODE:** CO.2069 · **Treeview:** Configuration > Assets > Transport Objects > Canal
- **DB view:** `OV_CANAL` (base `CANAL` table, versioned/date-effective); key `CODE`; other
  columns: `NAME`, `TIME_ZONE_REGION_CODE`, `OBJECT_START/END_DATE`.
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox — dryrun 5/5, live RF 5/5 (fresh
  re-run for `docs/lean-deliverable-backfill-workorder.md` Batch 9), robocop 9 baseline warnings,
  hygiene exit 0, DB self-clean 0 residual (fresh `oracledb` connection).

## Selectors `[from screens/Canal/canal_page.resource Variables section, 2026-08-28]`
| Purpose | Selector |
|---|---|
| Open | treeview search "Canal" -> `label.tv-link` |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data` (needs GO to load; single page, 2 real rows: `SUEZ`/`PANAMA`) |
| Grid filter | `Find Canal Row By Filter <code>` / `Clear Canal Row Filter` (shared T2 `Find/Clear Object Row By Filter`, explicit grid-filter wiring — wired into Update/Find/Verify-Found/Delete) |
| Delete date field | `${CANAL_DEL_ENDDATE}` = `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (one deliberate hardcoded id — row packs Start Date C:1 / End Date label C:2 / End Date field C:3, same documented shape as Bank's/Customer's own delete-date ids) |

### Insert form (`objectForm`) — labels (T3 resolves BY LABEL)
**`Canal Code`*** · **`Canal Name`*** · **`Start Date`*** (date) · Time Zone (dd, optional,
deliberately skipped). `*` = mandatory. Labels are screen-prefixed ("Canal Code"/"Canal Name",
NOT the generic Bank "Code"/"Name") — same shape as State's "State Code"/"State Name" precedent —
passed as `code_label=Canal Code` on every T2 call.

### Update tab (`updateAttributes`)
`Canal Code` (read-only) · **`Canal Name`** (only field present in updateAttributes; Start/End
Date live only in `objectdates`, not here).

### Delete (date-close) — `objectdates`
**`End Date`** = Start Date -> row leaves `OV_CANAL` (true date-effective delete).

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/canal_page.resource`
  (label-driven, properties-file-driven, explicit grid-filter wiring, full Bank pattern) + suite
  `tests/Configuration/Assets/Transport_Objects/canal_iud.robot` — 5-TC (TC01 clean-state, TC02
  insert, TC03 update, TC04 find, TC05 delete) — live 5/5.
- **Test data:** `testdata/canal_{insert,update,form_verify,grid_verify}.properties`. Fixed test
  code `CANAL_KIEL` (not a generated unique code) — confirmed absent from `OV_CANAL` live
  (only real rows `SUEZ`/`PANAMA`); every run must complete TC05 delete to keep the code free for
  the next run.
- **Playwright:** `py/canal_iud.py` — pre-existing (2026-07-26), unchanged by PR #458. Not
  rebuilt or extended going forward (Universal Screen Engine `py/engine.py` is the owner-decided
  replacement for hand-written Playwright drivers — Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- **Credentials:** `resources/credentials.py` — `CANAL_EC_USER`/`CANAL_EC_PASS` (screen-specific
  pair, falls back to shared `EC_USER`/`EC_PASS`, then `sysadmin`/`sysadmin` local-sandbox
  default).

## Mandatory-yellow fields
`Canal Code`, `Canal Name`, `Start Date` (Insert form). `Canal Name` only on Update (Code
read-only, Start/End Date not present on the update tab). `End Date` on the delete tab
(`objectdates`).

## Quirks
- **Screen-prefixed labels**, not the generic Bank "Code"/"Name" — Canal's own labels are "Canal
  Code"/"Canal Name". Threaded through as `code_label=Canal Code` on every shared T2 call. Do not
  assume the generic Bank label set applies here without checking (same lesson as State).
- **Small, single-page grid** (2 real rows) — grid-filter wiring is applied anyway for
  consistency/future-proofing (matches Bank/Account's own explicit-filter usage), not because the
  grid currently needs it to locate a row.
- No mandatory dropdown (Time Zone is optional) — no navigator cascade at all (plain OV, Bank
  family, not Area family).
