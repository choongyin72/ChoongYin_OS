# SOW - External Location IUD (Configuration > Assets > Facility_Objects)

- **Screen:** External Location   **BF:** CO.0227   **View:** `OV_EXTERNAL_LOCATION`   **Base:** `EXTERNAL_LOCATION`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), NO mandatory nav scope (GO only), date-effective.
- GO only (navigator fields are optional filters, no mandatory scope); fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_EL<timestamp>`; self-clean = absent in OV_EXTERNAL_LOCATION.
- Deliverables: driver `py/external_location_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/external_location_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
