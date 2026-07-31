# SOW - Truck IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Truck   **BF:** CO.0264   **View:** `OV_TRUCK` (0 rows on the sandbox - our AUTOTEST row is the first)   **Base:** `TRUCK`
- **Type:** PLAIN OV (Bank family) with a **CUSTOM grid id `truck_object:form:T_data`** (not the usual
  `manage_object_nav_nav:form:T_data`). Navigator has NO fields at all - just GO to populate the grid.
- **Mandatory set (from EC's own save-time error message, not from the yellow scan):**
  Truck Code / Truck Name / Start Date + **Licence Plate No** (text) + **Tractor Gross Vehicle
  Quantity**, **Vehicle Gross Combined Quantity**, **Unladen Truck Quantity** (numeric texts) +
  **UOM** and **Transport Company** (dropdowns, first-available). EC revealed these iteratively:
  each save named the next missing field, which is more reliable than the yellow-cell heuristic
  (several of these render white).
- Start Date 2000-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_TK_<timestamp>` per run;
  self-cleaning.
- **First screen built by the NEW plain-OV generator `tmp/gen_ov.py`** (see JOURNAL for the 6 defects
  that audit exposed and fixed).

## Known risks
- The mandatory set is screen-specific and larger than a typical Bank-family screen; if EC config
  changes, re-derive by reading EC's save-time "Required fields are empty" message.
