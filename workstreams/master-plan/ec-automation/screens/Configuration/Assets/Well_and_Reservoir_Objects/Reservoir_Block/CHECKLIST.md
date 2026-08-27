# Reservoir Block - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_This CHECKLIST was backfilled 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 10)
to reflect the CURRENT automation state - the screen was upgraded to the full Bank-pattern shape by
PR #466 (Batch 9, merged 2026-08-23), but this bundle's docs still described the earlier, superseded
2026-07-26 partial build until this backfill. No RF automation file was touched by this backfill._

## Step 0 - check-existing gate
- [x] **0a.** KB map exists (`ec-ui-knowledge/screens/reservoir_block.md`) - refreshed by this backfill, not re-scanned from zero.
- [x] **0b.** `grep -ril "reservoir_block" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` -> found; this is the ONLY implementation (RF T3/suite via PR #466, Playwright driver from the 2026-07-26 build) - reused/extended, not duplicated.
- [x] **0c.** Reused shared engine: T3 delegates to T2 `manage_object.resource` + T1 `common.resource` + `libraries/DbVerify.py`; zero shared-keyword changes in PR #466.

## A. Bundle artifacts - `screens/Configuration/Assets/Well_and_Reservoir_Objects/Reservoir_Block/`
- [x] **1.** `reservoir_block_sow.md` - rewritten this backfill to describe the current Bank-pattern shape.
- [x] **2.** `README.md` - rewritten this backfill; exact dryrun/live/DB-self-clean commands included.
- [x] **3.** `JOURNAL.md` - rewritten this backfill; covers both the 2026-07-26 original build and the 2026-08-23 Batch 9 conversion (real content pulled from PR #466's body), plus this backfill's own entry.
- [ ] **4.** Playwright driver - **N/A / pre-existing, untouched.** `py/reservoir_block_iud.py` predates the Bank-pattern conversion (built 2026-07-26) and is explicitly waived going forward per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (Universal Screen Engine replaces this role) - not rebuilt or re-verified by PR #466 or this backfill.
- [ ] **5.** `investigation/` - **N/A / pre-existing, untouched.** `investigation/recon.py` predates the conversion (2026-07-26); waived going forward per Section H, same reasoning as item 4.
- [x] **6.** `evidence/` - `evidence/backfill-2026-08-28/` added this backfill (dryrun N/A not needed here, live output.xml/log.html/report.html + 25 per-TC screenshots, all <2MB, ~1.8MB total); original `evidence/reservoir_block_0[1-5]_*.png` + `rf_report.html` from the 2026-07-26 build kept for history.
- [x] **7.** `CHECKLIST.md` - this file, rewritten this backfill.

## B. RF files - treeview-mirrored
- [x] **8.** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_page.resource` - rebuilt by PR #466 (2026-08-23) to the Bank/Berth shape; NOT touched by this backfill.
- [x] **9.** Suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_iud.robot` - rebuilt by PR #466 (5-TC shape); NOT touched by this backfill.

## C. Verification gates (real evidence, this backfill - 2026-08-28)
- [x] **10.** robocop - `py -m robocop check pageobjects/.../reservoir_block_page.resource tests/.../reservoir_block_iud.robot` -> exit 1, **9 issues** (8x DOC02 missing test-case documentation, 1x VAR02 unused variable). Matches PR #466's own cited baseline parity with the accepted `berth_iud.robot` exemplar - not a regression.
- [x] **11.** `--dryrun` - `robot --dryrun tests/.../reservoir_block_iud.robot` -> **5/5 PASS**, 0 fail.
- [x] **12.** LIVE run - `EC_HEADLESS=true robot tests/.../reservoir_block_iud.robot` -> **5/5 PASS** (TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete). Evidence in `evidence/backfill-2026-08-28/`.
- [x] **13.** DB ground-truth - fresh `oracledb` connection, `SELECT CODE FROM OV_RESV_BLOCK WHERE CODE LIKE 'AUTOTEST%'` -> `[]` (0 rows) after the live run, confirming insert->update->find->delete round-tripped through the real DB view, not just the UI.
- [x] **14.** FULL I-U-D scope - TC02 Insert + TC03 Update + TC05 Delete all present and passing (not I/D only).
- [x] **15.** Self-clean confirmed - same fresh-connection query as item 13, run AFTER the live run -> 0 residual `AUTOTEST%` rows in `OV_RESV_BLOCK`.
- [x] **16.** Hygiene PASS - `py scripts/check_bundle_hygiene.py` (from repo root) -> exit 0, `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (2 pre-existing warnings reported are in `Contract_Area/investigation/`, unrelated to this screen).

## D. Delivery
- [x] **17.** Registry row - `docs/ec_screen_registry.md` Reservoir Block row already reflects the Batch 9 conversion (MODIFIED by PR #466, not re-touched by this backfill).
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` Reservoir Block row already reflects the conversion (MODIFIED by PR #466).
- [x] **19.** PR - this backfill's PR uses the standard 6-field body (What was backfilled / Files added / DB ground-truth evidence / Self-clean confirmed / Rules applied / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/reservoir_block.md` - rewritten this backfill to describe the current Bank-pattern selectors/properties-file wiring (was describing the superseded 2026-07-26 build).
- [x] **21.** Reuse clause - this screen was already implemented (Step 0 found it); this backfill produced/refreshed JOURNAL (#3), evidence (#6), and KB map (#20) as required, on top of the already-passing tests from PR #466.

_Items 10-16 evidence cited above is from a real run executed 2026-08-28 for this backfill (dryrun +
one live confirmation), not restated unverified from PR #466 - though the results match PR #466's own
cited figures. The pre-existing `VERIFY-REPORT.md` in this bundle is from the 2026-07-26 build (4/4)
and is now superseded by the C-section evidence above; it is left in place for history rather than
deleted, per the append-only/no-silent-deletion convention._
