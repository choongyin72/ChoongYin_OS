# JOURNAL - Contract Inventory (CO.2054) OV-GM IUD

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 4)
to cover the 2026-08-26 Area-pattern conversion (PR #556), modeled on
`screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure. The original
2026-08-02 entry is kept below as history._

## Built
- **2026-08-02 (original build, PR #314):** reusable OV-GM engine `py/ec_object_iud.py` + thin
  driver `py/contract_inventory_iud.py`; label-driven T3
  `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource`; RF suite
  `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot` (4-TC, PROVEN-value
  navigator, suite-level login). `verify_screen.py` -> OVERALL PASS (robocop 0, hygiene 0, dryrun
  4/4, LIVE RF 4/4, Playwright 8/8, DB residual 0).
- **2026-08-26 (PR #556, Area-pattern conversion):** rebuilt the T3 and suite to the full Area
  pattern - 5 TCs (added TC04 Find), per-TC login/logout with `CONTRACT_INVENTORY_EC_USER`/
  `CONTRACT_INVENTORY_EC_PASS`, properties-file-driven insert/update/verify (5 new
  `testdata/contract_inventory_*.properties` files), explicit grid-filter wiring
  (`Find/Clear Contract Inventory Row By Filter`, 26 `Find Object Row By Filter` hits in
  `output.xml`), navigator fill delegated to the shared T2 `Apply Navigator From Properties` with
  ZERO shared-file changes needed. Fixed test code changed from a per-run `AUTOTEST_CI_<timestamp>`
  to the fixed `AUTOTEST_CONTRACT_INVENTORY` (confirmed absent from `OV_CONTRACT_INVENTORY` via a
  fresh `oracledb` connection before use).

## Done well
- Full I-U-D DB-verified vs `OV_CONTRACT_INVENTORY` (insert Contract Inventory Name/Code, update
  Contract Inventory Name, delete End=Start); self-clean 0 residual, confirmed via a fresh
  independent `oracledb` connection at PR #556's own merge.
- The conversion correctly re-verified the pre-existing registry note ("Business Unit -> Contract
  Area cascade") against a live mandatory-yellow DOM check instead of trusting the note as-written
  - it read as a genuine 2-level mandatory cascade, but the live check found only Business Unit
  (`C:1`) is genuinely mandatory-yellow+empty; Contract Area (`C:2`) stays optional even after
  `C:1` is filled. Both are still filled in the navigator properties file for behavioral parity
  with the already-proven prior scope, but the DISTINCTION between "genuinely mandatory" and
  "kept for parity" is now correctly documented - a direct application of the repo's
  no-guessing/verify-everything rule, and the same discipline the repo's memory records for
  Tract/External Location false-pattern-matches.
- Zero inline DB-verify calls left in `contract_inventory_iud.robot` after the conversion (grep-
  confirmed) - DB proof now comes from the mandatory live-run self-clean check (shared T2
  `Verify Object Removed`) rather than a screen-local assertion, consistent with every other
  Area-pattern-converted screen in this batch series.
- Field-reuse check done live before assuming a conflict: `objectForm` has no "Business
  Unit"/"Contract Area" field, so the navigator's own values and the form fields never collide.

## Done wrong / lessons
- The original 2026-08-02 SOW/README predated the JOURNAL/evidence/KB-map restoration rule and PR
  #556's conversion - this backfill is the direct fix for that gap (owner decision 2026-08-27
  retiring the 2026-08-23/26 lean waiver, Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- **This backfill task's own dispatch brief described a "detached-HEAD collision-recovery" story
  for Contract Inventory specifically.** That story was checked against PR #556's real body text,
  its commit message (`f2c3a0b4`), and its branch reflog (`feature/contract-inventory-area-
  pattern`) - none of the three contains any mention of a detached HEAD, a branch collision, or a
  push-to-new-remote-ref recovery. Per this repo's own no-guessing rule, that story is NOT written
  into this JOURNAL as fact. What IS a real, disclosed incident from this batch series is a
  **different** git/branch-name collision that happened to the sibling screen **Contract**
  (CO.2016, PR #546, same conversion wave: two agents independently used the same worktree branch
  name `feature/contract-area-pattern-conversion`, requiring a cherry-pick fix and, ultimately,
  owner-approved intervention on the OTHER PR, #542). It is documented in full in
  `screens/Configuration/Assets/Contract_Objects/Contract/JOURNAL.md`, not here - the brief for
  this task appears to have conflated Contract Inventory with Contract, a plausible mix-up given
  how similar the two screen names and PR numbers are, but not something to carry forward as this
  screen's own history without verification.
- The one genuine, disclosed collision-adjacent fact that DOES belong to PR #556 itself: the
  reviewer's own merge comment on PR #556 noted the branch's `credentials.py` hunk carried FOUR
  credential pairs (Contract Inventory's own, plus Pilot/Pipeline Segment/Property's) - a
  sibling-carry-over from a shared working state during concurrent conversions. The reviewer
  confirmed the final merged state was clean (exactly one pair per screen, values
  house-pattern-identical) but flagged it as "the same shared-checkout hazard class as the Split
  Key batch: isolated worktrees per parallel task, always." That is the real, disclosed
  operational lesson for THIS screen's PR - a credentials-file carry-over risk, not a git
  branch/HEAD collision.

## Blockers -> resolution
- No live-run blocker is recorded in PR #556's own body (live RF 5/5 on the first cited attempt,
  full-tree dryrun 878/878, zero collisions). See "Done wrong / lessons" above for the
  investigation into the (unconfirmed, and now ruled out) detached-HEAD story raised in this
  backfill task's own brief, and the real credentials.py carry-over the reviewer did disclose.
- This backfill's own evidence-capture run: see "Evidence" below for the actual result (pass/fail,
  retry count) of the one live re-run performed for this backfill.

## Decisions
- Playwright driver `py/contract_inventory_iud.py` and its `investigation/recon.py` stay unchanged
  and permanently un-rebuilt for Area-pattern work - the Universal Screen Engine is the
  owner-decided replacement for hand-written Playwright drivers going forward (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  updated IN PLACE by PR #556, not duplicated - this backfill does not touch them again.
- The fixed test code `AUTOTEST_CONTRACT_INVENTORY` (not per-run timestamped) is deliberate: it
  must be confirmed absent from `OV_CONTRACT_INVENTORY` before first use, and TC05 (delete) must
  complete every run so the code stays free for the next run - same convention as every other
  Area-pattern-converted screen.

## Evidence
- Original 2026-08-02 build: `evidence/ci_0[1-5]_*.png` + `evidence/results.json` (Playwright 8/8,
  RF 4/4, `VERIFY-REPORT.md` OVERALL PASS).
- PR #556 conversion (2026-08-26): live RF 5/5 pass, full-tree dryrun 878/878, robocop 7 issues
  (2 VAR02 + 5 DOC02, exact parity with Facility Class 1's own baseline), fresh-connection DB
  self-clean = 0 residual `AUTOTEST%` rows, 26 `Find Object Row By Filter` hits in `output.xml` -
  all cited in PR #556's own body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` - see that folder's own
  `results_summary.md` for the dryrun/live-run/DB-self-clean numbers actually captured by this
  task (real numbers, not copied from the PR #556 body).
