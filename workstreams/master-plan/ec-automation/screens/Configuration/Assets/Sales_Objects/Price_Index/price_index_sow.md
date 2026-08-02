# SOW - Price Index IUD (Configuration > Assets > Sales_Objects)

- **Screen:** Price Index   **BF:** CO.3009   **View:** `OV_PRICE_INDEX`   **Base:** `PRICE_INDEX`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_PI_<timestamp>`; self-clean = absent in OV_PRICE_INDEX.
- Deliverables: driver `py/price_index_iud.py`, T3 `pageobjects/Configuration/Assets/Sales_Objects/price_index_page.resource`,
  suite `tests/Configuration/Assets/Sales_Objects/price_index_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
