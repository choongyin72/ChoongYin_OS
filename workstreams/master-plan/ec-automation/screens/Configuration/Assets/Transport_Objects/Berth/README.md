# Berth (CO.2012) — OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Transport Objects > Berth**. Full Insert / Update /
Delete (End Date = Start Date), DB-verified against `OV_BERTH`, self-cleaning. Built **label-driven, zero
hardcoded field ids**, properties-file-driven, T2-consolidated on the shared engine + T2. Folder-sibling of
Port (CO.2003) but **single-page** grid. **One of the two original exemplar screens (with Bank) the whole
Bank-pattern initiative is modeled on** — rebuilt to that full shape in PR #454 (merged 2026-08-23).

_Backfilled 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 8) — README refreshed to the
current PR #454 shape; the RF automation itself was NOT touched by this backfill._

## Artifacts
- **SOW:** `berth_sow.md`
- **Playwright driver:** `../../../../py/berth_iud.py` (thin; shared engine `py/ec_object_iud.py` + `libraries/DbVerify.py`) — unchanged since 2026-07-26
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Transport_Objects/berth_page.resource` — rebuilt PR #454 (properties-file-driven, grid-filter wired)
- **RF suite:** `../../../../tests/Configuration/Assets/Transport_Objects/berth_iud.robot` — rebuilt PR #454 (5 TCs, per-TC Login/Logout, fixed test code `AUTOTEST_BERTH`)
- **Testdata:** `../../../../testdata/berth_{insert,update,form_verify,grid_verify}.properties`
- **investigation/** recon.py (2026-07-26/08-02, pre-PR#454; not re-run — Playwright driver unaffected) ·
  **evidence/** berth_0[1-5]_*.png + rf_report.html (2026-07-26, pre-PR#454) + this backfill's
  `backfill_2026-08-28/` (dryrun + live output.xml/log.html/report.html/screenshots)
- **VERIFY-REPORT.md** — historical, auto-generated 2026-07-26 by `scripts/verify_screen.py` (OVERALL PASS,
  4-TC numbers now superseded by CHECKLIST.md's current 5-TC evidence — kept, not deleted)

## Run
- Playwright: `EC_HEADED=0 py -X utf8 workstreams/master-plan/ec-automation/py/berth_iud.py` → 7/7 ALL PASS
- RF dryrun: `robot --dryrun --outputdir results workstreams/master-plan/ec-automation/tests/Configuration/Assets/Transport_Objects/berth_iud.robot`
- RF live (headless): `EC_HEADLESS=true robot --outputdir results workstreams/master-plan/ec-automation/tests/Configuration/Assets/Transport_Objects/berth_iud.robot`
- DB self-clean check (fresh connection, after a live run):
  ```sql
  SELECT code, name, object_end_date FROM OV_BERTH WHERE code = 'AUTOTEST_BERTH';
  -- expect 0 rows after TC05 Delete runs
  SELECT COUNT(*) FROM OV_BERTH;
  -- expect 11 (real production berths, never touched)
  ```

## Verified (real runs, not hand-ticked)
- **2026-07-26 (original build):** robocop 0 · hygiene 0 · dryrun 4/4 · LIVE RF 4/4 · Playwright 7/7 · self-clean 0 residual.
- **2026-08-23 (PR #454 conversion, per its PR body):** live RF 5/5 · full-tree dryrun 753/753 · DB self-clean
  0 residual (fresh connection) · grid-filter fired (15 `Find Berth Row By Filter` hits in output.xml).
- **2026-08-28 (this backfill, re-run for evidence only):** dryrun **5/5 PASS** · live headless **5/5 PASS**
  (`evidence/backfill_2026-08-28/live_output.xml`) · DB self-clean **0 residual** `AUTOTEST_BERTH` rows,
  11 real production rows confirmed untouched · robocop **9 issues** (DOC02/COM04/DOC03/MISC06 baseline
  class, same category as Bank's own 13 — not a new class) · hygiene `check_bundle_hygiene.py` → **PASS**.
