# RF backfill evidence run — Customer — 2026-08-28

Re-run of the already-proven `customer_iud.robot` suite, captured as evidence for the
lean-deliverable backfill (`docs/lean-deliverable-backfill-workorder.md`, Batch 6). No RF
automation file was modified for this run.

## Command
```
EC_HEADLESS=true py -m robot --outputdir Workplaces/customer-backfill/evidence_run \
    tests/Configuration/Assets/Commercial_Objects/customer_iud.robot
```

## Result
```
TC01 Verify Clean State                                               | PASS |
TC02 Insert Customer Data                                             | PASS |
TC03 Update Customer Data                                             | PASS |
TC04 Find Customer Data                                               | PASS |
TC05 Delete Customer Data                                             | PASS |
5 tests, 5 passed, 0 failed
```

## Full-tree dryrun (same session)
```
py -m robot --dryrun --outputdir /tmp/customer_dryrun tests/
883 tests, 883 passed, 0 failed
```

## robocop (customer_page.resource + customer_iud.robot)
7 issues (2 VAR02 + 5 DOC02) — identical count to PR #435's cited baseline.

## DB self-clean (fresh oracledb connection, ECKERNEL_EC/energy@localhost:1521/ORCL)
```sql
SELECT COUNT(*) FROM OV_CUSTOMER WHERE CODE = 'AUTOTEST_CUST';
-- 0
```

## Filter-wiring check
`grep -c "Find Customer Row By Filter" output.xml` = 15 (fired across TC02-TC05, matches the
Find/Clear-per-TC wiring in `customer_page.resource`).

## Hygiene
`py scripts/check_bundle_hygiene.py` → `RESULT: PASS` (no hardcoded creds in Customer's own
files, pure ASCII, no CHECKLIST/VERIFY-REPORT contradictions). The single WARN reported by the
scan belongs to an unrelated bundle (Contract Area's `investigation/live_recon_contract_area.py`),
not Customer.

Raw artifacts in this folder: `log.html`, `report.html`, `output.xml`.
