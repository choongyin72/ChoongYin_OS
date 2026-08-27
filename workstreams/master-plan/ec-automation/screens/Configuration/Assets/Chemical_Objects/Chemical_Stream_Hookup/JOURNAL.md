# JOURNAL - Chemical Stream Hookup (CO.0260) OV-GM IUD

## 2026-08-01
- **Branch:** `feature/chemical-stream-hookup-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'chemical_stream_hookup'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/chemical_stream_hookup/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: Production Unit -> Area -> Facility Class 1 cascade + GO. Mandatory Chemical Stream Hookup Code / Chemical Stream Hookup Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal the nav PU - probe per screen). Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

## 2026-08-26 — Area-pattern conversion (PR #544)

### Built
- Converted the RF IUD suite from the OLD pattern (4 TCs, single suite-level login, inline `Apply
  OV-GM Navigator First Available`, screen-local inline DB-verify wrapper keywords) to Area's full
  pattern: 5 TCs (added TC04 Find), per-TC login/logout, fixed test code `AUTOTEST_CSH` (replacing
  the old timestamped `AUTOTEST_CSH_<timestamp>`), properties-file-driven insert/update, explicit
  grid-filter wiring (`Find/Clear Chemical Stream Hookup Row By Filter`), and the mandatory
  3-level cascade navigator (Production Unit -> Area -> Facility Class 1) delegated to the shared
  T2 `Apply Navigator From Properties` keyword via a new
  `testdata/chemical_stream_hookup_navigator.properties`.
- New test-data files: `chemical_stream_hookup_{navigator,insert,update,form_verify,grid_verify}.properties`.
- Registry row (`docs/ec_screen_registry.md`) MODIFIED in place (not a new row); scorecard row
  modified likewise.
- `resources/manage_object.resource` (shared T2) NOT modified — no gap found for this screen's
  cascade.

### Done well
- Live-probed the 3 navigator values instead of assuming a sibling screen's scope: "the mandatory
  3-level cascade navigator ... whose 3 values were confirmed LIVE via a temporary probe (not
  guessed, not copied from Well's own 'P1 ...' scope)" (PR #544 body). Values:
  `AS1 EC Exploration Norway` / `AS1_Area` / `AS1_Facility_01`.
- Kept the screen's standalone `mandatory_field_gate.resource` pre-flight check exactly as-is per
  explicit owner instruction — extracted a new T3-local `Fill Object Form Fields And Save With
  Gate` helper (to stay under the house keyword-length convention) rather than inlining the gate
  call twice or touching the shared gate resource itself.
- Full verification before declaring done: live run 5/5 PASS, full-tree dryrun 850/850 PASS (zero
  collisions), robocop 7 issues (VAR02 x2 + DOC02 x5) at exact parity with Area's own
  reference-pattern files, DB self-clean via a FRESH oracledb connection both before (`AUTOTEST_CSH`
  count = 0) and after (`AUTOTEST%` count = 0) the run, and a `grep -c` confirming zero inline
  DB-verify calls remain in the `.robot` file (pure-screen verification; the one DB check that
  remains lives in the shared T2 `Verify Object Removed`).
- Isolated worktree (`C:/tmp/wt-csh`, `feature/chemical-stream-hookup-area-pattern`), synced with
  `origin/master` before pushing, no self-merge, no shared-file edits outside the two owned RF
  files plus the additive `credentials.py`/registry/scorecard rows.

### Done wrong / lessons
- No regressions or wrong turns disclosed in PR #544's body for this specific conversion.

### Blockers -> resolution
- None disclosed in PR #544.

### Decisions
- Playwright bundle stays waived permanently for this conversion and this backfill (owner decision
  2026-08-27, `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — `py/chemical_stream_hookup_iud.py`
  from the 2026-08-01 build is preserved as-is, NOT touched, re-verified, or regenerated.
- The RF suite remains the maintained/live test; the Playwright driver is historical reference
  only (README.md updated to say so explicitly).

### Evidence
- Live run: `EC_HEADLESS=true robot .../chemical_stream_hookup_iud.robot` -> 5/5 PASS.
- Full-tree dryrun: `robot --dryrun tests/` -> 850/850 PASS, zero collisions.
- `robocop check` on the 2 changed files -> 7 issues (VAR02 x2 + DOC02 x5), parity with Area.
- DB self-clean: fresh oracledb connection before AND after -> 0 rows / 0 residual `AUTOTEST%` in
  `OV_CHEM_STRM_HOOKUP`.
- `grep -c "Find Object Row By Filter" output.xml` -> 22 hits (filter keyword genuinely fired).
- No screenshot evidence was captured for this conversion (RF run, not Playwright) — see
  `README.md` and `CHECKLIST.md` item 6 for how this backfill records that gap honestly.

## 2026-08-27 — Documentation/evidence backfill (this task)

_This entry documents the retroactive backfill required by `docs/lean-deliverable-backfill-workorder.md`
(Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retiring the 2026-08-23/26 lean waiver). Chemical
Stream Hookup already had a FULL bundle (SOW/README/JOURNAL/evidence/investigation/CHECKLIST/
VERIFY-REPORT/KB map) from its original 2026-08-01 build — predating the lean waiver entirely — but
those artifacts described only the OLD 4-TC pre-conversion structure. This backfill updates them to
also document the PR #544 Area-pattern conversion; it does NOT rebuild, modify, or re-verify the RF
automation, the Playwright driver, or `mandatory_field_gate.resource`._

### Built
- Updated `chemical_stream_hookup_sow.md` (added §2, the PR #544 conversion story + live-probed
  navigator values + the mandatory_field_gate design-decision writeup).
- Updated `README.md` (added the RF run commands, DB self-clean query, and an explicit note that
  no screenshot evidence exists for the 5-TC conversion — cited from PR #544 instead of fabricated).
- Updated this `JOURNAL.md` with the two sections above.
- Updated `CHECKLIST.md` to reflect the current (post-PR #544) state of every gate, citing PR #544
  and the registry row as evidence sources where no fresh command was re-run.
- Updated `ec-ui-knowledge/screens/chemical_stream_hookup.md` (KB map) with the 5-TC structure,
  the confirmed navigator values, the `mandatory_field_gate.resource` mechanism, and the
  `Find/Clear ... Row By Filter` grid-filter wiring.

### Done well
- Every claim in the updated docs is traceable to a real source: PR #544's body text (fetched via
  `gh pr view 544`), `docs/ec_screen_registry.md`'s Chemical Stream Hookup row,
  `chemical_stream_hookup_page.resource`'s own Variables/Documentation, and the
  `testdata/chemical_stream_hookup_navigator.properties` comment header.
- Did not fabricate evidence: confirmed via file timestamps that the existing `evidence/csh_0*.png`
  screenshots (2026-08-01/02) and `results/_verify_live/chemical_stream_hookup_tc0*.png`
  (2026-08-01) both PREDATE PR #544 (merged 2026-08-26) — they document the OLD 4-TC structure,
  not the current one. Rather than presenting them as evidence of the current suite, this backfill
  states that plainly and cites the PR #544 body's own verification output instead.
- `mandatory_field_gate.resource` and `manage_object.resource` were read-only inputs — neither was
  modified.

### Done wrong / lessons
- None — no automation files were touched, no live run was executed by this backfill task (per the
  task's own scope: "you do NOT need to execute a fresh live run").

### Blockers -> resolution
- None.

### Decisions
- Evidence for the 5-TC structure rests primarily on PR #544's own already-executed,
  already-merged verification record, cited throughout. This session additionally captured one
  fresh confirmation run for evidence purposes (see the entry below) — still a docs/evidence
  backfill; no automation file was touched to produce it.

### Evidence
- PR #544: https://github.com/choongyin72/ChoongYin_OS/pull/544 (merged 2026-08-26T08:05:59Z).
- Registry row: `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (Chemical Stream
  Hookup row, modified in place by PR #544).
- Pre-existing screenshots (2026-08-01/02, pre-conversion): `evidence/csh_0[1-5]_*.png`,
  `evidence/results.json`.

## 2026-08-27 (same day) — fresh confirmation run for evidence capture

_Item 4 of `docs/lean-deliverable-backfill-workorder.md` allows re-running the screen's live suite
ONE more time for fresh evidence capture ("this does not need a NEW live-testing pass beyond what
'done' already required - it's evidence capture of a real run, not a fresh verification cycle").
This entry records that one confirmation run, executed against the already-working, unmodified
PR #544 automation._

### Built
- No automation files changed. Ran the EXISTING, ALREADY-MERGED PR #544 suite as-is, from the
  isolated worktree `C:/tmp/wt-csh-backfill`, purely to capture fresh evidence artifacts.

### Done well
- Checked for stray `chrome.exe` processes BEFORE the live run (`tasklist | grep -i chrome` ->
  only an unrelated `chrome-native-host.exe`, no stray browser) per the standing rule to rule out
  an environment issue before assuming a code defect.
- `robot --dryrun` -> **5/5 PASS, 0 fail**.
- `robocop check` on the 2 automation files -> **7 issues (VAR02 x2 + DOC02 x5)** — exact parity
  with PR #544's own cited count.
- Confirmed the corp sandbox reachable first (`curl -sk https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
  -> HTTP 302) before running live.
- `EC_HEADLESS=true robot ... chemical_stream_hookup_iud.robot` -> **5/5 PASS, 0 fail**.
- `grep -c "Find Object Row By Filter" output.xml` -> **15 hits** (non-zero; filter keyword
  genuinely fired — a different count from PR #544's cited 22 is expected, this is an independent
  fresh run producing its own `output.xml`, not the same file).
- `grep -c` for inline DB-verify keywords in the `.robot` FILE ITSELF (source, not output.xml,
  which legitimately shows 1 hit via the shared T2's own internal call to `Verify Object Removed`)
  -> **0** — confirms pure-screen verification, matching PR #544's design.
- Fresh `oracledb` connection (`localhost:1521/ORCL`, `ECKERNEL_EC`) AFTER the run ->
  `SELECT COUNT(*) FROM OV_CHEM_STRM_HOOKUP WHERE CODE LIKE 'AUTOTEST%'` = **0** (self-clean
  confirmed independently, not reused from the test session).
- `py scripts/check_bundle_hygiene.py` (repo-wide) -> **RESULT: PASS** (no hardcoded creds, ASCII
  clean, no CHECKLIST/VERIFY-REPORT contradiction attributable to this screen).

### Done wrong / lessons
- None. No blockers hit.

### Evidence
- `evidence/2026-08-27-area-pattern-backfill/log.html`, `report.html`, `output.xml`,
  `results.json` — the real artifacts from this run.
