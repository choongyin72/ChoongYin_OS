# JOURNAL - Collection Point (CO.0205) OV-GM IUD

## 2026-08-01
- **Branch:** `feature/collection-point-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'collection_point'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/collection_point/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: Production Unit -> Area -> Operator Route cascade + GO. Mandatory Collection Point Code / Collection Point Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons (2026-08-01 build)
- OV-GM: nav cascade uses PROVEN explicit values (scripts/find_populated_scope.py), not first-available - do not assume the first option has usable data underneath. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

---

## 2026-08-26 — Area-pattern conversion (PR #541, `feature/collection-point-area-pattern`)

_Backfilled 2026-08-27 (`docs/lean-deliverable-backfill-workorder.md`, Batch 3 — owner decision
2026-08-27 retired the lean waiver that let this conversion ship without SOW/README/JOURNAL/
evidence/CHECKLIST/KB-map). Content below is pulled from PR #541's real body and commit history,
not invented after the fact._

### Built
- Converted Collection Point's RF automation from the OLD bespoke pattern (4 TCs, suite-level
  login, inline nav-fill via 3x `Select EC Dropdown Option` + `Apply Navigator`, timestamped test
  code, inline screen-local DB-verify wrapper keywords) to Area's full pattern: 5 TCs (added TC04
  Find), per-TC login/logout, navigator fill delegated to the shared T2 `Apply Navigator From
  Properties` keyword, fixed test code `AUTOTEST_COLLECTION_POINT`, properties-file-driven
  insert/update/verify, explicit `Find/Clear Collection Point Row By Filter` grid-filter wiring
  (Update/Find/Verify-Found/Delete only), zero inline DB-verify calls remaining in the suite.
- Files touched: `pageobjects/.../collection_point_page.resource` (rebuilt), `tests/.../
  collection_point_iud.robot` (rebuilt), `resources/credentials.py` (additive
  `COLLECTION_POINT_EC_USER`/`COLLECTION_POINT_EC_PASS`), 5 new/updated `testdata/
  collection_point_*.properties` files, `docs/ec_screen_registry.md` + `docs/automation-
  scorecard.md` (existing rows MODIFIED, not duplicated).

### Done well
- **3-level cascade timing re-confirmed live, not assumed:** the navigator's genuine 3-level
  Production Unit -> Area -> Operator Route SAME-ROW cascade (C:1/C:2/C:3, C:4 absent) was
  re-verified live via a dedicated recon script (`tmp/recon_cp_navigator_cascade.py`) rather than
  trusted from the pre-existing driver's own documentation, per the owner's standing "no
  guessing" rule. The shared T2 keyword's flat 0.7s sleep between levels was confirmed live
  SUFFICIENT for this screen's redraw timing at BOTH the PU->Area and Area->Operator Route
  transitions — no shared-file change, no per-screen extra `Sleep` needed. This is a SECOND
  independent live confirmation that the shared keyword's default timing generalizes across
  screens (the first was Chemical Stream Hookup in Batch 2) — proof it isn't a one-off fit, not
  just a repeat of the same case.
- No shared T1/T2 file changes (`resources/manage_object.resource` untouched) — the whole
  conversion lived in Collection Point's own T3/suite/testdata files.
- Only Collection Point's own files staged (no `git add -A`).
- Full `tests/` tree dryrun: 850/850 pass, 0 failed — the conversion introduced zero collisions
  with any other screen's suite.
- Filter keyword confirmed actually firing (not just present in the code): 11 hits for `Find
  Collection Point Row By Filter` (T3 wrapper), 15 for the underlying T2 `Find Object Row By
  Filter`, grepped from the live run's `output.xml`.
- Live RF suite 5/5 pass (EC_HEADLESS=true) at the time of PR #541, with DB ground-truth
  evidence: fresh oracledb connection confirmed `AUTOTEST_COLLECTION_POINT` had 0 rows in
  `OV_COLLECTION_POINT` before the run, then a SEPARATE fresh connection confirmed 0 rows after —
  self-clean confirmed via two independent connections, not the same session's cached state.

### Done wrong / lessons
- None disclosed as a defect in PR #541 itself — robocop's 7 issues (VAR02 x2 + DOC02 x5) were
  called out explicitly as EXACT PARITY with Area's/Facility Class 1's own reference-pattern
  baseline, not a regression introduced by this conversion.
- This backfill task (2026-08-27) itself hit a real, session-level environmental issue while
  re-running the suite for fresh evidence: repeated stray `chrome-headless-shell.exe` processes
  (confirmed via `tasklist | grep -i chrome` before/after each attempt) caused several live runs
  to crash mid-suite (`Could not find active page` / `Playwright process has been terminated`)
  even after killing them, because another concurrent process kept re-spawning them in this
  shared session. This is NOT a Collection Point suite defect — one clean re-run this session
  (`results/_backfill_verify_live2`) got TC01-04 to full PASS before TC05 hit the same
  environmental crash, and a DB check via a fresh connection confirmed `OV_COLLECTION_POINT` had
  0 `AUTOTEST_COLLECTION_POINT` rows both before and after every attempt (including the crashed
  ones) — no residual test data was ever left behind. PR #541's own already-merged 5/5 live
  evidence is not superseded by this session's environmental flakiness.

### Blockers -> resolution
- Live-run instability during this backfill's re-verification pass (see above) -> resolved by
  documenting the environmental cause honestly (tasklist evidence + DB residual checks each
  attempt) rather than claiming a clean 5/5 this session that did not actually happen, and citing
  the dryrun (5/5, this session) + PR #541's already-merged live 5/5 as the load-bearing evidence
  for "the automation works," per this backfill's own scope ("do NOT re-run the full original
  build" / "if it fails, report that as a real regression" — this was reported, and traced to
  environment, not code).

### Decisions
- No RF/T3/testdata changes made during this backfill — this task is documentation/evidence only,
  per `docs/lean-deliverable-backfill-workorder.md`.
- Playwright driver `py/collection_point_iud.py` + its `investigation/recon.py` remain from the
  2026-08-01 build, untouched by PR #541 and out of scope for this backfill (Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` keeps items 4/5 permanently waived for Area-pattern work).

### Evidence
- PR #541 (merged 2026-08-26, `feature/collection-point-area-pattern` -> master): live RF 5/5,
  robocop 7 issues (parity baseline), full-tree dryrun 850/850, DB self-clean 0 residual (two
  independent fresh connections).
- This backfill (2026-08-27): dryrun 5/5 (`evidence/dryrun_output.xml`), best live re-run TC01-04
  PASS / TC05 environment-crash (`evidence/live_TC01-04_pass_output.xml`), DB residual checks 0
  rows before/after every attempt, robocop 7 issues reproduced (parity confirmed), hygiene PASS.
