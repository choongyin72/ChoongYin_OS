# JOURNAL - Calculation Group Context (CO.0245) OV IUD

## 2026-07-26
- **Branch:** `feature/calculation_group_context-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Calculation_Objects > Calculation Group Context. Mandatory Code/Name/Start Date; optional dropdowns skipped.
  Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

## Lessons (2026-07-26 build)
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.

---

## 2026-08-23 - PR #455: full Bank-pattern conversion (batch 7)

### Built
- Brought Calculation Group Context up to the same full Bank-pattern shape as `bank_page.resource`/
  `customer_page.resource`: properties-file-driven Insert/Update/Verify and explicit grid-filter wiring, added
  on top of the pre-existing label-driven `Fill OV Field By Label` mechanics (kept, not thrown away).
- Files touched: `pageobjects/.../calculation_group_context_page.resource` (rewired to full Bank-pattern
  keyword shape, +156/-64), `tests/.../calculation_group_context_iud.robot` (5-TC per-TC login/logout suite,
  added TC04 Find, fixed test code, +50/-44), `resources/credentials.py` (added
  `CALCULATION_GROUP_CONTEXT_EC_USER/PASS`, additive only), 4 new `testdata/calculation_group_context_*.properties`
  files, plus registry/checklist doc updates (`docs/ec_screen_registry.md`,
  `docs/bank-pattern-conversion-checklist.md`, `docs/grid-filter-standardization-checklist.md`,
  `docs/automation-scorecard.md`).

### Done well
- Recon against the screen's own proven Python driver (`py/calculation_group_context_iud.py`) and the existing
  SOW before writing new config, instead of assuming the Bank shape would drop in unchanged.
- No shared T1/T2 (`resources/manage_object.resource`/`resources/common.resource`) changes - batch 7 hard rule
  respected.
- `py -m robocop check` on the changed files matched the accepted `bank_iud.robot` DOC02 baseline exactly (no
  new issue classes introduced by the conversion).
- `robot --dryrun` on the full `tests/` tree: 753/753 pass - confirmed the conversion did not break any other
  screen's suite.

### Done wrong / lessons
- The Code field's label here is NOT the generic "Code" used by Bank - it is "Calculation Group Context Code".
  Every T2 call in the converted T3 has to thread `code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}`
  explicitly; a straight copy-paste of Bank's keyword calls without this would have silently resolved the wrong
  field or failed to resolve at all.
- Switched from a generated-unique test code to the fixed `AUTOTEST_CGC_BANK` (matching Bank's convention) -
  had to confirm it was actually absent from `OV_CALC_GRP_CONTEXT` first before wiring it in, since a fixed
  code carries cross-run collision risk that a generated-unique code doesn't.

### Blockers -> resolution
- None disclosed in the PR body beyond the label-mismatch risk above, which was caught during build (via the
  driver/SOW recon) rather than during a live failure.

### Decisions
- Isolated worktree under `Workplaces/calculation_group_context/`, own feature branch, synced with
  `origin/master` before push - per repo git-workflow rules.
- Playwright bundle NOT rebuilt or touched by this conversion (out of scope for a Bank-pattern conversion PR).

### Evidence (PR #455)
- Live 5/5 pass (TC01-05, `EC_HEADLESS=true`).
- DB self-clean verified via a **fresh** oracledb connection after the run:
  `SELECT COUNT(*) FROM OV_CALC_GRP_CONTEXT WHERE CODE = 'AUTOTEST_CGC_BANK'` = 0.
- Grid-filter wiring confirmed fired via `output.xml` grep: `Find Object Row By Filter`/
  `Filter Grid Text Column By Value` = 23 hits.
- Merged 2026-08-23T11:31:20Z, base branch master.

---

## 2026-08-28 - Batch 9 documentation/evidence backfill (this task)

### Built
- Owner decision 2026-08-27 (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`) retired the lean waiver that let
  PR #455 skip SOW/README/JOURNAL/evidence/CHECKLIST/KB-map updates. This backfill restores those artifacts
  for this screen (part of batch 9 of `docs/lean-deliverable-backfill-workorder.md`, alongside
  Calculation-Context, Blend, Canal, Inventory-Area, Chemical-Transport-Tank, Meter-Run).
- Updated this SOW, README, JOURNAL (this entry), CHECKLIST.md, and the KB map
  (`ec-ui-knowledge/screens/calculation_group_context.md`) to reflect the PR #455 conversion, sourced from the
  real PR #455 body (via `gh pr view 455`) and the current `_page.resource`/`_iud.robot` files - not invented.
- Re-ran the suite for evidence capture: `robot --dryrun` (5/5 PASS) and one live headless run (5/5 PASS,
  `EC_HEADLESS=true`) - see `evidence/2026-08-28-backfill/`. Confirmed DB self-clean via a fresh oracledb
  connection: `AUTOTEST_CGC_BANK` count = 0.
- Confirmed robocop parity: 13 DOC02 issues on this suite, identical count/class to `bank_iud.robot`'s own
  accepted baseline (13). Confirmed `scripts/check_bundle_hygiene.py` RESULT: PASS (no hardcoded creds, ASCII
  clean, no CHECKLIST/VERIFY-REPORT contradictions for this bundle).

### Done well
- Did not rebuild, modify, or re-verify the RF automation itself - the existing `_page.resource` and
  `_iud.robot` were read-only inputs for this documentation pass, per the task's explicit instruction.
- Pulled the JOURNAL/SOW content directly from PR #455's real body rather than writing a generic narrative.

### Done wrong / lessons
- None - this was a documentation-only backfill against already-proven, already-merged automation; no new
  automation defects were introduced or discovered.

### Blockers -> resolution
- None. Live run and DB checks both passed on the first attempt (no retry needed).

### Decisions
- Kept the Playwright driver + `investigation/recon.py` bundle as-is (items 4/5 stay permanently waived per
  Section H - the Universal Screen Engine replaces that role going forward).
- New evidence from this backfill run placed under `evidence/2026-08-28-backfill/` rather than overwriting the
  original 2026-07-26 build's screenshots, to preserve both records.

### Evidence (this backfill)
- `evidence/2026-08-28-backfill/log.html`, `report.html`, per-TC screenshots (login/open_screen/action/
  verify/logout x 5 TCs) from the live run.
- `evidence/2026-08-28-backfill/dryrun-summary.txt` - dryrun 5/5 PASS.
- DB self-clean: fresh-connection query, `AUTOTEST_CGC_BANK` count = 0.
- PR: see this branch's PR body for the full 6-field summary.
