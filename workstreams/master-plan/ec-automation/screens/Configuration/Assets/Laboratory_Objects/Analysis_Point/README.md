# Analysis Point — IUD automation bundle

**Screen:** Configuration > Assets > Laboratory Objects > Analysis Point
**Type:** OV-GM (groupmodel, **3-level cascade**), date-effective.
**Delete:** End Date = Start Date (true delete from `OV_ANALYSIS_POINT`).
**Status:** ✅ live **4/4 PASS**, DB-verified, self-cleaning. See [analysis_point_sow.md](analysis_point_sow.md).

## Layout
- `playwright/ec_iud_analysis_point.py` — freestyle proof (cascade nav → insert → update → End=Start delete; env creds).
- `investigation/` — read-only recon: `analysis_point_db_recon.py`, `analysis_point_scope.py`, `recon_analysis_point_live.py`, `analysis_point_residue.py`.
- `evidence/` — screenshots + `ec_iud_analysis_point_result.json`.

## Run
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=false py -m robot --outputdir results/ap_live \
  tests/Configuration/Assets/Laboratory_Objects/analysis_point_iud.robot
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Laboratory_Objects/Analysis_Point/playwright/ec_iud_analysis_point.py
```

## Key facts
- **Gated 3-level cascade**: PU `nav:form:G:0:R:1:C:1:dd` → Area `…C:2:dd` → Facility `…C:3:dd` + GO before the grid (`manageObject:form:T_data`) loads. Driven by `Select EC Dropdown Option` (dds at C:1–C:3, not C:0).
- Insert mandatory: Start Date (R:0), Code (R:2), Name (R:3), **Type dd (R:4)**. Plus **Op PU/Area/Facility dds (R:10/11/12) = nav scope** — the groupmodel link required for the row to list (set even though not yellow).
- OV-GM grid redraws lazily after Save+GO → T3 `Row Should Exist` waits for the row span (R17).
- Scope P1 Production Unit / P1 Area / P1 Facility 1; date 2003-01-01 (ref dds). Test data `AUTOTEST_AP_*`; referenced objects read-only seed. Credentials from env (R16).
