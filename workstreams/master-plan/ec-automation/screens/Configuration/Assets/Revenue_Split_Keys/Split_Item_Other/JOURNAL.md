# JOURNAL - Split Item Other (CD.0017) OV IUD

_Screen: Configuration > Assets > Revenue_Split_Keys > Split Item Other (OV, date-effective).
View `OV_SPLIT_ITEM_OTHER`, class `SPLIT_ITEM_OTHER`, controller `manage_object_nav`. Not the
same screen as the "* Split Key" siblings (class `SPLIT_KEY`, view `OV_SPLIT_KEY`)._

## 2026-07-26 - original build
- **Branch:** `feature/split_item_other-iud` (10th OV-reuse-target). Check-existing gate: only
  this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Revenue_Split_Keys > Split Item Other. Mandatory Code/Name/Start
  Date; optional dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, no mandatory
  dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 7/7.

### Lessons (2026-07-26)
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.

## 2026-08-23 - Bank-pattern rebuild (PR #471, Batch 10)

### Built
- Upgraded the T3 (`split_item_other_page.resource`) and suite (`split_item_other_iud.robot`)
  from the partial label-driven build above to the full Bank/Berth pattern:
  properties-file-driven insert/update/verify (`Insert Object From Properties And Verify Code`,
  `Update Object From Properties`, `Verify Object Insert Exists`/`Verify Object Form Record`/
  `Verify Object Found`) and explicit grid-filter wiring (`Find/Clear Split Item Other Row By
  Filter` -> shared T2) wired into Update/Find/Verify-Found/Delete.
- New testdata files: `split_item_other_insert.properties`, `_update.properties`,
  `_form_verify.properties`, `_grid_verify.properties`.
- Rebuilt to the 5-TC business narrative (TC01 Verify Clean State / TC02 Insert / TC03 Update /
  TC04 Find / TC05 Delete) with per-TC Login/Logout on one Suite-Setup browser, and a dedicated
  credential pair `SPLIT_ITEM_OTHER_EC_USER`/`SPLIT_ITEM_OTHER_EC_PASS` (additive to
  `resources/credentials.py`), matching the 2026-08-22 standing decision that every EC screen
  gets its own credentials.
- MODIFIED (did not re-add) the existing `docs/ec_screen_registry.md` and
  `docs/automation-scorecard.md` rows from the 2026-07-26 build.

### Done well
- Confirmed the live field set directly from the existing page object plus the already-proven
  Playwright driver `py/split_item_other_iud.py` - no CSS/label guessing needed. Mandatory
  `Split Item Code` (screen-prefixed) / GENERIC `Name` (not screen-prefixed) / `Start Date`; no
  mandatory dropdowns.
- Live 5/5 (TC01-05). `robot --dryrun` on the full `tests/` tree: 767/767 pass (no cross-screen
  regression). `Find Object Row By Filter` confirmed fired 30x via `grep -c` on output.xml - not
  assumed from the code, checked against the real run.
- Fresh `oracledb` connection query confirmed 0 residual `AUTOTEST_SIO` rows both before and
  after the live run - the self-clean claim is DB-verified, not screen-inferred.
- No shared T1/T2 (`manage_object.resource`/`common.resource`) edits needed - Bank's grid-filter
  helper already existed generically in T2, so this was a pure T3/suite/testdata change.

### Done wrong / lessons
- None disclosed as a defect in PR #471's body - `py -m robocop check` on the changed files
  returned exit 1 with the same baseline 9 DOC02/VAR02 style warnings as the merged
  `berth_iud.robot` exemplar (missing `[Documentation]` on some test cases) - a known, accepted
  style gap shared across the Bank-pattern family, not a regression introduced by this PR.

### Blockers -> resolution
- None recorded in PR #471.

### Decisions
- Reused the shared engine's grid-filter keyword rather than writing a screen-specific filter
  mechanism - keeps Split Item Other consistent with Bank/Berth/Stream Item Category.
- Playwright driver (`py/split_item_other_iud.py`) left untouched - out of scope for this
  RF-pattern conversion.

### Evidence (2026-08-23)
- Live RF: `results/_live_split_item_other/output.xml` (5/5).
- Filter-fired grep: `grep -c "Find Object Row By Filter" output.xml` = 30.
- DB self-clean: fresh-connection `SELECT CODE, NAME FROM ov_split_item_other WHERE CODE LIKE
  'AUTOTEST%'` = 0 rows.

## 2026-08-28 - documentation/evidence backfill (this task, Batch 10 of the backfill work order)

_Owner decision 2026-08-27 retired the 2026-08-23/26 lean waiver (`docs/IUD-DELIVERABLE-CHECKLIST.md`
Section H) - SOW/README/JOURNAL/evidence/CHECKLIST/KB map must be backfilled for every screen
converted under the old lean rule. This entry documents that backfill, not a new build._

### Built
- Refreshed `split_item_other_sow.md`, `README.md`, this `JOURNAL.md`, `CHECKLIST.md`, and
  `ec-ui-knowledge/screens/split_item_other.md` to reflect the 2026-08-23 Bank-pattern rebuild
  (the prior versions of these files still described the superseded 2026-07-26 label-driven
  4/4 build).
- Added fresh evidence to `evidence/`: `2026-08-28_live_output.xml` + `2026-08-28_live_log.html`
  from a real re-run of the existing suite (see below). Original 2026-07-26 screenshots and
  `rf_report.html` kept as historical evidence, not deleted.

### Done well
- Did NOT touch the RF automation (page object, suite, testdata) or the Playwright driver -
  re-ran the existing, already-proven suite exactly as-is.
- Re-verified independently rather than trusting the 2026-08-23 PR body alone:
  - `robot --dryrun` on `split_item_other_iud.robot`: 5/5 pass.
  - `EC_HEADLESS=true robot` live run: 5/5 pass (TC01-TC05).
  - `py -m robocop check` on the T3 + suite: exit 1, 9 issues - all DOC02 (missing
    `[Documentation]` on TC03/TC04/TC05 and similar) - matches the baseline PR #471 already
    disclosed, no new regression.
  - `py scripts/check_bundle_hygiene.py`: PASS (no hardcoded creds in this screen's files, pure
    ASCII, no CHECKLIST/VERIFY-REPORT contradiction for this bundle). One unrelated WARN was
    reported for a different screen's (Contract Area) `investigation/` script - not this one.
  - Fresh `oracledb` connection: `SELECT CODE, NAME FROM OV_SPLIT_ITEM_OTHER WHERE CODE LIKE
    'AUTOTEST%'` = 0 rows, confirming self-clean after the fresh live run.

### Done wrong / lessons
- None - this was a documentation-only pass; no automation code was written or changed.

### Blockers -> resolution
- None. Live run succeeded on the first attempt (no retry needed).

### Decisions
- Kept the pre-existing `VERIFY-REPORT.md` (2026-07-26, pre-Batch-10) as a historical artifact
  rather than deleting it, since it documents real evidence from a real run; the bundle's
  README/CHECKLIST now point to the newer 2026-08-23/2026-08-28 evidence as the current state
  of truth.

### Evidence (2026-08-28)
- `evidence/2026-08-28_live_output.xml`, `evidence/2026-08-28_live_log.html` (5/5 live pass).
- Fresh-connection self-clean query result: 0 rows.
