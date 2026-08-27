# Field — IUD automation bundle

Insert / Update / Delete automation for the EC **Field** screen
(Configuration → Assets → Commercial Objects → Field).

Field is an **OV-GM (groupmodel manage-object)** screen: the grid loads only after the
mandatory single **Area** navigator dropdown + GO. DELETE = **End Date = Start Date**
(EC true delete — row removed from `OV_FIELD`).

**Primary automation is Robot Framework**, converted to the full **Area pattern** (owner
standing rule 2026-08-26 — any navigator screen matching Area's layout follows Area's full
5-TC/per-TC-login/pure-screen-verify structure). See `field_sow.md` for the classification and
`JOURNAL.md` for the real build history (PR #525 + PR #529).

## RF files (already merged — this bundle documents them, does not modify them)
- T3 page object: `pageobjects/Configuration/Assets/Commercial_Objects/field_page.resource`
- Suite: `tests/Configuration/Assets/Commercial_Objects/field_iud.robot`
- Test data: `testdata/field_navigator.properties`, `field_insert.properties`,
  `field_update.properties`, `field_form_verify.properties`, `field_grid_verify.properties`
- Credentials: `FIELD_EC_USER`/`FIELD_EC_PASS` in `resources/credentials.py`

## Run commands
From `workstreams/master-plan/ec-automation/`:

```bash
# Dryrun (syntax/keyword resolution check, whole tree)
py -m robot --dryrun tests/

# Live run, this screen only, headless
EC_HEADLESS=true py -m robot --outputdir results tests/Configuration/Assets/Commercial_Objects/field_iud.robot

# Live run, headed (watchable)
EC_HEADLESS=false py -m robot --outputdir results tests/Configuration/Assets/Commercial_Objects/field_iud.robot
```

## DB self-clean check (OV_FIELD, fixed test code AUTOTEST_FIELD)
Run against the local sandbox EC database (`localhost:1521/ORCL`, user `ECKERNEL_EC`) with a
FRESH connection (not a connection held open through the test run):

```sql
SELECT COUNT(*) FROM OV_FIELD WHERE CODE LIKE 'AUTOTEST%';
-- expect 0 both BEFORE (proves the fixed code is free) and AFTER (proves TC05 Delete cleaned up)
```

## Bundle contents
- `field_sow.md` — statement of work: classification, navigator/grid/field shape, test data, dev story
- `README.md` — this file
- `JOURNAL.md` — real build history (Built / Done well / Done wrong-lessons / Blockers→resolution / Decisions / Evidence)
- `CHECKLIST.md` — `docs/IUD-DELIVERABLE-CHECKLIST.md` copy, ticked with real evidence
- `evidence/` — screenshots + results from the original 2026-06-12 Playwright build (legacy,
  kept unchanged) plus a `backfill-2026-08-27/` subfolder with this session's dryrun/live RF
  run artifacts
- `investigation/`, `playwright/` — legacy 2026-06-12 Playwright-era artifacts, kept unchanged;
  items 4/5 of the deliverable checklist are waived for Bank-/Area-pattern work going forward
  (the Universal Screen Engine replaces the hand-written-Playwright-driver role)

## KB selector map
`ec-ui-knowledge/screens/field.md` — nav path, DB view, grid id, insert/update/delete
selectors, mandatory fields, quirks.
