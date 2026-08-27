# Vendor — IUD automation bundle

Insert / Update / Delete automation for the EC **Vendor** screen
(Configuration → Assets → Commercial Objects → Vendor).

Vendor is a **Manage Object (OV) screen, plain Bank pattern** (no navigator section —
confirmed live 2026-08-23: only the universal Date + GO as-at-date bar). DELETE =
**End Date = Start Date** (zero-length window) — EC true delete, object removed from
`OV_VENDOR`.

The RF suite is the **live, authoritative** automation (converted from an older
hardcoded-field-id pattern to the label-driven, properties-file-driven, T2-consolidated
"Bank pattern" in PR #439, Batch 4, merged 2026-08-23). The `playwright/` folder holds an
**older reference driver that predates that conversion** — per owner decision 2026-08-27
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), a new/refreshed Playwright bundle is
permanently waived for Bank-/Area-pattern screens (the Universal Screen Engine replaces that
role); the existing Playwright files are left as-is, untouched by this backfill.

## Run — RF suite (authoritative)
```bash
# Dryrun (syntax + keyword resolution only, no browser)
robot --dryrun --outputdir /tmp/vendor-dryrun tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot

# Live headless run
EC_HEADLESS=true robot --outputdir /tmp/vendor-live tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot

# Live headed run (watchable)
EC_HEADLESS=false robot --outputdir /tmp/vendor-live tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot
```

## DB self-clean check (fresh connection, not reused from the suite)
```bash
py -c "
import oracledb
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL', tcp_connect_timeout=15)
cur = conn.cursor()
cur.execute(\"SELECT COUNT(*) FROM OV_VENDOR WHERE CODE='AUTOTEST_VEND'\")
print(cur.fetchone()[0])
conn.close()
"
```
Expected: `0` — the suite's fixed test code `AUTOTEST_VEND` must be absent both before TC01
and after TC05 (TC05's delete cleans up so the next run can reuse the same fixed code).

## Grid-filter-fired check (confirms `Find Vendor Row By Filter` actually ran)
```bash
grep -c 'name="Find Vendor Row By Filter"' /tmp/vendor-live/output.xml
```
Expected: `5` (one hit per TC that touches a row: TC02-TC05, plus TC04's Find step).

## Folder
- `pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource` (T3, actual repo
  location — outside this bundle, under `pageobjects/`) — label-driven locators + thin IUD
  wrappers delegating to T2 (`resources/manage_object.resource`) and T1 (`resources/common.resource`).
- `tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot` (actual repo location,
  under `tests/`) — TC01 clean-state / TC02 insert / TC03 update / TC04 find / TC05 delete.
- `testdata/vendor_insert.properties`, `vendor_update.properties`, `vendor_form_verify.properties`,
  `vendor_grid_verify.properties` (actual repo location, under `testdata/`).
- `vendor_sow.md` — statement of work / spec (classification, mandatory fields, test data, dev story).
- `JOURNAL.md` — per-branch work journal (built / done well / lessons / blockers / decisions / evidence).
- `CHECKLIST.md` — the 21-item IUD deliverable checklist, ticked with evidence citations.
- `evidence/` — `rf_backfill_2026-08-28/` (this backfill's re-run: output.xml, log.html,
  results-summary.txt) plus the pre-existing `playwright/`-era screenshots + `vendor_results.json`.
- `playwright/`, `investigation/` — pre-existing, PRE-CONVERSION reference material; permanently
  waived from a fresh build per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`; not touched
  by this backfill.

## KB selector map
`ec-ui-knowledge/screens/vendor.md` — nav path, DB view, grid id, insert/update/delete
selectors, mandatory-yellow fields, quirks, last-verified date.
