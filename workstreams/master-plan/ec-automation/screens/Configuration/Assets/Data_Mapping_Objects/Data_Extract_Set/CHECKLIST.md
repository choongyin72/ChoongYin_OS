# Data Extract Set - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Backfilled 2026-08-28 (Batch 11, `docs/lean-deliverable-backfill-workorder.md`) per Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md` - the 2026-08-23 lean waiver (Section G) that let PR #474 skip
SOW/JOURNAL/evidence/CHECKLIST/KB is retired. Playwright driver (items 4/5) stays waived - the
Universal Screen Engine replaces that role per the owner's 2026-08-27 decision._

## Step 0 - check-existing gate
- [x] 0a KB map existed (`ec-ui-knowledge/screens/data_extract_set.md`, 2026-07-26) - refreshed by this
  backfill to reflect the 2026-08-23 Bank-pattern rebuild.
- [x] 0b grep `data_extract_set_page.resource` across `pageobjects/tests/testdata` -> only this
  screen's own files; sibling `data_extract_setup_page.resource` (Data Extract Setup, SP.0043)
  confirmed as a DIFFERENT screen, untouched.
- [x] 0c PR #474 reused all needed shared T2 keywords (`Insert/Update Object From Properties`,
  `Find/Clear Object Row By Filter`, `Verify Object Insert Exists/Form Record/Found/Removed/Does Not
  Exist`, `Find Object Record`) - zero `resources/manage_object.resource` or `resources/common.resource`
  changes.

## A. Bundle artifacts - `screens/Configuration/Assets/Data_Mapping_Objects/Data_Extract_Set/`
- [x] **1.** `data_extract_set_sow.md` - refreshed this backfill (2026-08-28) to describe the FULL
  Bank-pattern shape + the Owner Class mandatory-field correction from PR #474.
- [x] **2.** `README.md` - refreshed this backfill with the current run commands and DB self-clean
  query.
- [x] **3.** `JOURNAL.md` - refreshed this backfill: Built (both 2026-07-26 original + 2026-08-23
  PR #474 rebuild) / Done well / Done wrong-lessons / Blockers->resolution / Decisions / Evidence,
  pulled from PR #474's real body.
- [ ] **4.** Playwright driver - **N/A, permanently waived** (Section H) - the Universal Screen Engine
  replaces hand-written Playwright drivers going forward. Pre-existing `py/data_extract_set_iud.py`
  (7/7 per PR #474) is untouched.
- [ ] **5.** `investigation/` - **N/A, permanently waived** (Section H), same reasoning as #4.
  Pre-existing `investigation/recon.py` (2026-07-26 build) left in place, untouched.
- [x] **6.** `evidence/` - pre-existing `data_extract_set_0[1-5]_*.png` + `rf_report.html` (2026-07-26,
  4-TC era, retained for history) PLUS this backfill's own live-run capture:
  `evidence/live_run_2026-08-28/` - 23 step screenshots + `output.xml` + `log.html` + `report.html`
  from a real `EC_HEADLESS=true robot` run today (see item 12).
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, PR #474 - NOT modified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_set_page.resource`
  - label-driven, properties-file-driven, grid-filter-wired (mirrors `bank_page.resource`).
- [x] **9.** Suite `tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot` - 5 TCs
  (clean-state / insert / update / find / delete), per-TC Login/Logout.

## C. Verification gates (this backfill's own re-run, 2026-08-28 - screen-scoped, not a full-tree run)
- [x] **10.** robocop clean - re-run fresh this backfill (2026-08-28):
  `py -m robocop check pageobjects/.../data_extract_set_page.resource tests/.../data_extract_set_iud.robot`
  -> "Found 9 issues" (5 DOC02 + 4 VAR02), matching PR #474's cited same-profile-as-`berth_iud.robot`
  result exactly - quality-suggestions only, no regression, no new file touched.
- [x] **11.** `--dryrun` - **5/5 PASS** (this backfill, 2026-08-28):
  `robot --dryrun --outputdir results/_dryrun_des tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot`
  -> "5 tests, 5 passed, 0 failed".
- [x] **12.** LIVE headless run - **5/5 PASS** (this backfill, 2026-08-28):
  `EC_HEADLESS=true robot --outputdir results/_live_des tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot`
  -> "5 tests, 5 passed, 0 failed". Artifacts in `evidence/live_run_2026-08-28/`.
- [x] **13.** DB ground-truth - exact assertion: T2 `Verify Object Removed` ->
  `Code Should Be Absent In View OV_SUMMARY_SET` (DbVerify.py), plus this backfill's own independent
  fresh-connection query (below).
- [x] **14.** FULL I-U-D scope - Insert (Code/Name/Start Date/Owner Class) + Update (Name) + Delete
  (End Date = Start Date) all present and passed in today's live run.
- [x] **15.** Self-clean confirmed - fresh `oracledb` connection (`ECKERNEL_EC`/`localhost:1521/ORCL`,
  this backfill, 2026-08-28, run AFTER the live suite completed):
  `SELECT CODE FROM OV_SUMMARY_SET WHERE CODE = 'AUTOTEST_DXT'` -> `[]` (0 residual rows).
- [x] **16.** Hygiene - re-run fresh this backfill (2026-08-28): `py scripts/check_bundle_hygiene.py`
  -> "RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
  contradictions, doc rows match declared families" (scanned 167 bundles + 272 recon scripts
  repo-wide, including this backfill's own new CHECKLIST.md).

## D. Delivery
- [x] **17.** Registry row - already present, `docs/ec_screen_registry.md` line ~280 (MODIFIED by
  PR #474, not re-touched by this backfill).
- [x] **18.** Scorecard row - already present, `docs/automation-scorecard.md` (MODIFIED by PR #474,
  not re-touched by this backfill).
- [x] **19.** PR - this backfill's own PR, standard 6-field body, base = master, never self-merged.

## E. Knowledge base
- [x] **20.** KB map `ec-ui-knowledge/screens/data_extract_set.md` - refreshed this backfill to
  reflect the 5-TC Bank-pattern shape, grid-filter wiring, and the Owner Class mandatory correction.
- [x] **21.** Reuse clause - this IS a reuse-run scenario (PR #474 rebuilt existing automation);
  JOURNAL + evidence + KB map all refreshed, not just re-ticked.

_This backfill added ONLY documentation and evidence-capture artifacts - no RF/Playwright file was
touched. Items 4/5 (Playwright driver, investigation/) stay permanently unticked/N/A per Section H's
Universal Screen Engine waiver, not because anything is missing._
