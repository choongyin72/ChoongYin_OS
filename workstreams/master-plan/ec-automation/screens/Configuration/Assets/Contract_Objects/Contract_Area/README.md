# Contract Area — IUD automation bundle

**Screen:** Configuration > Assets > Contract Objects > Contract Area
**Type:** OV (Manage-Object), date-effective, **Business-Unit-gated (OV-GM)** — sibling of Transport System.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_CONTRACT_AREA`).
**Status:** ✅ live **4/4 PASS**, DB-verified, self-cleaning. See [contract_area_sow.md](contract_area_sow.md).

## Layout
- `playwright/ec_iud_contract_area.py` — freestyle Playwright proof (clean→insert→update→delete, self-cleaning).
- `investigation/` — read-only recon: `db_recon_contract_area.py`, `live_recon_contract_area.py`,
  `bu_distribution.py`, `treeview_path.py`, `grid_columns.py`.
- `evidence/` — screenshots + `ec_iud_contract_area_result.json` from a full run.

## Run
```bash
# RF suite (the proof — headed, DB-verified):
cd workstreams/master-plan/ec-automation
EC_HEADLESS=false py -m robot --outputdir results/ca_live2 \
  tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot

# Playwright bundle (freestyle; EC_HEADED=1 to watch, EC_BU/EC_CODE to override):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Contract_Objects/Contract_Area/playwright/ec_iud_contract_area.py
```

## Key facts
- Navigator **Business Unit** dd `nav:form:G:0:R:1:C:1:dd` is mandatory; pick a BU + GO (`button:form:B`) before the grid (`manageObject:form:T_data`) loads.
- Insert **Business Unit Name** dd `…objectForm:form:G:0:R:5:C:1:dd` must equal the nav BU (default scope: **ECP Norway**) or the inserted row never lists in the filtered grid.
- OV-GM grids redraw lazily after Save+GO — the T3 "Row Should Exist" waits for the row span before asserting.
- Test data `AUTOTEST_CA_*` only; the referenced Business Unit is read-only seed data — existing rows are never touched.
