# JOURNAL — Orifice Plate (CO.0089) OV IUD

_Screen: Configuration > Assets > Stream_Objects > Orifice Plate. View `OV_ORIFICE_PLATE`._
_This JOURNAL is refreshed 2026-08-28 (lean-deliverable-backfill, Batch 10 —
`docs/lean-deliverable-backfill-workorder.md`). The original 2026-07-26 entry below is kept for
history; a new entry below it covers PR #463's real Bank-pattern conversion and this backfill
session. Modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`._

## 2026-07-26 (original build — superseded by PR #463)
- **Branch:** `feature/orifice_plate-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Stream_Objects > Orifice Plate. Mandatory Code/Name/Start Date; optional
  dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, mandatory extras beyond
  Code/Name/Start Date: Material (dropdown), Diameter [mm], Measurement Temp [deg R]).
- Label-driven T3 (no hardcoded ids). Playwright driver → 7/7; RF T3+suite → live 4/4.
- `verify_screen.py` → OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.
- **Lesson:** plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.

## 2026-08-23 — PR #463, Batch 8 of the Bank-pattern conversion project

### Built
Rebuilt `orifice_plate_page.resource` and `orifice_plate_iud.robot` to mirror Bank/Berth exactly,
replacing the 2026-07-26 generator-scaffolded/label-driven-only pattern:
- Properties-file-driven insert/update/verify: `Insert Object From Properties And Verify Code` /
  `Update Object From Properties`, backed by new `testdata/orifice_plate_{insert,update,
  form_verify,grid_verify}.properties`.
- Explicit `Find Orifice Plate Row By Filter` / `Clear Orifice Plate Row Filter`, wired into
  Update/Find/Verify-Found/Delete (not Verify-Removed/Does-Not-Exist — matching the Bank/Berth
  convention).
- Dedicated credential pair `ORIFICE_PLATE_EC_USER`/`ORIFICE_PLATE_EC_PASS` added (additive) to
  `resources/credentials.py`.
- Fixed test code `AUTOTEST_ORIFICE_PLATE` (confirmed free in `OV_ORIFICE_PLATE` before wiring in),
  replacing the earlier timestamp-suffixed unique code.
- Added **TC04 Find** — the prior suite only had TC01 Verify-Clean-State / TC02 Insert / TC03
  Update / TC04 Delete, with no Find test case at all; Delete was renumbered to TC05.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  **MODIFIED, not added** — this replaced the 2026-07-26 build's rows in place.

### Done well
- Full I-U-D + Find, DB-verified against `OV_ORIFICE_PLATE`; live RF **5/5 PASS**.
- `robot --dryrun` on the full `tests/` tree: 758/758 PASS (no regression to sibling suites).
- Filter keyword fired 13x in the live run's `output.xml`.
- DB self-clean confirmed via a fresh `oracledb` connection (not reusing the test run's own
  connection) — 0 residual `AUTOTEST%` rows before and after.
- No shared T1/T2 keyword changes needed for this screen — zero risk to sibling suites.

### Done wrong / lessons
- None disclosed as a defect in PR #463's own body — this was a clean upgrade of an already-working
  suite, not a bug fix. The one real risk called out by the PR itself was procedural, not a code
  bug: the shared-doc-file collision risk (registry/scorecard rows modified, not added) when
  several sibling Batch 8 PRs touch the same files — flagged explicitly so the merge step would
  watch for stale duplicate rows (a lesson carried over from the Batch 7 PR #458/#459 merge-conflict
  incident).

### Blockers → resolution
- None. `py -m robocop check` on the test suite reports 9 issues (1x VAR02 + 5x DOC02) — this is an
  accepted pattern, not a blocker (identical count/shape to the Batch 7 exemplar `berth_iud.robot`).

### Decisions
- Grid-filter wired only into Update/Find/Verify-Found/Delete, not Verify-Removed/Does-Not-Exist —
  consistent with Account/Bank/Berth/State's convention (owner, 2026-08-22).
- Every EC screen gets its own dedicated credential pair (owner standing decision, 2026-08-22).
- Playwright driver (`py/orifice_plate_iud.py`) left untouched — out of scope for the RF-pattern
  conversion, and now permanently superseded by the Universal Screen Engine per Section H.

### Evidence
- PR #463 citations: live 5/5, dryrun 758/758 (full tree), robocop 0 (page object) / 9 (suite,
  accepted pattern), hygiene PASS, filter fired 13x, DB self-clean 0 residual (fresh connection).

## 2026-08-28 — this backfill session (lean-waiver retirement, Batch 10)

### Built
Refreshed `orifice_plate_sow.md`, `README.md`, this `JOURNAL.md`, `CHECKLIST.md`, `evidence/`, and
`ec-ui-knowledge/screens/orifice_plate.md` — all of which still described the 2026-07-26 build (4
TCs, no grid filter, generic engine narrative) despite PR #463 having replaced the underlying
automation on 2026-08-23. **No RF/py automation files were touched.**

### Done well
- Re-ran the existing suite (unmodified) to capture fresh evidence: `robot --dryrun` 5/5 PASS,
  `EC_HEADLESS=true robot` (live) 5/5 PASS, filter fired 13x (matches PR #463's own citation),
  robocop 9 issues (matches PR #463's own citation), hygiene PASS, DB self-clean 0 residual via a
  fresh connection — every number in this refresh was independently reproduced this session, not
  copied blind from the PR body.

### Done wrong / lessons
- The pre-existing bundle under `screens/.../Orifice_Plate/` was stale relative to the merged
  automation for over 5 days (PR #463 merged 2026-08-23, this refresh 2026-08-28) — PR #463 itself
  never touched the `screens/` bundle, only the RF/testdata/credentials/registry/scorecard files.
  This is the exact gap the lean-deliverable-backfill project exists to close.

### Blockers → resolution
- None.

### Decisions
- Kept the original 2026-07-26 JOURNAL entry (above) rather than deleting it — the backfill work
  order asks for real history, not a smoothed-over single narrative.

### Evidence
- `evidence/rf_log_2026-08-28.html`, `evidence/rf_report_2026-08-28.html`,
  `evidence/rf_output_2026-08-28.xml`, per-TC screenshots (`TC0[1-5] *_*.png`) — all from the
  2026-08-28 live re-run in this session.
