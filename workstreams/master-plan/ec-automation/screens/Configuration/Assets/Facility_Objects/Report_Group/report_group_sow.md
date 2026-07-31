# SOW - Report Group IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Report Group   **BF:** CO.0158   **View:** `OV_REPORT_GROUP`   **Base:** `REPORT_GROUP`
- **Type:** PLAIN OV (Bank family; grid `report_group_table:form:T_data`), date-only navigator + GO, date-effective.
- Date-only navigator -> GO populates the grid; fields resolved BY LABEL; extra mandatory dropdowns first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_RG<timestamp>`; self-clean = absent in OV_REPORT_GROUP.
- Deliverables: driver `py/report_group_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/report_group_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/report_group_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
