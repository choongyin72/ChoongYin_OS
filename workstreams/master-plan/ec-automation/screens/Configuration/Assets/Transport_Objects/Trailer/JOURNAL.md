# JOURNAL - Trailer (CO.0265) plain-OV IUD

## 2026-07-31
- **Branch:** `feature/trailer-iud`. Group A #6, sibling of Truck (CO.0264).
- **Recon (executed):** empty navigator (zero nav fields, GO only), custom grid id
  `trailer_object:form:T_data`, mandatory = Code/Name/Start Date + Licence Plate No +
  Trailer Type/UOM/Transport Company dds. DB: OV_TRAILER = 0 rows (our row is the first).
- **First screen through the AUDITED plain-OV generator with zero debugging:** driver 8/8 and all 5
  verify gates PASS on the FIRST run. The 6 defects fixed during the Truck audit (GO re-query,
  UNSAVED CHANGES dialog, grid-id key, extra_texts, LEN03 split, leftover `assert pu`) all held here.
- **The new #278 vocabulary validator immediately proved its worth:** the registry row came out
  correct (the family-aware fix from PR #279 worked), but `check_row_vocab.py` FLAGGED the scorecard
  row - I had only made the REGISTRY template family-aware, not the SCORECARD one, so the scorecard
  still said "(OV-GM, CO.0265) ... OV-GM gated-navigator ... Op PU first-available" on a plain-OV
  screen. Fixed the second template too (family-aware tag + descriptor), removed the bad row,
  regenerated, re-validated: clean. Regression-checked all 5 families (ovgm/plain/custom/tv) - no
  breakage.

## Lessons
- The validator caught a defect the same class of check was created for, on its FIRST real use, in a
  place I had not thought to fix - evidence that type-correctness checks beat edit-landed checks.
- When fixing a templating defect, enumerate EVERY template that emits the same vocabulary (registry
  AND scorecard AND KB), not just the one the last bug surfaced in.

## 2026-08-23 — PR #475, Batch 10 Bank-pattern conversion

_This section backfilled 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (owner
decision retiring the 2026-08-23/26 lean waiver — Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).
The RF automation described below was already built and merged in PR #475 on 2026-08-23; this entry
narrates what that PR's body actually recorded — it is not a new build and no automation file was
touched to produce it._

### Built
Rebuilt Trailer's RF page object/suite (`trailer_page.resource`/`trailer_iud.robot`) to the full
Bank-pattern shape (properties-file-driven insert/update/verify + explicit grid-filter wiring),
matching `bank_page.resource`/`berth_page.resource` exactly — part of Batch 10's 5-screen
expanded-scope conversion round.
- `pageobjects/Configuration/Assets/Transport_Objects/trailer_page.resource` (rebuilt)
- `tests/Configuration/Assets/Transport_Objects/trailer_iud.robot` (rebuilt, per-TC Login/Logout)
- `testdata/trailer_{insert,update,form_verify,grid_verify}.properties` (new)
- `resources/credentials.py` (additive: `TRAILER_EC_USER`/`TRAILER_EC_PASS`)
- `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` — modified existing rows (from the
  2026-07-31 generator-scaffolded build), not added new rows
- `docs/bank-pattern-conversion-checklist.md`, `docs/grid-filter-standardization-checklist.md` —
  appended own row under the pre-merged Batch 10 header (no new section header)

### Done well
- Live run (`EC_HEADLESS=true`) of `trailer_iud.robot`: **5/5 pass**. Fresh `oracledb` connection
  (`SELECT CODE FROM OV_TRAILER WHERE CODE LIKE 'AUTOTEST%'`) returned 0 rows both before and after
  the run.
- `robot --dryrun` on the full `tests/` tree: 767/767 pass.
- `py -m robocop check` on both changed files: 9 issues (4 VAR02 + 5 DOC02) — same count/type as
  the already-merged `berth_iud.robot` baseline (verified side-by-side), advisory only, exit=0.
- Filter keyword confirmed fired 23x via `output.xml` grep.
- Self-clean confirmed: 0 residual `AUTOTEST_TRAILER`/`AUTOTEST%` rows in `OV_TRAILER`, verified via
  a fresh oracledb connection after the live run.

### Done wrong / lessons
- No regression or defect disclosed in PR #475's own body — the conversion trusted the pre-existing
  proven Playwright driver's field set and grid-id constant instead of re-deriving from a static
  scan (see Decisions below), carrying forward a lesson from the Process Train Batch-9 audit rather
  than surfacing a new mistake here.

### Blockers -> resolution
- None disclosed. Clean same-day merge.

### Decisions
- **Grid id kept as Trailer's own** `trailer_object:form:T_data`, NOT switched to the shared
  `manage_object_nav_nav:form:T_data` constant other Bank-family screens use — confirmed via the
  proven driver, a real documented quirk of this screen, not an oversight.
- **Mandatory field set trusted from the proven driver** (Licence Plate No + 3 first-available
  dropdowns) over a static label/CSS scan (Process Train Batch-9 lesson) — Licence Plate No kept
  rather than dropped.
- **Batch 10 ground rule followed:** no shared `manage_object.resource`/`common.resource` changes.
- **Registry/scorecard rows updated as a clean full replacement**, not left stale alongside new text
  (Merge-conflict lesson carried forward from Batch 7/8/9).

### Evidence
- PR #475 (`gh pr view 475`): live 5/5, full-tree dryrun 767/767, robocop 9 issues (parity with
  Berth baseline), DB self-clean 0/0 (fresh connection), filter keyword fired 23x.

## 2026-08-28 — Documentation/evidence backfill (this session)

_Per `docs/lean-deliverable-backfill-workorder.md` Batch 11. No RF file (`trailer_page.resource`,
`trailer_iud.robot`, `testdata/trailer_*.properties`) was modified to produce this backfill — this
session only added/refreshed SOW/README/JOURNAL/evidence/CHECKLIST/KB-map documentation._

### Evidence captured this session
- `robot --dryrun tests/Configuration/Assets/Transport_Objects/trailer_iud.robot` → **5/5 PASS**.
- `py -m robocop check pageobjects/.../trailer_page.resource tests/.../trailer_iud.robot` →
  **9 issues** (4 VAR02 + 5 DOC02) — matches PR #475's own cited 9-issue baseline exactly. No drift.
- `EC_HEADLESS=true robot tests/Configuration/Assets/Transport_Objects/trailer_iud.robot` →
  **5/5 PASS** (single run, no retry needed).
- DB self-clean: fresh `oracledb` connection to the local sandbox,
  `SELECT COUNT(*) FROM OV_TRAILER WHERE CODE LIKE 'AUTOTEST%'` → **0** residual rows.
- `py scripts/check_bundle_hygiene.py` (repo root) → PASS (167 bundles + 272 recon scripts scanned;
  the one WARN reported is in an unrelated Contract_Area recon script, not Trailer).
- Evidence artifacts added to `evidence/`: `log.html`, `output.xml`, `report.html`,
  `playwright-log.txt`, per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,logout}.png`)
  from this session's clean 5/5 run, alongside the pre-existing 2026-07-31 Playwright evidence
  (`tr_01_loaded.png` ... `tr_05_final.png`, `results.json`).

### Decisions
- Playwright driver (`py/trailer_iud.py`) left untouched — permanently waived for Bank-/Area-pattern
  work per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`; kept as historical reference only.
