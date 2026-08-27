# Contract Area — IUD automation bundle

**Screen:** Configuration > Assets > Contract Objects > Contract Area
**Type:** OV (Manage-Object), date-effective, **Business-Unit-gated (OV-GM)** — Area-pattern sibling.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_CONTRACT_AREA`).
**Status:** ✅ live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning.
See [contract_area_sow.md](contract_area_sow.md) and [JOURNAL.md](JOURNAL.md).

**The maintained/live test is the Robot Framework suite**, converted to the full Area-pattern
5-TC structure via PR #542 (2026-08-26). The Playwright driver below is the original 2026-06-18
reference implementation, preserved unchanged — per owner decision 2026-08-27
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no new/updated Playwright bundle is built for
Area-pattern conversions (the Universal Screen Engine replaces that role going forward).

## Layout
- `playwright/ec_iud_contract_area.py` — freestyle Playwright proof (clean→insert→update→delete,
  self-cleaning). Original 2026-06-18 build, NOT modified by PR #542 or this backfill.
- `investigation/` — read-only recon: `db_recon_contract_area.py`, `live_recon_contract_area.py`,
  `bu_distribution.py`, `treeview_path.py`, `grid_columns.py`. Original build, unchanged.
- `evidence/` — screenshots + `ec_iud_contract_area_result.json` from the original full run, plus
  `backfill_2026-08-27/` (RF dryrun + live output captured by this backfill).
- `contract_area_sow.md` — statement of work / spec (updated 2026-08-27 with the PR #542
  conversion story, §3.2).
- `JOURNAL.md` — work journal (added 2026-08-27 backfill).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-27 backfill).

## Run — Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_CONTRACT_AREA code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot
```

## DB self-clean check (ground truth — OV_CONTRACT_AREA)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_CONTRACT_AREA`) is absent and no `AUTOTEST%`
residual rows exist:
```sql
SELECT COUNT(*) FROM OV_CONTRACT_AREA WHERE CODE = 'AUTOTEST_CONTRACT_AREA';   -- expect 0
SELECT CODE FROM OV_CONTRACT_AREA WHERE CODE LIKE 'AUTOTEST%';                 -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view, not a
screen-specific `CONTRACT_AREA_CODE` column.)

## Run — Playwright (original reference, unmodified since 2026-06-18)
```bash
# from this folder — headless (default); a unique AUTOTEST_CA_<timestamp> code is generated per run
py -X utf8 playwright/ec_iud_contract_area.py

# live (visible browser)
EC_HEADED=1 py -X utf8 playwright/ec_iud_contract_area.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_BU` | `ECP Norway` | override the navigator Business Unit scope |
| `EC_CODE` | auto timestamp | override the test code |

## Key facts
- Navigator **Business Unit** dd `nav:form:G:0:R:1:C:1:dd` is mandatory; pick a BU + GO
  (`button:form:B`) before the grid (`manageObject:form:T_data`) loads. As of PR #542, the fill
  goes through the shared T2 `Apply Navigator From Properties`, driven by
  `testdata/contract_area_navigator.properties`.
- Insert **Business Unit Name** dd `…objectForm:form:G:0:R:5:C:1:dd` must equal the nav BU
  (default scope: **ECP Norway**) or the inserted row never lists in the filtered grid.
- OV-GM grids redraw lazily after Save+GO — the T3 keywords wait for the row span before asserting.
- The RF suite uses the FIXED test code `AUTOTEST_CONTRACT_AREA` (not a per-run timestamp — see
  PR #542); the Playwright driver still uses a unique `AUTOTEST_CA_<timestamp>` per run.
- The referenced Business Unit is read-only seed data — existing rows are never touched.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Contract_Objects/contract_area_page.resource`
- Suite: `tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot`
- Test data: `testdata/contract_area_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/contract_area.md`
