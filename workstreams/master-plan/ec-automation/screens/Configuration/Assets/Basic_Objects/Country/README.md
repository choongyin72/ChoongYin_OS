# Country — IUD bundle (Bank pattern)

Insert / Update / Delete automation for the EC **Country** screen
(Configuration > Assets > Basic Objects > Country).

Country is a **plain Manage Object (OV)** screen — no navigator dropdown/date, matching Bank's
layout (not Area's OV-GM cascade). DELETE = **End Date = Start Date** (zero-length window), which
EC treats as a true delete (object removed from `OV_COUNTRY`).

The **maintained automation is the Robot Framework suite** below, rebuilt to the Bank pattern
(label-driven, properties-file-driven, T2-consolidated) in PR #428 (merged 2026-08-23). The
Playwright bundle in this folder (`playwright/`, `investigation/`) is a **superseded reference**
kept for history — the Universal Screen Engine is the owner-decided replacement for hand-written
Playwright drivers going forward (per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H); do not
extend it.

## Run the RF suite (real commands)

From `workstreams/master-plan/ec-automation/`:

```bash
# Structure-only dry run (no browser, no login)
robot --dryrun tests/Configuration/Assets/Basic_Objects/country_iud.robot

# Live headless run (the real proof - logs in, drives the screen, DB-verifies)
EC_HEADLESS=true robot tests/Configuration/Assets/Basic_Objects/country_iud.robot

# Live headed run (watch it)
EC_HEADLESS=false robot tests/Configuration/Assets/Basic_Objects/country_iud.robot
```

## DB self-clean check pattern
The suite's own TC05 (`Verify Country Record Removed` -> shared T2 `Verify Object Removed`) already
asserts `Code Should Be Absent In View OV_COUNTRY <code>` after delete - this IS the self-clean
check; a live PASS on TC05 is sufficient DB ground-truth evidence. To re-check independently with
a fresh connection (e.g. after an interrupted run), query:
```sql
SELECT COUNT(*) FROM OV_COUNTRY WHERE CODE = 'AUTOTEST_COUNTRY';
-- expect 0
```

## Robocop / hygiene
```bash
py -m robocop check pageobjects/Configuration/Assets/Basic_Objects/country_page.resource \
  tests/Configuration/Assets/Basic_Objects/country_iud.robot
# 9 issues (4 VAR02 + 5 DOC02) - same baseline PR #428 established; not a regression.

# from repo root:
py scripts/check_bundle_hygiene.py
```

## Folder contents
- `country_sow.md` — statement of work / spec (classification, DOM refs, test data, dev story).
- `JOURNAL.md` — work journal (Built / Done well / Done wrong-lessons / Blockers->resolution / Decisions / Evidence).
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence.
- `evidence/` — 2026-06-11 Playwright screenshots + results JSON (preserved), plus
  `evidence/rf_backfill_2026-08-28/` — this backfill's RF re-run (log.html, output.xml, 26
  per-step screenshots, results summary).
- `playwright/ec_iud_country.py` — superseded Playwright reference (not maintained).
- `investigation/` — pre-conversion recon scripts (superseded).

## Where the real automation lives
- RF page object (T3, Bank pattern): `pageobjects/Configuration/Assets/Basic_Objects/country_page.resource`
- RF suite: `tests/Configuration/Assets/Basic_Objects/country_iud.robot`
- Properties files: `testdata/country_{insert,update,form_verify,grid_verify}.properties`
- Shared T2: `resources/manage_object.resource` — T1: `resources/common.resource` (both untouched by this backfill)
- KB selector map: `ec-ui-knowledge/screens/country.md`
- Registry row: `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`
