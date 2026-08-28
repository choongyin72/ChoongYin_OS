# JOURNAL — Royalty Depositor IUD

_Screen: Configuration > Assets > Royalty Objects > Royalty Depositor (RC.0052), OV
date-effective. View `OV_ROYALTY_DEPOSITOR`._
_This JOURNAL backfills PR #448's real conversion narrative (merged 2026-08-23, Batch 5 of the
Bank-pattern conversion project) — the bundle predated the JOURNAL rule. Backfilled 2026-08-28
per `docs/lean-deliverable-backfill-workorder.md` Batch 8 (owner decision 2026-08-27 retiring the
Section G lean waiver)._

## Built (PR #448, 2026-08-23)
- Converted the older hardcoded-field-id IUD driver to the label-driven, properties-file-driven,
  T2-consolidated **Bank pattern** (mirrors `bank_page.resource`/`state_page.resource`), including
  explicit grid-filter wiring from day one.
- Rebuilt `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource`
  (160 additions / 66 deletions) and
  `tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot` (56/39, per-TC
  login/logout, 5 TCs).
- Added 4 new properties files: `testdata/royalty_depositor_{insert,update,form_verify,grid_verify}.properties`.
- Additive credentials: `ROYALTY_DEPOSITOR_EC_USER`/`_PASS` in `resources/credentials.py`.
- Updated `docs/ec_screen_registry.md`, `docs/grid-filter-standardization-checklist.md`,
  `docs/automation-scorecard.md`.
- No shared-file edits — reused T2 `resources/manage_object.resource` and T1
  `resources/common.resource` as-is.

## Done well
- Recon-first, no guessing: live DOM scan of `objectForm`/`updateAttributes` labels and
  `MandatoryCellStyle` classes before writing any config — found the screen uses
  SCREEN-PREFIXED labels ("Royalty Depositor Code"/"Royalty Depositor Name") and a much richer
  optional field set than the prior driver ever used; kept field scope unchanged (no scope
  expansion).
- Full I-U-D DB-verified against `OV_ROYALTY_DEPOSITOR`: insert `Code Should Be Present In View`
  (TC02), delete via `Verify Object Removed` (TC05). Fresh independent oracledb connection after
  the full suite confirmed 0 residual `AUTOTEST_ROYALTY_DEP` rows.
- `output.xml` grep confirmed `Find Royalty Depositor Row By Filter` fired exactly 5 times
  (Update/Find/Verify-Insert-Exists/Verify-Found/Delete) — explicit grid-filter wiring proven, not
  assumed.
- `robocop check` on the 2 changed RF files → 8 issues (3 VAR02 + 5 DOC02) at/under the
  established Bank-pattern baseline. `robot --dryrun` on the full `tests/` tree → 745/745 PASS
  (net +1 vs the pre-conversion 744/744 — straight swap, no TC-count change).
- IUD Fill Only Needed Fields: only Code/Name/Start Date filled on insert — the only mandatory
  fields, matching the already-proven prior driver's own scope.
- Git workflow followed: isolated sparse-checkout clone under `Workplaces/royalty_depositor/`,
  feature branch off `origin/master`, synced with master before push, own PR, no self-merge.

## Done wrong / lessons
- First live attempt hit a transient shared-sandbox account lockout **plus** a cross-session
  "unsaved changes" dialog artifact from a concurrent parallel Batch-5 agent sharing the same
  `sysadmin` login on the shared sandbox — not a defect in this screen's automation. Retried once
  with a genuine evidence-based fix (waited out the lockout, self-cleaned the leftover row via the
  UI, re-verified DB clean) rather than blind-guessing a second theory — confirmed clear 5/5 on
  retry.
- **2026-08-25 follow-up alignment fix:** the original conversion had carried over a leftover
  inline `Royalty Depositor Should Exist In DB` keyword and its TC02 call — this violated Bank's
  own pure-screen-only verification convention (owner decision 2026-08-18: no DB check inside the
  screen-verification keywords, DB checks live only in the dedicated DbVerify assertions). Same
  deviation class as DOA Credit Limit (PR #503). Also uppercased a stray `ov_royalty_depositor`
  prose reference to the house `OV_ROYALTY_DEPOSITOR` naming convention. Re-verified live 5/5,
  full-tree dryrun 841/841, DB self-clean 0 residual after the fix.

## Blockers -> resolution
- Shared-sandbox account lockout + stale dialog (above) -> single retry after a genuine fix
  (waited out lockout + self-cleaned leftover row), not a second guess-based theory. No data
  damage; no hard blocker beyond the one retry.

## Decisions
- Kept the legacy standalone Playwright bundle (`playwright/ec_iud_royalty_depositor.py`,
  predates PR #448) as a historical reference rather than rebuilding it to match the new Bank
  pattern — new Playwright drivers are waived by owner decision 2026-08-27 (the Universal Screen
  Engine, `py/engine.py`, now covers that role for new work).
- RF stays the single verification stack for this screen (Playwright + RF are not kept in lockstep
  going forward for Bank-pattern conversions).

## Evidence
- PR #448 live run (2026-08-23): RF `royalty_depositor_iud.robot` 5/5 PASS (after the one retry
  described above); `robot --dryrun` full-tree 745/745 PASS; robocop 8 issues (baseline).
- 2026-08-25 alignment-fix re-verification: live 5/5, full-tree dryrun 841/841, DB self-clean 0
  residual.
- **2026-08-28 backfill confirmation run** (this task, no automation files touched): dryrun 5/5
  PASS on the screen suite; full-tree dryrun 883/883 PASS; live headless run 5/5 PASS; robocop on
  the 2 RF files → 9 issues (at/near the established baseline; no new files changed by this
  backfill task); fresh-connection DB self-clean query confirmed 0 residual
  `AUTOTEST_ROYALTY_DEP` rows in `OV_ROYALTY_DEPOSITOR` after the run. Artifacts captured at
  `evidence/2026-08-28-live-run/` (log.html, report.html, output.xml, Browser-library playwright
  log, and a screenshot per TC step/login/logout).
