# Facility Class 1 - EC Object IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > Facility Class 1 (BF CO.0019). OV-GM
(manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.

Built 2026-07-30 as an early OV-GM screen (PR #262, on the gated-navigator capability PR #244).
Converted 2026-08-26 to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE in two
stacked PRs (**#526** navigator-fill -> shared `Apply Navigator From Properties`; **#530** full
structural conversion) - see `facility_class_1_sow.md` and `JOURNAL.md` for the real history.
This backfill (2026-08-27, `docs/lean-deliverable-backfill-workorder.md`) adds the documentation/
evidence artifacts the 2026-08-23/26 lean waiver skipped around that already-working, already-merged
automation. **No RF/Playwright code was changed by this backfill.**

## What's here
- `facility_class_1_sow.md` - classification, navigator/grid/form shape, test data, dev story.
- `JOURNAL.md` - per-branch work journal (built / done-well / lessons / blockers / decisions / evidence).
- `CHECKLIST.md` - `docs/IUD-DELIVERABLE-CHECKLIST.md` copy, ticked with real evidence.
- `VERIFY-REPORT.md` - gate summary (robocop / hygiene / dryrun / live run).
- `evidence/` - `fc1_0N_*.png` (2026-07-30 Playwright driver run) + `log.html`/`report.html`/`output.xml`
  (2026-08-27 backfill live RF run, this bundle).
- `investigation/recon.py` - original 2026-07-30 recon (retained; not rebuilt).
- **Code (lives in `ec-automation`, not in this bundle folder):**
  - T3: `pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource`
  - Suite: `tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot`
  - Properties: `testdata/facility_class_1_{navigator,insert,update,form_verify,grid_verify}.properties`
  - Playwright driver (retained, not part of this backfill): `py/facility_class_1_iud.py`
  - KB selector map: `ec-ui-knowledge/screens/facility_class_1.md`

## Run the suite (from `workstreams/master-plan/ec-automation/`)

```bash
# dry-run (syntax/keyword-resolution check, no browser)
robot --dryrun tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot

# live headless run
EC_HEADLESS=true robot tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot

# live headed run (visible browser)
robot tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot
```

Expected: **5 tests, 5 passed, 0 failed** (TC01 Verify Clean State / TC02 Insert / TC03 Update /
TC04 Find / TC05 Delete). Test code is the FIXED `AUTOTEST_FC1` - the suite must complete TC05 so
the code is free again for the next run (no generated/timestamped code to avoid collisions).

## DB self-clean check (fresh connection, same pattern PRs #526/#530 used)

Same query PRs #526/#530 ran independently of the RF library's own DB check - a small standalone
script (fresh `oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")`)
running:

```sql
SELECT COUNT(*) FROM OV_FCTY_CLASS_1 WHERE CODE LIKE 'AUTOTEST_FC1%'
```

Expected: `0` after a completed run (TC05 deletes the fixed-code row every time).

## robocop / hygiene

```bash
# from workstreams/master-plan/ec-automation/
robocop check pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot

# from repo root
py scripts/check_bundle_hygiene.py
```
