# Split Item Other (CD.0017) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Revenue_Split_Keys > Split Item Other**.
Full Insert / Update / Delete (End Date = Start Date), DB-verified against
`OV_SPLIT_ITEM_OTHER`, self-cleaning. Built label-driven 2026-07-26, then **rebuilt 2026-08-23
(PR #471, Batch 10) to the full Bank/Berth pattern**: properties-file-driven insert/update/verify
+ explicit grid-filter wiring, 5-TC business narrative, per-TC login/logout.

NOT the same screen as the 6 sibling "* Split Key" screens (Product/Company/Field/Stream Item
Category/Other/Stream Item Split Key) - those share a different class `SPLIT_KEY` and view
`OV_SPLIT_KEY`. This screen's class is `SPLIT_ITEM_OTHER`, view `OV_SPLIT_ITEM_OTHER`.

## Artifacts
- **SOW:** `split_item_other_sow.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/split_item_other_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Revenue_Split_Keys/split_item_other_iud.robot`
- **Testdata:** `../../../../testdata/split_item_other_{insert,update,form_verify,grid_verify}.properties`
- **Playwright driver (pre-existing, unchanged):** `../../../../py/split_item_other_iud.py`
- `investigation/` recon.py (pre-existing) - `evidence/` screenshots + `2026-08-28_live_{output.xml,log.html}`
  (fresh backfill evidence run) + `rf_report.html` (original 2026-07-26 run)
- `CHECKLIST.md` - this bundle's 21-item deliverable checklist
- `VERIFY-REPORT.md` - auto-generated 2026-07-26 by `scripts/verify_screen.py` (pre-Batch-10;
  kept as historical record, superseded by the fresh gate evidence cited in CHECKLIST.md below)

## Run commands
```bash
# Dryrun (from workstreams/master-plan/ec-automation/)
python -m robot --dryrun --outputdir results/_dryrun_split_item_other \
    tests/Configuration/Assets/Revenue_Split_Keys/split_item_other_iud.robot

# Live headless run
EC_HEADLESS=true python -m robot --outputdir results/_live_split_item_other \
    tests/Configuration/Assets/Revenue_Split_Keys/split_item_other_iud.robot

# DB self-clean check (fresh connection, run AFTER the live suite completes)
py -c "
import os, oracledb
conn = oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),
    password=os.environ.get('EC_DB_PASS','energy'),
    dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur = conn.cursor()
cur.execute(\"SELECT CODE, NAME FROM OV_SPLIT_ITEM_OTHER WHERE CODE LIKE 'AUTOTEST%'\")
print(cur.fetchall())
"
# expected: [] (0 residual rows)
```

## Verified (real runs, not hand-ticked)
- 2026-07-26 (original build, label-driven): robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 7/7, self-clean 0 residual.
- 2026-08-23 (PR #471, Bank-pattern rebuild): live 5/5, dryrun 767/767 (full tree),
  `Find Object Row By Filter` fired 30x (output.xml grep), DB self-clean 0 residual via fresh
  connection.
- 2026-08-28 (this backfill, doc-only, automation NOT touched): re-ran the existing suite once -
  dryrun 5/5 pass, live headless 5/5 pass, robocop 9 issues (same baseline DOC02/VAR02 style
  warnings as the merged `berth_iud.robot` exemplar, no regression), hygiene PASS
  (`check_bundle_hygiene.py`), DB self-clean 0 residual via a fresh `oracledb` connection.
