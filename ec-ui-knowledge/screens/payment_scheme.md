# Screen: Payment Scheme

- **Type:** OV (EC Object Configuration, date-effective, plain Manage Object — NO navigator)
- **Treeview path:** Configuration > Assets > Financial Objects > Payment Scheme
- **Open via:** menu search
- **DB view (ground truth):** `OV_PAYMENT_SCHEME` (key `CODE`; also `NAME`, `OBJECT_START_DATE`,
  `OBJECT_END_DATE`, plus optional `Comments`/`Description`)
- **Last verified:** 2026-08-28 (backfill session) — 2026-08-22 (live build, PR #420) · local
  sandbox · live I-U-D 5/5 DB-verified both times
- **Pattern:** Bank/State pattern (label-driven, properties-file-driven, T2-consolidated) — see
  `bank.md` for the shared OV pattern this screen follows; this file only records what is
  Payment-Scheme-specific.

## Selectors `[from payment_scheme_page.resource Variables section, PR #420]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (col0 = Code); GO button `button:form:B` confirmed present, count=1 |
| Insert (+) | hover the toolbar Insert menu -> submenu "New Object" (same mechanism as Bank) |
| Save | toolbar Save (enabled after edit) |
| Row filter | `Find Payment Scheme Row By Filter` / `Clear Payment Scheme Row Filter` -> delegate to
  shared T2 `Find/Clear Object Row By Filter` against the grid id above |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |

### New Object form (`objectForm`)
Fields, in order: Code, Name, Start Date, End Date, Comments, Description. Only **Code, Name,
Start Date** carry the mandatory-yellow background (`rgb(252, 249, 192)`) — confirmed live
2026-08-22. Labels are the **generic** "Code"/"Name" (NOT screen-prefixed like State's
"State Code"/"State Name"). No mandatory dropdown on this screen.

### Update tab (`updateAttributes`)
Only **Name** is listed in the update properties file — Code is read-only in `updateAttributes`
and Start Date lives only in `objectdates`, not `updateAttributes` (same pattern as Bank/State).

### Delete (date-close) — `objectdates`
**EC Object delete = set End Date = Start Date -> Save -> GO** (row leaves `OV_PAYMENT_SCHEME`).
Toolbar Delete is not used for EC Objects (same as Bank).

## Quirks
- No navigator section at all — plain OV, unlike OV-GM screens (Area/Well/etc.) that require a
  mandatory navigator pick + GO before the grid loads.
- Field labels are the generic "Code"/"Name", not screen-prefixed — do not assume every OV screen
  prefixes its labels with the screen name (State does; Payment Scheme/Bank/Object List do not).
- `CODE` column is `VARCHAR2(32)` in `OV_PAYMENT_SCHEME` — the fixed test code
  `AUTOTEST_PAYMENT_SCHEME` (23 chars) fits with no shortening needed.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (maintained):** T3
  `ec-automation/pageobjects/Configuration/Assets/Financial_Objects/payment_scheme_page.resource` +
  suite `ec-automation/tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot` (T2
  `manage_object.resource` + T1 `common.resource` + `libraries/DbVerify.py`). Converted to the
  Bank/State pattern in PR #420 (merged 2026-08-22); re-run live 5/5 clean during the 2026-08-28
  documentation backfill.
- **Playwright (legacy reference, waived — not maintained going forward):**
  `ec-automation/screens/Configuration/Assets/Financial_Objects/Payment_Scheme/playwright/ec_iud_payment_scheme.py`,
  from the original 2026-06-11 build. Per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`
  (2026-08-27), a new Playwright driver is not built for Bank-/Area-pattern work — the Universal
  Screen Engine replaces that role.
