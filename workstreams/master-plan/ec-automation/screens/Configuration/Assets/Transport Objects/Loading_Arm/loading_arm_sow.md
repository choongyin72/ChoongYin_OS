# SOW - Loading Arm IUD (Configuration > Assets > Transport Objects)

- **Screen:** Loading Arm   **BF:**    **View:** `OV_LOADING_ARM`   **Base:** `LOADING_ARM`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_LA_<timestamp>`; self-clean = absent in OV_LOADING_ARM.
- Deliverables: driver `py/loading_arm_iud.py`, T3 `pageobjects/Configuration/Assets/Transport Objects/loading_arm_page.resource`,
  suite `tests/Configuration/Assets/Transport Objects/loading_arm_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
