# Trailer - IUD bundle

**Screen:** Configuration > Assets > Transport_Objects > Trailer (BF CO.0265). PLAIN OV (Bank family)
with a custom grid id `trailer_object:form:T_data` and a date-only navigator (GO only, no mandatory
cascade). Sibling of Truck. View `OV_TRAILER`. Date-effective; DELETE = End Date = Start Date.

> **2026-08-23 (PR #475, Batch 10):** the RF page object/suite below was rebuilt to the full
> Bank-pattern shape (properties-file-driven insert/update/verify, explicit grid-filter wiring,
> T2-consolidated, per-TC Login/Logout) — see `trailer_sow.md` Addendum for the conversion story.
> This is the CURRENT maintained automation; the original 2026-07-31 `py/trailer_iud.py` driver
> (Playwright) is kept unmodified as a historical reference (Playwright bundle permanently waived
> for Bank-/Area-pattern work, `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H).

## Files in this bundle
- `trailer_sow.md` — SOW: classification, nav/grid/cell shape, test data, dev story (original
  2026-07-31 build + the 2026-08-23 Bank-pattern conversion addendum).
- `README.md` — this file.
- `JOURNAL.md` — per-branch work journal, pulled from PR #475's real body.
- `evidence/` — `tr_0[1-5]_*.png` + `results.json` from the original 2026-07-31 Playwright run,
  plus `log.html`/`output.xml`/`report.html`/`playwright-log.txt`/per-TC screenshots from a live RF
  run captured 2026-08-28 (this backfill session).
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence citations.
- `investigation/` — pre-existing recon scripts from the original build (unchanged; Playwright/
  investigation stay permanently waived for new Bank-/Area-pattern work per Section H).

## Automation (current, maintained)
- **RF page object (T3):**
  `pageobjects/Configuration/Assets/Transport_Objects/trailer_page.resource` — label-driven,
  properties-file-driven, delegates to shared T2 `resources/manage_object.resource`.
- **RF suite:** `tests/Configuration/Assets/Transport_Objects/trailer_iud.robot` — 5 TCs (Clean
  State / Insert / Update / Find / Delete), each with its own Login/Logout, fixed test code
  `AUTOTEST_TRAILER`.
- **Test data:** `testdata/trailer_{insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** `resources/credentials.py` — `TRAILER_EC_USER`/`TRAILER_EC_PASS` (per-screen
  dedicated credential pair, owner standing decision 2026-08-22).

## Run — from `workstreams/master-plan/ec-automation/`

```bash
# structure-only dryrun (no browser/DB)
robot --dryrun tests/Configuration/Assets/Transport_Objects/trailer_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Transport_Objects/trailer_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Transport_Objects/trailer_iud.robot
```

## DB self-clean check pattern

```sql
SELECT COUNT(*) FROM OV_TRAILER WHERE CODE LIKE 'AUTOTEST%';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```
Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_TRAILER", "AUTOTEST_TRAILER")` — `None` = confirmed absent.

KB selector map: `ec-ui-knowledge/screens/trailer.md`.
