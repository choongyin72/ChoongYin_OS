# SOW - Price Object IUD (Configuration > Assets > Sales_Objects)

- **Screen:** Price Object   **BF:** CO.3016   **View:** `OV_PRICE_OBJECT`   **Base:** `PRODUCT_PRICE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_PO_<timestamp>`; self-clean = absent in OV_PRICE_OBJECT.
- Deliverables: driver `py/price_object_iud.py`, T3 `pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource`,
  suite `tests/Configuration/Assets/Sales_Objects/price_object_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
