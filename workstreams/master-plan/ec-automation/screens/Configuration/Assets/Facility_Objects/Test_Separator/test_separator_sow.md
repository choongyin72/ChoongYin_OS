# SOW - Test Separator IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Test Separator   **BF:** CO.0040   **View:** `OV_TESTSEPARATOR`   **Base:** `SEPARATOR`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_TSEP_<timestamp>`; self-clean = absent in OV_TESTSEPARATOR.
- Deliverables: driver `py/test_separator_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/test_separator_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/test_separator_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
