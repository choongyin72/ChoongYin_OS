# SOW - Price Rate IUD (Configuration > Assets > Sales_Objects)

- **Screen:** Price Rate   **BF:** CO.3024   **View:** `OV_PRICE_RATE`   **Base:** `PRICE_RATE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_PRT_<timestamp>`; self-clean = absent in OV_PRICE_RATE.
- Deliverables: driver `py/price_rate_iud.py`, T3 `pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource`,
  suite `tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
