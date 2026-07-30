# SOW - Lifting Account IUD (Configuration > Assets > Transport Objects)

- **Screen:** Lifting Account   **BF:** CO.2004   **View:** `OV_LIFTING_ACCOUNT`   **Base:** `LIFTING_ACCOUNT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_LA_<timestamp>`; self-clean = absent in OV_LIFTING_ACCOUNT.
- Deliverables: driver `py/lifting_account_iud.py`, T3 `pageobjects/Configuration/Assets/Transport Objects/lifting_account_page.resource`,
  suite `tests/Configuration/Assets/Transport Objects/lifting_account_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
