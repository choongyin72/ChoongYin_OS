# Royalty Owner - IUD bundle

Configuration > Assets > Royalty Objects > **Royalty Owner** (RC.0051).
Manage-Object (OV) screen, Bank family (no navigator). DELETE = End Date = Start Date (true
delete in `OV_ROYALTY_OWNER`). RF suite rebuilt to the full Bank pattern via PR #447
(2026-08-23, Batch 5 Bank-pattern conversion) — label-driven, properties-file-driven,
T2-consolidated, explicit grid-filter wiring included from day one.

## Contents
- `royalty_owner_sow.md` - Statement of Work (original recon + design + acceptance criteria,
  plus a Section 5 addendum documenting the PR #447 Bank-pattern conversion).
- `JOURNAL.md` - per-branch work journal (built / done well / lessons / blockers / decisions /
  evidence), backfilled 2026-08-28 from PR #447's real body.
- `CHECKLIST.md` - the 21-item IUD deliverable checklist, ticked with evidence for this screen.
- `playwright/ec_iud_royalty_owner.py` - pre-existing freestyle Playwright IUD walkthrough
  (screenshots per step). Predates the Universal Screen Engine decision (2026-08-16); left
  untouched — no NEW Playwright work is required for Bank-/Area-pattern screens going forward
  (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- `evidence/` - screenshots + `output.xml` from live runs (original 2026-06-25 build, plus a
  fresh 2026-08-28 backfill re-run under `evidence/2026-08-28_backfill_run/` — see
  `evidence/EVIDENCE-SUMMARY.md`).

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).
- Fixed test code `AUTOTEST_ROYALTY_OWNER` (not per-run generated) — every run must complete
  TC05 (delete) to free the code for the next run.

## Run
```bash
# RF (the proof) - headless live run from the ec-automation root:
EC_HEADLESS=true robot --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot

# RF - headed live run (visual demo):
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot

# Dry-run only (no browser, syntax/keyword-resolution check):
robot --dryrun tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot

# Robocop lint (T3 + suite):
robocop check pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot

# Playwright walkthrough (demo / screenshots) - pre-existing, untouched by this backfill:
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Royalty_Owner/playwright/ec_iud_royalty_owner.py
```

## DB self-clean check (fresh connection, run after any live suite)
```sql
SELECT COUNT(*) FROM OV_ROYALTY_OWNER WHERE CODE = 'AUTOTEST_ROYALTY_OWNER';
-- Expect 0 after TC05 (delete) completes. Non-zero = residual test data, investigate before
-- reporting the run as clean.
```

Env: this repo's local/dev sandbox (see this repo's `CLAUDE.md` "Verified Data Sources" for the
current live web/DB endpoints — the original SOW's 2026-06-25 sandbox URL is historical, not
necessarily the current target). DB connection resolves via `EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`
env vars with local-sandbox fallbacks (see `libraries/DbVerify.py`). Test data
`AUTOTEST_ROYALTY_OWNER` only; self-cleaning.
