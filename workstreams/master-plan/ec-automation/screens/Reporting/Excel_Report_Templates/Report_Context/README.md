# Report Context (RP.0007) — bundle overview

Reporting > Excel Report Templates > Report Context. Custom-URL OV, no navigator, DELETE = End
Date = Start Date. RF automation is already built and merged (PR #487, 2026-08-24); this bundle is
a documentation/evidence backfill only (`docs/lean-deliverable-backfill-workorder.md`, Batch 12) —
no automation file was touched by this backfill.

## Files in this bundle
- `report_context_sow.md` — classification, navigator/grid/cell shape, test data, dev story.
- `JOURNAL.md` — built/done-well/lessons/blockers/decisions/evidence, pulled from PR #487.
- `CHECKLIST.md` — the 21-item deliverable checklist, ticked with real evidence citations.
- `evidence/` — one fresh live headless run (2026-08-28, 5/5 PASS): `log.html`, `report.html`,
  `output.xml`, and per-TC step screenshots.

Real automation lives outside this folder, under the standard treeview-mirrored paths:
- T3 page object: `workstreams/master-plan/ec-automation/pageobjects/Reporting/Excel_Report_Templates/report_context_page.resource`
- Suite: `workstreams/master-plan/ec-automation/tests/Reporting/Excel_Report_Templates/report_context_iud.robot`
- Test data: `workstreams/master-plan/ec-automation/testdata/report_context_{insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/report_context.md`
- Registry row: `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (already present, added by PR #487)
- Scorecard row: `docs/automation-scorecard.md` (already present, added by PR #487)

## Exact commands

Run from `workstreams/master-plan/ec-automation/`.

**Dryrun (syntax/keyword check only, no browser):**
```
py -m robot --dryrun --outputdir results/report_context_dryrun tests/Reporting/Excel_Report_Templates/report_context_iud.robot
```

**Live headless run:**
```
EC_HEADLESS=true py -m robot --outputdir results/report_context_live tests/Reporting/Excel_Report_Templates/report_context_iud.robot
```

**DB self-clean check (fresh connection, run AFTER a live suite so TC05 has already deleted the
test row):**
```python
import os, oracledb
conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()
cur.execute("SELECT code, name FROM ov_rept_context WHERE code LIKE 'AUTOTEST%'")
print(cur.fetchall())  # expect []
conn.close()
```
(Save as a scratch `.py` file and run via `py <file>` — per project convention, never `py -c`.)

## Last verified
2026-08-28 — dryrun 5/5, live headless 5/5 (first attempt, no retry needed), DB self-clean 0
residual `AUTOTEST_REPORT_CONTEXT` rows in `OV_REPT_CONTEXT` (fresh connection, post-run).
