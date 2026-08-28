# Screen: Bank Account

- **Type:** OV (Manage Object, plain Bank-pattern, date-effective) — no mandatory navigator.
  Bank family, but with extra mandatory ref dropdowns; distinct screen from **Bank** (CO.0001,
  the Bank-pattern exemplar) — do not confuse the two.
- **Treeview path:** Configuration > Assets > Financial Objects > Bank Account
- **DB view (ground truth):** `OV_BANK_ACCOUNT` (key `CODE`)
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox — RF live 5/5 (this backfill session,
  see JOURNAL.md); RF suite itself last rebuilt 2026-08-23 (PR #478, Bank-pattern conversion,
  FINAL screen of the 23-screen candidate pool)
- **Pattern:** Bank/Berth's label-driven, properties-file-driven, T2-consolidated pattern.
  Source = `bank_account_page.resource` (T3, verified live 2026-08-23).

## Selectors `[from bank_account_page.resource Variables section, transcribed 2026-08-28]`

| Purpose | Selector |
|---|---|
| Open screen | search `Bank Account` → `label.tv-link` "Bank Account" |
| Grid (rows) | `manage_object_nav_nav:form:T_data` (`${BANK_ACCOUNT_TABLE}` = shared `${OV_MANAGE_OBJECT_TABLE}`) |
| Grid-filter | `Find/Clear Bank Account Row By Filter` -> shared T2 `Find/Clear Object Row By Filter` on the grid's Code column (15 hits confirmed live) |
| Code label (SCREEN-PREFIXED, confirmed live 2026-08-23 — NOT generic "Code" like Bank) | `Bank Account Code` (`${BANK_ACCOUNT_CODE_LABEL}`) |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Bank Account Code` |
| Delete End Date field (hardcoded, not label-driven — same row-packing rationale as Bank's `${BANK_DEL_ENDDATE}`: Start Date sits at C:1, End Date LABEL at C:2, End Date INPUT at C:3) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (`${BANK_ACCOUNT_DEL_ENDDATE}`) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

## Mandatory / yellow fields
Confirmed live 2026-08-23 via a fresh objectForm/updateAttributes ECCell label dump (30 fields):
- **Insert (`objectForm`):** Bank Account Code, Name, Start Date (static MandatoryCellStyle) +
  **Bank** and **Currency** ref dropdowns (static MandatoryCellStyle). **Sort Code** and
  **Customer** are NOT static-mandatory on a live scan but are kept per the screen's own already-
  proven Playwright driver (conditional-mandatory business rule, invisible to static CSS, only
  surfacing as a save-time banner — Process Train Batch-9 lesson). A live **Vendor** dropdown
  also exists (not in the proven driver, not static-mandatory) — deliberately OMITTED
  (IUD-fill-only-needed-fields).
- Reference dropdowns (Bank/Customer/Currency) filled with `__FIRST__` and deliberately EXCLUDED
  from the round-trip form-label compare `@{BANK_ACCOUNT_FORM_LABELS}` (a resolved reference
  value can re-render different display text after reload — Storage Flow Batch-10 precedent).
  `@{BANK_ACCOUNT_FORM_LABELS}` = `Bank Account Code, Name, Sort Code`.
- **Update (`updateAttributes`):** Bank Account Code is read-only there; Name + Sort Code are the
  2 fields actually changed on Update (mirrors Bank's own Name+Description update pair). Start/End
  Date live only in `objectdates`, not `updateAttributes` — same convention as Bank.

## Test data (fixed, not generated)
Code `AUTOTEST_BACC` (fixed — every run must complete TC05 delete so the code is free for the
next run) | Name `AUTOTEST Bank Account` (+` UPDATED`) | Start=End `2003-01-01` | Sort Code
`000000`/`000001` | Bank/Customer/Currency `__FIRST__`.

## Quirks
- Code label is SCREEN-PREFIXED "Bank Account Code" — Bank Account is the exception, not the
  Bank family's norm.
- 3 mandatory/quasi-mandatory reference dropdowns (Bank/Customer/Currency) + Sort Code — Bank
  itself has none of these; do not assume Bank's field layout carries over.
- Same OV invariants as everywhere: navigator GO after save (N/A here, no navigator), DB as
  ground truth, End=Start true delete.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `pageobjects/Configuration/Assets/Financial_Objects/bank_account_page.resource` (T2
  `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot` (5 TCs: Clean
  State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot`
  -> live 5/5 (this backfill session, 2026-08-28), self-clean 0 residual in `OV_BANK_ACCOUNT`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — Universal Screen Engine replaces this role going
  forward):** `screens/Configuration/Assets/Financial_Objects/Bank_Account/playwright/
  ec_iud_bank_account.py`, kept unchanged since the 2026-06-11 build.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `screens/Configuration/Assets/Financial_Objects/Bank_Account/`.
