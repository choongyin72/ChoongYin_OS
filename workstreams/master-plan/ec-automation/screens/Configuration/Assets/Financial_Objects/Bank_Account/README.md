# Bank Account — Playwright IUD (superseded reference) + RF suite

> **RF suite is the maintained deliverable** (rebuilt 2026-08-23, PR #478, Bank-pattern
> conversion — FINAL screen of the confirmed 23-screen candidate pool). The standalone
> `playwright/ec_iud_bank_account.py` below is a **pre-existing reference bundle from the
> 2026-06-11 build**, kept unchanged per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (the
> Playwright driver stays permanently waived for Bank-/Area-pattern work — the Universal Screen
> Engine replaces that role going forward).

Insert / Update / Delete automation for the EC **Bank Account** screen
(Configuration → Assets → Financial Objects → Bank Account). Bank Account is a distinct screen
from **Bank** (the Bank-pattern exemplar, CO.0001) — do not confuse the two bundles.

Bank Account is a **Manage Object (OV)** screen, no mandatory navigator. DELETE = **End Date =
Start Date** (zero-length window) — EC true delete (object removed from `OV_BANK_ACCOUNT`).

## RF suite — current shape (the deliverable to run, rebuilt 2026-08-23 PR #478)

5-TC structure (TC01 Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete), each TC with
its own Login/Logout, a **fixed** test code `AUTOTEST_BACC`, properties-file-driven insert/update
(`testdata/bank_account_{insert,update,form_verify,grid_verify}.properties`), and explicit
grid-filter wiring (`Find/Clear Bank Account Row By Filter`, delegating to the shared T2
`Find/Clear Object Row By Filter`). See `bank_account_sow.md` Section 7 for the full conversion
history (pulled from PR #478's real body).

### Run — from `workstreams/master-plan/ec-automation/`
```bash
# structure-only dryrun (no browser/DB)
robot --dryrun tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot
```

### DB self-clean check pattern
```sql
SELECT COUNT(*) FROM OV_BANK_ACCOUNT WHERE CODE LIKE 'AUTOTEST_BACC%';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```
Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_BANK_ACCOUNT", "AUTOTEST_BACC")` — `None` = confirmed absent.

## Playwright reference (pre-existing, unchanged since 2026-06-11)
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_bank_account.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_bank_account.py
```

## Files in this bundle
- `bank_account_sow.md` — SOW: classification, nav/grid/cell shape, test data, dev story
  (original 2026-06-11 build + the 2026-08-23 PR #478 conversion addendum in Section 7).
- `README.md` — this file.
- `JOURNAL.md` — per-branch work journal (built/done-well/lessons/decisions/evidence), updated
  this session with the PR #478 conversion + this backfill's own evidence-capture run.
- `evidence/` — screenshots + `bank_account_results.json` from the original 2026-06-11 Playwright
  run, PLUS `log.html`/`output.xml`/`report.html`/`playwright-log.txt`/per-TC screenshots from a
  live RF run captured 2026-08-28 (this backfill session).
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence citations.
- `VERIFY-REPORT.md` — hand-assembled report citing this backfill's own executed gates.
- `playwright/`, `investigation/` — the pre-existing Playwright reference bundle (unchanged; see
  Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` — permanently waived for further build, kept
  as historical reference, not rebuilt).

KB selector map: `ec-ui-knowledge/screens/bank_account.md`.
