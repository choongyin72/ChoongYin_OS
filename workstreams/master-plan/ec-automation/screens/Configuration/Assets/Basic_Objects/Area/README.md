# Area — Playwright IUD

Insert / Update / Delete automation for the EC **Area** screen
(Configuration → Assets → Basic Objects → Area), implemented in **Playwright** (Python).

Area is a **Manage Object (OV-GM groupmodel)** screen. DELETE = **End Date = Start Date** (zero-length window),
which EC treats as a true delete (object removed from `OV_AREA`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_area.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_area.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `400` | ms slow-motion per action (headed only) |
| `EC_CODE` | auto timestamp | override the test code |
| `EC_URL` / `EC_DB_DSN` | sandbox | override targets |

## Folder
- `playwright/ec_iud_area.py` — thin config over the shared engine (`../_shared/iud_engine.py`)
- `investigation/` — recon scripts (DOM scans + DB probes) used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `area_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Basic_Objects/area_iud.robot` (the maintained test;
this bundle is the preserved Playwright reference + discovery trail).

## RF suite — current shape (post PR #521/#523, 2026-08-25) — this is the deliverable to run

The maintained suite is now the Bank-pattern 5-TC structure (TC01 Clean State, TC02 Insert, TC03
Update, TC04 Find, TC05 Delete), each TC with its own Login/Logout, a **fixed** test code
`AUTOTEST_AREA`, properties-file-driven insert/update, and the mandatory Production Unit navigator
fill delegated to the shared T2 keyword `Apply Navigator From Properties`
(`testdata/area_navigator.properties`). See `area_sow.md` Section 7 for the full history.

### Run — from `workstreams/master-plan/ec-automation/`

```bash
# structure-only dryrun (no browser/DB) — across the whole suite tree
robot --dryrun tests/Configuration/Assets/Basic_Objects/area_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Basic_Objects/area_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Basic_Objects/area_iud.robot
```

### DB self-clean check pattern

```sql
SELECT COUNT(*) FROM OV_AREA WHERE CODE LIKE 'AUTOTEST_AREA%';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```
Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_AREA", "AUTOTEST_AREA")` — `None` = confirmed absent.

### Files in this bundle
- `area_sow.md` — SOW: classification, nav/grid/cell shape, test data, dev story (original build +
  the 2026-08-25/26 conversion addendum).
- `README.md` — this file.
- `JOURNAL.md` — per-branch work journal for the conversion (built/done-well/lessons/decisions/evidence).
- `evidence/` — screenshots + `results.json` from the original 2026-06-11 Playwright run, PLUS
  `log.html`/`output.xml`/`report.html`/per-TC screenshots from a live RF run captured 2026-08-27.
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence citations.
- `playwright/`, `investigation/` — the pre-existing Playwright reference bundle (unchanged; see
  Section G/H of `docs/IUD-DELIVERABLE-CHECKLIST.md` — the Playwright driver stays waived for new
  Bank-/Area-pattern work but this pre-existing one was left in place, not deleted).

KB selector map: `ec-ui-knowledge/screens/area.md`.
