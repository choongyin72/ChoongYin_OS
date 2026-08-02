# SOW - Message Group IUD (Configuration > Messaging)

- **Screen:** Message Group   **BF:** CO.0236   **View:** `OV_MESSAGE_GROUP`   **Base:** `MESSAGE_GROUP`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_MG<timestamp>`; self-clean = absent in OV_MESSAGE_GROUP.
- Deliverables: driver `py/message_group_iud.py`, T3 `pageobjects/Configuration/Messaging/message_group_page.resource`,
  suite `tests/Configuration/Messaging/message_group_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
