# SOW - Channel IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Channel   **BF:** CO.2077   **View:** `OV_CHANNEL`   **Base:** `CHANNEL`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CHN_<timestamp>`; self-clean = absent in OV_CHANNEL.
- Deliverables: driver `py/channel_iud.py`, T3 `pageobjects/Configuration/Assets/Transport_Objects/channel_page.resource`,
  suite `tests/Configuration/Assets/Transport_Objects/channel_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
