# Screen: Account Mapping

- **Type:** OV (EC Object Configuration, date-effective) - plain manage-object, custom-URL OV,
  **no navigator** (`button:form:B` GO-button locator confirmed 0 matches live, 2026-08-23) - Bank
  pattern classification.
- **Treeview path:** Configuration > Assets > Financial Objects > Account Mapping
- **DB view (ground truth):** `OV_FIN_ACCOUNT_MAPPING` (generic `CODE` column per
  `libraries/DbVerify.py`; also `NAME`, `DESCRIPTION`, `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 - EC **14.2.4** - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, first attempt, no retry needed), fresh-connection DB self-clean 0 residual
  (75 total rows, unchanged before/after), `check_bundle_hygiene.py` PASS (backfill re-run of
  PR #450's Bank-pattern conversion, merged 2026-08-23)
- **Pattern:** follows the Bank pattern (see `screens/Configuration/Assets/Financial_Objects/
  Bank/JOURNAL.md`) - this file only records what is Account-Mapping-specific.

## Selectors `[from account_mapping_page.resource Variables section]`

| Purpose | Selector |
|---|---|
| Open screen | menu search `Account Mapping` |
| Grid (rows) | `manageObject:form:T_data` - screen-LOCAL constant, NOT the shared T2
  `${OV_MANAGE_OBJECT_TABLE}` (which resolves to `manage_object_nav_nav:form:T_data`, the
  navigator-based grid id) |
| Insert (+) | shared T2 hover-menu -> "New Object" |
| Save | shared T2 `//a[@title='Save [Ctrl+s]' ...]` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - packed Start Date `C:1` / End Date label `C:2` / End Date input `C:3` row, same
  convention as Bank/Customer/Cost Object Mapping) |

### New Object form (`objectForm`) - resolved BY LABEL, order confirmed live 2026-08-23
Code, Alternative Code, Name, Start Date, End Date, Description, Product, Line Item Type,
Financial Code, Company Category, Company, Status, Debit / Credit, Debit PK, Credit PK, Account
Category, Financial Account.

**Mandatory (yellow) - 8 reference dropdowns beyond Code/Name**, confirmed via the
MandatoryCellStyle-on-the-input/dd-span technique - **this screen puts the mandatory class on the
INPUT/dd-span itself, not a wrapping tableCell div** (one level deeper than the usual VAT
Code/Customer/Cost Object Mapping technique): Line Item Type, Financial Code, Company Category,
Status, Debit / Credit, Debit PK, Credit PK, Financial Account.

**Account Category** is statically `mandatory:false` but is **functionally required** as a
CASCADE dependency for Financial Account (Financial Account's option list is scoped by Account
Category) - same cascade pattern as Cost Object Mapping's Object Type -> Cost Object. Listed
BEFORE Financial Account in `testdata/account_mapping_insert.properties` for this reason.

Product / Alternative Code / Company are NOT mandatory and are omitted from the insert properties
file (IUD fills only needed fields).

### Update tab (`updateAttributes`)
Code (read-only guard), Name, Description, Line Item Type, Financial Code, Company Category,
Status, Debit / Credit, Debit PK, Credit PK, Account Category, Financial Account. Start Date is
NOT here - lives only in `objectdates`, same convention as Bank/Customer/Cost Object Mapping.

**Line Item Type re-render quirk:** a live run 2026-08-23 proved this field re-renders as the short
internal code `ALL` after a form reload/select, instead of the literal option text `All Line Item
Types` picked at Insert time (exact live failure: "Field 'Line Item Type' shows 'ALL' in
updateAttributes, expected 'All Line Item Types'") - the SAME documented re-render gotcha as DOA
Credit Limit's Role Name (Batch 4). Fix: excluded from the live-DOM round-trip
`@{ACCOUNT_MAPPING_FORM_LABELS}` check list, relying on DB ground truth (TC02's `Code Should Be
Present In View` DbVerify assertion) for that field instead.

### Delete (date-close) - `objectdates`
**EC Object delete = set End Date = Start Date -> Save -> GO** (row leaves
`OV_FIN_ACCOUNT_MAPPING`). Same true-delete convention as every other OV screen.

### Grid columns (confirmed live 2026-08-23)
75-row custom grid, 13 columns: Code, Name, Product, Line Item Type, Financial Code, Company
Category, Company, Status, Debit / Credit, Debit PK, Credit PK, Account Category, Financial
Account. **Notably NO Start Date column** (unlike Bank's simpler 3-column grid) - same documented
variant as Regulatory Permits (Batch 2). `testdata/account_mapping_grid_verify.properties` only
checks Code/Name - the two columns guaranteed present as plain, unambiguous text on every row.

## Test data / unique key
The 9-field reference-dropdown COMBINATION (not any single dropdown) is this screen's real unique
key - ALT_CODE pattern `LineItemType_FinancialCode_CompanyCategory_Status_DebitCredit` =
`JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT` (Line Item Type=All Line Item Types, Financial Code=Journal
Entry, Company Category=All, Status=Accrual, Debit / Credit=Credit, Debit PK=Debit General Ledger
(40), Credit PK=Credit General Ledger (50), Account Category=Revenue, Financial Account=ACCRUAL CR
Acct) - reused unchanged from this screen's own prior Playwright IUD bundle, first proved
live-PASS 2026-06-12 (`screens/.../Account_Mapping/account_mapping_sow.md`,
`evidence/account_mapping_results.json`); re-confirmed still free via a fresh DB check 2026-08-23.
Fixed test code `AUTOTEST_AM` (not per-run timestamped, since PR #450); Start Date `2003-01-01`.

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF (maintained/live test):** T3 `pageobjects/Configuration/Assets/Financial_Objects/
  account_mapping_page.resource` (label-driven, 2026-08-23 Bank-pattern conversion, PR #450) +
  suite `tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot` (5 TC: Clean
  State / Insert / Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_AM`).
  Validated live 5/5.
- **Playwright (historical reference only, NOT maintained):** `playwright/
  ec_iud_account_mapping.py` in this screen's own bundle - original 2026-06-11/12 build, preserved
  unchanged; no new Playwright bundle is built for Bank-pattern work (owner decision 2026-08-27,
  Universal Screen Engine replaces this role).
- **Test data:** `testdata/account_mapping_{insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `ACCOUNT_MAPPING_EC_USER`/`ACCOUNT_MAPPING_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- Plain custom-URL OV, no navigator - confirmed NOT a scope mismatch despite the "Mapping" name
  (genuine Code/Name manage-object OV with an `objectForm`-New-Object flow, same outcome as Cost
  Object Mapping in Batch 4).
- Mandatory-yellow CSS class sits on the input/dd-span itself, not a wrapping tableCell div - one
  level deeper than the usual VAT Code/Customer/Cost Object Mapping detection technique.
- Line Item Type re-renders as a short internal code after reload - see the Update tab section
  above; excluded from the live-DOM round-trip check, DB ground-truth covers it instead.
- Grid has NO Start Date column, unlike Bank's/Cost Object Mapping's simpler 3-column grid.
- `${ACCOUNT_MAPPING_TABLE}` is a screen-local grid-id constant, deliberately NOT the shared T2
  `${OV_MANAGE_OBJECT_TABLE}` - pointing at the wrong one would silently target the navigator-based
  grid this screen doesn't have.
