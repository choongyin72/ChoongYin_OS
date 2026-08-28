# Target Mapping Configuration (IS.0002) — bundle overview

Find-only RF suite for Configuration > Integration Services > Import > Target Mapping
Configuration. This screen does not support Insert/Update/Delete (owner-confirmed + independently
re-confirmed live — see `target_mapping_configuration_sow.md`), so the suite is named
`target_mapping_configuration_find.robot`, not `_iud.robot`, and has only 2 test cases:

- **TC01** — clean-state / initial-load check (navigator renders, GO loads the grid, at least one
  row visible).
- **TC04** — find an existing real row and cross-check it against the DB
  (`OV_IMP_TARGET_MAPPING`).

There is no TC02 (Insert), TC03 (Update), or TC05 (Delete) — this is intentional scope, not a gap.

## Files
- `pageobjects/Configuration/Integration_Services/target_mapping_configuration_page.resource` (T3)
- `tests/Configuration/Integration_Services/target_mapping_configuration_find.robot` (suite)

Both files are pre-existing (built in PR #488, merged 2026-08-24) and are NOT modified by this
backfill — this bundle only adds the documentation/evidence artifacts required by
`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H.

## Commands

Run from `workstreams/master-plan/ec-automation/`.

**Dryrun (this suite only):**
```
robot --dryrun --outputdir results/_tmc_dryrun tests/Configuration/Integration_Services/target_mapping_configuration_find.robot
```

**Dryrun (full tree, collision check):**
```
robot --dryrun --outputdir results/_tmc_dryrun_tree tests/
```

**Live headless run (TC01 + TC04 only — the suite's full scope):**
```
EC_HEADLESS=true robot --outputdir screens/Configuration/Integration_Services/Target_Mapping_Configuration/evidence tests/Configuration/Integration_Services/target_mapping_configuration_find.robot
```
Expect **2/2 PASS** — this is the suite's complete scope, not a partial run.

## No DB self-clean needed — row-count-unchanged proof instead
This suite never inserts, updates, or deletes anything, so the usual "self-clean = 0 residual"
check does not apply. Instead, the equivalent evidence is a fresh-connection row count on
`OV_IMP_TARGET_MAPPING` taken before and after the live run, proving the table was untouched:

```python
import oracledb
# fresh connection, no caching from a prior session
conn = oracledb.connect(user=..., password=..., dsn=...)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_IMP_TARGET_MAPPING")
print(cur.fetchone()[0])
```

Original build evidence: 117 → 117 across the live run (`tmp/tmc_rowcount_check.py`, PR #488).
This backfill re-ran the same check — see `JOURNAL.md` "Evidence" for the re-run figures.
