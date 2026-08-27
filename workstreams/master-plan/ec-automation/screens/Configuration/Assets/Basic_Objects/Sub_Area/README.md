# Sub Area — IUD Automation Bundle

Insert / Update / Delete automation for the EC **Sub Area** screen
(Configuration → Assets → Basic Objects → Sub Area).

Sub Area is an **OV-GM (groupmodel manage-object)** screen, gated by a genuine 2-level
Production Unit → Area navigator cascade + GO. DELETE = **End Date = Start Date** (zero-length
window), which EC treats as a true delete (object removed from `OV_SUB_AREA`).

**The maintained/live test is the Robot Framework suite**, converted to the full Area-pattern
5-TC structure via PR #538 (2026-08-26; see `JOURNAL.md` and `sub_area_sow.md` §3.2). The
Playwright driver below is the original 2026-06-11 reference implementation, preserved unchanged
— per owner decision 2026-08-27, no new/updated Playwright bundle is built for Area-pattern
conversions (the Universal Screen Engine replaces that role going forward).

## Run — Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_SUB_AREA code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot
```

## DB self-clean check (ground truth — OV_SUB_AREA)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a
mid-test session), to confirm the fixed test code (`AUTOTEST_SUB_AREA`) is absent and no
`AUTOTEST%` residual rows exist:
```sql
SELECT COUNT(*) FROM OV_SUB_AREA WHERE CODE = 'AUTOTEST_SUB_AREA';   -- expect 0
SELECT CODE FROM OV_SUB_AREA WHERE CODE LIKE 'AUTOTEST%';            -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view, not a
screen-specific `SUB_AREA_CODE` column — confirmed live 2026-08-27 during this backfill.)

## Run — Playwright (original reference, unmodified since 2026-06-11)
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_sub_area.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_sub_area.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `400` | ms slow-motion per action (headed only) |
| `EC_CODE` | auto timestamp | override the test code |
| `EC_URL` / `EC_DB_DSN` | sandbox | override targets |

## Folder
- `playwright/ec_iud_sub_area.py` — thin config over the shared engine (`../_shared/iud_engine.py`); original 2026-06-11 build, NOT modified by PR #538 or this backfill
- `investigation/` — recon scripts (DOM scans + DB probes) used to learn the screen (original build)
- `evidence/` — screenshots + results JSON from the original full insert → update → delete run, plus `backfill_2026-08-27/` (RF dryrun + live output captured by this backfill)
- `sub_area_sow.md` — statement of work / spec (updated 2026-08-27 with the PR #538 conversion story)
- `JOURNAL.md` — work journal (added 2026-08-27 backfill)
- `CHECKLIST.md` — deliverable checklist (added 2026-08-27 backfill)

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource`
- Suite: `tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot`
- Test data: `testdata/sub_area_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/sub_area.md`
