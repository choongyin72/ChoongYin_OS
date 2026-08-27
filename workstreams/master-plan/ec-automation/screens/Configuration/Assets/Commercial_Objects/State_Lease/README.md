# State Lease — Bundle Overview

Insert / Update / Delete automation for the EC **State Lease** screen
(Configuration > Assets > Commercial Objects > State Lease).

State Lease is a **Manage Object (OV)** screen, plain (no mandatory navigator/cascade dropdown),
converted to the **Bank pattern** (label-driven, properties-file-driven, T2-consolidated RF suite)
via PR #440 (merged 2026-08-23, Batch 4). DELETE = **End Date = Start Date** (zero-length window) —
EC true delete (object removed from `OV_STATE_LEASE`).

The RF suite is the current, maintained automation for this screen. The `playwright/` +
`investigation/` folders are the **older, pre-conversion reference bundle** (built 2026-06-12,
predates the Bank-pattern conversion and the engine/Playwright-waiver decision) — kept for history
only; per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, no new Playwright driver is built or
maintained for Bank-pattern screens going forward (the Universal Screen Engine replaces that role).

## Run — RF suite (current automation)
```bash
# from workstreams/master-plan/ec-automation/

# dryrun (single suite)
robot --dryrun --outputdir results/_statelease_dryrun tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot

# live headless run
EC_HEADLESS=true robot --outputdir results/_statelease_live tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot
```

## Run — legacy Playwright reference (historical only, not maintained)
```bash
py -X utf8 playwright/ec_iud_state_lease.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_state_lease.py   # watchable
```

## DB self-clean check (fresh connection, run after any live pass)
```sql
-- Expect 0 rows before AND after every run
SELECT COUNT(*) FROM OV_STATE_LEASE WHERE CODE = 'AUTOTEST_STL';
```
Or via the shared `DbVerify.py`: `Code Should Be Absent In View    OV_STATE_LEASE    AUTOTEST_STL`.

## Folder
- `pageobjects/.../state_lease_page.resource` (T3) + `tests/.../state_lease_iud.robot` (suite) — the
  real, current, live-verified RF automation (outside this bundle folder; see repo-root paths above).
- `state_lease_sow.md` — statement of work / spec (classification, mandatory fields, dev story).
- `JOURNAL.md` — work journal (built / done well / lessons / blockers / decisions / evidence).
- `CHECKLIST.md` — the 21-item IUD deliverable checklist, ticked with evidence.
- `evidence/` — screenshots + `state_lease_results.json` from the original 2026-06-12 Playwright run,
  plus this backfill's RF re-run artifacts.
- `playwright/`, `investigation/` — legacy pre-conversion reference bundle (historical, not maintained).

## Equivalent RF suite (repo-root paths)
- T3: `workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/state_lease_page.resource`
- Suite: `workstreams/master-plan/ec-automation/tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot`
- KB selector map: `ec-ui-knowledge/screens/state_lease.md`
