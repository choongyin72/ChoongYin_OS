# SOW - Production Separator IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Production Separator   **BF:** CO.0042   **View:** `OV_PRODSEPARATOR`   **Base:** `SEPARATOR`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_PSEP_<timestamp>`; self-clean = absent in OV_PRODSEPARATOR.
- Deliverables: driver `py/production_separator_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
