# JOURNAL - Canal (CO.2069) OV IUD

## 2026-07-26 (original build)
- **Branch:** `feature/canal-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Transport_Objects > Canal. Mandatory Code/Name/Start Date; optional
  dropdowns skipped. Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4
  (argument-driven keyword shape: `Insert Canal Record`/`Update Canal Name`/`Delete Canal`).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 7/7.

## 2026-08-23 (PR #458 — Batch 7, full Bank-pattern conversion)
- **Built:** Rebuilt `canal_page.resource` and `canal_iud.robot` from the argument-driven shape
  above to the full Bank pattern — properties-file-driven insert/update/verify (T2
  `Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/Removed/
  Does Not Exist`) plus explicit grid-filter wiring (`Find/Clear Canal Row By Filter`, wired into
  Update/Find/Verify-Found/Delete). Suite grew from 4 TCs to the standard 5-TC Bank shape (added
  TC01 clean-state check). 4 new properties files added:
  `testdata/canal_{insert,update,form_verify,grid_verify}.properties`. `resources/credentials.py`
  gained `CANAL_EC_USER`/`CANAL_EC_PASS` (additive-only). Fixed test code changed to `CANAL_KIEL`.
- **Done well:** No shared T1/T2 keyword changes needed (`manage_object.resource`/
  `common.resource` untouched) — every keyword the conversion needed already existed from earlier
  Bank-pattern batches. Recon-first via the existing driver/registry/DB before writing config
  (`docs/ec_screen_registry.md`, this bundle's own `canal_sow.md`, the already-proven
  `py/canal_iud.py`) rather than re-discovering mandatory fields from scratch. Fill-only-needed-
  fields discipline kept: Canal Code/Canal Name/Start Date only, Time Zone dropdown left out — no
  scope expansion beyond the already-proven driver.
- **Done wrong / lessons:** none disclosed in PR #458's body — the conversion applied a proven
  pattern (Bank/Port/State precedent) with no reported flake, wrong classification, or shared-file
  regression. The one real gotcha (Canal's on-screen labels are screen-prefixed — "Canal Code"/
  "Canal Name", not the generic Bank "Code"/"Name") had already been identified during the
  2026-07-26 original build, not newly discovered here — threaded through via `code_label=Canal
  Code` on every T2 call, same shape as State's own precedent.
- **Blockers -> resolution:** none reported.
- **Decisions:** keep the fixed test code `CANAL_KIEL` (not a generated unique code) —
  pre-confirmed absent from `OV_CANAL` (only real rows `SUEZ`/`PANAMA`); every run must complete
  TC05 so the code stays free for the next run.
- **Evidence (PR #458):** live 5/5 (`EC_HEADLESS=true robot tests/.../canal_iud.robot`); fresh
  `oracledb` connection confirmed 0 residual `CANAL_KIEL` rows post-run; grid-filter keywords fired
  15x `Find Canal Row By Filter` / 15x `Clear Canal Row Filter` (per `output.xml` grep); robocop 9
  baseline style warnings (same categories/count as Bank's own accepted baseline); dryrun 753/753
  pass on the full `tests/` tree at the time.

## 2026-08-28 (this backfill — Batch 9 of `docs/lean-deliverable-backfill-workorder.md`)
- **Built:** Refreshed this bundle's SOW/README/JOURNAL/evidence/CHECKLIST + added a KB selector
  map (`ec-ui-knowledge/screens/canal.md`, did not previously exist) — restoring the deliverables
  PR #458's then-current lean waiver (Section G, `docs/IUD-DELIVERABLE-CHECKLIST.md`) was allowed
  to skip, per Section H's 2026-08-27 retirement of that waiver. **No RF file
  (`canal_page.resource`/`canal_iud.robot`/`testdata/canal_*.properties`) was touched.**
- **Done well:** confirmed the screen's existing automation via grep + registry before touching
  anything (`docs/ec_screen_registry.md` row, `gh pr view 458`'s real body) rather than inventing
  a narrative; re-ran the suite live once for fresh evidence rather than trusting PR #458's cited
  numbers alone — got 5/5 pass on the first attempt, no retry needed.
- **Done wrong / lessons:** this screen already HAD a partial bundle (from the 2026-07-26 original
  build, predating the Bank-pattern conversion) that a first grep for "existing bundle" almost
  missed — the docs describe the OLD 4-TC argument-driven shape, not PR #458's 5-TC Bank-pattern
  shape. Refreshed in place rather than creating a duplicate/parallel bundle (same lesson as
  Batch 1's "several screens had pre-existing bundles predating the lean rule that needed
  refreshing, not fresh creation").
- **Blockers -> resolution:** none — dryrun, live run, robocop, and hygiene all passed on the
  first attempt.
- **Decisions:** kept the pre-existing evidence (`canal_0[1-5]_*.png`, `rf_report.html`) in place
  for history rather than deleting it, added the fresh 2026-08-28 run's artifacts alongside under
  `evidence/rf_batch9_2026-08-28/` rather than overwriting.
- **Evidence (this backfill, 2026-08-28):**
  - dryrun: 5/5 pass — `evidence/rf_batch9_2026-08-28/dryrun_output.xml`.
  - live: 5/5 pass, first attempt — `evidence/rf_batch9_2026-08-28/{output.xml,log.html,report.html}`.
  - DB self-clean: fresh `oracledb` connection, `SELECT CODE FROM OV_CANAL` -> `[SUEZ, PANAMA]`
    only, 0 `CANAL_KIEL` residual.
  - robocop: 9 issues (DOC02/style baseline, same category/count as PR #458 cited).
  - hygiene: `py scripts/check_bundle_hygiene.py` -> exit 0, PASS.
