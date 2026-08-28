# JOURNAL - Data Extract Set IUD

_Screen: Configuration > Assets > Data_Mapping_Objects > Data Extract Set (OV, date-effective,
Bank family). View `OV_SUMMARY_SET`. This JOURNAL was backfilled 2026-08-28 (Batch 11 of
`docs/lean-deliverable-backfill-workorder.md` - Section H retired the 2026-08-23 lean waiver that
let PR #474's Bank-pattern conversion skip SOW/JOURNAL/evidence/KB). Pulled from PR #474's real
body and the pre-existing 2026-07-26 entry below, not invented._

## Built

### 2026-07-26 (original build, generic engine)
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Data_Mapping_Objects > Data Extract Set. Plain Bank-layout OV (single
  Date+GO nav, mandatory extra beyond Code/Name/Start Date: Owner Class dropdown).
- Label-driven T3 (no hardcoded ids), built on the shared `ec_object_iud.py` engine + `DbVerify.py`.
- Playwright driver -> 7/7; RF T3 + suite (4 TCs) -> live 4/4.
- `verify_screen.py` -> OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

### 2026-08-23 (PR #474, Batch 10 - Bank-pattern conversion)
- Rebuilt `data_extract_set_page.resource` + `data_extract_set_iud.robot` to the FULL Bank-pattern
  shape used by `bank_page.resource`/`berth_page.resource`: properties-file-driven insert/update/
  verify, explicit grid-filter wiring (`Find/Clear Data Extract Set Row By Filter`), dedicated
  credential pair (`DATA_EXTRACT_SET_EC_USER/PASS` in `resources/credentials.py`), fixed test code
  `AUTOTEST_DXT` (replacing the earlier timestamp-suffixed code).
- New testdata: `data_extract_set_{insert,update,form_verify,grid_verify}.properties`.
- Suite expanded from 4 TCs to 5 (clean-state / insert / update / find / delete), each with its own
  Login/Logout on one browser opened in Suite Setup - Bank/Berth's convention.
- No `resources/manage_object.resource` or `resources/common.resource` changes - all needed T2
  keywords already existed.
- Registry (`ec_screen_registry.md`) and scorecard (`automation-scorecard.md`) rows **MODIFIED**, not
  added - this screen already had a 2026-07-26 build.

## Done well
- Full I-U-D DB-verified vs `OV_SUMMARY_SET` (insert Code/Name/Owner Class, update Name, delete
  End=Start absent); self-clean 0 residual via a **fresh** `oracledb` connection, checked both
  before AND after the live run (not assumed from the suite's own PASS status).
- Live RF 5/5 (2026-08-23); `robot --dryrun` on the FULL tests/ tree: 767/767 PASS (no regression
  introduced elsewhere).
- Sibling screen `Data Extract Setup` (SP.0043, `data_extract_setup_page.resource`) explicitly
  identified and left untouched - confirmed as a DIFFERENT screen, not a duplicate/typo target.

## Done wrong / lessons
- **Factual error carried from the 2026-07-26 build:** the original SOW/registry row described
  Owner Class as an "optional dropdown, skipped." Re-checking the live form and the screen's own
  SOW during the 2026-08-23 rebuild showed Owner Class is actually **mandatory** at Insert (present
  in `objectForm`, just not in `updateAttributes`). PR #474 corrected this in the registry row text
  directly ("also corrects a factual error in the old row"). Lesson: a prior build's own SOW is a
  starting point, not a substitute for re-verifying mandatory/optional against the live form before
  reusing it in a rebuild.
- **This backfill's own gap (documentation debt, not automation):** the 2026-07-26 bundle's SOW,
  README, JOURNAL, CHECKLIST, and the KB map (`ec-ui-knowledge/screens/data_extract_set.md`) were
  never updated when PR #474 rebuilt the RF layer 2026-08-23 - they sat one generation stale
  (describing 4 TCs / no grid-filter / no properties files) even though the code and registry row
  had already moved on. This backfill (2026-08-28) is what closes that gap.

## Blockers -> resolution
- No hard blockers on either the 2026-07-26 build or the 2026-08-23 rebuild; PR #474 reports a
  clean run with no data-damage or flake disclosed in its body.

## Decisions
- Playwright driver (`py/data_extract_set_iud.py`) stays as-is, unchanged by PR #474 and untouched by
  this backfill - owner decision 2026-08-27 (Section H) waives new Playwright-bundle work in favour
  of the Universal Screen Engine going forward.
- Fixed test code (`AUTOTEST_DXT`) chosen over the earlier timestamp-suffixed code to match
  Bank/Berth's convention - trades a small self-clean risk (a failed run leaves the code stuck since
  EC never lets a deleted code be reused) for consistency with the rest of the Bank-pattern fleet.

## Evidence
- PR #474: live RF 5/5, dryrun 767/767 (full tree), DB self-clean before/after via fresh connection,
  robocop same-profile-as-`berth_iud.robot` (5 DOC02 + 4 VAR02, no regression).
- This backfill's evidence-capture run: see `evidence/` (screenshots from the 2026-07-26 build,
  pre-dating the rebuild's TC numbering, retained for history) + this session's own live-run capture
  under `evidence/live_run_2026-08-28/` (see `README.md` / `CHECKLIST.md` for the exact result).
