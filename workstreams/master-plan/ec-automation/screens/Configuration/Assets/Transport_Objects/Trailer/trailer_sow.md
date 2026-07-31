# SOW - Trailer IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Trailer   **BF:** CO.0265   **View:** `OV_TRAILER` (0 rows on the sandbox - our AUTOTEST row is the first)   **Base:** `TRAILER`
- **Type:** PLAIN OV (Bank family) with a **CUSTOM grid id `trailer_object:form:T_data`** and an
  **EMPTY navigator** (no nav fields at all - GO alone populates the grid). Sibling of Truck (CO.0264).
- **Mandatory set (live-scan verified):** Trailer Code / Trailer Name / Start Date +
  **Licence Plate No** (text) + **Trailer Type**, **UOM**, **Transport Company** (dropdowns,
  first-available). Lighter than Truck: no quantity fields are mandatory here.
- Start Date 2000-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_TR_<timestamp>` per run;
  self-cleaning.
- Built by the audited plain-OV generator `tmp/gen_ov.py` - **8/8 driver and 5/5 gates on the FIRST
  run**, no per-screen debugging needed (the 6 defects that generator audit fixed on Truck paid off).

## Known risks
- Mandatory set is screen-specific; if EC config changes, re-derive from EC's save-time
  "Required fields are empty" message.
