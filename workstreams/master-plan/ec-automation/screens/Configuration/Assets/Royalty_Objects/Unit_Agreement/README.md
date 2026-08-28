# Unit Agreement - IUD bundle

Configuration > Assets > Royalty Objects > **Unit Agreement** (RC.0055), app `EC_REVN`.
Manage-Object (OV) screen, Bank family - **no navigator** (date-only, not OV-GM).
DELETE = End Date = Start Date (true delete in `OV_UNIT_AGR`).
⚠️ View/slug mismatch: DB view `OV_UNIT_AGR` (base table `UNIT_AGR`) does not derive from the
"unit_agreement" slug.

**Status:** the RF suite was converted to the full label-driven, properties-file-driven,
T2-consolidated **Bank pattern** via PR #446 (merged 2026-08-23, Batch 5). Live **5/5 PASS**,
DB-verified, self-cleaning. See [unit_agreement_sow.md](unit_agreement_sow.md) Section 0 for the
real conversion story pulled from PR #446's own body, and [JOURNAL.md](JOURNAL.md).

This README, `JOURNAL.md`, `evidence/backfill_2026-08-28/`, and `CHECKLIST.md` were added/refreshed
by the 2026-08-28 deliverable backfill (`docs/lean-deliverable-backfill-workorder.md`, Batch 8) -
**the RF automation itself was NOT modified by this backfill.** Per owner decision 2026-08-27
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), the Playwright driver below is left as the
original 2026-06-25 reference implementation, unmodified - the Universal Screen Engine replaces
that role for new work, not a rebuilt per-screen Playwright bundle.

## Contents
- `unit_agreement_sow.md` - Statement of Work (recon + design + acceptance criteria; Section 0
  added 2026-08-28 covers the PR #446 Bank-pattern conversion).
- `playwright/ec_iud_unit_agreement.py` - freestyle Playwright IUD walkthrough (screenshots per
  step) - original 2026-06-25 build, NOT modified by PR #446 or this backfill.
- `evidence/` - screenshots from the original live run, plus `backfill_2026-08-28/` (RF dryrun +
  live run output, robocop, hygiene, and DB self-clean evidence captured by this backfill).
- `JOURNAL.md` - work journal (added 2026-08-28 backfill; this screen never had one before).
- `CHECKLIST.md` - deliverable checklist (added 2026-08-28 backfill; this screen never had one before).

## RF suite (the proof, maintained + live)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot`
- Test data:      `testdata/unit_agreement_{insert,update,form_verify,grid_verify}.properties`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).
- KB selector map: `ec-ui-knowledge/screens/unit_agreement.md`

## Run
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning - TC05 deletes the fixed
#    AUTOTEST_UA code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot

# Playwright walkthrough (original 2026-06-25 reference, demo / screenshots):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Unit_Agreement/playwright/ec_iud_unit_agreement.py
```

## DB self-clean check (ground truth - OV_UNIT_AGR)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_UA`) is absent and no `AUTOTEST%` residual rows
exist:
```sql
SELECT COUNT(*) FROM OV_UNIT_AGR WHERE CODE = 'AUTOTEST_UA';   -- expect 0
SELECT CODE FROM OV_UNIT_AGR WHERE CODE LIKE 'AUTOTEST%';      -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (defaults from
`resources/environment.py`, overridable via `EC_URL`), DB `localhost:1521/ORCL` (`ECKERNEL_EC`/
`energy`, overridable via `EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`). Test data `AUTOTEST_UA` (fixed
code, RF suite) or `AUTOTEST_UA_*` (per-run, Playwright driver) only; self-cleaning.
