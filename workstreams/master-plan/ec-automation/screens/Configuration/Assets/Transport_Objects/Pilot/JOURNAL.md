# JOURNAL - Pilot (CO.2079) OV-GM IUD

## 2026-07-31
- **Branch:** `feature/pilot-iud`. Group A #8. Standard OV-GM - the plainest screen of this batch.
- **Registry-first check mattered here:** an early substring-based audit had wrongly listed Pilot as
  "already documented (PASS)" (it was matching the *Pilot Boat* row). `grep -c "^| Pilot |"` = 0 and
  the exact-match audit proved it genuinely unbuilt. Same defect class as issue #278/#265: a loose
  match reporting a wrong-but-plausible answer.
- **Recon (executed):** 3-level cascade + GO, grid `manageObject:form:T_data`, mandatory
  Code/Name/Start Date only, Op Production Unit present. DB: OV_PILOT = 8 rows.
- Generated with `tmp/gen_ovgm.py`; **8/8 driver and all 5 gates PASS on the FIRST run.**
- **Validator improvement made here:** `tmp/check_row_vocab.py` reported "4 rows for Pilot" because
  its prefix match also caught "Pilot Boat". Tightened to EXACT first-cell equality; re-validated -
  Pilot 2 rows, Pilot Boat 2 rows, both clean. (Also proved the validator correctly reports
  "no row found" for a screen whose PR is not yet merged - e.g. Driver on this branch.)

## Lessons
- Prefix matching keeps producing wrong-but-plausible results (Pilot/Pilot Boat here; the phantom
  screen names earlier). Match identifiers EXACTLY - in audits and in tooling.

## 2026-08-26 - PR #560: Area-pattern structural conversion

### Built
- Converted Pilot's existing OV-GM RF suite from the old single-login/4-TC/inline-DB-verify/
  "Apply OV-GM Navigator First Available" pattern to the full Area-pattern structure: 5 TCs (added
  TC04 Find) with per-TC Login/Logout, fixed `AUTOTEST_PILOT` test code, navigator fill delegated
  to the shared `Apply Navigator From Properties` keyword, properties-file-driven insert/update/
  verify, explicit `Find/Clear Pilot Row By Filter` grid-filter wiring, zero inline DB-verify calls.
- New: `testdata/pilot_{navigator,insert,update,form_verify,grid_verify}.properties`; additive
  `PILOT_EC_USER`/`PILOT_EC_PASS` in `resources/credentials.py`.

### Done well
- Live recon (2026-08-26) confirmed Pilot's navigator is a single-group, same-row 3-level cascade
  (`nav:form:G:0:R:1:C:1/C:2/C:3` = Production Unit -> Area -> Facility Class 1, all
  MandatoryCellStyle) - the exact shape already proven on Well. FITS the Area pattern; no
  reclassification needed.
- Live headless run 5/5 PASS, run TWICE (once shared tree, once isolated worktree) - both 5/5.
  Fresh oracledb connection after the run: 0 rows for `AUTOTEST%` in `OV_PILOT` (self-clean
  confirmed). `Find Object Row By Filter` confirmed firing 15x via grep on output.xml. Full-tree
  dryrun 875/875, zero collisions. robocop parity (7 issues, same kind/count as Area's own baseline
  - not a regression). Bundle hygiene PASS.

### Decisions (not "done wrong" - a genuine, evidenced exception)
- **Op Production Unit kept as `__FIRST__`, not forced to reuse the navigator's Production Unit
  value.** The general field-reuse rule (applied elsewhere, e.g. Area's Op Production Unit =
  navigator PU) does NOT apply here: the pre-existing `py/pilot_iud.py` driver's own code comment
  states "the nav PU is not necessarily a valid Op PU option" - live evidence that Op Production
  Unit's value domain is INDEPENDENT of the navigator's Production Unit for this screen, proven by
  that driver's own 8/8 pass using `__FIRST__`. This is a documented, evidenced exception applied
  deliberately, not a rule violation or an oversight.
- Pilot remains classified OV-GM throughout - the genuine 3-level navigator + GO gesture was kept,
  not removed; only the RF STRUCTURE (TC count, login pattern, properties-driven fill/verify) was
  converted to match Area's shape.

### Blockers -> resolution
- None disclosed in PR #560's body - clean conversion, no regression, no flake.

## 2026-08-28 - Documentation/evidence backfill (this session)

_Per `docs/lean-deliverable-backfill-workorder.md` (owner decision 2026-08-27, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`, Batch 5) - backfilling SOW/README/JOURNAL/evidence/CHECKLIST/
KB map around already-merged, already-live-tested automation (PR #560). No RF file
(`pilot_page.resource`, `pilot_iud.robot`, `testdata/pilot_*.properties`) was modified to produce
this session's artifacts._

### Built
- Refreshed `pilot_sow.md` with a 2026-08-28 addendum documenting PR #560's real conversion + the
  Op Production Unit exception (pulled from `gh pr view 560`'s body, not invented).
- Refreshed `README.md` to describe the current 5-TC RF shape (was stale, describing the old 4-TC
  in-suite-DB-verify shape).
- This `JOURNAL.md` entry.
- Refreshed `CHECKLIST.md` against the current 21-item `docs/IUD-DELIVERABLE-CHECKLIST.md`.
- Refreshed `ec-ui-knowledge/screens/pilot.md` (was stale, describing the pre-#560 4-TC structure
  and the old `verify_screen.py`-only gate history).

### Done well
- Isolated worktree (`C:/tmp/wt-pilot-backfill`), branch `docs/pilot-backfill-artifacts`, off
  `origin/master` - no shared-environment interference.
- `robot --dryrun tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` -> **5/5 PASS**.
- `EC_HEADLESS=true robot tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` -> **5/5
  PASS on the first live run** - no retry needed, no regression from PR #560.
- `py -m robocop check pageobjects/.../pilot_page.resource tests/.../pilot_iud.robot` -> **7
  issues** (DOC02, missing TC-level `[Documentation]`) - matches PR #560's cited 7-issue baseline
  exactly, no drift.
- `py scripts/check_bundle_hygiene.py` (repo-wide) -> PASS.
- `DbVerify.fetch_object("OV_PILOT", "AUTOTEST_PILOT")` via a fresh oracledb connection (script:
  `Workplaces/pilot-backfill/db_selfclean_check.py`) -> `None` (confirmed absent) after the live run.
- Grid-filter keyword confirmed firing: `grep -c "Find Pilot Row By Filter\|Find Object Row By
  Filter"` on this session's output.xml -> 29.
- Evidence captured: `log.html`/`output.xml`/`report.html` from the live run, added alongside the
  pre-existing 2026-07-31 Playwright evidence (`pl_0[1-5]_*.png`, `results.json` - unchanged).

### Done wrong / lessons
- None - the live run passed clean on the first attempt; no automation defect or flake surfaced
  during this backfill's evidence capture.

### Blockers -> resolution
- None. No live-run timeout or browser error was hit during this session's evidence capture (the
  live run did exceed the tool's 120s foreground window and was moved to background execution by
  the harness, but it completed normally with exit code 0 and 5/5 PASS - not a failure requiring
  the retry-once/disclose protocol).

### Decisions
- Automation files (`pilot_page.resource`, `pilot_iud.robot`, `testdata/pilot_*.properties`) were
  NOT touched - this backfill only adds documentation/evidence around already-working automation,
  per the work order's explicit instruction.
- The pre-existing `investigation/` recon script and the original `VERIFY-REPORT.md` (2026-07-31,
  predating PR #560) were left as historical record, not rebuilt or deleted - items 4/5 of the
  21-item checklist stay permanently waived for further build (Section H).

### Evidence
- PR #560: cited live 5/5 (x2 runs), full-tree dryrun 875/875, DB self-clean 0/0, robocop 7-issue
  parity, hygiene PASS - see `gh pr view 560` for the exact commands/output cited.
- This backfill session (2026-08-28):
  - `robot --dryrun` -> 5/5 PASS.
  - `EC_HEADLESS=true robot` -> 5/5 PASS (first attempt).
  - `py -m robocop check` -> 7 issues (DOC02, matches PR #560 baseline).
  - `py scripts/check_bundle_hygiene.py` -> PASS.
  - `DbVerify.fetch_object("OV_PILOT", "AUTOTEST_PILOT")` -> `None` (self-clean confirmed, fresh
    connection).
  - Grid-filter grep count: 29 hits in this session's output.xml.
  - Evidence artifacts: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html` (new,
    this session), alongside `evidence/pl_0[1-5]_*.png`, `evidence/results.json` (pre-existing,
    unchanged).
