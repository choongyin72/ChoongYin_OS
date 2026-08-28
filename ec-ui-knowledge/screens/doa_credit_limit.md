# Screen: DOA Credit Limit

- **Type:** OV (EC Object Configuration / Manage Object, date-effective), **no navigator** (only
  the universal Date+GO as-at-date bar).
- **Treeview path:** Configuration > Assets > Financial Objects > DOA Credit Limit
- **Open via:** menu search / treeview
- **DB view (ground truth):** `OV_DOA_CREDIT_LIMIT` (key `DOA_CREDIT_LIMIT_CODE`; also
  `DOA_CREDIT_LIMIT_NAME`, `DOA_TYPE`, `CREDIT_LIMIT`, `CURRENCY`, `ROLE_ID`,
  `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 (backfill session) · EC **14.2.4** · local sandbox · live RF 5/5
  DB-verified (RF suite converted 2026-08-23 in PR #443)
- **Pattern:** Bank-pattern (label-driven, properties-file-driven, T2-consolidated) — this file
  records what is DOA-Credit-Limit-specific.

## Selectors `[from doa_credit_limit_page.resource Variables section]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (reused via shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`) |
| Delete date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date input; End Date label at `C:2`) |
| Insert Code | `tab:tabPanel:objectForm:form:G:0:R:0:C:1:in` |
| Insert Name | `tab:tabPanel:objectForm:form:G:0:R:1:C:1:in` |
| Insert Start Date | `tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input` |
| Insert Credit Limit | `tab:tabPanel:objectForm:form:G:0:R:5:C:1:in` (mandatory numeric text) |
| Update Code (read-only guard) | `tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in` |
| Update Name | `tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in` |

## Field labels (live-confirmed 2026-08-23, screen-prefixed — NOT generic)

- `DOA Credit Limit Code` / `DOA Credit Limit Name` — screen-prefixed labels, not the generic
  "Code"/"Name" a plain manage-object screen usually has. Confirmed live, not assumed from Bank's
  convention.
- Grid columns: exactly **4** — Code / Name / Start Date / End Date (confirmed live).

## Mandatory-yellow fields (`MandatoryCellStyle`, confirmed live via raw outerHTML dump)

| Field | Type | Test value used | Notes |
|---|---|---|---|
| DOA Credit Limit Code | text | `AUTOTEST_DOA` | fixed test code (reusable — cleaned up every run) |
| DOA Credit Limit Name | text | `AUTOTEST DOA Credit Limit` | |
| Start Date | date | `2003-01-01` | matches `EC_TEST_START_DATE_REFDD` convention (reference-dropdown date-scope) |
| DOA Type | reference dropdown | `Amount Based` (literal, NOT `__FIRST__`) | first of 2 real options: Amount Based / Quantity Based |
| Credit Limit | numeric text (`ECNumberCell`) | `5000` | |
| Role Name | reference dropdown | `ANALYTICS.REPORTADMIN` (literal, NOT `__FIRST__`) | first of 33 real catalogued options |

## Quirks

- **Currency is a CONDITIONAL-mandatory business rule, invisible to the static
  `MandatoryCellStyle` scan** (its CSS class is `{mandatory:false}`). A live Save without it fails
  with the real EC banner "Amount Based DOA Requires a currency" when DOA Type = Amount Based.
  `Currency=USD` is included in the insert data as a result (a real catalogued option, not the
  dropdown's first option ARS — chosen to match this screen's own pre-existing production rows,
  all of which use USD).
- **Role Name re-renders as its Description on reload**, not the raw code used to select it: after
  any `updateAttributes` reload, the dropdown shows `Report Administrator` instead of the selected
  `ANALYTICS.REPORTADMIN`. A live-DOM round-trip check against the same insert literal would
  always fail here — `Role Name` is deliberately excluded from the live-DOM round-trip form-label
  list (`@{DOA_CREDIT_LIMIT_FORM_LABELS}` in the page object); DB ground-truth (`ROLE_ID` column)
  still independently verifies it. Same re-render gotcha class as Account Mapping's Line Item Type.
  Same deviation-fix precedent as several other Batch-4/5 screens' 2026-08-25 alignment pass
  (registry cites "same deviation class as DOA Credit Limit (PR #503)").
- `DOA Credit Limit Code` is read-only in `updateAttributes` (`MandatoryCellStyleWhite` class) —
  used only as a select-row guard on Update, never edited.
- Start Date/End Date live only in `objectdates`/`objectForm` (Insert-only) — not present in
  `updateAttributes`.

## Automation (code lives in ec-automation — this file is the MD selector reference)

- **RF (current, live-tested):** T3
  `ec-automation/pageobjects/Configuration/Assets/Financial_Objects/doa_credit_limit_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot`
  (T2 `manage_object.resource` + `DbVerify.py`). Test data:
  `ec-automation/testdata/doa_credit_limit_{insert,update,form_verify,grid_verify}.properties`.
  Validated live 5/5 (PR #443, 2026-08-23; re-confirmed 2026-08-28 backfill).
- **Playwright (legacy, 2026-06-11 build, permanently waived from further maintenance per Section H
  of `docs/IUD-DELIVERABLE-CHECKLIST.md`):**
  `ec-automation/screens/Configuration/Assets/Financial_Objects/DOA_Credit_Limit/playwright/ec_iud_doa_credit_limit.py`.
