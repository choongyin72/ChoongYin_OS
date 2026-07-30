# SOW - Test Device IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Test Device   **BF:** CO.0123   **View:** `OV_TEST_DEVICE`   **Base:** `TEST_DEVICE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_TD_<timestamp>`; self-clean = absent in OV_TEST_DEVICE.
- Deliverables: driver `py/test_device_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/test_device_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/test_device_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
