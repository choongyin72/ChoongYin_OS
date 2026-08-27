# JOURNAL — Contract (CO.2016) OV-GM IUD

_Refreshed 2026-08-27 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 3)
to cover the 2026-08-26 Area-pattern conversion (PR #546), modeled on
`screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure. The original
2026-08-02 entry is kept below as history._

## Built
- **2026-08-02 (original build):** reusable OV-GM engine `py/ec_object_iud.py` + thin driver
  `py/contract_iud.py`; label-driven T3 `pageobjects/Configuration/Assets/Contract_Objects/
  contract_page.resource`; RF suite `tests/Configuration/Assets/Contract_Objects/contract_iud.robot`
  (4-TC, inline navigator, suite-level login). `verify_screen.py` -> OVERALL PASS (robocop 0,
  hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 8/8, DB residual 0).
- **2026-08-26 (PR #546, Area-pattern conversion):** rebuilt the T3 and suite to the full Area
  pattern — 5 TCs (clean-state/insert/update/find/delete), per-TC login/logout with dedicated
  `CONTRACT_EC_USER`/`CONTRACT_EC_PASS`, properties-file-driven insert/update/verify (5 new
  `testdata/contract_*.properties` files), explicit grid-filter wiring
  (`Find/Clear Contract Row By Filter`), navigator fill delegated to the shared T2
  `Apply Navigator From Properties`. Fixed test code changed from a per-run
  `AUTOTEST_CT_<timestamp>` to the fixed `AUTOTEST_CONTRACT` (confirmed absent before use).

## Done well
- Full I-U-D DB-verified vs `OV_CONTRACT` (insert Contract Name/End Date/Contract Year Start,
  update Contract Name, delete End=Start); self-clean 0 residual, both at PR #546's own merge and
  re-confirmed fresh by this backfill on 2026-08-27 (`AUTOTEST_CONTRACT` exact count = 0,
  `AUTOTEST%` prefix count = 0).
- The conversion correctly caught and fixed a wrong navigator value in its own task brief
  ("TS3 BU") against the real, already-proven value in the screen's own prior driver ("TS5 BU")
  instead of trusting the brief blindly — a direct application of the repo's
  no-guessing/verify-everything rule.
- Zero inline DB-verify calls left in the `.robot`/`.resource` files after the conversion — DB
  proof now comes from the mandatory live-run self-clean check (shared T2 `Verify Object Removed`)
  rather than a screen-local assertion, consistent with every other Area-pattern-converted screen.

## Done wrong / lessons
- The original 2026-08-02 SOW/README predated the JOURNAL/evidence/KB-map rule and PR #546's
  conversion — this backfill is the direct fix for that gap (owner decision 2026-08-27 retiring
  the 2026-08-23/26 lean waiver).
- End Date being MANDATORY on Insert (not just a delete-trigger field, as on most other OV-GM
  screens) and the extra mandatory Contract Year Start field are genuine, unusual traits of this
  specific screen — worth flagging so no future conversion of a "similar-looking" OV-GM screen
  assumes Contract's shape is the norm (same caution the repo's memory already records for
  Tract/External Location-style false-pattern-matches).

## Blockers -> resolution
- **Genuine branch-name collision (the real incident this backfill must capture honestly):**
  Contract's conversion agent and Contract Area's conversion agent were independently dispatched
  with the SAME worktree branch name, `feature/contract-area-pattern-conversion`. Contract's
  worktree was apparently created from a point that already included Contract Area's commit;
  pushing from Contract's worktree silently appended Contract's own commit onto Contract Area's
  branch/PR (#542), instead of creating Contract's own branch.
  - **Detection:** Contract's own agent noticed unexpected commit history in its worktree (a
    commit it did not author sitting underneath its own) — this was self-detected, not flagged by
    a human or a CI check.
  - **Self-fix (Contract's own side, done without escalation):** cherry-picked ONLY Contract's own
    commit onto a fresh branch off `origin/master` (`contract-conversion-fix`), resolving one
    `credentials.py` merge conflict by keeping only the `CONTRACT_EC_USER`/`CONTRACT_EC_PASS`
    lines and dropping the Contract Area lines that did not belong in this PR. Raised PR #546 from
    that clean branch.
  - **What Contract's agent could NOT fix itself:** PR #542 (Contract Area's own PR) still had
    Contract's commit appended on top of Contract Area's own commit. An attempted force-push to
    unwind PR #542's branch back to its pre-collision commit was BLOCKED by the environment's own
    safety guardrail against destructive rewrites of an already-published PR branch.
  - **Resolution:** required separate, owner-approved intervention — a force-push to restore PR
    #542's branch, carried out only after being disclosed to the owner first, outside the scope of
    Contract's own agent session. This is the correct order of operations per the repo's own
    "validate before destructive git" and "external system approval" rules: an agent that hits a
    guardrail on a destructive/shared-state fix should stop and escalate, not find a workaround.
  - **No data damage:** the collision was purely a git branch/PR bookkeeping issue — no live EC
    data or DB rows were affected by the collision itself; the flakiness noted below is unrelated
    and was caught independently via DB reads.
- **Transient UI-timing flakiness (unrelated to the collision):** the original PR #546 live run
  needed 3 attempts — the first two hit `Could not find active page`-class failures during
  AJAX-heavy navigator/grid redraws post-Update and post-Delete. A DB read after both flaky
  attempts already showed 0 residual rows, confirming the underlying business logic (including the
  delete) was correct both times and the flakiness was purely UI-timing, not a code defect. This
  backfill's own evidence-capture run (2026-08-27) hit the same flake class once (TC02-TC05 failed
  with `Could not find active page` on attempt 1); retried ONCE per the workorder's instruction and
  got a clean 5/5 on attempt 2 — no further retries taken, no grinding.

## Decisions
- Playwright driver `py/contract_iud.py` and its `investigation/recon.py` stay unchanged and
  permanently un-rebuilt for Area-pattern work — the Universal Screen Engine is the owner-decided
  replacement for hand-written Playwright drivers going forward (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  updated IN PLACE by PR #546, not duplicated — this backfill does not touch them again.
- The fixed test code `AUTOTEST_CONTRACT` (not per-run timestamped) is deliberate: it must be
  confirmed absent from `OV_CONTRACT` before first use, and TC05 (delete) must complete every run
  so the code stays free for the next run — same convention as every other Area-pattern-converted
  screen.

## Evidence
- Original 2026-08-02 build: `evidence/ct_0[1-5]_*.png` + `evidence/results.json` (Playwright 8/8,
  RF 4/4, `VERIFY-REPORT.md` OVERALL PASS).
- PR #546 conversion (2026-08-26): live RF 5/5 pass (third attempt, first two DB-confirmed clean
  despite UI-timing flakiness), full-tree dryrun 850/850, robocop 7 issues (parity with Area's own
  baseline), fresh-connection DB self-clean = 0 residual `AUTOTEST%` rows — all cited in PR #546's
  own body.
- This backfill (2026-08-27): `evidence/backfill_2026-08-27/` — dryrun 5/5, live run attempt 1
  (flake, disclosed) + attempt 2 (5/5 PASS, `log.html`/`report.html`/`output.xml` kept), fresh
  DB self-clean re-check (`db_selfclean_check_output.txt`: both counts 0), robocop re-check
  (`robocop_output.txt`: 7 issues, same as PR #546), hygiene PASS. See
  `evidence/backfill_2026-08-27/results_summary.md` for the full narrative.
