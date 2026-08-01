# SOW - Collection Point IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Collection Point   **BF:** CO.0205   **View:** `OV_COLLECTION_POINT`   **Base:** `COLLECTION_POINT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CP<timestamp>`; self-clean = absent in OV_COLLECTION_POINT.
- Deliverables: driver `py/collection_point_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
