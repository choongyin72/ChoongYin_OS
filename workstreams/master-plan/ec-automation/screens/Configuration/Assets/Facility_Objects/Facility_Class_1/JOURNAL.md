# JOURNAL - Facility Class 1 (CO.0019) OV-GM IUD

## 2026-07-30
- **Branch:** `feature/ov-gm-facility-class-1` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/facility_class_1/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade Production Unit -> Area. Mandatory Facility Class 1 Code / Facility Class 1 Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.

## 2026-08-26 - Area-pattern conversion (PR #526 + PR #530)

### Built
- **PR #526** (`feature/facility-class-1-navigator-shared-keyword`): converted the navigator-fill from
  the original "Apply OV-GM Navigator First Available" to the new shared T2 keyword
  `Apply Navigator From Properties` (`resources/manage_object.resource`, unmodified) - exercising the
  screen's genuine **2-level Production Unit -> Area cascade** addressed same-row, increasing column
  (`nav:form:G:0:R:1:C:1:dd` then `...C:2:dd`). New `testdata/facility_class_1_navigator.properties`
  (real values: `Op Production Unit=AS1 EC Exploration Norway`, `Op Area=AS1_Area`).
- **PR #530** (`feature/facility-class-1-bank-pattern`, stacked on #526): full structural conversion to
  Area's Bank-pattern shape - 5 TCs (Verify Clean State/Insert/Update/Find/Delete), per-TC
  Login/Logout on one Suite-Setup-opened browser, dedicated `FACILITY_CLASS_1_EC_USER`/`_EC_PASS`
  credentials, FIXED test code `AUTOTEST_FC1` (replacing the generated `AUTOTEST_FC1_<timestamp>`),
  4 new properties files (insert/update/form_verify/grid_verify), explicit
  `Find/Clear Facility Class 1 Row By Filter` grid-filter wiring, and PURE SCREEN verification in the
  `.robot` file (zero inline DB-verify calls - TC05's DB check lives inside the shared T2
  `Verify Object Removed`).

### Done well
- **First live exercise of the shared keyword's multi-column same-row cascade shape.** Area itself
  (the role-model screen) only has a single navigator dropdown, so `Apply Navigator From Properties`
  had never been proven against a C:1/C:2-same-row addressing shape before this screen. Confirmed by a
  DEDICATED live recon (`tmp/recon_fc1_navigator_cascade.py`) before writing any properties/config -
  not extrapolated from Area's single-dropdown shape or from any other screen.
- **Zero shared-file changes needed.** `resources/manage_object.resource` was not touched by either
  PR (confirmed via `git status --porcelain` before each commit) - the existing flat 0.7s sleep inside
  the shared keyword was already sufficient for the dependent Area dropdown to populate after PU
  selection, re-verified live under the new per-TC login/logout restructuring in PR #530 (all 5 TCs,
  each re-running the cascade after a fresh login, passed).
- Real field labels/grid columns RE-CONFIRMED live during PR #530 rather than assumed from Area:
  objectForm/updateAttributes use screen-prefixed "Facility Class 1 Code"/"Facility Class 1 Name";
  grid columns (live `manageObject:form:T_head` scan) are Code/Name/Start Date/End Date - matching
  Area's 4-column shape, but confirmed rather than copied.
- Fixed code `AUTOTEST_FC1` confirmed FREE in `OV_FCTY_CLASS_1` (fresh oracledb connection) before
  being wired into the suite - avoided reusing the DB self-clean confidence gap the old generated-code
  pattern papered over.

### Done wrong / lessons
- **PR #530's stacked-base assumption was initially wrong.** The task that produced #530 assumed #526
  was "already merged" - `gh pr view 526` showed it was still OPEN at that point, so #530 had to be
  built stacked on #526's branch instead. Both PRs eventually merged in the correct order
  (#526 -> #530), but the initial premise about merge state was not verified first. Lesson already
  generalized in this repo's standing rules: verify PR state via the tool, don't assume from a task
  brief.
- objectForm was found to expose "Op Production Unit"/"Op Area" fields live during PR #530 - broader
  than the original 2026-07-30 build's documented "no Op Production Unit field" note. Correctly left
  unfilled (the proven driver inserts successfully without them) rather than treating the discovery as
  a new mandatory requirement to chase.

### Blockers -> resolution
- No hard blockers on either PR. The only open question going in - whether the shared keyword's
  addressing scheme would extend cleanly to a same-row multi-column cascade - was resolved by recon
  BEFORE implementation (per this repo's no-guessing rule), not by trial-and-error against the live
  screen.

### Decisions
- Facility Class 1 stays classified OV-GM (navigator-gated) - the Area-pattern conversion is
  STRUCTURAL (TC count, login/logout shape, fixed code, properties-driven fill, pure-screen-verify),
  never a reclassification to a plain Bank-shaped (no-navigator) screen.
- The pre-existing `py/facility_class_1_iud.py` Playwright driver and `investigation/recon.py` are
  RETAINED as-is (still passing) and NOT rebuilt as part of either PR or this backfill - per the
  owner's 2026-08-27 decision, new Playwright bundles are not built for Bank-/Area-pattern
  conversions; the Universal Screen Engine is the forward replacement.

### Evidence
- PR #526: live RF 4/4 pass (structure unchanged by this PR); independent DB self-clean query
  (fresh oracledb connection) = 0 `AUTOTEST_FC1_%` rows.
- PR #530: live RF **5/5 pass**; independent DB self-clean query = 0 `AUTOTEST_FC1%` rows;
  `grep -c "Find Facility Class 1 Row By Filter\|Find Object Row By Filter" output.xml` = **26**;
  zero inline DB-verify calls in the `.robot` file (grep exit 1, no matches); `robocop check` on both
  changed files = 7 issues (2 VAR02 + 5 DOC02), identical in kind/count to Area's own baseline (not a
  regression); full-tree `robot --dryrun tests/` = 847/847 passed.

## 2026-08-27 - Documentation/evidence backfill (this bundle)

### Built
- Owner decision 2026-08-27 retired the 2026-08-23/26 lean-deliverable waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) - SOW/README/JOURNAL/evidence/CHECKLIST.md/KB map
  must be backfilled for every screen converted under the old lean rule since 2026-08-23. Facility
  Class 1 is item 4 of Batch 1 in `docs/lean-deliverable-backfill-workorder.md`.
- This backfill added/updated `facility_class_1_sow.md`, `README.md`, this JOURNAL section,
  `CHECKLIST.md`, `evidence/` (fresh live-run artifacts), and `ec-ui-knowledge/screens/facility_class_1.md`
  around the already-working, already-merged PR #526/#530 automation. **No RF/Playwright code was
  changed.**

### Done well
- Real facts pulled from `gh pr view 526`/`gh pr view 530` bodies (not invented) - the "first live
  exercise of the multi-column same-row cascade" and "zero shared-file changes" narrative above is
  the PRs' own disclosed history, transcribed, not a fresh retelling.
- Re-ran the already-proven suite ONE time live for fresh evidence rather than re-verifying/rebuilding
  it: `robot --dryrun` = 5/5 pass; `EC_HEADLESS=true robot ...` = **5 tests, 5 passed, 0 failed**;
  fresh-connection DB self-clean = 0 `AUTOTEST_FC1%` residual rows; filter-fired grep = 26 (matches
  PR #530's cited count exactly); `robocop check` = 7 issues (2 VAR02 + 5 DOC02, same non-regression
  baseline PR #530 cited); repo-root `py scripts/check_bundle_hygiene.py` = PASS (no hardcoded creds,
  pure ASCII, no CHECKLIST/VERIFY-REPORT contradictions).

### Decisions
- The original 2026-07-30 `evidence/fc1_0N_*.png` screenshots (from the Playwright driver's own run)
  are RETAINED alongside the new 2026-08-27 RF `log.html`/`report.html`/`output.xml` - both are real
  evidence of real runs, from two different (still-valid) automation stacks, not superseded by each
  other.

### Evidence
- This backfill's live RF run: `evidence/log.html`, `evidence/report.html`, `evidence/output.xml`
  (2026-08-27, 5/5 pass).
- Original 2026-07-30 Playwright driver run: `evidence/fc1_0[1-5]_*.png`, `evidence/results.json`.
