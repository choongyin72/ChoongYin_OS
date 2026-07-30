# SOW - Storage IUD (Configuration > Assets > Tank and Storage Objects)

- **Screen:** Storage   **BF:** CO.0034   **View:** `OV_STORAGE`   **Base:** `STORAGE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_STOR_<timestamp>`; self-clean = absent in OV_STORAGE.
- Deliverables: driver `py/storage_iud.py`, T3 `pageobjects/Configuration/Assets/Tank and Storage Objects/storage_page.resource`,
  suite `tests/Configuration/Assets/Tank and Storage Objects/storage_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
