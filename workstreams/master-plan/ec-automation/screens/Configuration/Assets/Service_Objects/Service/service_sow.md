# SOW - Service IUD (Configuration > Assets > Service_Objects)

- **Screen:** Service   **BF:** CO.2103   **View:** `OV_SERVICE`   **Base:** `SERVICE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_SV<timestamp>`; self-clean = absent in OV_SERVICE.
- Deliverables: driver `py/service_iud.py`, T3 `pageobjects/Configuration/Assets/Service_Objects/service_page.resource`,
  suite `tests/Configuration/Assets/Service_Objects/service_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
