# SOW - Well Hole IUD (Configuration > Assets > Well and Reservoir Objects)

- **Screen:** Well Hole   **BF:** CO.0051   **View:** `OV_WELL_HOLE`   **Base:** `WELL_HOLE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_WELL_HOLE_<timestamp>`; self-clean = absent in OV_WELL_HOLE.
- Deliverables: driver `py/well_hole_iud.py`, T3 `pageobjects/Configuration/Assets/Well and Reservoir Objects/well_hole_page.resource`,
  suite `tests/Configuration/Assets/Well and Reservoir Objects/well_hole_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
