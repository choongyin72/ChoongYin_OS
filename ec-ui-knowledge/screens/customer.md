# Screen: Customer

- **Type:** OV (EC Object Configuration, date-effective), Bank pattern, no navigator.
- **Treeview path:** Configuration > Assets > Commercial Objects > Customer
- **Open via:** menu search (same mechanic as Bank)
- **DB view (ground truth):** `OV_CUSTOMER` (key `CODE`; also `NAME`, `DESCRIPTION`,
  `ERP_CUSTOMER_CODE`, `OFFICIAL_NAME`, `CUSTOMER_GROUP`, object start/end date)
- **Last verified:** 2026-08-28 · EC **14.2.4** · local sandbox · live I-U-D 5/5 DB-verified
  (RF suite `customer_iud.robot`, re-run for the documentation backfill; original build/conversion
  live-confirmed 2026-08-23, PR #435)
- **Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated). Follows
  `bank_page.resource`'s shape; this file records what is Customer-specific.

## Selectors `[from pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource, Variables section]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | `${OV_MANAGE_OBJECT_TABLE}` → resolves to `manage_object_nav_nav:form:T_data` (shared T2 constant, not re-hardcoded here) |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (row packs Start Date C:1 / End Date label C:2 / End Date input C:3 — same shape as Bank's `${BANK_DEL_ENDDATE}`) |
| Row filter (Find) | `Find Customer Row By Filter` keyword → delegates to shared T2 `Find Object Row By Filter` on `${CUSTOMER_TABLE}` |
| Row filter (Clear) | `Clear Customer Row Filter` keyword → shared T2 `Clear Object Row Filter` |
| Login | `Login To EC Screen` (T1 common.resource) with `CUSTOMER_EC_USER`/`CUSTOMER_EC_PASS` |
| Open screen | `Open EC Screen    Customer` (T1 common.resource) |

### Form field labels (`@{CUSTOMER_FORM_LABELS}`, confirmed live 2026-08-23 — identical mandatory
set on `objectForm` (Insert) AND `updateAttributes` (Update))
`Code`, `Name`, `Description`, `ERP Customer Code`, `Official Name`, `Customer Group`.
Start Date / End Date deliberately excluded from this list — they live only in `objectdates`,
not `updateAttributes`.

### Mandatory-yellow fields (MandatoryCellStyle, confirmed live)
Code, Name, Start Date, ERP Customer Code, Official Name, Customer Group. Description is
optional (included anyway for business-realistic test data, matching Bank's own convention).

### Grid columns
Code / Name / Start Date / End Date (4 columns — Bank convention).

## Quirks
- **Customer Group's real first dropdown option is the literal `Non Group`** — used verbatim in
  `testdata/customer_insert.properties`, NOT the `__FIRST__` sentinel. This is the VAT Code
  round-trip-verify gotcha (Batch 2): `__FIRST__` never resolves to literal display text for the
  TC02 `Verify Object Insert Exists` comparison, which reads the SAME properties file back
  against the live screen.
- Fixed test code `AUTOTEST_CUST` (not a timestamped code) — EC never lets a deleted code be
  reused, so every run must complete TC05 (delete) to keep the code free for the next run.
- No mandatory navigator dropdown — only the universal Date + GO as-at-date bar (0 mandatory nav
  dropdowns, confirmed live 2026-08-23).

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (primary, current):** T3 `ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Commercial_Objects/customer_iud.robot` (T2
  `manage_object.resource` + T1 `common.resource`). Converted to the Bank pattern via PR #435
  (2026-08-23). Live 5/5 both at conversion and at this documentation backfill (2026-08-28).
- **Playwright (legacy, 2026-06-12, permanently waived from rebuild per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H items 4/5):**
  `ec-automation/screens/Configuration/Assets/Commercial_Objects/Customer/playwright/ec_iud_customer.py`.
- **Bundle:** `ec-automation/screens/Configuration/Assets/Commercial_Objects/Customer/` — SOW,
  README, JOURNAL, evidence, CHECKLIST (backfilled 2026-08-28).
