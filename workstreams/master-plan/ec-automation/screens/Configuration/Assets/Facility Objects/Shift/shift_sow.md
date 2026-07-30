# SOW - Shift IUD (Configuration > Assets > Facility Objects)

- **Screen:** Shift   **BF:** CO.0224   **View:** `OV_SHIFT`   **Base:** `SHIFT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_SHIFT_<timestamp>`; self-clean = absent in OV_SHIFT.
- Deliverables: driver `py/shift_iud.py`, T3 `pageobjects/Configuration/Assets/Facility Objects/shift_page.resource`,
  suite `tests/Configuration/Assets/Facility Objects/shift_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
