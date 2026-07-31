# SOW - Driver IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Driver   **BF:** CO.0266   **View:** `OV_DRIVER` (0 rows on the sandbox - our AUTOTEST row is the first)   **Base:** `DRIVER`
- **Type:** PLAIN OV (Bank family) with a **CUSTOM grid id `driver_object:form:T_data`** and an
  **EMPTY navigator** (GO alone populates the grid). Third of the Truck/Trailer/Driver cluster.
- **Mandatory set:** Driver Code / Driver Name / Start Date + **Driver Licence No** (text) +
  **Gender of driver** (dropdown, first-available).
  *Driver Licence No renders WHITE, so the yellow-cell scan missed it* - EC's own save-time message
  ("Required fields are empty: Driver Licence No[DRIVER_LICENCE_NUMBER]") supplied it. Second screen
  where EC's message was the reliable field spec.
- Start Date 2000-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_DR_<timestamp>` per run;
  self-cleaning.

## Known risks
- Mandatory set is screen-specific; re-derive from EC's save-time message if config changes.
