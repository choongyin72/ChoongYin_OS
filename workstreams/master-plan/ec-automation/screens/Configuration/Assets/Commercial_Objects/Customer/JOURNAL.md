# JOURNAL — Customer IUD

_Screen: Configuration > Assets > Commercial Objects > Customer (OV, Manage-Object, no navigator).
View `OV_CUSTOMER`. This JOURNAL was backfilled 2026-08-28 (RF Bank-pattern conversion PR #435
predated the JOURNAL rule — Section G's 2026-08-23 lean waiver skipped it; Section H, 2026-08-27,
retired that waiver and restored the requirement). Content below is pulled from PR #435's real
body and this session's re-verification, not invented._

## Built (2026-08-23, PR #435, Batch 3 of the Bank-pattern conversion project)
- Converted the Customer screen's IUD RF suite from the old hardcoded-field-id pattern to
  Bank/Account's label-driven, properties-file-driven, T2-consolidated pattern, with explicit
  grid-filter wiring (`Find Customer Row By Filter` / `Clear Customer Row Filter`) included from
  day one.
- Files touched: `pageobjects/.../customer_page.resource` (rewritten), `tests/.../customer_iud.robot`
  (rewritten), 4 new `testdata/customer_*.properties` files, `resources/credentials.py`
  (additive `CUSTOMER_EC_USER`/`CUSTOMER_EC_PASS`), plus registry/scorecard/checklist docs.
- Same batch as Field Group/Licence/MMS Lease/Operator Lease.
- Predates this screen's own Playwright reference build (2026-06-12), which is separate/legacy
  and was not touched by the RF conversion.

## Done well
- Live recon before build: confirmed nav-free (0 mandatory nav dropdowns) and confirmed the
  mandatory field set is IDENTICAL on `objectForm` and `updateAttributes` (Code, Name, Start
  Date, ERP Customer Code, Official Name, Customer Group).
- Grid-filter wiring included from the start rather than deferred as a follow-up.
- Full I-U-D DB-verified against `OV_CUSTOMER`: live run 5/5 PASS (`EC_HEADLESS=true`); fresh
  oracledb connection confirmed `SELECT COUNT(*) FROM OV_CUSTOMER WHERE CODE = 'AUTOTEST_CUST'`
  = 0, both before and after the run.
- Full `tests/` dryrun: 735/735 pass (at merge time, 2026-08-23).
- robocop: 7 issues (2 VAR02 + 5 DOC02) — fewer than the established 9-issue baseline at the time.
- Isolated git clone under `Workplaces/customer/`, own branch — no shared T1/T2 file edits, no
  other Batch-3 screen touched.

## Done wrong / lessons
- Customer Group's real first option is the literal `Non Group` — used verbatim in the insert
  properties file, NOT `__FIRST__`. This is the VAT Code round-trip-verify gotcha from Batch 2:
  `__FIRST__` never resolves to literal text for the TC02 round-trip comparison against
  `Verify Object Insert Exists`, so any screen with a mandatory reference dropdown must read
  back the real first-option text live and hardcode that string, not the `__FIRST__` sentinel.
- No other issue or regression was disclosed in PR #435's body for this screen — the batch cited
  a clean live run and self-clean, unlike some sibling batches (e.g. Account Mapping's Batch 6
  Line Item Type re-render gotcha) that hit and fixed a real live defect.

## Blockers -> resolution
- None disclosed in PR #435. No hard blockers recorded for this screen's conversion.

## Decisions
- Grid id reused the shared T2 constant `${OV_MANAGE_OBJECT_TABLE}` (resolves to
  `manage_object_nav_nav:form:T_data`) rather than a screen-local literal — same convention as
  Bank/Account, avoiding duplication across screens that share the same grid shape.
- The 2026-06-12 Playwright reference bundle (`playwright/ec_iud_customer.py`,
  `investigation/*.py`, `evidence/customer_*.png`) was left untouched by the RF conversion and
  is not rebuilt by this backfill — items 4/5 of the deliverable checklist are permanently
  waived for Bank-pattern work per Section H (2026-08-27), and this screen already had them from
  before that rule existed.

## Evidence
- Original (PR #435, 2026-08-23): live run 5/5 PASS, DB self-clean 0 residual (fresh connection),
  full dryrun 735/735, robocop 7 issues, filter wiring fired 5x in that run's output.xml.
- Backfill re-run (this session, 2026-08-28 — evidence capture only, no automation change):
  live run 5/5 PASS, full-tree dryrun 883/883 PASS (tree has grown since 2026-08-23), robocop
  still 7 issues (2 VAR02 + 5 DOC02, identical count), DB self-clean 0 residual (fresh
  connection), filter keyword fired 15x in this run's output.xml (`Find Customer Row By Filter`
  count across TC02-TC05). Raw artifacts:
  `evidence/rf_backfill_2026-08-28/{log.html,report.html,output.xml,results_summary.md}`.
- Legacy Playwright evidence (2026-06-12, unchanged): `evidence/customer_0[1-8]_*.png` +
  `evidence/customer_results.json`.
