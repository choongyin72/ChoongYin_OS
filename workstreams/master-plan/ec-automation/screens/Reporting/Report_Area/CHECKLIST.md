# Report Area — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

## Step 0 — check-existing gate
- [x] 0a KB map created / 0b grep ec-automation → NONE (uncovered) / 0c reused shared engine + DbVerify (thin driver, zero engine changes).

## A. Bundle artifacts
- [x] 1 `report_area_sow.md`  · [x] 2 `README.md`  · [x] 3 `JOURNAL.md`
- [x] 4 Playwright flow → `py/report_area_iud.py` (py/ per owner rule; env-creds, ASCII)
- [x] 5 `investigation/` (recon.py, recon_update.py)  · [x] 6 `evidence/` (rpta_0[1-5]_*.png + rf_report.html)  · [x] 7 `CHECKLIST.md`

## B. RF files
- [x] 8 T3 `pageobjects/Reporting/report_area_page.resource`
- [x] 9 Suite `tests/Reporting/report_area_iud.robot` (clean→insert→update→delete)

## C. Verification gates
- [x] 10 robocop (follows bank pattern) · [x] 11 `--dryrun` 4/4 · [x] 12 LIVE 4/4 (RF) + Playwright 7/7
- [x] 13 DB ground-truth — `Code Should Be Present/Absent In View OV_REPORT_AREA` (insert/delete) + `Field Should Equal In View OV_REPORT_AREA <code> NAME` (update)
- [x] 14 FULL I-U-D  · [x] 15 Self-clean 0 residual (Playwright `count_like`)
- [ ] 16 Hygiene — `check_bundle_hygiene.py` (driver in py/, ASCII-clean; reviewer confirm)

## D. Delivery
- [x] 17 Registry row  · [x] 18 Scorecard row  · [x] 19 PR (R9 body; base master)

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/report_area.md`
- [x] 21 Reuse clause — N/A (new build); JOURNAL + evidence + KB map all produced

_Update = Name only (OV_REPORT_AREA has no Description column). Item 16 checker targets bundle/playwright/*.py; driver lives in py/ per owner rule — ASCII + env-creds confirmed._
