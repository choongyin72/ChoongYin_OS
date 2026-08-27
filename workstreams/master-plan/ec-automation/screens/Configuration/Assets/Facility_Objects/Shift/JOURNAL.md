# JOURNAL - Shift (CO.0224) OV-GM IUD

_Screen: Configuration > Assets > Facility_Objects > Shift (OV-GM, date-effective). View
`OV_SHIFT`. Modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s
structure per `docs/lean-deliverable-backfill-workorder.md` (Batch 4)._

## Built

### 2026-07-31 - original 4-TC build (`feature/shift-iud-v3`)
- Previously PARKED: mandatory free-text field **Start Time (HH:MI)** - the field class the
  OV-GM generator cannot fill (only Code/Name/Start Date + dropdowns/popups).
- **UNPARKED without any generator change:** hand-built (4 prior hand-builds had already
  established the pattern) - the fix was literally one extra text field in the insert list.
- **Field semantics from EXISTING DATA (owner technique):** owner screenshot of the P1 S001
  row's edit form gave every element's ground truth - Start Time format '07:00', Op Production
  Unit set to the nav PU, Duration/Period/Cycle optional.
- Navigator = SPECIFIC P1 values (P1 Production Unit -> P1 Area -> P1 Facility 1); Op
  Production Unit = nav PU (parent-matching).
- `verify_screen.py` -> OVERALL PASS (first try): robocop 0, hygiene 0, dryrun 4/4, LIVE RF
  4/4, Playwright 8/8. DB residual 0.

### 2026-08-26 - PR #547: converted to Area's full pattern
- **What was built (from PR #547's own body):** converted Shift's existing RF automation
  (bespoke inline-navigator, suite-level-login OLD pattern) to Area's full pattern: 5 TCs
  (TC01 Verify Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete), per-TC
  login/logout, navigator fill delegated to the shared T2 `Apply Navigator From Properties`
  keyword driven by a new `shift_navigator.properties` (EXPLICIT SPECIFIC P1 values for the
  genuine 3-level Production Unit -> Area -> Facility Class 1 same-row cascade, confirmed via
  the prior driver's literal locators `nav:form:G:0:R:1:C:1/2/3:dd`), fixed test code
  (`AUTOTEST_SHIFT`), properties-file-driven insert/update/verify, explicit grid-filter wiring,
  zero inline DB-verify calls. The mandatory free-text Start Time (HH:MI) insert-form field was
  kept exactly as the prior driver proved it (`07:00`) - just moved into
  `shift_insert.properties`, auto-detected as a plain text field by the existing shared
  `Fill OV Field By Label Any Kind` mechanism, no special-casing needed.
- **Files touched (PR #547):** `pageobjects/.../shift_page.resource` (rebuilt to Area's shape),
  `tests/.../shift_iud.robot` (rebuilt: 5 TCs, per-TC login), `resources/credentials.py`
  (added `SHIFT_EC_USER`/`SHIFT_EC_PASS`, additive only), 5 new `testdata/shift_*.properties`
  files, plus the registry/scorecard rows modified (not new entries).
- **Evidence cited in PR #547:** live run 5/5 PASS; full-tree dryrun 850/850 PASS (0 regression);
  robocop parity - 10 issues, same pre-existing DOC02/COM04/DOC03/MISC06 shape as Area's own
  baseline, no new issues; DB self-clean (fresh `oracledb` connection, `localhost:1521/ORCL`,
  `ECKERNEL_EC`) - `OV_SHIFT` `CODE='AUTOTEST_SHIFT'` = 0 and `CODE LIKE 'AUTOTEST%'` = 0;
  grid-filter fired 15x / cleared 15x (`grep -c` on `output.xml`); zero inline DB-verify calls
  confirmed by grep.

### 2026-08-28 - this backfill (Batch 4, `docs/lean-deliverable-backfill-workorder.md`)
- Added the SOW/README/JOURNAL/evidence/CHECKLIST/KB-map artifacts that Section G's now-retired
  lean waiver had skipped around PR #547's already-merged conversion (owner decision
  2026-08-27, Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Re-ran the suite once live purely to capture fresh evidence - **did not modify any RF/
  Playwright automation file**. Results: dryrun 5/5 PASS, full-tree dryrun 883/883 PASS, live
  headless 5/5 PASS (first attempt, no retry needed), robocop 7 issues/exit=0 (DOC02-only,
  non-fatal, no regression - this backfill touched no RF files), hygiene PASS (repo-wide scan,
  no Shift contradiction), DB self-clean 0 residual via a fresh `oracledb` connection.

## Done well
- PR #547's conversion reused the shared T2 `Apply Navigator From Properties` keyword instead
  of inlining a bespoke navigator fill - Shift now follows the same shape as every other
  converted OV-GM screen (Area/Well/Facility Class 1), reducing screen-specific code to the
  properties file + a handful of thin wrapper keywords.
- The mandatory free-text Start Time field was NOT re-engineered during the structural
  conversion - it was moved as-is into the properties file, avoiding scope creep into a
  conversion that was supposed to be structure-only.
- This backfill's live re-run passed 5/5 on the first attempt, confirming the merged PR #547
  automation is genuinely still working, not just claimed-working.

## Done wrong / lessons
- **Windows long-path git-worktree failure (2026-08-26, during the PR #547 conversion
  session):** creating the isolated worktree for the conversion work failed on a Windows
  long-path limitation partway through checkout. This was a genuine environment/tooling
  incident, not a Shift-screen or automation defect. **Resolution (owner-approved):**
  `git config --local core.longpaths true` was applied, after which the worktree checkout
  completed normally. Verified for this backfill session: `git config --local core.longpaths`
  on the main repo clone returns `true`, and creating this backfill's own worktree
  (`C:/tmp/wt-shift-backfill`) completed cleanly with no long-path error - confirming the fix
  is still in effect and the incident has not recurred.
- The 2026-07-31 build's original JOURNAL entry noted the "generator extension" framing for the
  free-text field had gone stale (treating a one-line addition as a tooling project) - carried
  forward here since it remains a good general lesson, not re-litigated.

## Blockers -> resolution
- **2026-08-26 (PR #547 session):** Windows long-path git-worktree checkout failure -> resolved
  via owner-approved `git config --local core.longpaths true` (see "Done wrong / lessons" above).
- **2026-08-28 (this backfill):** no blockers - dryrun, full-tree dryrun, live run, hygiene, and
  DB self-clean all passed on the first attempt; no retry was needed.

## Decisions
- Playwright bundle (`py/shift_iud.py`) stays as-is and out of this backfill's scope - Section H
  of `docs/IUD-DELIVERABLE-CHECKLIST.md` permanently waives rebuilding/re-verifying the
  Playwright bundle for Bank-/Area-pattern conversions, since the Universal Screen Engine is
  the owner-decided replacement going forward.
- The pre-existing `evidence/` screenshots (`sh_0[1-5]_*.png`, dated 2026-07-31) were left in
  place rather than deleted or overwritten - they document a real prior run of the (now
  superseded) 4-TC/Playwright shape. The new RF live-run evidence from this backfill was added
  as a separate dated subfolder, `evidence/rf_backfill_2026-08-28/`, to avoid conflating the two.

## Evidence
- PR #547 (2026-08-26): live RF 5/5, full-tree dryrun 850/850, robocop parity (10 issues, no
  new), DB self-clean confirmed - see PR #547 body (`gh pr view 547`) for the exact citations.
- This backfill (2026-08-28): `evidence/rf_backfill_2026-08-28/` - `log.html`/`report.html`/
  `output.xml` from a live 5/5 run, plus per-TC-step screenshots and `results-summary.md`
  documenting every command run and its real output.
