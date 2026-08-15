# SOW - Financial Item Template (EC_Revenue > Financial Item)

- **Screen:** Financial Item Template   **BF:** FI.0002   **Base:** `FINANCIAL_ITEM_TEMPLATE`
- **Type:** TV (inline-editable grid `templ:form:T_data`), physical delete (no End Date=Start Date
  convention - that's OV/OV-GM only).
- Built via the Universal Screen Engine (`engine.py`), Phase 4 Pilot 2 (2026-08-14) - the first-ever
  TV generator (`gen_tv_iud_bundle.py`). Full narrative + 3 real gaps found/fixed (Insert/Delete
  flyout text is "Template", not the screen title; mandatory Valid From/DAYTIME field; date-in-
  grid-cell wrapper-vs-nested-input gap in `universal_classifier.py`) is in
  `docs/universal_screen_engine_design.md` section 23 - not duplicated here.
- **Mandatory fields** (confirmed live via `Engine.field_inventory()`): Financial Item Template
  Code, Financial Item Template Name, Valid From. Business Unit/Contract Area/Date navigator
  fields are all optional filters - not filled.
- IUD: INSERT -> UPDATE(Name) -> DELETE (physical row removal via toolbar Delete). New-row
  resolution: the blank row after Insert is NOT reliably found by an empty-string substring match
  (an existing row's optional blank column can match first) - resolve by requiring BOTH Code and
  Name cells empty, the real signature of the new row.
- Test data `AUTOTEST_FIT_<NNN>`; self-clean = physically absent from `FINANCIAL_ITEM_TEMPLATE`.
- Deliverables: driver `py/financial_item_template_iud.py`, this SOW, `README.md`, `JOURNAL.md`,
  `evidence/` (fresh 2026-08-16 run, `AUTOTEST_FIT_001`).
