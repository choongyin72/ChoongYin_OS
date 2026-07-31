# SOW - Cargo Planning Forecast IUD (EC Transport > Cargo Planning > Forecast)

- **Screen:** Cargo Planning Forecast   **BF:** CP.0030   **View:** `OV_FCST_MNGR_FCST_LIST`
  (resolved EMPIRICALLY from the resolver's 2 candidates - the row also lands in
  `OV_FORECAST_TRAN_CP`; both over base `FORECAST`)   **Base:** `FORECAST`
- **Type:** custom EC Transport forecast-manager screen: navigator = **PER-FIELD groups**
  `nav:form:G:1..G:4:R:1:C:0` (PU -> Area -> FC1 -> **Storage**), SPECIFIC P1 values +
  `P1_CRUDE_STOR` (owner screenshot; first-available AS1 left the Storage level empty = the
  original park). Grid = **`fcst:form:T_data`** (custom prefix).
- **The circled `new_fcst` panel + COPY FROM FORECAST/ORIGINAL buttons = the copy-existing-forecast
  dialog (owner-confirmed) - NOT used; the standard `tab:tabPanel:objectForm` is the insert form.**
- **Mandatory extra: END DATE at insert** (unusual) - Start 2026-01-01 / End 2026-12-31 spans the
  nav date (2026-07-29) so the row lists. **Storage Name = nav Storage** (parent-matching).
- **DELETE = End Date = Start Date** - proven a true delete on this screen (row leaves grid + both
  views) despite the mandatory insert End Date.
- Unique `AUTOTEST_CPF_<timestamp>` per run; self-cleaning (residual checked in BOTH views).

## Known risks
- Nav scope + Storage are DATA-dependent (P1 objects); re-derive if renamed/removed.
- The screen has NEW OBJECT / NEW VERSION insert modes - the suite uses NEW OBJECT only.
