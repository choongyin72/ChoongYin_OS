# JOURNAL — Berth (CO.2012) OV IUD

## 2026-07-26
- **Branch:** `feature/berth-iud` **stacked on `feature/port-iud`** (depends on PR #203 — needs the shared-engine
  pagination + wait helpers). Check-existing gate: only `py/berth_iud.py` (this build); reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Transport Objects > Berth (same folder as Port). **Two Port-sibling predictions
  proven WRONG by recon:** (1) grid is **single page** (11 rows, `paginator pages: 0`) — not paginated like Port;
  (2) **Port Name dropdown is OPTIONAL**, not a mandatory reference. ⇒ plain OV, mandatory Code/Name/Start Date only.
- **Label-driven from the start** — no hardcoded `R:n:C:n` ids.
- **Bug found (delete):** Playwright INSERT/UPDATE passed; DELETE first FAILED the grid-absence check while DB
  confirmed the row was gone from `OV_BERTH` (count 0). Root cause = **async grid redraw after delete+GO** (mirror
  of the Port insert-appear timing). **Generic fix:** added engine `wait_for_row_absent` (polls until the row is
  gone from every page). Additive (new symbol; the pagination changes it sits beside were Bank-canary-validated on
  #203). Re-run → **7/7 ALL PASS + self-clean**.
- **RF** T3 + suite (label-driven). `verify_screen.py` → **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4,
  **LIVE RF 4/4**, **Playwright 7/7**. (RF's Browser auto-wait already tolerated the delete redraw; only the
  Playwright driver needed the new helper.)

## Lessons
- Folder-siblings are NOT the same screen — recon each (both Port-based predictions were wrong here).
- Delete assertions need absence-polling (`wait_for_row_absent`), not an immediate `not row_exists` — the grid
  redraws async after delete+GO. Now generic for every OV screen.

## 2026-08-23 — PR #454 "Berth Bank-pattern completion" (Batch 7 of the Bank-pattern conversion project)

### Built
Rebuilt Berth's RF page object/suite (`berth_page.resource`/`berth_iud.robot`) from partially label-driven
to the full properties-file-driven, T2-consolidated Bank/State pattern: added `Insert Object From Properties
And Verify Code`/`Update Object From Properties`/`Verify Object Insert Exists`/`Verify Object Form Record`/
`Verify Object Found`/`Verify Object Does Not Exist` consolidated keywords and explicit `Find/Clear Berth
Row By Filter` grid-filter wiring (wired into Update/Find/Verify-Found/Delete), matching
`bank_page.resource`/`state_page.resource` exactly. Files touched: `berth_page.resource` (rebuilt),
`berth_iud.robot` (rebuilt: per-TC Login/Logout, 5-TC narrative, fixed test code `AUTOTEST_BERTH`),
`resources/credentials.py` (additive `BERTH_EC_USER`/`BERTH_EC_PASS`), 4 new `testdata/berth_*.properties`
files, plus registry/scorecard/checklist doc rows. No changes to `resources/manage_object.resource` or
`resources/common.resource` (shared T1/T2 untouched, per that round's rule).

### Done well
- Live run (`EC_HEADLESS=true`) of `berth_iud.robot`: **5 tests, 5 passed, 0 failed**. Filter keyword fired:
  output.xml grep showed 15 hits for `Find Berth Row By Filter` / 15 for `Clear Berth Row Filter`.
- DB self-clean: a separate, fresh `oracledb` connection queried `OV_BERTH` for `AUTOTEST_BERTH` after the
  live run — 0 rows returned.
- `robot --dryrun` on the full `tests/` tree: **753 tests, 753 passed, 0 failed**.
- `py -m robocop check` on `berth_page.resource`: the pre-existing DOC02/COM04/DOC03/MISC06 warnings on
  `berth_iud.robot`/`credentials.py` were confirmed to match the exact same baseline already present on
  `bank_iud.robot`, not a new issue introduced by this change.
- Recon-first via the existing KB map `ec-ui-knowledge/screens/berth.md` + the already-proven Playwright
  driver `py/berth_iud.py` (no live-DOM re-scan needed, both mutually consistent on mandatory fields Berth
  Code/Berth Name/Start Date and screen-prefixed labels). IUD-fills-only-needed-fields honored (Insert =
  Code/Name/Start Date, Update = Name only, matching the proven driver's exact field scope).

### Done wrong / lessons
- None disclosed as new in this PR's body — this was a lean/mechanical pattern-conversion of already-proven
  selectors, not a fresh recon; the only "gotchas" carried forward were the ones already logged in the
  2026-07-26 entry above (folder-sibling mismatch, delete-redraw timing).

### Decisions
- Test code changed from a `<timestamp>`-suffixed unique code to the fixed `AUTOTEST_BERTH` (Bank/State
  convention) — confirmed free via a fresh oracledb query on `OV_BERTH.CODE` before and after the live run.
- Isolated sparse-checkout clone under `Workplaces/berth/`; explicit-path staging (no `git add -A`).
- This PR itself was NOT stacked (unlike the original 2026-07-26 build, which was stacked on the Port
  pagination PR #203) — the Bank-pattern conversion round reused the shared engine as-is.

### Evidence (per PR #454's own body)
- Live run: 5/5 pass, self-clean confirmed (fresh-connection DB re-read, 0 residual `AUTOTEST_BERTH` rows).
- Full-tree dryrun: 753/753 pass.
- Registry/scorecard/checklist doc rows updated: `docs/ec_screen_registry.md`, `docs/automation-scorecard.md`,
  `docs/grid-filter-standardization-checklist.md` (Batch 7 section, 37/37 pool), `docs/bank-pattern-conversion-checklist.md`
  (Batch 7 section, original 23-screen table not reopened).

## 2026-08-28 — Lean-deliverable backfill (Batch 8 of `docs/lean-deliverable-backfill-workorder.md`)

### Built
No automation changed. Refreshed `berth_sow.md`/`README.md`/`CHECKLIST.md`/`ec-ui-knowledge/screens/berth.md`
to describe the current (post-#454) shape, appended this JOURNAL entry from PR #454's real body, and captured
a fresh evidence run into `evidence/backfill_2026-08-28/`.

### Done well
- Dryrun re-run: **5/5 PASS** (`evidence/backfill_2026-08-28/dryrun_output.xml`).
- Live headless re-run (`EC_HEADLESS=true`): **5/5 PASS** on first attempt, no retry needed
  (`evidence/backfill_2026-08-28/live_output.xml`/`live_report.html`/`live_log.html` + per-TC screenshots).
- DB self-clean re-verified via a fresh `oracledb` connection (routed through the local DSN alias
  `localhost:1521/ORCL` that `libraries/DbVerify.py`/`resources/environment.py` already default to — the
  direct `db.plutodev...` hostname timed out from this box; the local alias is the one actually reachable
  and is what the RF suite itself used during its own in-suite DB checks): `OV_BERTH` has 0 residual
  `AUTOTEST_BERTH` rows and exactly 11 real production rows (matching the SOW's long-standing count).
- robocop re-run on `berth_page.resource`/`berth_iud.robot`: **9 issues**, all in the DOC02/COM04/DOC03/MISC06
  class already disclosed in PR #454's body; cross-checked against Bank's own robocop output (13 issues,
  same category) to confirm this is the same baseline noise, not a new defect.
- hygiene: `py scripts/check_bundle_hygiene.py` → **RESULT: PASS** (no hardcoded creds, pure ASCII, no
  CHECKLIST/VERIFY-REPORT contradiction).

### Done wrong / lessons
- A direct `oracledb.connect(..., dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")` from this
  worktree/session timed out (`DPY-6005`) on the first AND retry attempt — this box reaches the DB only via
  the `localhost:1521/ORCL` alias that the repo's own `resources/environment.py`/`libraries/DbVerify.py`
  already default to. Disclosing plainly rather than smoothing over: my first two connection attempts used
  the wrong DSN, not a real DB outage — the RF suite's own in-suite DB checks (which use the correct default)
  passed throughout with 0 real failures.

### Evidence
- `evidence/backfill_2026-08-28/dryrun_output.xml` (5/5), `live_output.xml`/`live_log.html`/`live_report.html`
  (5/5) + per-TC login/action/logout/verify screenshots, `hygiene_output.txt`, `robocop_output.txt`.
