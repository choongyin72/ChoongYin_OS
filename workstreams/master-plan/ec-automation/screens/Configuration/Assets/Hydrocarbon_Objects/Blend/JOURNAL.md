# JOURNAL - Blend (CO.0219) OV IUD

## 2026-07-26
- **Branch:** `feature/blend-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Hydrocarbon_Objects > Blend. Mandatory Code/Name/Start Date; optional dropdowns skipped.
  Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

## Lessons (2026-07-26 build)
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.

## 2026-08-23 - Batch 7 Bank-pattern conversion (PR #457)
- **Built:** upgraded Blend from its prior PARTIAL label-driven RF build to the FULL
  properties-file-driven, grid-filter-wired "Bank pattern" - matching
  `bank_page.resource`/`customer_page.resource`/`state_page.resource`.
- **Files touched:** `pageobjects/.../blend_page.resource` rebuilt (`Find/Clear Blend Row By
  Filter` delegating to shared T2; properties-file-driven Insert/Update/Verify via `Insert Object
  From Properties And Verify Code` / `Update Object From Properties` / `Verify Object Insert
  Exists` / `Verify Object Form Record` / `Verify Object Found`; `code_label=Blend Code` threaded
  through since Blend's Code field is screen-prefixed, matching State's precedent); suite
  `tests/.../blend_iud.robot` converted to the 5-TC pattern (TC01 clean-state / TC02 insert / TC03
  update / TC04 find / TC05 delete), fixed test code `AUTOTEST_BLEND`, per-TC Login/Logout; new
  `testdata/blend_insert.properties`, `blend_update.properties`, `blend_form_verify.properties`,
  `blend_grid_verify.properties`; `resources/credentials.py` appended `BLEND_EC_USER`/
  `BLEND_EC_PASS` (additive only); `docs/ec_screen_registry.md`,
  `docs/grid-filter-standardization-checklist.md`, `docs/automation-scorecard.md` updated. No
  shared T1/T2 file touched - every needed keyword already existed.
- **Done well:** recon-first (fresh live DOM scan confirmed OV_BLEND columns and the mandatory set
  - `Blend Code`*/`Blend Name`*/`Start Date`* via `MandatoryCellStyle` - before writing testdata,
  per CLAUDE.md NO GUESSING); reused the existing partial page object instead of discarding it;
  isolated sparse-checkout clone per the Batch 7 ground rules
  (`tmp/batch7_shared_findings.md`).
- **Verification:** full-tree `robot --dryrun` 753/753 pass; live `EC_HEADLESS=true` run of
  `blend_iud.robot` 5/5 pass, first attempt; DB self-clean via a fresh oracledb connection - 0
  residual `AUTOTEST_BLEND` rows in `OV_BLEND`; filter keyword fired 50 hits across TC02-TC05
  (`output.xml` grep for `Find Blend Row By Filter`/`Clear Blend Row Filter`); `robocop check` on
  changed files exit=1, same DOC02/VAR02-only advisory-warning profile as the `bank_iud.robot`
  exemplar baseline (exit=1, 26 similar warnings) - no new issue categories introduced.
- **Decisions:** kept the delete field id hardcoded (not label-driven), matching Bank's/Customer's
  own documented precedent for the objectdates row shape.
- **Blockers -> resolution:** none disclosed in PR #457's body beyond the routine recon-before-build
  discipline; no flakes or re-attempts reported.
- **Evidence:** PR #457 body (dryrun 753/753, live 5/5, self-clean 0 residual, robocop
  exit=1/no-new-category, filter keyword 50 hits); registry + scorecard rows appended at merge.

## 2026-08-28 - Backfill (this session, `docs/lean-deliverable-backfill-workorder.md` Batch 9)
- **Built:** nothing added to the RF/Playwright automation. Refreshed the documentation/evidence
  bundle (`blend_sow.md`, `README.md`, this `JOURNAL.md`, `CHECKLIST.md`, `VERIFY-REPORT.md`,
  `ec-ui-knowledge/screens/blend.md`) which had been left dated 2026-07-26 describing the
  SUPERSEDED partial 4-TC build, even though PR #457 (2026-08-23) had already replaced that
  automation with the 5-TC Bank pattern and updated the registry/scorecard rows accordingly - the
  bundle docs and KB map were the only stale pieces.
- **Done well:** confirmed real file paths via grep + registry lookup before touching anything;
  read `docs/ec_screen_registry.md` and `docs/automation-scorecard.md` first and found both
  already correct (append-only rows from the PR #457 merge) - so this backfill left those two
  files untouched, only refreshing the bundle-local docs and KB map.
- **Verification (evidence-capture re-run only, per the workorder - not a fresh build/verify
  cycle):** screen-scoped `robot --dryrun` 5/5 pass; live `EC_HEADLESS=true` run 5/5 pass, first
  attempt (no retry needed); `robocop check` on the T3+suite exit=1, 7 issues, all DOC02 (missing
  `[Documentation]` on TC04/TC05) / advisory class, same category as PR #457's own baseline - no
  regression; `scripts/check_bundle_hygiene.py` (repo root) exit=0 PASS; DB self-clean confirmed via
  a fresh Python process + `DbVerify.code_should_be_absent_in_view("OV_BLEND", "AUTOTEST_BLEND")` -
  0 residual rows.
- **Decisions:** copied the fresh `output.xml`/`log.html`/`report.html` + one `_verify` screenshot
  per TC into `evidence/` under a `blend_backfill_2026-08-28_*` prefix, keeping the original
  2026-07-26 evidence files (`blend_0[1-5]_*.png`, `rf_report.html`) alongside rather than deleting
  them, so the bundle shows both the original build's evidence and the current-state re-run.
- **Blockers -> resolution:** none - live run passed first attempt, no timeout/browser error
  triggered the retry-once-then-disclose rule.
- **Evidence:** `evidence/blend_backfill_2026-08-28_output.xml`,
  `evidence/blend_backfill_2026-08-28_log.html`, `evidence/blend_backfill_2026-08-28_report.html`,
  `evidence/backfill_2026-08-28_TC0[1-5]_*_verify.png`.
