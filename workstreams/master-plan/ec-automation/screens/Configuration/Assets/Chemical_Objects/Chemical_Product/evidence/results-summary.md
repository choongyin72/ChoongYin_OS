# Evidence — Chemical Product backfill run (2026-08-28)

Captured as part of the Batch 12 lean-deliverable backfill
(`docs/lean-deliverable-backfill-workorder.md`). The RF automation was NOT modified — this is a
re-run of the already-proven suite from PR #486 to capture fresh evidence artifacts.

## Dryrun (screen-scoped)
```
robot --dryrun --outputdir results/chemical_product_dryrun tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot
5 tests, 5 passed, 0 failed
```
Artifact: `dryrun/output.xml`.

## Live headless run
```
EC_HEADLESS=true robot --outputdir results/chemical_product_live tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot
TC01 Verify Clean State           | PASS |
TC02 Insert Chemical Product Data | PASS |
TC03 Update Chemical Product Data | PASS |
TC04 Find Chemical Product Data   | PASS |
TC05 Delete Chemical Product Data | PASS |
5 tests, 5 passed, 0 failed
```
Artifacts: `live/output.xml`, `live/log.html`, `live/TC0*.png` (5 TCs x login/open_screen/
action/verify/logout screenshots per TC, from the suite's existing `Capture Step` calls).

Keyword-firing check (`grep -c` on `live/output.xml`):
- `Find Object Row By Filter` fired 15x (grid-filter wiring confirmed active).
- `Remove Chem Usage Report Conf Child` fired 2x (Delete workaround confirmed active — once
  per Delete TC invocation path).

## DB ground truth — fresh-connection self-clean check
Run via `Workplaces/chemical-product-backfill/db_selfclean_check.py` (screen-scoped scratch
script, gitignored, not part of this bundle) on a **fresh** oracledb connection (separate from
the live-run session):

```
CHEM_PRODUCT AUTOTEST% rows: 0
OV_CHEM_PRODUCT AUTOTEST% rows: 0
Orphaned CHEM_USAGE_REPORT_CONF rows: 0
```

Self-clean confirmed: no residual `AUTOTEST_CHEMPROD` rows in `CHEM_PRODUCT`/`OV_CHEM_PRODUCT`,
and no orphaned `CHEM_USAGE_REPORT_CONF` rows left behind by the known-issue delete workaround.
