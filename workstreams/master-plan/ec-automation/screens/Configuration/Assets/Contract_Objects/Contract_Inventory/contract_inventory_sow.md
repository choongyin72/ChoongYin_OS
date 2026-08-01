# SOW - Contract Inventory IUD (Configuration > Assets > Contract_Objects)

- **Screen:** Contract Inventory   **BF:** CO.2054   **View:** `OV_CONTRACT_INVENTORY`   **Base:** `CONTRACT_INVENTORY`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CI_<timestamp>`; self-clean = absent in OV_CONTRACT_INVENTORY.
- Deliverables: driver `py/contract_inventory_iud.py`, T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource`,
  suite `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
