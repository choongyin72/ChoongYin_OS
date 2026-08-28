# Account Mapping — backfill evidence-capture run (2026-08-28)

Deliverable backfill per `docs/lean-deliverable-backfill-workorder.md` (Batch 8) — this is
evidence capture of the ALREADY-PROVEN Bank-pattern RF suite from PR #450 (2026-08-23), not a
fresh verification cycle. The RF automation itself was NOT modified.

## Commands run (from `workstreams/master-plan/ec-automation/`)

```bash
py -m robot --dryrun --outputdir Workplaces/account-mapping-backfill/dryrun \
    tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot

py -m robocop check pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource \
    tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot

EC_HEADLESS=true py -m robot --outputdir Workplaces/account-mapping-backfill/live \
    tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot

py Workplaces/account-mapping-backfill/db_selfclean_check.py   # fresh oracledb connection

py scripts/check_bundle_hygiene.py   # (run from repo root)
```

## Results

| Gate | Result |
|---|---|
| `--dryrun` | **5/5 PASS** (TC01–TC05), 0 failed. `dryrun_output.xml` |
| Robocop | **7 issues** (2× VAR02 `${TEST_CODE}`/`${END_DATE}` assigned-but-unused, 5× DOC02 missing test-case documentation) — same baseline pattern as sibling Bank-pattern conversions, not a regression. `robocop_output.txt` |
| Live headless run | **5/5 PASS on attempt 1** (TC01–TC05), no retry needed. `live_log.html` / `live_report.html` / `live_output.xml` |
| Grid-filter wiring | `Find Object Row By Filter` — 15 hits across dryrun+live `output.xml` (fired every TC, both structural and live passes) |
| DB self-clean (fresh `oracledb` connection, `EC_DB_DSN=localhost:1521/ORCL`, `ECKERNEL_EC`) | `AUTOTEST_AM` present = **0**; `AUTOTEST%` residual = **[]** (none); total `OV_FIN_ACCOUNT_MAPPING` rows = **75** (matches PR #450's own cited baseline, unchanged before/after) — `db_selfclean_check_output.txt` |
| Hygiene (`scripts/check_bundle_hygiene.py`, repo root) | **RESULT: PASS** — no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradiction. One pre-existing WARN cited (2 hardcoded-credential lines in a DIFFERENT screen's recon script, **Contract Area** `investigation/live_recon_contract_area.py` — not touched by this backfill). `hygiene_output.txt` |

## Conclusion
No regression found. PR #450's live 5/5 result is reproduced (5/5, no retry needed this run — the
retry PR #450 disclosed was for the Line Item Type re-render gotcha and is already fixed in the
current T3, so the gotcha's fix, not the gotcha itself, is what this run exercised). DB self-clean
holds: 0 residual test rows, row count unchanged. This backfill did not modify
`account_mapping_page.resource`, `account_mapping_iud.robot`, `credentials.py`, or any
`testdata/account_mapping_*.properties` file.
