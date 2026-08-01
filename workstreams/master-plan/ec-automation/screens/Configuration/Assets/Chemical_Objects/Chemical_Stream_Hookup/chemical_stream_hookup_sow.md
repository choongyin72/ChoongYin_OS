# SOW - Chemical Stream Hookup IUD (Configuration > Assets > Chemical_Objects)

- **Screen:** Chemical Stream Hookup   **BF:** CO.0260   **View:** `OV_CHEM_STRM_HOOKUP`   **Base:** `CHEM_STRM_HOOKUP`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CSH_<timestamp>`; self-clean = absent in OV_CHEM_STRM_HOOKUP.
- Deliverables: driver `py/chemical_stream_hookup_iud.py`, T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_page.resource`,
  suite `tests/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
