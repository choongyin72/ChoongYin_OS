# JOURNAL - Unit Agreement IUD

_Screen: Configuration > Assets > Royalty Objects > Unit Agreement (RC.0055), OV, Bank family (no
navigator, date-effective). View `OV_UNIT_AGR` (base `UNIT_AGR`, app `EC_REVN`). This screen never
had a JOURNAL before this backfill. Added 2026-08-28 (deliverable backfill,
`docs/lean-deliverable-backfill-workorder.md` Batch 8) to cover the 2026-08-23 Bank-pattern
conversion (PR #446), modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s
structure. Content below is pulled from PR #446's own body/commit history, not invented._

## Built
- **2026-06-25 (original build):** freestyle Playwright IUD walkthrough
  (`playwright/ec_iud_unit_agreement.py`) + hand-written, hardcoded-field-id RF T3/suite
  (`unit_agreement_page.resource` / `unit_agreement_iud.robot`), per-run test code
  `AUTOTEST_UA_<run>`.
- **2026-08-23 (PR #446, Bank-pattern conversion, Batch 5):** rewrote the T3
  (`pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource`, +158/-65 lines)
  and suite (`tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot`, +52/-41 lines)
  to the label-driven, properties-file-driven, T2-consolidated Bank pattern (mirrors
  `bank_page.resource`) - per-TC Login/Logout, 5-TC business-narrative structure (TC01 clean state,
  TC02 insert, TC03 update, TC04 find, TC05 delete), with explicit grid-filter wiring
  (`Find/Clear Unit Agreement Row By Filter`) included from day one. Added 4 new
  `testdata/unit_agreement_{insert,update,form_verify,grid_verify}.properties` files and an
  additive `UNIT_AGREEMENT_EC_USER`/`UNIT_AGREEMENT_EC_PASS` pair in `resources/credentials.py`.
  Test code changed from the original per-run `AUTOTEST_UA_<run>` to the fixed `AUTOTEST_UA`.

## Done well
- Full I-U-D DB-verified vs `OV_UNIT_AGR` (insert Unit Agreement Name/Code, update Unit Agreement
  Name, delete End=Start); PR #446's own body cites live 5/5 pass and 0 residual `AUTOTEST_UA` rows
  via a fresh `oracledb` connection after the run.
- Live recon (2026-08-23) confirmed real field labels BEFORE assuming from the pre-conversion SOW:
  "Unit Agreement Code"/"Unit Agreement Name" are screen-prefixed (not the generic "Code"/"Name"
  Bank itself uses) - a live objectForm/updateAttributes ECCell label scan, via a throwaway RF
  script deleted before commit, confirmed `updateAttributes` exposes exactly 3 labels (Unit
  Agreement Code read-only, Unit Agreement Name, Comments); Start Date/End Date live only in
  `objectForm`/`objectdates`.
- Confirmed the view/slug mismatch live rather than assuming `unit_agreement` maps directly to a
  same-named view: the real view is `OV_UNIT_AGR` on base table `UNIT_AGR` - `DbVerify` calls cite
  it explicitly.
- Confirmed the test code `AUTOTEST_UA` was free in `OV_UNIT_AGR` via a fresh DB connection before
  first use.
- Zero shared-file edits - reused T2's existing consolidated keywords
  (`resources/manage_object.resource`) and T1 (`resources/common.resource`) as-is.

## Done wrong / lessons
- This screen's documentation lagged its automation: the RF suite, registry row, and scorecard row
  were already complete and merged from PR #446 (2026-08-23), but no JOURNAL.md or CHECKLIST.md
  ever existed for it, and the SOW/README still described the PRE-conversion (2026-06-25) shape -
  exactly the gap Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (owner decision 2026-08-27)
  retired the lean waiver to fix. This backfill is the direct remedy.
- The pre-conversion SOW's Section 2.2 field-id table (generic ids, no label constants) describes
  the OLD driver, not the current T3 - kept as history in the SOW under a new Section 0, not
  deleted, per this repo's no-silent-deviation convention.

## Blockers -> resolution
- No live-run blocker is recorded in PR #446's own body (the PR's cited evidence is a clean 5/5
  pass with the DbVerify assertions `Code Should Be Present In View ov_unit_agr <code>` (TC02) and
  `Code Should Be Absent In View ov_unit_agr <code>` (TC05), plus a full `tests/` dryrun 745/745).
- This backfill's own evidence-capture run (2026-08-28): dryrun 5/5, live 5/5 on the first attempt
  - no retry needed, no browser/timeout error to disclose. See "Evidence" below.

## Decisions
- Playwright driver `playwright/ec_iud_unit_agreement.py` stays unchanged and permanently
  un-rebuilt for Bank-pattern work - the Universal Screen Engine is the owner-decided replacement
  for hand-written Playwright drivers going forward (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  updated by PR #446 already - this backfill does not touch them again.
- The fixed test code `AUTOTEST_UA` (not per-run) is deliberate: it must be confirmed absent from
  `OV_UNIT_AGR` before first use, and TC05 (delete) must complete every run so the code stays free
  for the next run - same convention as every other Bank-pattern-converted screen.

## Evidence
- Original 2026-06-25 build: `evidence/unit_agreement_tc0[1-4]_*.png` (pre-conversion Playwright
  walkthrough screenshots).
- PR #446 conversion (2026-08-23): live RF 5/5 pass, full `tests/` dryrun 745/745, DbVerify
  assertions `Code Should Be Present In View ov_unit_agr <code>` / `Code Should Be Absent In View
  ov_unit_agr <code>`, fresh-connection DB self-clean = 0 residual `AUTOTEST_UA` rows, 5
  `Find Unit Agreement Row By Filter` hits in `output.xml` - all cited in PR #446's own body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` - dryrun 5/5, robocop 11 issues (6
  VAR02 + 5 DOC02), live 5/5 (attempt 1, no retry), DB self-clean 0/0 before+after (fresh
  `oracledb` connection), 15 `Find Object Row By Filter` hits in this run's own `output.xml`,
  hygiene PASS. See that folder's own `results_summary.md` for the full breakdown (real numbers
  captured by this task, not copied from PR #446's body).
