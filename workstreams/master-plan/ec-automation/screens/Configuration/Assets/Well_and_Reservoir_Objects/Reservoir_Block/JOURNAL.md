# JOURNAL - Reservoir Block IUD

_Screen: Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block (CO.0133), OV,
date-effective. View `OV_RESV_BLOCK`. This JOURNAL covers both the original 2026-07-26 build AND
the 2026-08-23 Bank-pattern conversion (PR #466); the conversion sections were backfilled 2026-08-28
per `docs/lean-deliverable-backfill-workorder.md` (Batch 10) - the automation itself was not touched._

## 2026-07-26 - original build (superseded)
- **Branch:** `feature/reservoir_block-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block. Mandatory Code/Name/Start
  Date; optional dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- Label-driven T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4 (TC01-TC04
  only - no properties-file wiring, no explicit grid-filter keywords yet).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

### Lessons (2026-07-26)
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.

---

## 2026-08-23 - Batch 9 Bank-pattern conversion (PR #466)

### Built
- Rebuilt `reservoir_block_page.resource` (T3) from scratch to mirror `bank_page.resource`/
  `berth_page.resource` exactly: properties-file-driven Insert/Update/Verify (`testdata/
  reservoir_block_{insert,update,form_verify,grid_verify}.properties`, new) plus explicit grid-filter
  wiring (`Find Reservoir Block Row By Filter`/`Clear Reservoir Block Row Filter` -> shared T2
  `Find/Clear Object Row By Filter`) into Update/Find/Verify-Found/Delete.
- Rebuilt `reservoir_block_iud.robot`: per-TC login/logout (own credentials
  `RESERVOIR_BLOCK_EC_USER`/`RESERVOIR_BLOCK_EC_PASS`, additive in `resources/credentials.py`), fixed
  test code `AUTOTEST_RESVB` (confirmed absent from `OV_RESV_BLOCK` live before wiring in), full 5-TC
  shape (TC01 clean-state / TC02 insert / TC03 update / TC04 find / TC05 delete) - up from the prior
  build's 4 TCs.
- Reused the shared T1 (`common.resource`)/T2 (`manage_object.resource`) keywords as-is - **zero
  changes** to either shared-keyword file this round.

### Done well
- Live RF run: 5/5 pass (TC01-TC05).
- Fresh oracledb connection before build: `SELECT CODE FROM OV_RESV_BLOCK WHERE CODE LIKE 'AUTOTEST%'`
  -> 0 rows (code free). Same query after the live run -> 0 rows again (self-clean confirmed).
- `output.xml` grep confirmed the filter keywords were actually exercised, not just present in source:
  `Find Reservoir Block Row By Filter` fired 13x, `Find/Clear Object Row Filter` (T2) fired 15x each.
- `robot --dryrun` on the FULL `tests/` tree: 762/762 pass, no collisions with any other screen's suite.
- robocop on the changed files: exit 1, but the **same 9 baseline issues** (8x DOC02 missing-test-doc,
  1x VAR02 unused var) as the accepted `berth_iud.robot` exemplar - parity confirmed, no regression.

### Done wrong / lessons
- The Batch 9 ground-rules doc (`tmp/batch9_shared_findings.md`) assumed the "Batch 9 additions
  (pending)" section header in `docs/bank-pattern-conversion-checklist.md` /
  `docs/grid-filter-standardization-checklist.md` was already merged to master via PR #464. At the
  time this branch was cloned from `origin/master`, **PR #464 was still OPEN**, so PR #466 had to
  re-add the identical header text verbatim rather than append under an existing one. This was
  flagged explicitly in the PR body (not silently worked around) as a header-duplication conflict for
  whichever of the two PRs merged second.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows for
  Reservoir Block were **MODIFIED**, not newly added - the screen already had a 2026-07-26
  generator-scaffolded entry from the original build.

### Blockers -> resolution
- No hard blockers on this conversion; the shared engine + T2 pattern (already proven on Bank/Berth)
  applied directly with zero screen-specific tuning beyond the label set.

### Decisions
- No changes to `resources/manage_object.resource` or `resources/common.resource` this round
  (per the Batch 9 "no shared-keyword changes" rule) - Reservoir Block's own T3 absorbed all the
  screen-specific wiring.
- Playwright driver `py/reservoir_block_iud.py` left unchanged - the conversion project is RF-only;
  the Playwright bundle for this screen predates and is untouched by the Bank-pattern round.

### Evidence
- Original build (2026-07-26): `evidence/reservoir_block_0[1-5]_*.png` (Playwright 7/7) +
  `evidence/rf_report.html` (RF 4/4).
- Batch 9 conversion (2026-08-23, cited in PR #466): live RF 5/5, `output.xml` filter-keyword grep
  counts above, fresh-connection self-clean query results above.

---

## 2026-08-28 - documentation/evidence backfill (this task, Batch 10)

### Built
- Rewrote `reservoir_block_sow.md`, `README.md`, this `JOURNAL.md`, and
  `ec-ui-knowledge/screens/reservoir_block.md` to describe the CURRENT (post-PR #466) Bank-pattern
  shape - all four were still describing the superseded 2026-07-26 partial build (4/4, no properties
  files, no grid-filter wiring) even though the automation itself had moved on a month earlier.
- Re-ran the suite once for fresh evidence (dryrun 5/5, live headless 5/5) and captured the output
  into `evidence/backfill-2026-08-28/` (output.xml, log.html, report.html, per-TC screenshots - all
  under 2MB individually, ~1.8MB combined).
- Ran a fresh-connection DB self-clean check (`SELECT CODE FROM OV_RESV_BLOCK WHERE CODE LIKE
  'AUTOTEST%'` -> 0 rows) and `py scripts/check_bundle_hygiene.py` (PASS) to back the CHECKLIST ticks
  with real evidence rather than restating PR #466's claims unverified.
- **No RF automation file was modified, rebuilt, or re-verified from scratch** - this task only added
  documentation/evidence artifacts around the already-working, already-merged suite.

### Done well
- Caught that the pre-existing bundle (predating this backfill project) was stale relative to the
  actual current automation, rather than assuming "a bundle already exists" meant "the bundle is
  current."

### Evidence
- Dryrun: 5/5 pass, `Workplaces/reservoir-block-backfill/dryrun/` (scratch, gitignored).
- Live: 5/5 pass, `evidence/backfill-2026-08-28/output.xml` + `log.html` + `report.html` + screenshots.
- DB self-clean: fresh `oracledb` connection, `OV_RESV_BLOCK` AUTOTEST% -> `[]` (0 rows).
- Hygiene: `py scripts/check_bundle_hygiene.py` from repo root -> exit 0, RESULT: PASS.
