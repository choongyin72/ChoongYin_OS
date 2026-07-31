# SOW - Well Bore Interval IUD (Configuration > Assets > Well_and_Reservoir_Objects)

- **Screen:** Well Bore Interval   **BF:** CO.0057   **View:** `OV_WELL_BORE_INTERVAL` (167 rows, DB-verified)   **Base:** `WEBO_INTERVAL`
- **Type:** OV-GM with **6 PER-FIELD nav groups** `nav:form:G:1..G:6:R:1:C:0`. Grid `manageObject:form:T_data`.
- **SPECIFIC nav values (recon-verified):** G:1 P1 Production Unit -> G:2 P1 Area -> G:3 P1 Facility 1 ->
  G:4 **P1 W008 OP** (a REAL well) -> **G:6 P1 W008 WB001** (the WELL BORE). **G:5 returns ZERO
  options** under this scope (unusable filter, skipped) - the same pattern as Well Bore's G:5. Grid
  then lists the real interval `P1 W008 WB001 WBI001`.
- **Mandatory form field: 'Well Bore' POPUP** (pin R:4) whose list grid is **`Objects:form:T_data`**
  (recon-verified; contains exactly `P1 W008 WB001` under this scope) - not `PopupList:form:T_data`,
  so the generic engine/T1 helpers report a false "empty source list". Screen-local picker selects
  the nav-scope well bore BY VALUE.
- Start Date 2020-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_WBI_<timestamp>` per run;
  self-cleaning; the existing 167 intervals untouched.
- **Third screen of the well hierarchy** (Well -> Well Bore -> Well Bore Interval), all three now automated.

## Known risks
- Nav + popup values are DATA-dependent (P1 W008 OP / P1 W008 WB001); re-derive if the sandbox changes.
- G:5's purpose is unknown (no options in any scope tried) - if it ever populates, revisit whether it
  is a required filter.
