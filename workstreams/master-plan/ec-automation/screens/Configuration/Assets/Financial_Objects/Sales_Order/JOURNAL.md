# JOURNAL — Sales Order IUD

_Screen: Configuration > Assets > Financial Objects > Sales Order (plain OV manage-object, no
navigator). View `OV_PRODUCT_SALES_ORDER`. This JOURNAL was backfilled 2026-08-28 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 7; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`). Sales Order already had a `screens/` bundle predating the
lean rule (SOW + README + Playwright reference + investigation/ + evidence/, from the screen's
original Playwright build, 2026-06-11) — this backfill REFRESHES that bundle with the JOURNAL,
CHECKLIST, KB map, and a fresh evidence-capture run it never had, pulling real content from the
Bank-pattern conversion PR (#444, merged 2026-08-23), not inventing a narrative._

## Built

### Original Playwright build (pre-existing, 2026-06-11)
- `sales_order_sow.md` + `README.md` + `playwright/ec_iud_sales_order.py` (thin config over the
  shared Basic_Objects engine) + `investigation/` + `evidence/` (screenshots + `results.json`) —
  the screen's first-ever IUD bundle, predating both the Bank-pattern conversion and the lean
  waiver rule entirely. Left untouched by this backfill.

### Bank-pattern conversion (PR #444, merged 2026-08-23, Batch 5)
- Converted the RF side (`sales_order_page.resource` + `sales_order_iud.robot`) from the older
  hardcoded-field-id pattern to the label-driven, properties-file-driven, T2-consolidated "Bank
  pattern," mirroring Cost Object Mapping.
- Live recon resolved a real naming-based scope-mismatch concern flagged in
  `tmp/batch5_shared_findings.md` ("Sales Order" suggesting a possible document-header-plus-lines
  shape, like an invoice with line items) — confirmed live as a genuine nav-free manage-object OV
  (`NAV_DD_COUNT=0`, only the universal Date+GO as-at-date bar), the same outcome as Cost Object
  Mapping in Batch 4, not a scope mismatch.
- Confirmed live: Code label is screen-prefixed **"Product Sales Order Code"** (not generic
  "Code"); two mandatory reference dropdowns beyond Code/Name/Start Date — **Company** and
  **Field**, neither a cascade — filled with real literal option text (`Acme Chemicals` /
  `Apollo`, not `__FIRST__`, per the Batch 2 VAT Code round-trip gotcha); grid shows Product Sales
  Order Code/Name/Start Date/End Date (20+ pre-existing rows, e.g. `BU_0001`); fixed test code
  `AUTOTEST_SO`; explicit grid-filter wiring (`Find/Clear Sales Order Row By Filter`) included from
  day one.
- Files touched: `pageobjects/.../sales_order_page.resource` (rebuilt), `tests/.../sales_order_
  iud.robot` (rebuilt), 4 new `testdata/sales_order_*.properties` files, additive
  `SALES_ORDER_EC_USER`/`SALES_ORDER_EC_PASS` in `resources/credentials.py`, registry/scorecard
  rows and 3 standardization checklists updated.

### This backfill (2026-08-28)
- Added `JOURNAL.md` (this file), `CHECKLIST.md`, the KB selector map
  `ec-ui-knowledge/screens/sales_order.md`, and `evidence/backfill_2026-08-28/` (fresh dryrun +
  live re-run captured as evidence of the already-proven suite — no automation code touched).
- Reviewed and left as-is: `sales_order_sow.md` and `README.md` already existed from the original
  2026-06-11 Playwright build and already describe the screen's classification/mandatory
  fields/DB view correctly — `README.md`'s run commands were Playwright-only, so this backfill
  ADDS the RF run commands rather than replacing the file (see README.md's new "Run — Robot
  Framework" section).

## Done well
- Full I-U-D DB-verified vs `OV_PRODUCT_SALES_ORDER` (insert Name/Company/Field, update Name,
  delete End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb connection both
  by PR #444's own body and independently re-confirmed by this backfill.
- Real literal dropdown option text used for insert, not `__FIRST__` — avoids the Batch 2 VAT Code
  round-trip-verify gotcha (a `__FIRST__` sentinel never resolves to literal text for the
  post-insert form-compare check).
- Explicit grid-filter wiring (`Find/Clear Sales Order Row By Filter`) delegating to the shared T2
  keywords, included from day one, not bolted on later — confirmed fired 5x in this backfill's own
  fresh live output.xml (matches PR #444's own cited count).
- This backfill's own live run passed 5/5 on the FIRST attempt, no flake, no retry needed.

## Done wrong / lessons
- No regressions or wrong turns disclosed in PR #444's body for the original conversion.
- No flake or defect encountered during this backfill's evidence-capture run either — dryrun and
  live both passed clean on the first try (unlike some sibling backfills in this same work order
  that hit stray-process flakes; disclosed here for completeness, not smoothed over: none occurred
  here).

## Blockers -> resolution
- None. No hard blockers during the original conversion or this backfill; no data damage.

## Decisions
- Playwright bundle (`playwright/ec_iud_sales_order.py` + `investigation/`) is kept AS-IS from the
  original 2026-06-11 build — per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, no NEW Playwright
  work is done for Bank-pattern conversions (the Universal Screen Engine is the owner-decided
  replacement going forward), but a pre-existing driver from before the conversion is not deleted
  or touched, only left in place as a historical reference.
- The RF suite (`sales_order_page.resource` + `sales_order_iud.robot`) is the current, maintained
  automation for this screen; the Playwright driver is a historical reference only.
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original Playwright build (2026-06-11): `evidence/sales_order_0[1-8]_*.png` +
  `evidence/sales_order_results.json`.
- Bank-pattern conversion (PR #444, 2026-08-23): live RF run **5/5 pass**, DbVerify assertions
  `Code Should Be Present In View OV_PRODUCT_SALES_ORDER AUTOTEST_SO` (TC02) and
  `Code Should Be Absent In View OV_PRODUCT_SALES_ORDER AUTOTEST_SO` (TC05), fresh-connection
  self-clean 0 residual rows, filter-fired grep = 5, robocop 7 issues (2 VAR02 + 5 DOC02, at/below
  baseline), full `tests/` dryrun 745/745 — all cited in the PR body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless, same 3 files, first
  attempt, no retry), plus `summary.json` documenting the DB self-clean result (`OV_PRODUCT_
  SALES_ORDER`: 0 rows for `AUTOTEST_SO`, 0 residual `AUTOTEST%`, fresh connection), the
  re-confirmed 5-hit filter-fired grep, the re-confirmed robocop parity (7 issues, same shape as
  PR #444's own cited count), and `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS`.
