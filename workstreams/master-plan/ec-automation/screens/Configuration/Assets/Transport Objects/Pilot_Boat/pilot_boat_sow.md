# SOW - Pilot Boat IUD (Configuration > Assets > Transport Objects)

- **Screen:** Pilot Boat   **BF:**    **View:** `OV_PILOT_BOAT`   **Base:** `PILOT_BOAT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_PB_<timestamp>`; self-clean = absent in OV_PILOT_BOAT.
- Deliverables: driver `py/pilot_boat_iud.py`, T3 `pageobjects/Configuration/Assets/Transport Objects/pilot_boat_page.resource`,
  suite `tests/Configuration/Assets/Transport Objects/pilot_boat_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
