# Calculation Group Context - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (batch 9) - Section H retired the
2026-08-23/26 lean waiver (Section G) that had allowed PR #455's Bank-pattern conversion to skip items
1/3/4/5/6/7/20. Items 4 (Playwright driver) and 5 (investigation/) stay waived permanently (Universal Screen
Engine replaces that role). Items 1/2/3/6/7/20 are restored below with real evidence. No automation file
(pageobjects/tests/testdata/py driver) was touched by this backfill._

## Step 0 - check-existing gate
- [x] 0a KB map existed (`ec-ui-knowledge/screens/calculation_group_context.md`), read and refreshed to
      reflect the PR #455 conversion (was still describing the pre-conversion 2026-07-26 state).
- [x] 0b `grep -ril "calculation_group_context" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> found the existing 2026-07-26 build + PR #455's conversion. REUSED, not duplicated.
- [x] 0c Reused shared engine + T2 (`resources/manage_object.resource`) + T1 (`resources/common.resource`) +
      `libraries/DbVerify.py` + `libraries/PropertiesReader.py` - unchanged by this backfill.

## A. Bundle artifacts
- [x] 1 `calculation_group_context_sow.md` - updated to describe the current PR #455 Bank-pattern shape
      (classification, grid id, mandatory fields, fixed test code, dev story from the real PR #455 body).
- [x] 2 `README.md` - updated with exact dryrun/live/DB-self-clean commands.
- [x] 3 `JOURNAL.md` - appended a `2026-08-23 - PR #455` entry (built/done-well/done-wrong/decisions/evidence,
      sourced from `gh pr view 455`) and a `2026-08-28` backfill entry.
- [ ] 4 Playwright flow -> **N/A, permanently waived** (Section H: Universal Screen Engine replaces this role
      for Bank-/Area-pattern conversions going forward). Pre-existing `py/calculation_group_context_iud.py`
      left untouched, still referenced from README for context.
- [ ] 5 `investigation/` -> **N/A, permanently waived** (same reason as item 4). Pre-existing `recon.py` left
      untouched.
- [x] 6 `evidence/` - pre-existing `calculation_group_context_0[1-5]_*.png` + `rf_report.html` (2026-07-26
      build) kept; added `evidence/2026-08-28-backfill/` (this backfill's dryrun summary + live run
      log.html/report.html/screenshots).
- [x] 7 `CHECKLIST.md` (this file) - refreshed with real ticks/evidence for the current state.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8 T3 `pageobjects/Configuration/Assets/Calculation_Objects/calculation_group_context_page.resource` -
      full Bank-pattern shape since PR #455 (properties-driven insert/update/verify + explicit grid-filter
      wiring, label-driven field resolution kept).
- [x] 9 Suite `tests/Configuration/Assets/Calculation_Objects/calculation_group_context_iud.robot` - 5 TCs
      (clean-state, insert, update, find, delete), per-TC login/logout, fixed test code `AUTOTEST_CGC_BANK`.

## C. Verification gates - re-run for this backfill, real command output cited
- [x] 10 robocop parity - `py -m robocop check` on the T3+suite -> **13 issues**, all DOC02 (missing
      `[Documentation]` on TC01-05); confirmed identical count/class to `bank_iud.robot`'s own accepted
      baseline (also 13 DOC02) - no new issue class introduced by this or the PR #455 conversion. (The
      original 2026-07-26 pre-conversion JOURNAL cited "robocop 0" against a 4-TC suite with no per-TC
      Documentation requirement flagged at the time; PR #455 added TC04 and the current robocop config now
      flags this baseline DOC02 pattern across the whole Bank family - not a regression specific to this
      screen.) See `evidence/2026-08-28-backfill/dryrun-summary.txt`.
- [x] 11 `--dryrun` **5/5 PASS** - `py -m robot --dryrun ... calculation_group_context_iud.robot` (2026-08-28
      re-run). Output: `Workplaces/calculation-group-context-backfill/dryrun/output.xml`.
- [x] 12 LIVE RF run **5/5 PASS** - `EC_HEADLESS=true py -m robot ... calculation_group_context_iud.robot`
      (2026-08-28 re-run, real EC environment, one attempt, no retry needed). Evidence:
      `evidence/2026-08-28-backfill/log.html` + `report.html` + per-TC screenshots.
- [x] 13 DB ground-truth - `Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object Found`/
      `Verify Object Removed` against `OV_CALC_GRP_CONTEXT` (all fired during the live run, all PASS).
      Independently re-confirmed via a **fresh** oracledb connection after the run:
      `SELECT COUNT(*) FROM OV_CALC_GRP_CONTEXT WHERE CODE = 'AUTOTEST_CGC_BANK'` = **0**.
- [x] 14 FULL I-U-D - TC02 Insert, TC03 Update, TC05 Delete all present and passed (plus TC01 clean-state,
      TC04 Find).
- [x] 15 Self-clean confirmed - 0 residual `AUTOTEST_CGC_BANK` rows via the fresh connection above.
- [x] 16 Hygiene PASS - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded creds, ASCII
      clean, no CHECKLIST/VERIFY-REPORT contradiction for this bundle). One unrelated WARN reported for a
      different screen (Contract Area's `investigation/live_recon_contract_area.py`) - not this bundle, not
      touched by this task.

## D. Delivery (pre-existing, unchanged by this backfill)
- [x] 17 Registry row - `docs/ec_screen_registry.md` already carries the PR #455 conversion row (updated at
      PR #455's merge, 2026-08-23) - not re-appended by this backfill (no new build to register).
- [x] 18 Scorecard row - `docs/automation-scorecard.md` already carries the corresponding row from PR #455.
- [x] 19 PR - this backfill's own PR (branch `docs/calculation-group-context-backfill-artifacts`), standard
      6-field body, base branch master, never self-merged.

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/calculation_group_context.md` - refreshed to describe the current
      PR #455 Bank-pattern shape (grid-filter keywords, fixed test code, dedicated credentials) instead of
      the stale 2026-07-26 pre-conversion description.
- [x] 21 Reuse clause - satisfied: JOURNAL + evidence + KB map all refreshed for the reused/converted screen,
      not left at "tests still pass" alone.

_Section H scope note: this is a documentation/evidence backfill, not a rebuild. No pageobjects/tests/
testdata/py file was created, deleted, or modified by this task - only the `screens/.../Calculation_Group_
Context/` bundle and `ec-ui-knowledge/screens/calculation_group_context.md`._
