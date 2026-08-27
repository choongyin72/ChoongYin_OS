# JOURNAL - Well Hole (CO.0051) OV-GM IUD

_This JOURNAL covers three events: the 2026-07-31 base build, the 2026-08-26 Area-pattern
STRUCTURE conversion (PR #543), and this 2026-08-28 backfill (Batch 4 of
`docs/lean-deliverable-backfill-workorder.md` - the bundle had a base-build JOURNAL but was
missing the conversion's own entry, evidence refresh, and CHECKLIST refresh)._

## 2026-07-31
- **Branch:** `feature/ov-gm-well-hole` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/well_hole/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility Class 1. Mandatory Well Hole Code / Well Hole Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## 2026-08-26 - Area-pattern STRUCTURE conversion (PR #543, branch `feature/well-hole-area-pattern`)
- Converted Well Hole's RF IUD automation from the OLD pattern (4 TCs, `Apply OV-GM Navigator
  First Available`, single suite-level login, generated timestamp code) to Area's full pattern: 5
  TCs (Verify Clean State/Insert/Update/Find/Delete), per-TC login/logout, navigator fill delegated
  to the shared T2 `Apply Navigator From Properties` driven by a new
  `well_hole_navigator.properties`, properties-file-driven insert/update/verify, explicit
  grid-filter wiring, and zero inline DB-verify calls.
- **Real gotcha (from PR #543's own body):** the base build's first-available navigator scope was
  sparse/unreliable for this screen (a documented OV-GM characteristic - see the 2026-07-31 lesson
  above). The conversion instead reused the sibling Well screen's already-proven SPECIFIC "P1
  Production Unit/P1 Area/P1 Facility 1" scope (owner screenshot ground truth 2026-07-30) - but did
  NOT assume it would transfer: confirmed live 2026-08-26 that this exact scope also lists 20 real
  rows in `OV_WELL_HOLE`, and that "P1 Production Unit" is a valid Insert-form option, before
  committing to it. Copy-adapt-verify against a sibling, not a fresh guess and not a blind
  first-available fallback.
- Files touched: `pageobjects/.../well_hole_page.resource` (rewrite, 176+/63- lines),
  `tests/.../well_hole_iud.robot` (rewrite, 53+/45- lines),
  `testdata/well_hole_{insert,update,form_verify,grid_verify,navigator}.properties` (5 new files),
  `resources/credentials.py` (additive: `WELL_HOLE_EC_USER`/`WELL_HOLE_EC_PASS`),
  `docs/ec_screen_registry.md` + `docs/automation-scorecard.md` (Well Hole rows updated in place).
- No shared-file regression risk: `resources/manage_object.resource`'s `Apply Navigator From
  Properties` keyword already existed (added on PR #521/#523) - this PR did not modify it.
- Well Hole's Playwright bundle (`py/well_hole_iud.py`, live 8/8, 2026-07-31) explicitly left
  untouched by the conversion.
- Scope guard respected: only Well Hole (CO.0051) files touched; the sibling Well screen
  (`well_page.resource`, a separate task) was read-only referenced for its proven "P1" scope,
  never modified.
- PR #543's own cited evidence: live `EC_HEADLESS=true robot .../well_hole_iud.robot` -> 5 tests, 5
  passed, 0 failed; fresh-connection DB self-clean `SELECT COUNT(*) FROM OV_WELL_HOLE WHERE CODE
  LIKE 'AUTOTEST%'` -> 0 residual; `grep -c "Find Well Hole Row By Filter\|Find Object Row By
  Filter" output.xml` -> 29; robocop parity with Area's own baseline (7 issues, same VAR02/DOC02
  categories); full-tree dryrun 850/850.

## 2026-08-28 - Backfill (this task, `docs/lean-deliverable-backfill-workorder.md` Batch 4)
- Confirmed real file paths via `grep -ril well_hole_page.resource workstreams/master-plan/
  ec-automation` and the `docs/ec_screen_registry.md` Well Hole row (line 315) before touching
  anything; read the actual `well_hole_page.resource`/`well_hole_iud.robot` files and PR #543's
  real body (via `gh pr view 543`) rather than inventing a narrative.
- Re-ran the ALREADY-PROVEN 5-TC suite once for fresh evidence, no automation changes:
  - `py -m robot --dryrun` -> **5 tests, 5 passed, 0 failed** (this session).
  - `EC_HEADLESS=true py -m robot` -> **5 tests, 5 passed, 0 failed**, first attempt, no retry
    needed (unlike Tank's backfill session, which hit a real stray-process flake - Well Hole's
    live run passed clean on the first try).
  - `grep -c "Find Well Hole Row By Filter\|Find Object Row By Filter"` on this session's own
    `output.xml` -> **29** (matches PR #543's own citation).
  - robocop parity re-check: `well_hole_page.resource`+`well_hole_iud.robot` -> **7 issues** (2x
    VAR02 unused-var, 5x DOC02 missing-TC-doc); `area_page.resource`+`area_iud.robot` -> also **7
    issues**, same categories - confirmed parity independently, not just trusted from PR #543.
  - Fresh oracledb connection (`Workplaces/well-hole-backfill/dbcheck_selfclean.py`):
    `AUTOTEST_WELL_HOLE` count = **0**; `AUTOTEST%` residual rows = **[]**.
  - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (one pre-existing WARN unrelated to Well
    Hole, in Contract Area's `investigation/` scripts).
- Added `README.md` command section, refreshed `well_hole_sow.md` (superseding but keeping the
  original 4-TC-era text for history), refreshed this `JOURNAL.md`, refreshed `CHECKLIST.md`,
  refreshed `ec-ui-knowledge/screens/well_hole.md`, and copied the fresh
  `log.html`/`output.xml`/`report.html` from this session's live run into the pre-existing
  `evidence/` folder alongside the original `whl_0[1-5]_*.png`/`results.json` (kept, not deleted).
- Did NOT touch `pageobjects/`, `tests/`, `testdata/`, `resources/credentials.py`,
  `docs/ec_screen_registry.md`, or `docs/automation-scorecard.md` - this is a documentation/
  evidence-only backfill.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.
- The Area-pattern conversion (PR #543) shows the fix for that same first-available fragility: when
  a sibling screen has already proven a SPECIFIC nav scope works, verify it transfers (a fresh live
  check, not an assumption) rather than staying on first-available or guessing a new scope.

## Blockers -> resolution
- Base build (2026-07-31): none disclosed.
- Conversion (PR #543): none disclosed in the PR body; robocop/hygiene/dryrun/live all passed
  first-cited.
- This backfill (2026-08-28): none - dryrun, live run (first attempt, no retry needed per this
  task's process rule), DB self-clean, hygiene, and robocop parity all reproduced clean.

## Decisions
- Do NOT rebuild or re-verify the RF suite from scratch for this backfill - it, the registry row,
  and the scorecard row already exist and are already merged (PR #543). This task adds
  documentation/evidence artifacts only.
- Playwright driver (`py/well_hole_iud.py`) stays permanently waived from a new build per Section H
  of `docs/IUD-DELIVERABLE-CHECKLIST.md` (items 4/5).
- Kept the original 2026-07-31 `VERIFY-REPORT.md` as a historical record of the base build's own
  auto-generated 4-TC-shape gate run, rather than overwriting it with a fabricated re-run against a
  structure it no longer matches; fresh evidence for the CURRENT 5-TC suite lives in `evidence/`.

## Evidence
- Base build (2026-07-31): `VERIFY-REPORT.md` in this folder (robocop 0, hygiene 0, dryrun 4/4,
  live RF 4/4, Playwright 8/8).
- Area-pattern conversion (PR #543, 2026-08-26): cited inline in that PR's body - live 5/5,
  full-tree dryrun 850/850, fresh-connection DB self-clean 0 residual, filter-keyword grep = 29,
  robocop parity (7 issues) vs Area's baseline.
- This backfill (2026-08-28): `evidence/` folder - `output.xml`/`log.html`/`report.html` from a
  fresh live headless run (5/5 PASS, first attempt), plus this JOURNAL's own citations above for
  the fresh dryrun (5/5), DB self-clean (0/0), hygiene (PASS), and robocop parity (7/7) re-runs.
