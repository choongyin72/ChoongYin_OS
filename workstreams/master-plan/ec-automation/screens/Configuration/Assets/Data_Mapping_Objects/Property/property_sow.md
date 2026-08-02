# SOW - Property IUD (Configuration > Assets > Data_Mapping_Objects)

- **Screen:** Property   **BF:** SP.0059   **View:** `OV_PROPERTY`   **Base:** `CONTRACT_AREA`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_PROP<timestamp>`; self-clean = absent in OV_PROPERTY.
- Deliverables: driver `py/property_iud.py`, T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource`,
  suite `tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
