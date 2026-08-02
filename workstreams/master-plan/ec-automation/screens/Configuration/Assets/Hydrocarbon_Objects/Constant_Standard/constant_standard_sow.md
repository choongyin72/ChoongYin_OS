# SOW - Constant Standard IUD (Configuration > Assets > Hydrocarbon_Objects)

- **Screen:** Constant Standard   **BF:** CO.0102   **View:** `OV_CONSTANT_STANDARD`   **Base:** `CONSTANT_STANDARD`
- **Type:** TV-style inline-editable grid (`cstandard:form:T_data`), but `CLASS_TYPE=OBJECT`/`TIME_SCOPE_CODE=VERSIONED`
  per `class_cnfg` - date-effective underneath the TV-looking grid.
- No navigator. Insert: hover the Insert icon (scoped to its OWN `<li>`) -> click the menu item by its REAL
  title-case DOM text ("Constant Standard" - the visible ALL-CAPS is CSS styling) -> fill the blank row's
  Standard Code / Standard Name / Start Date / **Daytime** (a genuinely separate mandatory field).
- IUD: INSERT -> UPDATE(Name) -> DELETE(End Date = Start Date, set directly in the inline cell - NOT a
  physical toolbar delete). Test data `AUTOTEST_CS_<timestamp>`; self-clean = absent in `OV_CONSTANT_STANDARD`.
- Deliverables: driver `py/constant_standard_iud.py`, T3
  `pageobjects/Configuration/Assets/Hydrocarbon_Objects/constant_standard_page.resource`,
  suite `tests/Configuration/Assets/Hydrocarbon_Objects/constant_standard_iud.robot`, this SOW,
  `VERIFY-REPORT.md` (auto-generated).
