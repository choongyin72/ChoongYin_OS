# JOURNAL - Property (SP.0059) OV-GM IUD

## 2026-08-02
- **Branch:** `feature/retry-property-iud`. Previously parked (PR #313) as "silent Save failure + a
  real `ec_error()` detection gap" - the detection gap was fixed separately in #319/#326. Retried here.
- **Blocker chased down the wrong path first:** on retry, the Business Unit Name reference dropdown
  kept persisting the wrong value ("SS1 BU" instead of the requested "Royalty Canada"), reproduced
  live 4 times (raw DOM check, screenshots, video, and headed in front of the owner). Initially
  suspected/reported as a shared-engine defect in `select_dropdown()` (`py/ec_object_iud.py`) - the
  same symptom had also appeared on Price Index and Royalty Contract.
- **Real root cause (owner correction):** not a code defect at all. A Property record's Start Date
  was set to `2000-01-01`, but the target Business Unit "Royalty Canada" (`ROYALTY_CA`) only exists
  from `2003-01-01` onward (checked live: `OV_BUSINESS_UNIT.OBJECT_START_DATE`). EC's reference
  dropdowns only offer parent objects already effective by the child record's own Start Date - a
  child object cannot exist before its parent does. With `2000-01-01`, "Royalty Canada" wasn't even
  in the filtered option list (only SS1 BU/SS2 BU/TS5 BU were, matching what the panel actually
  showed); the code's fallback silently took the first option in that list instead of the requested
  one that wasn't there. Confirmed fix live + DB-verified with `AUTOTEST_PROP_FIXEDDATE` on
  Start Date `2003-01-01`: Business Unit persisted correctly as `ROYALTY_CA`. Cleaned (0 residual).
  Recorded as a standing lesson: [[feedback_child_object_date_must_follow_parent]].
- **Built** (generator `tmp/gen_ovgm.py`, config `nav_value="Royalty Canada"`,
  `extra_dropdowns=[["Business Unit Name","Royalty Canada"]]`, `start_date="2003-01-01"`): label-driven
  T3 (no hardcoded ids); thin driver `py/property_iud.py`; RF T3/suite.
- **Generator template gap found + fixed locally:** the generator's default single-level nav dropdown
  id template (`nav:form:G:0:R:1:C:1:dd`) does not match this screen's actual layout - Property's Date
  and Business Unit fields are TWO SEPARATE navigator groups (`G:0`=Date, `G:1`=Business Unit), not one
  group with Date at C:0/dropdown at C:1. Confirmed the real id live (`nav:form:G:1:R:1:C:0:dd_input`)
  and hand-corrected both `py/property_iud.py` and the T3's `${NAV_DD}` variable before running the
  live gate. Not pushed back into `tmp/gen_ovgm.py` itself this round - flagged here for whoever next
  hits a screen where Date and the mandatory dropdown are in different navigator groups.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright driver 8/8. DB residual 0.

## Lessons
- **Reference-dropdown screens need `Start Date >= the referenced object's own effective date`**, not
  just the plain default test date. This project already has `EC_TEST_START_DATE_REFDD` (2003-01-01)
  in `resources/environment.py` for exactly this; use it (or an equivalent >= 2003-01-01 date) whenever
  the New-Object form has ANY reference dropdown to another EC object.
- **Chase the data before the code.** Reproducing a symptom 4 times (screenshots/video/live) proved the
  symptom was real, but proved nothing about WHERE the fault was - the actual fault was in the test
  data (Start Date), not in `select_dropdown()`. The lesson: check the referenced object's own
  effective dates in the DB *before* concluding a shared function is defective, especially when the
  same symptom recurs across multiple unrelated screens (a shared wrong-assumption in test data setup
  is at least as likely as a shared code defect).
- **Don't assume the generator's navigator-id template transfers 1:1** to every OV-GM screen - the
  BU-gated single-dropdown pattern can have Date and the dropdown in either the same group or
  different groups; verify the live id before trusting the generated driver/T3.

## 2026-08-26 - Area-pattern conversion (PR #559)

### Built
Converted from the 2026-08-02 build (4/4 RF + 8/8 Playwright, hand-written driver
`py/property_iud.py`) to the full Area-pattern STRUCTURE: 5 TCs (added TC04 Find), per-TC Login/
Logout, fixed test code `AUTOTEST_PROPERTY`, properties-file-driven insert/update/verify,
explicit grid-filter wiring, zero inline DB-verify calls. Rebuilt `property_page.resource` (T3)
and `property_iud.robot` (suite); added `testdata/property_{insert,update,form_verify,
grid_verify,navigator}.properties`; added `PROPERTY_EC_USER`/`PROPERTY_EC_PASS` to
`resources/credentials.py`.

### Done well
- **Live recon fit decision applied proactively.** Property's OV-GM navigator has 2 DOM groups -
  `G:0` ("Date") and `G:1` ("Business Unit") - which superficially looks like the disqualifying
  "per-field navigator groups" shape. Live read-only recon
  (`Workplaces/property-area-pattern/recon_property_nav.py`, no Save/Insert/Delete) found `G:0`'s
  Date field already carries a non-empty default on load (`MandatoryCellStyleWhite`), so `G:1`'s
  Business Unit dropdown (at `C:0`, not the usual `C:1`) is the ONLY genuinely mandatory+empty
  field - exactly one group needs a fill, fitting Area's pattern, same shape already proven on
  Tract (PR #555). Unlike Tract's own build, this was correctly identified as fitting WITHOUT a
  wrong-then-corrected detour - the owner's Tract lesson (verify each field, not shape-match) was
  applied proactively here.
- Business Unit dropdown confirmed live to hold 16 options including "Royalty Canada" (matches
  the prior driver's proven value).
- Live 5/5 pass, full-tree dryrun 878/878 (zero collisions), robocop parity vs Area's own 7-issue
  baseline (same VAR02+DOC02 kind/count), DB self-clean confirmed (0 residual `AUTOTEST%` rows in
  `OV_PROPERTY` via a fresh independent oracledb connection), grid-filter keyword confirmed fired
  15 times via `grep -c "Find Object Row By Filter" output.xml`.

### Done wrong / lessons
- None disclosed as a build defect in this conversion's own PR body - the recon-first approach
  (checking each nav group's live mandatory+empty state before concluding fit/no-fit) avoided
  repeating Tract's earlier wrong-then-corrected classification.

### Blockers -> resolution
- **Shared working directory collision (real, disclosed in PR #559's body):** started in the
  shared repo checkout (`c:\Projects\ChoongYin_OS`) per the dispatched task's own git
  instructions. Mid-task, discovered other parallel Area-pattern-conversion agents were checking
  out and committing to their own branches in that SAME shared working directory, which silently
  discarded some in-progress uncommitted edits (`resources/credentials.py` + 3 docs files) via
  what appeared to be a forced branch switch. No functional/page-object files were lost (no other
  agent touched Property's own files). Resolution: re-did the lost doc/credentials edits from
  scratch in a dedicated git worktree (`c:/Projects/ChoongYin_OS_worktrees/property-area-pattern`)
  and re-ran every verification step there before pushing.

### Decisions
- Because the mandatory dropdown lives at `G:1/C:0` rather than the shared keyword's previously-
  assumed `G:0/C:1`, the shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`) needed the SAME optional `${group}`/`${start_col}`
  extension already added by Tract's own conversion (PR #555, merged 2026-08-26, ahead of
  Property's). Property's PR reused that existing extension rather than building a parallel one -
  called with `group=1 start_col=0`; default values preserve every existing caller's behavior
  unchanged (Area/Well/Test Separator/Chemical Tank/Price Object/Meter all still omit them).
- Playwright driver `py/property_iud.py` deliberately left untouched - this was an RF-only
  structural conversion, matching the owner's engine-replaces-Playwright direction.

### Evidence (PR #559)
- Live 5/5 pass (`EC_HEADLESS=true robot tests/Configuration/Assets/Data_Mapping_Objects/
  property_iud.robot`), full-tree dryrun 878/878, DB self-clean 0 residual `AUTOTEST%` rows
  (fresh oracledb connection), grid-filter grep count 15, robocop parity vs Area's baseline,
  `check_bundle_hygiene.py` PASS.

## 2026-08-28 - Lean-deliverable backfill (Batch 5, this session)

### Built
Owner decision 2026-08-27 retired the 2026-08-23/26 lean waiver (`docs/
IUD-DELIVERABLE-CHECKLIST.md` Section H) - this session backfills the SOW/README/JOURNAL/
evidence/CHECKLIST/KB-map artifacts that waiver had skipped for Property's PR #559 conversion.
Updated `property_sow.md`, `README.md`, this `JOURNAL.md`, `CHECKLIST.md`, and
`ec-ui-knowledge/screens/property.md` to reflect the real Area-pattern shape (5 TCs, `group=1
start_col=0`, Tract precedent) pulled from PR #559's own body - not invented. Did NOT touch
`property_page.resource`, `property_iud.robot`, `manage_object.resource`, or any other RF
automation file.

### Done well
- Re-ran the existing, already-proven suite ONE time live for fresh evidence, in an isolated
  worktree, without modifying it: dryrun 5/5 PASS, live headless run 5/5 PASS on the FIRST
  attempt (no retry needed), grid-filter grep count 15 (matches PR #559's own cited count),
  per-step screenshots captured automatically by the suite's own Capture Step calls.

### Done wrong / lessons
- None - this backfill only added documentation/evidence around an already-working, already-
  verified suite, per the work order's explicit "do NOT re-run the full original build" scope.

### Blockers -> resolution
- None encountered this session (no live-run timeout or browser error hit; no retry needed).

### Decisions
- Retained the original `VERIFY-REPORT.md` (from the 2026-08-02 build, pre-Area-pattern) as-is
  rather than regenerating it - the work order's scope is documentation/evidence backfill around
  the merged PR #559 conversion, not a fresh `verify_screen.py` run; the CHECKLIST cites the fresh
  dryrun/live-run/grep evidence captured this session directly instead.

### Evidence (this backfill session)
- `evidence/` - `property_backfill_live_summary.md` (dryrun 5/5, live 5/5, grid-filter grep=15,
  captured 2026-08-28) + the live run's own screenshots/log.html/output.xml copied in.
