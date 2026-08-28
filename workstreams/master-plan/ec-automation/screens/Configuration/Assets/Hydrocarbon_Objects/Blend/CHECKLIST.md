# Blend - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates + Section H)

_Refreshed 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md` Batch 9) to reflect the
2026-08-23 Bank-pattern conversion (PR #457) that superseded the 2026-07-26 partial build this
checklist previously described. No RF/Playwright automation was touched by this refresh._

## Step 0 - check-existing gate
- [x] 0a KB map existed (`ec-ui-knowledge/screens/blend.md`, 2026-07-26; refreshed 2026-08-28) -
      0b grep `ec-automation` for `blend_page.resource` -> only this build (confirmed 2026-08-28) -
      0c PR #457 reused shared T2 (`Find/Clear Object Row By Filter`, `Insert/Update Object From
      Properties`, `Verify Object Insert Exists/Form Record/Found`) - zero shared T1/T2 changes.

## A. Bundle artifacts
- [x] 1 `blend_sow.md` - refreshed 2026-08-28 to describe the current 5-TC Bank-pattern shape.
- [x] 2 `README.md` - refreshed 2026-08-28 with current run commands + both build eras' evidence.
- [x] 3 `JOURNAL.md` - refreshed 2026-08-28; 2026-08-23 (PR #457) and 2026-08-28 backfill entries
      added, pulled from PR #457's real body (no invented content).
- [ ] 4 Playwright flow -> `py/blend_iud.py` - **pre-existing from 2026-07-26 build, NOT rebuilt**;
      waived going forward per Section H (item 4 stays waived - Universal Screen Engine replaces
      this role). Left as-is, untouched.
- [ ] 5 `investigation/` (recon.py) - **pre-existing from 2026-07-26, NOT rebuilt**; waived going
      forward per Section H (item 5 stays waived). Left as-is, untouched.
- [x] 6 `evidence/` - original `blend_0[1-5]_*.png` + `rf_report.html` (2026-07-26, 4-TC) kept, plus
      `blend_backfill_2026-08-28_output.xml`/`_log.html`/`_report.html` + one `_verify.png`
      screenshot per TC from a fresh live 5/5 re-run (2026-08-28, this backfill).
- [x] 7 `CHECKLIST.md` - this file.

## B. RF files
- [x] 8 T3 `pageobjects/Configuration/Assets/Hydrocarbon_Objects/blend_page.resource` -
      properties-file-driven, grid-filter-wired (PR #457, 2026-08-23); label-driven for form
      fields, hardcoded (by design, documented) for the delete End Date field.
- [x] 9 Suite `tests/Configuration/Assets/Hydrocarbon_Objects/blend_iud.robot` - 5-TC pattern
      (TC01 clean-state / TC02 insert / TC03 update / TC04 find / TC05 delete).

## C. Verification gates
- [x] 10 robocop - exit=1, 7 issues, all DOC02 (missing `[Documentation]` on TC04/TC05), advisory
      class only - same profile PR #457 cited (exit=1, no new issue categories) - re-run 2026-08-28.
- [x] 11 `--dryrun` - screen-scoped 5/5 pass (2026-08-28 re-run); full-tree 753/753 pass (PR #457,
      2026-08-23).
- [x] 12 LIVE headless run - 5/5 pass, first attempt (2026-08-28 re-run,
      `evidence/blend_backfill_2026-08-28_output.xml`); PR #457 also cites 5/5 first attempt.
- [x] 13 DB ground-truth - `Code Should Be Present/Absent In View OV_BLEND` (insert/delete) +
      `Field Should Equal In View` equivalent screen-level checks (update, via `Verify Object Form
      Record`); confirmed absent via `DbVerify.code_should_be_absent_in_view("OV_BLEND",
      "AUTOTEST_BLEND")` on a fresh connection, 2026-08-28.
- [x] 14 FULL I-U-D - Insert (TC02) + Update (TC03) + Delete (TC05) all present, plus Find (TC04)
      and clean-state (TC01).
- [x] 15 Self-clean - 0 residual `AUTOTEST_BLEND` rows in `OV_BLEND`, confirmed via a fresh Python
      DB connection after the 2026-08-28 live re-run.
- [x] 16 Hygiene - `python scripts/check_bundle_hygiene.py` exit=0 PASS, 2026-08-28 re-run.

## D. Delivery
- [x] 17 Registry row - `docs/ec_screen_registry.md` (already correct from the PR #457 merge;
      not modified by this backfill).
- [x] 18 Scorecard row - `docs/automation-scorecard.md` (already correct from the PR #457 merge;
      not modified by this backfill).
- [x] 19 PR - this backfill's PR follows the standard R9-style body (What backfilled / Files added
      / Base branch = master); never self-merged.

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/blend.md` - refreshed 2026-08-28 to reflect the current
      Bank-pattern automation (grid-filter selectors, 5-TC, `Blend Code`/`Blend Name` labels) and
      today's last-verified date.
- [x] 21 Reuse clause - satisfied: JOURNAL + evidence + KB map all refreshed with real content from
      PR #457, not left describing the superseded build.

_Section H (2026-08-27, owner decision): items 1/2/3/6/7/20 restored and produced above; items 4/5
stay permanently waived (pre-existing driver/recon kept as-is, not rebuilt or re-verified)._
