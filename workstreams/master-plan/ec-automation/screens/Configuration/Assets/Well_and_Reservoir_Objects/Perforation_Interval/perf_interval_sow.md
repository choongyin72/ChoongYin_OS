# SOW - Perforation Interval IUD (Configuration > Assets > Well_and_Reservoir_Objects)

- **Screen:** Perforation Interval   **BF:** CO.0153   **View:** `OV_PERF_INTERVAL` (225 rows, DB-verified)   **Base:** `PERF_INTERVAL`
- **Type:** OV-GM with **7 PER-FIELD nav groups** `nav:form:G:1..G:7:R:1:C:0`. Grid `manageObject:form:T_data`.
- **SPECIFIC nav chain (recon-verified, 4 levels of the well hierarchy):** G:1 P1 Production Unit ->
  G:2 P1 Area -> G:3 P1 Facility 1 -> G:4 **P1 W008 OP** (well) -> **G:6 P1 W008 WB001** (well bore)
  -> **G:7 P1 W008 WB001 WBI001** (well bore interval). **G:5 returns ZERO options** (unusable
  filter, skipped - 4th screen with this quirk). Grid shows 'No records found' under this scope
  (that interval has no perforations yet - our AUTOTEST row is the first).
- **Mandatory 'Well Bore Interval' POPUP (pin R:6) - INNER-GO type:** the popup frame
  (`well_bore_interval_gm_popup`) INHERITS the outer nav scope (G:1-G:4/G:6 pre-filled,
  recon-verified) but its list grid `Objects:form:T_data` stays **EMPTY until the popup's own inner
  GO (`button:form:B`)** is clicked. The generic engine/T1 helpers wait on `PopupList:form:T_data`
  and never drive GO -> false "empty source list". Screen-local picker handles it.
- **Mandatory 'Reservoir Block Formation' dropdown** (R:7) -> first-available.
- Start Date 2020-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_PI_<timestamp>` per run;
  self-cleaning; the existing 225 perforation intervals untouched.
- **Completes the 4-level well hierarchy:** Well -> Well Bore -> Well Bore Interval -> Perforation Interval.

## Known risks
- Nav + popup values are DATA-dependent (the P1 W008 chain); re-derive if the sandbox changes.
- Popup TYPES now number three (plain PopupList / already-populated Objects grid / inner-GO Objects
  grid) - always recon a new screen's popup rather than reusing a sibling's handler blindly.
