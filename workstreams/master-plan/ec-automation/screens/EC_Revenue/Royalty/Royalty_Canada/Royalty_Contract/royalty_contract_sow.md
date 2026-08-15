# SOW - Royalty Contract INSERT+UPDATE-ONLY (EC_Revenue > Royalty > Royalty_Canada)

- **Screen:** Royalty Contract   **BF:** RC.0059   **View:** `OV_ROYALTY_CONTRACT`   **Base:** `ROYALTY_CONTRACT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- **Scope: INSERT -> UPDATE(Name) only. DELETE IS PERMANENTLY OUT OF SCOPE** (owner-confirmed
  2026-08-15, closes Issue #336, same precedent as Production Day Table CO.1033) - Contract Template
  "Royalty Fixed Percentage Canada" causes EC to auto-provision `CNTR_PG_SETUP` child rows with no UI
  path to remove them, so End=Start always fails with EC's own "Child record found..." error. Genuine
  EC product limitation (parent-child relationship), not a bug - see `investigation/ROOT_CAUSE_delete_blocked.md`.
- Test data `AUTOTEST_RC_<timestamp>` (RF suite) / `AUTOTEST_RC_003` (Playwright driver default).
  **Self-clean is impossible by design** - every proof run permanently adds one more residual row,
  accepted per owner decision (same as Production Day Table).
- Deliverables: driver `py/royalty_contract_iud.py`, T3 `pageobjects/EC_Revenue/Royalty/Royalty_Canada/royalty_contract_page.resource`,
  suite `tests/EC_Revenue/Royalty/Royalty_Canada/royalty_contract_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
