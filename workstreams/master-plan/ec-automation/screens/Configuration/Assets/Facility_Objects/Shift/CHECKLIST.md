# Shift - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 4) - Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23/26 lean waiver for Bank-/
Area-pattern work (except items 4/5, the Playwright bundle, which stays permanently waived)._

## Step 0 - check-existing gate
- [x] 0a - KB map `ec-ui-knowledge/screens/shift.md` existed (from the 2026-07-31 build);
      read and refreshed for this backfill, not re-scanned from scratch.
- [x] 0b - `grep -ril "shift_page.resource" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> the one existing implementation only (this bundle). No parallel copy.
- [x] 0c - Existing implementation reused as-is (shared T2 `Apply Navigator From Properties` +
      `manage_object.resource`); no rebuild.

## A. Bundle artifacts - `screens/Configuration/Assets/Facility_Objects/Shift/`
- [x] 1. `shift_sow.md` - refreshed to describe the Area-pattern (PR #547) structure + dev
      story pulled from PR #547's real body + the long-path incident.
- [x] 2. `README.md` - refreshed with the 5-TC shape + exact dryrun/live/DB-self-clean commands.
- [x] 3. `JOURNAL.md` - refreshed, modeled on Bank's JOURNAL.md structure, with the real
      2026-07-31 build, PR #547 conversion, and 2026-08-26 long-path incident -> resolution.
- [ ] 4. Playwright driver - **N/A, permanently waived** (Section H: items 4/5 stay waived for
      Bank-/Area-pattern work; the Universal Screen Engine supersedes hand-written Playwright
      drivers). `py/shift_iud.py` (pre-existing) left untouched.
- [ ] 5. `investigation/` - **N/A, permanently waived** (same Section H carve-out as item 4).
      Pre-existing `investigation/` folder in this bundle left untouched.
- [x] 6. `evidence/` - `evidence/rf_backfill_2026-08-28/` added: `log.html`/`report.html`/
      `output.xml` + per-TC-step screenshots from a real live 5/5 run, plus
      `results-summary.md` citing every command and its output. Pre-existing 2026-07-31
      `evidence/sh_0[1-5]_*.png` left in place (documents the prior 4-TC shape).
- [x] 7. `CHECKLIST.md` - this file.

## B. RF files - pre-existing, untouched by this backfill
- [x] 8. T3 `pageobjects/Configuration/Assets/Facility_Objects/shift_page.resource` (Area-
      pattern shape, PR #547; label-driven except the documented `${SHIFT_DEL_ENDDATE}`
      hardcoded id, same rationale as Area's/Facility Class 1's own).
- [x] 9. Suite `tests/Configuration/Assets/Facility_Objects/shift_iud.robot` (5 TCs: Verify
      Clean State / Insert / Update / Find / Delete, each with its own Login/Logout).

## C. Verification gates - re-run 2026-08-28 for this backfill (evidence capture, not a rebuild)
- [x] 10. robocop - `py -m robocop check pageobjects/.../shift_page.resource tests/.../shift_iud.robot`
      -> **7 issues found, exit=0** (DOC02-only "missing test-case documentation" warnings,
      non-fatal; no RF file was touched by this backfill, so this is the pre-existing shape,
      not a regression).
- [x] 11. `--dryrun` - single-suite: **5/5 PASS**. Full-tree (`robot --dryrun tests/`):
      **883/883 PASS**, 0 regression.
- [x] 12. LIVE headless run (`EC_HEADLESS=true robot tests/.../shift_iud.robot`) -
      **5/5 PASS**, first attempt, no retry needed.
- [x] 13. DB ground-truth - fresh `oracledb` connection (`localhost:1521/ORCL`, `ECKERNEL_EC`),
      run AFTER the live suite: `SELECT COUNT(*) FROM OV_SHIFT WHERE CODE = 'AUTOTEST_SHIFT'`
      = 0; `... WHERE CODE LIKE 'AUTOTEST%'` = 0. (Suite itself is pure-screen-verify per the
      Area-pattern convention; the DB check for TC05 Delete lives inside the shared T2
      `Verify Object Removed` keyword, confirmed present in `shift_page.resource`'s
      "Verify Shift Record Removed" wrapper.)
- [x] 14. FULL I-U-D scope - Insert (TC02) + Update (TC03) + Delete (TC05) all present and
      passed, plus TC01 clean-state and TC04 Find.
- [x] 15. Self-clean confirmed - 0 residual `AUTOTEST_SHIFT`/`AUTOTEST%` rows in `OV_SHIFT`
      after the live run (item 13).
- [x] 16. Hygiene - `py scripts/check_bundle_hygiene.py` (repo-root, whole-repo scan) ->
      **RESULT: PASS** - no hardcoded creds (R16) / pure ASCII (R20) / no CHECKLIST-vs-
      VERIFY-REPORT contradiction found for Shift.

## D. Delivery
- [x] 17. Registry row - already present, updated by PR #547 (`docs/ec_screen_registry.md`
      line for Shift describes the Area-pattern conversion); no further change needed by this
      backfill (doc-only addition, no re-append).
- [x] 18. Scorecard row - already present, updated by PR #547 (`docs/automation-scorecard.md`
      "Shift (OV-GM, CO.0224)" row); no further change needed by this backfill.
- [x] 19. PR - this backfill's own PR (branch `docs/shift-backfill-artifacts`), 6-field body,
      base = master, never self-merged.

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/shift.md` - refreshed: last-verified date
      updated to 2026-08-28, selectors cross-checked against the actual PR #547 page object
      (shared T2 navigator keyword, per-TC login, 5 TCs) rather than the stale 2026-07-31
      bespoke-driver description.
- [x] 21. Reuse clause - satisfied: this backfill (a reuse/documentation pass over an already-
      merged, already-working conversion) produced JOURNAL (#3), evidence (#6), and KB map
      (#20) refreshes, not tests-only.

---
_Gates 10-16 re-run live for this backfill on 2026-08-28; citations above are the actual
command output, not carried over from PR #547's numbers (those are cited separately, dated,
in JOURNAL.md and shift_sow.md's dev-story section)._
