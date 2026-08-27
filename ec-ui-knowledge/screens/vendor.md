# Screen: Vendor

- **Type:** OV (EC Object Configuration, date-effective), plain Bank pattern — **no navigator
  section** (confirmed live 2026-08-23 per PR #439/registry: only the universal Date + GO
  as-at-date bar, no mandatory nav dropdown).
- **Treeview path:** Configuration > Assets > Commercial Objects > Vendor
- **Open via:** `Open EC Screen    Vendor` (T1 `resources/common.resource`, matches `Vendor`
  from the menu-search treeview)
- **DB view (ground truth):** `OV_VENDOR` (key `CODE`; also `NAME`, `DESCRIPTION`,
  `OBJECT_START_DATE`/`OBJECT_END_DATE` via the Delete=End=Start convention)
- **Last verified:** 2026-08-28 (backfill re-run) · originally converted 2026-08-23 (PR #439,
  Batch 4) · local sandbox · live I-U-D 5/5 DB-verified on both dates
- **Pattern:** follows `resources/manage_object.resource` (T2, Bank pattern) — this file
  records what is Vendor-specific.

## Selectors `[from workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | `${OV_MANAGE_OBJECT_TABLE}` (T2's shared constant; T3 does not re-hardcode it) |
| Grid columns shown | Code / Name / Start Date / End Date (Bank convention) |
| Find/filter | `Find Vendor Row By Filter    ${code}` → delegates to T2 `Find Object Row By Filter    ${VENDOR_TABLE}    ${code}` (filters the grid's Code column) |
| Clear filter | `Clear Vendor Row Filter` → T2 `Clear Object Row Filter    ${VENDOR_TABLE}` |
| Insert | `Insert Vendor Record And Save` → T2 `Insert Object From Properties And Verify Code` fed by `testdata/vendor_insert.properties` |
| Update | `Update Vendor Record And Save` → T2 `Update Object From Properties` fed by `testdata/vendor_update.properties` |
| Delete (End Date input) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded — objectdates row packs Start Date at C:1 / End Date label at C:2 / End Date input at C:3, same documented shape as Bank's own `${BANK_DEL_ENDDATE}`) |
| Delete mechanism | End Date = Start Date (true delete) via T2 `Delete Object Via End Date` |
| Find/verify (grid+form) | `Find Vendor Record` / `Verify Vendor Record Found` → T2 `Find Object Record` / `Verify Object Found` |

## Mandatory-yellow fields `[confirmed live 2026-08-23, per PR #439 / registry]`
Identical set on **both** `objectForm` (Insert) and `updateAttributes` (Update) —
`MandatoryCellStyle` confirmed on each:
- Code (text, read-only after create in updateAttributes)
- Name (text)
- Start Date (date — lives only in `objectForm`/`objectdates`, NOT in `updateAttributes`)
- ERP Vendor Code (text)
- Official Name (text)
- Vendor Group (reference dropdown — real first option is the literal string
  `Contract Owner Vendor`; used verbatim for inserts/verification, NOT the `__FIRST__`
  sentinel — the VAT Code round-trip-verify gotcha: `__FIRST__` never resolves to literal
  text for a form-compare assertion)

Optional field used in the suite: **Description** (text) — included as TC03 Update's second
field alongside Name, matching Bank's/Customer's own Name+Description update pair.

`@{VENDOR_FORM_LABELS}` (the round-trip-compare set, from the T3 Variables section):
`Code, Name, Description, ERP Vendor Code, Official Name, Vendor Group`. Start Date is
deliberately excluded — it only exists in `objectdates`, not `updateAttributes`.

## Quirks
- Code/Name labels render as plain generic "Code"/"Name" (NOT screen-prefixed, unlike State
  Lease's "State Lease Code"/"State Lease Name" or Bank Account's "Bank Account Code").
- No mandatory navigator scope — a live scan confirmed `NAV_DD_COUNT=0`; only the universal
  Date + GO as-at-date bar is present. Do not add a navigator fill step for this screen.
- Fixed test code `AUTOTEST_VEND` (not a per-run timestamped code) — every run's TC05 must
  complete the delete so the code stays free for the next run; EC does not allow a deleted
  code to be reused otherwise.
- Grid-filter keyword (`Find Vendor Row By Filter`) confirmed fired via `output.xml` grep — 5
  hits both at original build (2026-08-23) and this backfill's re-run (2026-08-28).

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (authoritative):** T3
  `ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource` +
  suite `ec-automation/tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot` (T2
  `manage_object.resource` + T1 `common.resource` + `libraries/DbVerify.py`). Live 5/5, both
  at original build and this backfill's re-run.
- **Playwright:** an OLDER, pre-conversion reference driver
  (`ec-automation/screens/Configuration/Assets/Commercial_Objects/Vendor/playwright/ec_iud_vendor.py`)
  predates PR #439 and is left untouched — a fresh/refreshed Playwright bundle for this screen
  is permanently waived (owner decision 2026-08-27, `docs/IUD-DELIVERABLE-CHECKLIST.md`
  Section H) since the Universal Screen Engine (`py/engine.py`) replaces that role.
