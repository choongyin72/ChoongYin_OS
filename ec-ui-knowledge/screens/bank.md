# Screen: Bank

- **Type:** OV (EC Object Configuration, date-effective)
- **Treeview path:** Configuration > Assets > Financial Objects > Bank
- **Open via:** menu search
- **DB view (ground truth):** `ov_bank` (key `CODE`; also `NAME`, `DESCRIPTION`, `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-07-25 · EC **14.2.4** · local sandbox (`ap-f0a7g341jn6d:8443`) · live I-U-D 7/7 DB-verified
- **Pattern:** follows `../EC_OBJECT_CONFIG_IUD.md` (this file only records what is Bank-specific)

## Selectors `[fresh scan 2026-07-25]`

| Purpose | Selector |
|---|---|
| Open screen | fill `#menu:searchForm:searchTxt` = `Bank` → click `//label[contains(@class,'tv-link') and normalize-space()='Bank']` |
| Grid (rows) | `manage_object_nav_nav:form:T_data` (rows = `tr`; col0 = Code) |
| Row select | `#manage_object_nav_nav:form:T_data span` filtered by code text |
| Insert (+) | hover `//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]` → click submenu `//a[normalize-space()='New Object']` |
| Save | `//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]` |
| GO (reload) | `#button:form:B` |

### New Object form (`objectForm`) — one field per row, input at `…R:<r>:C:1`
Mandatory = yellow `rgb(252,249,192)`. Row→label:
`R0 Code*`, `R1 Name*`, `R2 Start Date*` (date), `R3 End Date` (date), `R4 Description`, `R5 Comments`,
`R6–R13 Address Line 1–8`, `R14 Swift Code`, `R15 Country` (dropdown). (`*` = mandatory)

### Update tab (`updateAttributes`) — Code read-only after create
`R0 Code (ro)`, `R1 Name`, `R2 Description`, `R3 Comments`, `R4–R11 Address 1–8`, `R12 Swift Code`, `R13 Country` (dropdown).

### Delete (date-close) — `objectdates`
Row R0: Start Date `…R:0:C:1:da_input`, **End Date `…R:0:C:3:da_input`** (label 'End Date' at C:2).
**EC Object delete = set End Date = Start Date → Save → GO** (row leaves `ov_bank`). Toolbar Delete is **not used** for EC Objects.

## Quirks
- The menu-search hit is a **`<label class="tv-link">`** on 14.2.4 (was `<span>` on ≤14.1.x) — match either.
- Insert is a **hover-menu**, not a titled button (`span.ui-icon-insert`); a generic `a[title*=New]` finds nothing.
- The `…C:0` label-cell id carries a generated suffix → resolve labels by **prefix** (`[id^="…C:0"]`), not exact `getElementById`.

## Automation
- Engine: `../lib/ec_object_iud.py` · DB verify: `../lib/ec_db_verify.py` · driver: `bank_iud.py`
- Run: `EC_HEADED=1 py -X utf8 ec-ui-knowledge/screens/bank_iud.py` → 7/7 PASS (grid + `ov_bank`), self-clean 0 residual.
- Evidence: `tmp/bank_iud/evidence/bank_0[1-5]_*.png`
