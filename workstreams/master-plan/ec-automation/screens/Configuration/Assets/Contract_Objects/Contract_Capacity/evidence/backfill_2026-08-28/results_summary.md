# Evidence capture — Contract Capacity backfill (Batch 4, 2026-08-28)

This folder holds the evidence for the **documentation backfill** task (owner decision
2026-08-27, `docs/lean-deliverable-backfill-workorder.md`, Batch 4). The RF automation itself was
**not modified** — it was already converted to the Area pattern by PR #535 (merged 2026-08-26).
This is a fresh evidence-capture run of that already-working suite, per the process rule: retry
once on failure, then disclose honestly.

## Dryrun
`robot --dryrun tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot`
→ 5 tests, 5 passed, 0 failed (0 keyword/import resolution errors).

## Live run — attempt 1 (`output_attempt1_TC05fail.xml`)
`EC_HEADLESS=true robot tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot`
→ **4 passed, 1 failed.** TC05 Delete Contract Capacity Data failed:
`Row AUTOTEST_CONTRACT_CAPACITY should NOT exist in manageObject:form:T_data: 1 != 0` — the
grid still showed the row immediately after the delete+GO refresh (consistent with the
page-object's own documented "OV-GM grids redraw lazily after Save+GO" quirk, not a code defect
introduced by this backfill task, since no automation file was touched).

## Live run — attempt 2 / retry (`output.xml`, `log.html`, `report.html`)
Same command, one retry per the process rule. **5 tests, 5 passed, 0 failed** (TC01 Verify Clean
State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete all PASS).

## DB ground-truth (fresh connection, after the passing retry)
```sql
SELECT COUNT(*) FROM OV_CONTRACT_CAPACITY WHERE CODE LIKE 'AUTOTEST%'
```
→ `0` (self-clean confirmed; TC01's clean-state check in attempt 2 also passed, confirming the
attempt-1 TC05 grid failure was a screen-render lag, not a real DB residual left over from
attempt 1).

## Disclosure
This is disclosed here rather than smoothed over, per the process rule for this backfill task:
the live suite is proven/already-shipped automation (PR #535), the flake was observed during
evidence capture and resolved by the single permitted retry — no automation file was edited to
"fix" it.
