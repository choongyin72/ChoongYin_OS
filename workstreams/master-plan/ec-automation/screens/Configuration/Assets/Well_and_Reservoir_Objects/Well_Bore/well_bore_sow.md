# SOW - Well Bore IUD (Configuration > Assets > Well_and_Reservoir_Objects)

- **Screen:** Well Bore   **BF:** CO.0054   **View:** `OV_WELL_BORE` (158 rows, DB-verified)   **Base:** `WEBO_BORE`
- **Type:** OV-GM with **PER-FIELD nav groups** `nav:form:G:1..G:4:R:1:C:0` = Production Unit /
  Area / Facility Class 1 / **Well & Well Hookup**. Grid `manageObject:form:T_data`.
- **SPECIFIC nav values required:** P1 Production Unit -> P1 Area -> P1 Facility 1 -> **P1 W008 OP**.
  The first-available G:4 option is `P1 Graph 001` (a GRAPH object with no bores -> grid empty), so a
  REAL well must be chosen. A 5th group G:5 ('Well') is scan-flagged mandatory but returns ZERO
  options under every scope tried -> unusable filter, skipped (grid loads on 4 levels; verified by
  the real bore `P1 W008 WB001` listing).
- **Mandatory form field: 'Well' POPUP** (pin R:7) whose list grid is **`Objects:form:T_data`**
  (a THIRD variant after `PopupList:form:T_data` and `manage_object_nav_nav:form:T_data`) - already
  populated on open (40 rows). Screen-local picker selects the **nav-scope well by value**; the
  popup's first row is the graph object and is deliberately not used.
- Start Date 2020-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_WB_<timestamp>` per run;
  self-cleaning; existing 158 bores untouched.

## Known risks
- Nav + popup values are DATA-dependent (P1 W008 OP); re-derive if the sandbox changes.
- Popup grid id is per-popup-TYPE - if EC changes this object popup, re-recon with
  `investigation/recon_wb_popup*.py` (banked).
