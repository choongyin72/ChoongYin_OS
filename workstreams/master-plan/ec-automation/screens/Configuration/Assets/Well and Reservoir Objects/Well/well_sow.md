# SOW - Well IUD (Configuration > Assets > Well and Reservoir Objects)

- **Screen:** Well   **BF:** CO.0049   **View:** `OV_WELL`   **Base:** `WELL`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_WL_<timestamp>`; self-clean = absent in OV_WELL.
- Deliverables: driver `py/well_iud.py`, T3 `pageobjects/Configuration/Assets/Well and Reservoir Objects/well_page.resource`,
  suite `tests/Configuration/Assets/Well and Reservoir Objects/well_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
