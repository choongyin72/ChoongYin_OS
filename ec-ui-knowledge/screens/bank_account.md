# Screen: Bank Account

- **Type:** OV (EC Object Configuration, date-effective) — Bank family, but with mandatory ref dropdowns
- **Treeview path:** Configuration > Assets > Financial Objects > Bank Account
- **DB view (ground truth):** `OV_BANK_ACCOUNT` (key `CODE`)
- **Last verified:** 2026-07-25 · EC 14.2.4 · local sandbox — RF 4/4 + Playwright ALL PASS (DB-verified)
- **Pattern:** follows `../EC_OBJECT_CONFIG_IUD.md`. Source = `bank_account_page.resource` (T3, verified live).

## Selectors `[from bank_account_page.resource, verified live 2026-07-25]`

| Purpose | Selector |
|---|---|
| Open screen | search `Bank Account` → `label.tv-link` "Bank Account" |
| Grid (rows) | `manage_object_nav_nav:form:T_data` |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) — mandatory set is BIGGER than Bank
| Row | Field | Kind | Mandatory |
|---|---|---|---|
| R0 | Code | text | ✅ |
| R1 | Name | text | ✅ |
| R2 | Start Date | date | ✅ |
| R8 | **Sort Code** | text | ✅ (test value `000000`) |
| R20 | **Bank** | ref dropdown (`:dd`) | ✅ (first option) |
| R21 | **Customer** | ref dropdown (`:dd`) | ✅ (first option) |
| R23 | **Currency** | ref dropdown (`:dd`) | ✅ (first option) |

Ref-dropdown rows were banner/recon-discovered; row indices differ from Bank — **do not assume Bank's layout.**
Dropdowns via `Select First EC Dropdown Option` (RF) / dd `_button` → panel option (Playwright).
Ref dropdowns only offer objects effective at the form Start Date (use Start Date >= seed dates).

### Update tab (`updateAttributes`)
`R0 Code (read-only)`, `R1 Name`. (Test updates Name.)

### Delete (date-close) — `objectdates`
End Date `…R:0:C:3:da_input` = Start Date → row leaves `OV_BANK_ACCOUNT`. Toolbar Delete not used (EC Object).

## Automation (code lives in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Financial_Objects/bank_account_page.resource` +
  suite `tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot` (T2 `manage_object` + `DbVerify.py`). Live 4/4.
- **Playwright:** legacy standalone bundle `screens/.../Financial_Objects/Bank_Account/playwright/ec_iud_bank_account.py` (ALL PASS).
  Could be migrated to the generic `py/ec_object_iud.py` driver (would need dropdown-fill support added to the engine).

## Quirks / difference vs Bank
- **3 mandatory reference dropdowns (Bank/Customer/Currency) + Sort Code** — Bank has none of these. This is the
  main reason Bank Account can't be a pure clone of Bank's driver: the engine needs dropdown handling for it.
