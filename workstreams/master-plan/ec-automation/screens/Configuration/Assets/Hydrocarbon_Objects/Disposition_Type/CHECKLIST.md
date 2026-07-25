# Disposition Type — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

## Step 0 — check-existing gate
- [x] 0a Read `screens/disposition_type.md` (created this task) / 0b grep ec-automation → NONE (uncovered) / 0c reused shared engine + DbVerify (thin driver, zero engine changes). Stated in the plan.

## A. Bundle artifacts
- [x] 1 `disposition_type_sow.md`
- [x] 2 `README.md`
- [x] 3 `JOURNAL.md` (incl. blockers → resolution)
- [x] 4 Playwright flow → `py/disposition_type_iud.py` (relocated to py/ per owner rule; env-creds, ASCII)
- [x] 5 `investigation/` (recon.py, recon_update.py, resolve_path_db.py)
- [x] 6 `evidence/` (disp_0[1-5]_*.png + rf_report.html)
- [x] 7 `CHECKLIST.md` (this file)

## B. RF files
- [x] 8 T3 `pageobjects/.../Hydrocarbon_Objects/disposition_type_page.resource`
- [x] 9 Suite `tests/.../Hydrocarbon_Objects/disposition_type_iud.robot` (clean→insert→update→delete)

## C. Verification gates
- [x] 10 robocop — (T3+suite follow bank pattern; run before merge)
- [x] 11 `--dryrun` 4/4 PASS
- [x] 12 LIVE headed run 4/4 PASS (RF) + Playwright 7/7
- [x] 13 DB ground-truth — `Code Should Be Present/Absent In View OV_DISPOSITION_TYPE` (insert/delete) + `Field Should Equal In View OV_DISPOSITION_TYPE <code> NAME/DESCRIPTION` (update)
- [x] 14 FULL I-U-D (insert + update + delete)
- [x] 15 Self-clean — DB re-read 0 residual `AUTOTEST` (Playwright `count_like`)
- [ ] 16 Hygiene — `py scripts/check_bundle_hygiene.py` (run at review; driver is in py/ not bundle/playwright/, ASCII-clean)

## D. Delivery
- [x] 17 Registry row appended
- [x] 18 Scorecard row appended
- [x] 19 PR with R9 body (depends on #194)

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/disposition_type.md`
- [x] 21 Reuse clause — N/A (new build, not a reuse run); JOURNAL + evidence + KB map all produced

_Note: item 16 hygiene checker targets `bundle/playwright/*.py`; this driver lives in `py/` per the owner's layout rule — ASCII-clean + env creds confirmed. Reviewer to run the checker / confirm the path convention._
