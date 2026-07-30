# SOW - Facility Class 1 IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Facility Class 1   **BF:** CO.0019   **View:** `OV_FCTY_CLASS_1`   **Base:** `FCTY_CLASS_1`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_FC1_<timestamp>`; self-clean = absent in OV_FCTY_CLASS_1.
- Deliverables: driver `py/facility_class_1_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
