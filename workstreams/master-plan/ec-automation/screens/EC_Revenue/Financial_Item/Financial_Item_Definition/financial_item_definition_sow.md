# SOW - Financial Item Definition (EC_Revenue > Financial Item)

- **Screen:** Financial Item Definition   **BF:** FI.0001   **View:** `OV_FINANCIAL_ITEM`   **Base:** `FINANCIAL_ITEM`
- **Type:** OV, custom-URL (grid `manageObject:form:T_data`), no navigator, date-effective.
- Built via the Universal Screen Engine (`engine.py`), Phase 4 Pilot 1 (2026-08-14) - the first
  genuinely new screen the engine ever built cold. Full narrative + 3 real engine gaps found/fixed
  (extra_fields convention, pagination-awareness, input-vs-span grid-cell rendering) is in
  `docs/universal_screen_engine_design.md` section 23 - not duplicated here.
- **Mandatory Insert fields** (confirmed live via `Engine.field_inventory()`): Item Code, Item
  Name, Start Date, Item Type, Default Cost Object Type, Format Mask, Data Fallback Method. Only
  these are filled - Contract Area/Currency-UOM/Comment/Description/Pre-defined Object Link(Type)/
  Unit Type are all optional and left blank.
- IUD: INSERT -> UPDATE(Item Name) -> DELETE(End=Start, toolbar Delete disabled by design - same
  OV date-effective convention as Bank). Test data `AUTOTEST_FID_<NNN>`; self-clean = absent in
  `OV_FINANCIAL_ITEM`.
- Deliverables: driver `py/financial_item_definition_iud.py`, this SOW, `README.md`, `JOURNAL.md`,
  `evidence/` (fresh 2026-08-16 run, `AUTOTEST_FID_006`).
