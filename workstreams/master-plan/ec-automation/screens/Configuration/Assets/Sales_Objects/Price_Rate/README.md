# Price Rate - EC Object IUD bundle

**Screen:** Configuration > Assets > Sales_Objects > Price Rate (BF CO.3024). OV-GM (grid
`manageObject:form:T_data`), navigator-GATED (single Business Unit dropdown, "SS2 BU"),
date-effective. See `price_rate_sow.md` and `JOURNAL.md`.

**The maintained/live test is the Robot Framework suite**, converted to the full Area-pattern 5-TC
structure via PR #534 (2026-08-26). The Playwright driver (`py/price_rate_iud.py`) is the original
2026-08-02 reference implementation, preserved unchanged - per owner decision 2026-08-27
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no new/updated Playwright bundle is built for
Area-pattern conversions (the Universal Screen Engine replaces that role going forward).

## Layout
- `price_rate_sow.md` - statement of work / spec (updated 2026-08-27 with the PR #534 conversion story).
- `JOURNAL.md` - work journal (added 2026-08-27 backfill).
- `CHECKLIST.md` - deliverable checklist (added 2026-08-27 backfill).
- `investigation/recon.py` - original read-only recon script (2026-08-02 build, unchanged).
- `evidence/` - original screenshots (`prt_0[1-5]_*.png`) + `results.json` from the 2026-08-02
  build, plus `backfill_2026-08-27/` (RF dryrun + live headless output + per-TC screenshots
  captured by this backfill).

## Run - Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning - TC05 deletes the fixed
#    AUTOTEST_PRICE_RATE code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot
```

## DB self-clean check (ground truth - OV_PRICE_RATE)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_PRICE_RATE`) is absent and no `AUTOTEST%`
residual rows exist:
```sql
SELECT COUNT(*) FROM OV_PRICE_RATE WHERE CODE = 'AUTOTEST_PRICE_RATE';   -- expect 0
SELECT CODE FROM OV_PRICE_RATE WHERE CODE LIKE 'AUTOTEST%';              -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

## Run - Playwright (original reference, unmodified since 2026-08-02)
```bash
# from workstreams/master-plan/ec-automation/ - headless (default)
py -X utf8 py/price_rate_iud.py

# live (visible browser)
EC_HEADED=1 py -X utf8 py/price_rate_iud.py
```

## Key facts
- Navigator **Business Unit** dd `nav:form:G:0:R:1:C:1:dd` (single dropdown, C:1 only, not a
  multi-level cascade) is mandatory; pick "SS2 BU" + GO (`button:form:B`) before the grid
  (`manageObject:form:T_data`) loads. As of PR #534, the fill goes through the shared T2
  `Apply Navigator From Properties`, driven by `testdata/price_rate_navigator.properties`.
- Insert **Business Unit** dd in `objectForm` must equal the nav value ("SS2 BU") or the inserted
  row never lists in the filtered grid.
- Field labels are SCREEN-PREFIXED: "Price Rate Code"/"Price Rate Name" (like Area's own "Area
  Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use.
- The RF suite uses the FIXED test code `AUTOTEST_PRICE_RATE` (not a per-run timestamp - see
  PR #534); the Playwright driver still uses `AUTOTEST_PRT_<timestamp>` per run.
- Delete = End Date set to Start Date (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`,
  hardcoded not label-driven - same documented rationale as Area/Bank's own End Date field).

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource`
- Suite: `tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot`
- Test data: `testdata/price_rate_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/price_rate.md`
