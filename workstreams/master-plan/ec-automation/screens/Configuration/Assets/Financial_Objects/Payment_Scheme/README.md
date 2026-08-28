# Payment Scheme — Playwright IUD

Insert / Update / Delete automation for the EC **Payment Scheme** screen
(Configuration → Assets → Financial Objects → Payment Scheme), implemented in **Playwright** (Python).

Payment Scheme is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_PAYMENT_SCHEME`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_payment_scheme.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_payment_scheme.py
```

## Folder
- `playwright/ec_iud_payment_scheme.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `payment_scheme_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot` (the maintained test;
this bundle's `playwright/` is the preserved reference + discovery trail from the original
2026-06-11 build).

## RF suite — current shape (post PR #420, 2026-08-22) — this is the deliverable to run

The maintained suite is the Bank/State-pattern 5-TC structure (TC01 Clean State, TC02 Insert,
TC03 Update, TC04 Find, TC05 Delete), each TC with its own Login/Logout, a **fixed** test code
`AUTOTEST_PAYMENT_SCHEME`, properties-file-driven insert/update via
`testdata/payment_scheme_{insert,update,form_verify,grid_verify}.properties`, and explicit
grid-filter wiring (`Find/Clear Payment Scheme Row By Filter`). No navigator — plain OV. See
`payment_scheme_sow.md` Section 7 for the full conversion history.

### Run — from `workstreams/master-plan/ec-automation/`

```bash
# structure-only dryrun (no browser/DB)
robot --dryrun tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot
```

### DB self-clean check pattern

```sql
SELECT COUNT(*) FROM OV_PAYMENT_SCHEME WHERE CODE = 'AUTOTEST_PAYMENT_SCHEME';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```
Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_PAYMENT_SCHEME", "AUTOTEST_PAYMENT_SCHEME")` — `None` = confirmed absent.

### Files in this bundle
- `payment_scheme_sow.md` — SOW: classification, nav/grid/cell shape, test data, dev story
  (original 2026-06-11 build + the 2026-08-22 PR #420 conversion addendum).
- `README.md` — this file.
- `JOURNAL.md` — per-branch work journal for the conversion (built/done-well/lessons/decisions/
  evidence).
- `evidence/` — screenshots + `payment_scheme_results.json` from the original 2026-06-11
  Playwright run, PLUS `log.html`/`output.xml`/`report.html`/per-TC screenshots from a live RF
  run captured 2026-08-28.
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence citations.
- `playwright/`, `investigation/` — the pre-existing Playwright reference bundle (unchanged; see
  Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` — the Playwright driver stays waived for
  Bank-/Area-pattern work but this pre-existing one was left in place, not deleted).

KB selector map: `ec-ui-knowledge/screens/payment_scheme.md`.
