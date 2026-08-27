# RF live run - Well Hookup - 2026-08-27 (backfill evidence capture)

Backfill task per `docs/lean-deliverable-backfill-workorder.md` - this is a re-run of the
ALREADY-PROVEN Area-pattern suite (PR #539, merged 2026-08-26) to capture evidence, not a
fresh verification cycle and not a rebuild.

## Commands run (from `workstreams/master-plan/ec-automation/`, isolated worktree)

```
robot --dryrun --test "*Well Hookup*" tests/
EC_HEADLESS=true robot -d Workplaces/well-hookup-backfill/results tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot
```

## Results

- **Dryrun:** 5/5 PASS, 0 failed (TC01-TC05, full parse + keyword resolution clean).
- **Live headless run:** 5/5 PASS, 0 failed.
  - TC01 Verify Clean State - PASS
  - TC02 Insert Well Hookup Data - PASS
  - TC03 Update Well Hookup Data - PASS
  - TC04 Find Well Hookup Data - PASS
  - TC05 Delete Well Hookup Data - PASS
- **Grid-filter wiring fired:** `grep -c "Find Object Row By Filter" output.xml` -> **15** (consistent
  with the 15 cited in PR #539's own body).
- **DB self-clean (fresh connection):** `SELECT COUNT(*) FROM OV_WELL_HOOKUP WHERE CODE LIKE 'AUTOTEST%'`
  -> **0** residual rows, confirmed via a fresh `oracledb` connection
  (`localhost:1521/ORCL`, `ECKERNEL_EC`) opened only for this check.
- **robocop** (`py -m robocop check` on the T3 + suite): **7 issues** (2 VAR02 + 5 DOC02) - same
  kind/count as PR #539's own accepted baseline (matches Facility Class 1/Area's accepted shape;
  no regression).
- **Hygiene** (`py scripts/check_bundle_hygiene.py`, run repo-wide from `C:/tmp/wt-wellhookup-backfill`):
  `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
  contradictions, doc rows match declared families`. (The single WARN printed by this run is for an
  unrelated screen, Contract_Area's `investigation/live_recon_contract_area.py` - not Well Hookup.)

Artifacts in this folder: `output.xml`, `log.html`, `report.html` from the live headless run above.
No RF screenshot-per-step flag exists for this T3 (screen verification is grid/form-value based, not
screenshot-based) - `log.html`/`output.xml` are the run's real evidence record.
