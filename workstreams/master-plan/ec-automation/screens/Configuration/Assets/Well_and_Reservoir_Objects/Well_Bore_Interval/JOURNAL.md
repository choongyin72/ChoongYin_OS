# JOURNAL - Well Bore Interval (CO.0057) OV-GM 6-group nav + mandatory-popup IUD

_This JOURNAL covers three events: the 2026-07-31 base build, the 2026-08-27 Area-pattern
STRUCTURE conversion (PR #563), and this 2026-08-28 backfill (Batch 5 of
`docs/lean-deliverable-backfill-workorder.md` - the bundle had a base-build JOURNAL but was
missing the conversion's own entry, evidence refresh, and CHECKLIST refresh)._

## 2026-07-31
- **Branch:** `feature/well-bore-interval-iud`. Group A #3 - completes the well hierarchy
  (Well -> Well Bore -> Well Bore Interval).
- **Recon facts (all executed, nothing assumed):** 6 per-field nav groups. Under P1 + real well:
  **G:5 = ZERO options** (unusable filter, skipped - same as Well Bore's G:5), **G:6 = exactly one
  option, the well bore `P1 W008 WB001`**. Grid then lists the real interval `P1 W008 WB001 WBI001`.
  Mandatory 'Well Bore' popup (pin R:4) list grid = `Objects:form:T_data`, containing exactly the
  nav-scope bore. DB: OV_WELL_BORE_INTERVAL = 167 rows, base WEBO_INTERVAL.
- **Built by ADAPTING the proven Well Bore pair** (driver/T3/suite) rather than the generator
  (per-field nav + popup unsupported). The blanket rename needed 2 real corrections, both caught by
  post-edit greps: the popup LABEL on this screen is 'Well Bore' (not 'Well'), and G:6 had to be
  added to the navigator sequence.
- One robocop FAIL (LEN03: nav keyword 11/10 keywords) -> refactored into a `Select Nav Group Value`
  helper (also removes 5 repeated Sleep lines), re-ran clean.
- Driver 8/8 on the FIRST run; `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0,
  dryrun 4/4, LIVE RF 4/4, Playwright 8/8. Self-clean 0 residual.

## 2026-08-27 - Area-pattern STRUCTURE conversion (PR #563, branch `feature/well-bore-interval-area-pattern`)
- Converted Well Bore Interval's RF IUD automation from the OLD pattern (4 TCs, suite-level login,
  timestamped code, inline DB-verify calls) to the full Area-pattern structure: 5 TCs (Verify Clean
  State/Insert/Update/Find/Delete), per-TC login/logout on one Suite-Setup browser, a FIXED test
  code `AUTOTEST_WBI`, properties-file-driven insert/update/verify, explicit grid-filter wiring,
  and zero inline DB-verify calls.
- **Real gotcha (from PR #563's own body) - the genuine per-field nav shape, and why a BESPOKE T3
  keyword was used instead of the shared one:** the screen's 7 (6 usable) separate per-field
  `nav:form:G:1..G:6` groups are NOT the single-row/increasing-column cascade shape the shared T2
  `Apply Navigator From Properties` keyword (`resources/manage_object.resource`) supports. This is
  a GENUINE non-fit - confirmed on TWO separate live checks (the 2026-07-31 base build's own recon,
  and a fresh 2026-08-27 re-check via `Workplaces/well-bore-interval-area-pattern/
  recon_wbi_nav_live.py`, read-only, no save) - unlike the Meter/Tract cases elsewhere in this
  project where an initial "non-fit" call was later found WRONG on closer field-by-field
  inspection. Well Bore Interval's per-field shape held up both times. The conversion therefore
  built a BESPOKE, screen-local T3 keyword `Apply Well Bore Interval Navigator` - modeled on
  `well_page.resource`'s own pre-2026-08-26 "Apply Well Navigator" keyword (the project's existing
  precedent for a genuinely per-field-groups navigator) - which loops through the groups the
  already-proven driver (`py/well_bore_interval_iud.py`) actually fills (G:1 Production Unit / G:2
  Area / G:3 Facility Class 1 / G:4 'Well & Well Hookup' / G:6 'Well Bore'), skipping G:5 ('Well',
  present but zero usable options under this scope), then clicks GO once.
  `resources/manage_object.resource` was NOT touched - this is a bespoke-but-legitimate keyword
  local to this screen, not a shared-file extension.
- Files touched: `pageobjects/.../well_bore_interval_page.resource` (rewrite, 215+/89- lines),
  `tests/.../well_bore_interval_iud.robot` (rewrite, 59+/45- lines),
  `testdata/well_bore_interval_{navigator,insert,update,form_verify,grid_verify}.properties` (5
  new files), `resources/credentials.py` (additive:
  `WELL_BORE_INTERVAL_EC_USER`/`WELL_BORE_INTERVAL_EC_PASS`), `docs/ec_screen_registry.md` +
  `docs/automation-scorecard.md` + `docs/bank-pattern-conversion-checklist.md` +
  `docs/grid-filter-standardization-checklist.md` (Well Bore Interval rows/sections updated in
  place per R38, all four docs in the same diff).
- Well Bore Interval's Playwright bundle (`py/well_bore_interval_iud.py`, live 8/8, 2026-07-31)
  explicitly left untouched by the conversion; its proven NAV tuple values (`P1 Production
  Unit`/`P1 Area`/`P1 Facility 1`/`P1 W008 OP`/`P1 W008 WB001`) were read directly from source and
  reused verbatim in the new navigator properties file.
- PR #563's own cited evidence: fresh independent oracledb connection confirmed `AUTOTEST_WBI`
  FREE in `OV_WELL_BORE_INTERVAL` before the run (count = 0); live
  `EC_HEADLESS=true robot .../well_bore_interval_iud.robot` -> 5 tests, 5 passed, 0 failed;
  fresh-connection DB self-clean `SELECT COUNT(*) FROM OV_WELL_BORE_INTERVAL WHERE CODE LIKE
  'AUTOTEST%'` -> 0 residual; `grep -c "Find Object Row By Filter" output.xml` -> 15; robocop 7
  issues (2 VAR02 + 5 DOC02), exact parity with `area_page.resource`/`area_iud.robot`'s own
  baseline; full-tree dryrun 881/881 tests passed, 0 collisions; hygiene PASS (one pre-existing
  unrelated WARN on a different screen); zero inline DB-verify calls confirmed via grep in the new
  suite; checked `docs/navigator-screens-not-matching-area.md` for a prior "does not fit" entry -
  none found, nothing to correct.

## 2026-08-28 - Backfill (this task, `docs/lean-deliverable-backfill-workorder.md` Batch 5)
- Confirmed real file paths via `grep -rli well_bore_interval workstreams/master-plan/
  ec-automation` and the `docs/ec_screen_registry.md` Well Bore Interval row (line 316) before
  touching anything; read the actual `well_bore_interval_page.resource`/`well_bore_interval_iud.robot`
  files and PR #563's real body (via `gh pr view 563`) rather than inventing a narrative.
- Re-ran the ALREADY-PROVEN 5-TC suite once for fresh evidence, no automation changes:
  - `py -m robot --dryrun` -> **5 tests, 5 passed, 0 failed** (this session).
  - `EC_HEADLESS=true py -m robot` -> **5 tests, 5 passed, 0 failed**, first attempt, no retry
    needed.
  - `grep -c "Find Well Bore Interval Row By Filter\|Find Object Row By Filter"` on this session's
    own `output.xml` -> **27** (grid-filter keyword confirmed firing repeatedly; PR #563's own
    citation was 15 from its own separate run - both non-zero and consistent with the keyword
    firing on every Find/Update/Delete/Verify step, not a regression).
  - robocop parity re-check: `well_bore_interval_page.resource`+`well_bore_interval_iud.robot` ->
    **7 issues** (2x VAR02 unused-var, 5x DOC02 missing-TC-doc); `area_page.resource`
    (`pageobjects/Configuration/Assets/Basic_Objects/`) +`area_iud.robot` -> also **7 issues**,
    same categories - confirmed parity independently, not just trusted from PR #563.
  - Full-tree dryrun `tests/` -> **883 tests, 883 passed, 0 failed** (this session's own count;
    differs slightly from PR #563's cited 881 because other screens' suites have grown since - no
    collision either way).
  - Fresh oracledb connection (`Workplaces/well-bore-interval-backfill/dbcheck_selfclean.py`):
    `AUTOTEST_WBI` count = **0**; `AUTOTEST%` residual rows = **[]**.
  - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (one pre-existing WARN unrelated to Well
    Bore Interval, in Contract Area's `investigation/` scripts).
- Added `README.md` command section, refreshed `well_bore_interval_sow.md` (superseding but
  keeping the original 4-TC-era text for history), refreshed this `JOURNAL.md`, refreshed
  `CHECKLIST.md`, refreshed `ec-ui-knowledge/screens/well_bore_interval.md`, and copied the fresh
  `log.html`/`output.xml`/`report.html` from this session's live run into the pre-existing
  `evidence/` folder alongside the original `wbi_0[1-5]_*.png`/`results.json` (kept, not deleted).
- Did NOT touch `pageobjects/`, `tests/`, `testdata/`, `resources/credentials.py`,
  `docs/ec_screen_registry.md`, `docs/automation-scorecard.md`, or any other screen's files - this
  is a documentation/evidence-only backfill.

## Lessons
- Adapting a proven sibling pair is fast but the clone-error checklist matters: label text and nav
  sequence differ even between adjacent hierarchy screens - grep every substituted token afterwards.
- The "phantom mandatory nav group" pattern (scan says mandatory, zero options in every scope) has
  now appeared on 3 screens (Well G:5, Well Bore G:5, WBI G:5) - treat it as a known EC quirk, and
  prove the grid loads without it rather than hunting for values.
- A genuine per-field-groups navigator that fails the shared T2 keyword does NOT block a structural
  Area-pattern conversion - a bespoke, screen-local T3 keyword (modeled on an existing project
  precedent, here Well's own pre-2026-08-26 keyword) can adopt the surrounding 5-TC/properties-file
  structure while keeping the genuine navigator gesture intact, without ever touching the shared
  file. This is a different outcome from a screen whose "non-fit" call turns out to be wrong on
  closer inspection (Tract) - both are legitimate, but they are not the same finding and should not
  be described as if they were.

## Blockers -> resolution
- Base build (2026-07-31): none disclosed.
- Conversion (PR #563): none disclosed in the PR body; robocop/hygiene/dryrun/live all passed
  first-cited.
- This backfill (2026-08-28): none - dryrun, live run (first attempt, no retry needed per this
  task's process rule), DB self-clean, hygiene, and robocop parity all reproduced clean.

## Decisions
- Do NOT rebuild or re-verify the RF suite from scratch for this backfill - it, the registry row,
  and the scorecard row already exist and are already merged (PR #563). This task adds
  documentation/evidence artifacts only.
- The bespoke `Apply Well Bore Interval Navigator` T3 keyword stays screen-local, not promoted into
  `resources/manage_object.resource` - the shared keyword genuinely does not support a per-field-
  groups navigator, and forcing this shape into it would risk regressing every same-row-cascade
  screen that already relies on it.
- Playwright driver (`py/well_bore_interval_iud.py`) stays permanently waived from a new build per
  Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (items 4/5).
- Kept the original 2026-07-31 `VERIFY-REPORT.md` as a historical record of the base build's own
  auto-generated 4-TC-shape gate run, rather than overwriting it with a fabricated re-run against a
  structure it no longer matches; fresh evidence for the CURRENT 5-TC suite lives in `evidence/`.

## Evidence
- Base build (2026-07-31): `VERIFY-REPORT.md` in this folder (robocop 0, hygiene 0, dryrun 4/4,
  live RF 4/4, Playwright 8/8).
- Area-pattern conversion (PR #563, 2026-08-27): cited inline in that PR's body - live 5/5,
  full-tree dryrun 881/881, fresh-connection DB self-clean 0 residual, filter-keyword grep = 15,
  robocop parity (7 issues) vs Area's own baseline.
- This backfill (2026-08-28): `evidence/` folder - `output.xml`/`log.html`/`report.html` from a
  fresh live headless run (5/5 PASS, first attempt), plus this JOURNAL's own citations above for
  the fresh dryrun (5/5), full-tree dryrun (883/883), DB self-clean (0/[]), hygiene (PASS), and
  robocop parity (7/7) re-runs.
