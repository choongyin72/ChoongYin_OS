# SOW - Well Hookup IUD (Configuration > Assets > Facility Objects)

- **Screen:** Well Hookup   **BF:** CO.0108   **View:** `OV_WELL_HOOKUP`   **Base:** `WELL_HOOKUP`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_WELL_HOOKUP_<timestamp>`; self-clean = absent in OV_WELL_HOOKUP.
- Deliverables: driver `py/well_hookup_iud.py`, T3 `pageobjects/Configuration/Assets/Facility Objects/well_hookup_page.resource`,
  suite `tests/Configuration/Assets/Facility Objects/well_hookup_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
