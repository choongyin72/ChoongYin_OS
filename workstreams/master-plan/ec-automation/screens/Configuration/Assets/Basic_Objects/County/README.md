# County — IUD Bundle (Bank pattern)

Insert / Update / Delete automation for the EC **County** screen
(Configuration → Assets → Basic Objects → County).

County is a **Manage Object (OV)** screen, no navigator section — same layout as Bank/State.
DELETE = **End Date = Start Date** (zero-length window), which EC treats as a true delete
(object removed from `OV_COUNTY`).

**The maintained, current test is the Robot Framework suite**, converted to the label-driven,
properties-file-driven, T2-consolidated **Bank pattern** in PR #429 (2026-08-23) and aligned to
Bank's exact pure-screen-verify convention in PR #489 (2026-08-24). The `playwright/` folder below
is the ORIGINAL 2026-06-11 reference build, preserved for history — it was NOT touched by the
Bank-pattern conversion and is not the maintained automation.

## Run the RF suite (current, maintained)
From `workstreams/master-plan/ec-automation/`:
```bash
# dryrun (structure check, no browser)
robot --dryrun --outputdir results/_dryrun tests/Configuration/Assets/Basic_Objects/county_iud.robot

# live headless run (5 TCs: clean-state / insert / update / find / delete)
EC_HEADLESS=true robot --outputdir results/_county tests/Configuration/Assets/Basic_Objects/county_iud.robot

# live headed (visible browser)
EC_HEADLESS=false robot --outputdir results/_county tests/Configuration/Assets/Basic_Objects/county_iud.robot
```

## DB self-clean check (fresh connection, after a live run)
```sql
SELECT CODE FROM OV_COUNTY WHERE CODE LIKE 'AUTOTEST%';
-- expect 0 rows once TC05 (delete) has run
```

## Folder
- `pageobjects/Configuration/Assets/Basic_Objects/county_page.resource` — T3 page object (Bank pattern, current)
- `tests/Configuration/Assets/Basic_Objects/county_iud.robot` — 5-TC RF suite (Bank pattern, current)
- `testdata/county_*.properties` — insert/update/form-verify/grid-verify properties files
- `playwright/ec_iud_county.py` — ORIGINAL 2026-06-11 Playwright reference (thin config over `../_shared/iud_engine.py`), superseded, kept for history
- `investigation/` — recon scripts (DOM scans + DB probes) from the original 2026-06-11 build
- `evidence/` — screenshots + results JSON (original build) + latest live re-run for this backfill
- `county_sow.md` — statement of work / spec (v2.0 current classification + v1.0 history)
- `JOURNAL.md` — real work journal, backfilled 2026-08-28 from PR #429/#489 history
- `CHECKLIST.md` — IUD deliverable checklist, ticked against real evidence

## History
- PR #429 — original Bank-pattern conversion (2026-08-23).
- PR #489 — pure-screen-verify alignment fix, removed 2 inline DB-verify keywords to match `bank_iud.robot` exactly (2026-08-24).
