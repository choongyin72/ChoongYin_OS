# SOW - Tug Boat IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Tug Boat   **BF:** CO.2080   **View:** `OV_TUG_BOAT`   **Base:** `TUG_BOAT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_TB_<timestamp>`; self-clean = absent in OV_TUG_BOAT.
- Deliverables: driver `py/tug_boat_iud.py`, T3 `pageobjects/Configuration/Assets/Transport_Objects/tug_boat_page.resource`,
  suite `tests/Configuration/Assets/Transport_Objects/tug_boat_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
