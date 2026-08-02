# SOW - Division Order IUD (EC_Revenue > Royalty > Royalty_USA)

- **Screen:** Division Order   **BF:** RC.0058   **View:** `OV_DIVISION_ORDER`   **Base:** `CONTRACT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_DO_<timestamp>`; self-clean = absent in OV_DIVISION_ORDER.
- Deliverables: driver `py/division_order_iud.py`, T3 `pageobjects/EC_Revenue/Royalty/Royalty_USA/division_order_page.resource`,
  suite `tests/EC_Revenue/Royalty/Royalty_USA/division_order_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
