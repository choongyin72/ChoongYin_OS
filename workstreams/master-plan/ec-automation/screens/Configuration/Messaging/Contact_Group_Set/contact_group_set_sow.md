# SOW - Maintain Contact Group Set IUD (Configuration > Messaging)

- **Screen:** Maintain Contact Group Set   **BF:** CO.0225   **View:** `OV_CONTACT_GROUP_SET`   **Base:** `CONTACT_GROUP`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CGS_<timestamp>`; self-clean = absent in OV_CONTACT_GROUP_SET.
- Deliverables: driver `py/contact_group_set_iud.py`, T3 `pageobjects/Configuration/Messaging/contact_group_set_page.resource`,
  suite `tests/Configuration/Messaging/contact_group_set_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
