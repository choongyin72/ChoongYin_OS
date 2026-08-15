# IUD Task - Deliverable Checklist (Financial Item Definition)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. Playwright-side items are backed by a fresh live
run (`AUTOTEST_FID_006`, 2026-08-16); RF-side items are deliberately deferred - see note below.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** No `ec-ui-knowledge/screens/financial-item-definition.md` existed before this bundle - now added (#20).
- [x] **0b.** Existing work found (driver + design doc narrative from Phase 4 Pilot 1, never
      packaged) - REUSED/EXTENDED (fresh live re-verification), not rebuilt in parallel.
- [x] **0c.** Uses the Universal Screen Engine (`py/engine.py`) directly - no shared-file changes needed.

## A. Bundle artifacts
- [x] **1.** `financial_item_definition_sow.md`.
- [x] **2.** `README.md`.
- [x] **3.** `JOURNAL.md` (includes the reviewer follow-up disclosure).
- [x] **4.** `playwright/ec_iud_financial_item_definition.py` - delegates to `py/financial_item_definition_iud.py`.
- [x] **5.** `investigation/` - 4 real recon scripts (menu-path lookup, treeview tooltip check, mandatory-field confirmation, DB residual verify).
- [x] **6.** `evidence/` - 7 screenshots, fresh 2026-08-16 run.
- [x] **7.** This file.

## B. RF files - DEFERRED, not built
- [ ] **8.** T3 page object - **deferred.** This screen was built via the Universal Screen Engine
      (`engine.py`), not the classic T2/T3 pattern. Will revisit once RF can properly adopt the new
      engine implementation directly (see PR #379 discussion) rather than duplicating a
      hand-written T3 that would become redundant.
- [ ] **9.** Suite - **deferred**, same reason as #8.

## C. Verification gates
- [ ] **10.** robocop clean - N/A, no RF files exist yet (deferred, see #8/#9).
- [x] **16.** Hygiene PASS - `check_bundle_hygiene.py` exit=0 (applies to the Playwright/Python side, which does exist).
- [ ] **11.** `--dryrun` - N/A, no RF suite exists yet (deferred).
- [ ] **12.** LIVE RF suite - N/A, no RF suite exists yet (deferred).
- [x] **13.** DB ground-truth - live driver run + direct DB query, both confirm `AUTOTEST_FID_006`
      inserted/updated/deleted correctly against `OV_FINANCIAL_ITEM`.
- [x] **14.** FULL I-U-D scope - Insert + Update + Delete all proven, live, via the Playwright driver.
- [x] **15.** Self-clean confirmed - 0 residual for `AUTOTEST_FID_006` after delete.

## D. Delivery
- [x] **17.** Registry row appended to `docs/ec_screen_registry.md`.
- [x] **18.** Scorecard row appended to `docs/automation-scorecard.md`.
- [x] **19.** PR (#379) with R9 6-field body; R8 sync; not self-merged.

## E. Knowledge base
- [x] **20.** `ec-ui-knowledge/screens/financial-item-definition.md`.
- [x] **21.** Reuse clause - Step 0 found existing (unpackaged) work; JOURNAL + evidence + KB map all produced in this pass.

## Note on the RF gap (owner-confirmed 2026-08-16)
Owner decision: proceed with this CHECKLIST in the standard shape, but leave items 8-9 (and the
gates that depend on them, 10-12) explicitly deferred rather than built now or faked as passing.
This will be revisited once the RF layer can properly call into the Universal Screen Engine
directly (architecture discussed in PR #379's review thread), instead of duplicating a
hand-written T3 for a screen the engine already drives generically.
