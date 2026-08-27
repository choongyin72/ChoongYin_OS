# Backfill evidence — Well Bore — 2026-08-28

Batch 5 (final Area-pattern wave), lean-deliverable-backfill-workorder. This capture is evidence
of the ALREADY-PROVEN automation from PR #564 (merged 2026-08-27) — the RF suite itself was NOT
rebuilt or modified for this backfill.

## Commands run
- `robot --dryrun tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot` → **5/5 PASS, 0 fail** (`../dryrun/` locally, not committed — dryrun has no evidentiary value beyond the count).
- `EC_HEADLESS=true robot --outputdir <bundle>/evidence/backfill_2026-08-28 tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot` → **5/5 PASS, 0 fail** on the first attempt (no retry needed). See `log.html`/`output.xml`/`report.html` in this folder.
- `robocop check tests/.../well_bore_iud.robot pageobjects/.../well_bore_page.resource` → exit 1, **7 issues** (5x DOC02 missing test-case docs, 2x VAR02 unused vars) — see `robocop_output.txt`. Same shape/count as Area's own baseline (parity, not a regression).
- `py scripts/check_bundle_hygiene.py` (repo root) → **RESULT: PASS** (no hardcoded creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradiction). One unrelated pre-existing WARN for Contract Area's investigation script, not this screen.
- Fresh independent `oracledb` connection to `localhost:1521/ORCL` (`ECKERNEL_EC`):
  - `SELECT COUNT(*) FROM OV_WELL_BORE WHERE UPPER(CODE) LIKE 'AUTOTEST%'` → **0** (self-clean confirmed after the live run above).
  - `SELECT COUNT(*) FROM OV_WELL_BORE` → **158** (pre-existing rows intact, unchanged from the 2026-07-31/2026-08-27 counts).
- Filter-keyword usage: `grep -c "Find Well Bore Row By Filter\|Clear Well Bore Row Filter" output.xml` → **19** hits (Find/Clear pair fired across TC02-TC05 + Verify wrappers), confirming the explicit grid-filter wiring the PR #564 body describes actually fires live.

## Result
All gates green; no automation change; this folder is documentation/evidence only, per the
lean-deliverable-backfill-workorder (docs/lean-deliverable-backfill-workorder.md).
