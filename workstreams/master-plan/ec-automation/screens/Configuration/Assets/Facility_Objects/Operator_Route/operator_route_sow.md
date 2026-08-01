# SOW - Operator Route IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Operator Route   **BF:** CO.0244   **View:** `OV_OPERATOR_ROUTE`   **Base:** `OPERATOR_ROUTE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_OR_<timestamp>`; self-clean = absent in OV_OPERATOR_ROUTE.
- Deliverables: driver `py/operator_route_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
