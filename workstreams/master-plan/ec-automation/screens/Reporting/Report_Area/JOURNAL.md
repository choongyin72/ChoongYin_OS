# JOURNAL — Report Area IUD

_Screen: Reporting > Report Area (RP.0017, OV, date-effective). View `OV_REPORT_AREA`._
_Branch: feature/report-area-iud (off master; #194 foundation already merged). 2026-07-25._

## Built
- Playwright: thin driver `py/report_area_iud.py` on the shared engine `py/ec_object_iud.py` + `DbVerify.py` — zero engine changes.
- RF: T3 `pageobjects/Reporting/report_area_page.resource` + suite `tests/Reporting/report_area_iud.robot` (reuse T2 `manage_object` + `DbVerify.py`).
- KB map `ec-ui-knowledge/screens/report_area.md`.

## Done well
- 2nd OV-reuse-target after Disposition Type; branched cleanly off master (foundation merged, no stacking).
- Full I-U-D DB-verified vs `OV_REPORT_AREA`: Playwright **7/7**, RF **4/4** (update DB-verified via `Field Should Equal In View`). Self-clean 0 residual.
- Simplest OV so far (Code/Name/Start Date only; no Description, no dropdowns) — clean recon-first build.

## Problems / blockers
- **No hard blockers** — both tools passed first try (payoff of the merged foundation; selector/hook/path issues from earlier screens were already solved + captured).
- Grid empty on open (needs GO) — expected for this screen (not a defect); handled by GO after open in driver + T3 `Apply Navigator`.
- Treeview path resolved authoritatively from DB treeview JSON (Reporting > Report Area) — note it sits under top-level **Reporting**, not Configuration/Assets.

## Done wrong (minor self-notes — logged for honesty)
- Used an **inline `py <<heredoc`** once to confirm CODE/NAME columns — a bend of the "no inline python, write a script file in tmp/" rule. Should have dropped it in `tmp/`. No impact; noting to not repeat.
- Left the OV tracker's sub-header reading **"Uncovered (35)"** while the two entries were ticked + totals said 33 — stale count. Fixed in the same commit as this note.

## Decisions
- Update covers Name only (no Description column exists). Plain OV → engine unchanged.
- Code in `py/`; bundle folder holds docs/investigation/evidence (per owner layout rule).

## Evidence
- Playwright: `evidence/rpta_0[1-5]_*.png` (7/7). RF: `evidence/rf_report.html` + `results/_rpta/report.html` (4/4). 2026-07-25.

---

## 2026-08-23 — Batch 9 Bank-pattern conversion (PR #468)

_From here on, the entry style matches Bank's JOURNAL (Built / Done well / Done wrong-or-lessons /
Blockers→resolution / Decisions / Evidence), per `docs/lean-deliverable-backfill-workorder.md`._

### Built
- Upgraded the RF suite from its partial label-driven build (`Fill OV Field By Label`, no
  properties-file-driven insert, no explicit grid-filter wiring) to the full Bank/Berth pattern:
  `Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/Removed/
  Does Not Exist`, and explicit `Find/Clear Report Area Row By Filter` wired into Update/Find/
  Verify-Found/Delete.
- `pageobjects/Reporting/report_area_page.resource` rebuilt: label-driven, properties-file-driven,
  T2-consolidated, mirroring `bank_page.resource`/`berth_page.resource` exactly.
- `tests/Reporting/report_area_iud.robot` rebuilt: fixed test code `AUTOTEST_RPTA` (confirmed free
  in `OV_REPORT_AREA` via a fresh oracledb connection before wiring it in), per-TC Login/Logout on
  one browser opened once in Suite Setup, added TC04 Find (suite grew from 4 TCs to 5).
- New properties files: `testdata/report_area_{insert,update,form_verify,grid_verify}.properties`.
- `resources/credentials.py`: additive-only `REPORT_AREA_EC_USER`/`REPORT_AREA_EC_PASS`.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  modified in place (not added — the rows already existed from the 2026-07-25 build).

### Done well
- Live RF 5/5 at PR #468 merge time. Full-tree `robot --dryrun tests/` 762/762 pass — no
  regressions to any other screen's suite.
- Filter-keyword wiring confirmed fired: `Find Object Row By Filter` → 28 hits in that PR's own
  live `output.xml`.
- robocop parity with `berth_page.resource`/`berth_iud.robot`'s own baseline (9 identical-category
  issues — VAR02 unused suite variables + DOC02 missing TC docs).
- No shared T1/T2 file changes needed — reused every consolidated T2 keyword as-is.

### Done wrong / lessons
- **Real gotcha (disclosed in PR #468, not smoothed over):** the date field's real label is
  **"Start date"** (lowercase "date"), not "Start Date" (capital D). This was found live via a
  reproducible 30s locator timeout when the capital-D form was tried first, then fixed by matching
  the pre-existing page object's own recon comment. Documented in the registry/scorecard rows and
  the properties file's own header comment for future re-use.
- The header-race note in PR #468's own body: `tmp/batch9_shared_findings.md` claimed master
  already had a pre-created "Batch 9 additions (pending)" header (from PR #464), but a fresh
  `git fetch origin master` at build time showed PR #464 had not actually landed. The worker added
  its own "## Batch 9 additions (2026-08-23)" header rather than blocking on one that didn't exist
  yet — flagged explicitly in the PR body as needing a possible post-merge consolidation pass,
  following the same precedent as Batch 7/8.
- This screen's bundle (SOW/README/JOURNAL/CHECKLIST/evidence/KB map) was **NOT** refreshed at
  PR #468 merge time — the 2026-08-23..26 lean waiver (later retired 2026-08-27, Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`) allowed the RF conversion to ship without the doc/evidence
  bundle around it. This 2026-08-28 backfill closes that gap; it is not a new build.

### Blockers → resolution
- No hard blockers in PR #468's own body. This backfill session hit none either (EC sandbox
  reachable, no stray chrome/node processes, live 5/5 first attempt, no retry needed).

### Decisions
- Playwright driver (`py/report_area_iud.py`) is out of scope for both PR #468 and this backfill —
  kept unchanged, permanently waived per Section H (Universal Screen Engine replaces that role
  going forward).
- Screen stays under top-level **Reporting** (not Configuration/Assets) — bundle path unchanged at
  `screens/Reporting/Report_Area/`.

### Evidence
- PR #468 (2026-08-23): live RF 5/5; DB self-clean via fresh oracledb connection, 0 residual
  `AUTOTEST%` rows in `OV_REPORT_AREA`; full-tree dryrun 762/762 pass; robocop 9 issues (parity with
  Berth's baseline).
- This backfill (2026-08-28, doc/evidence only, no RF file touched):
  - `robot --dryrun tests/Reporting/report_area_iud.robot` → 5/5 pass.
  - Full-tree `robot --dryrun tests/` → **883/883 pass**, no regressions.
  - `EC_HEADLESS=true robot` live re-run → **5/5 pass**, first attempt, no flake; artifacts kept in
    `evidence/2026-08-28_backfill/` (`log.html`, `output.xml`, `report.html`, `playwright-log.txt`,
    per-TC screenshots).
  - `py -m robocop check` on the changed files → **9 issues** (VAR02 x4 + DOC02 x5) — same shape as
    PR #468's own cited baseline; no new category, no regression.
  - `Find Object Row By Filter` → 15 hits confirmed in this session's own `output.xml` (a fresh
    5-TC run naturally fires the keyword fewer times than the specific run PR #468 cited 28 hits
    from — same keyword, same wiring, no functional gap).
  - `py scripts/check_bundle_hygiene.py` (repo root) → `PASS` (167 bundles + 273 recon scripts
    scanned; the one WARN in the output is a pre-existing, unrelated Contract Area recon script).
  - `investigation/check_autotest_residual.py` (new, this session, additive) →
    `AUTOTEST residual rows in OV_REPORT_AREA: []` after the live re-run.
