# RF Evidence Capture — Country — 2026-08-28 (lean-waiver backfill, Batch 6)

Re-run of the ALREADY-MERGED, already-working RF suite (PR #428, merged 2026-08-23) to capture
evidence for the retired lean waiver (`docs/lean-deliverable-backfill-workorder.md`). No RF
files were modified for this capture.

## Commands run
```
robot --dryrun --output NONE --report NONE --log NONE tests/Configuration/Assets/Basic_Objects/country_iud.robot
EC_HEADLESS=true robot --outputdir <this evidence run> tests/Configuration/Assets/Basic_Objects/country_iud.robot
```

## Results
- `--dryrun`: 5/5 PASS (TC01-TC05).
- Live headless run: **5/5 PASS** (TC01 Verify Clean State, TC02 Insert Country Data,
  TC03 Update Country Data, TC04 Find Country Data, TC05 Delete Country Data).
- Grid-filter wiring fired live: `grep -o 'name="Find Country Row By Filter"' output.xml` → **5 hits**.
- DB ground truth: TC05's `Verify Country Record Removed` → shared T2 `Verify Object Removed` →
  `Code Should Be Absent In View OV_COUNTRY AUTOTEST_COUNTRY` — PASSED, confirming 0 residual rows
  in `OV_COUNTRY` after the run (self-clean).
- robocop on the 2 RF files (`country_page.resource` + `country_iud.robot`): **9 issues**
  (4 VAR02 + 5 DOC02) — same count/kind PR #428 cited as its baseline; no new issue classes.
- Hygiene: `py scripts/check_bundle_hygiene.py` (run from repo root) → **PASS** — no hardcoded
  creds / ASCII violations in this screen's files (the one WARN reported is Contract Area's
  `investigation/`, unrelated to Country).

## Artifacts in this folder
- `log.html` / `output.xml` — full RF run log/report data from the live run above.
- `TC0*_*.png` — per-step screenshots captured by the suite's own `Capture Step` calls
  (login/open_screen/action/verify/logout per TC), 26 files total.

## Provenance
- [from fresh scan, live run 2026-08-28] All PASS/hit counts above.
- [from PR #428 body] robocop baseline count (9 issues, same kind), original live 5/5 confirmation,
  DB self-clean confirmation via fresh connection.
