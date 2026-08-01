# SOW - Contract Capacity IUD (Configuration > Assets > Contract_Objects)

- **Screen:** Contract Capacity   **BF:** CO.2044   **View:** `OV_CONTRACT_CAPACITY`   **Base:** `CONTRACT_CAPACITY`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CC<timestamp>`; self-clean = absent in OV_CONTRACT_CAPACITY.
- Deliverables: driver `py/contract_capacity_iud.py`, T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource`,
  suite `tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
