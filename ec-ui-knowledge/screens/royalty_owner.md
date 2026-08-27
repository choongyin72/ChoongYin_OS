# Screen: Royalty Owner

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain manage-object, NO navigator (not OV-GM)
- **BF_CODE:** RC.0051 · **Treeview:** Configuration > Assets > Royalty Objects > Royalty Owner
- **DB view:** `OV_ROYALTY_OWNER` (base `COMPANY`/`COMPANY_VERSION`; app `EC_REVN`)
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox — live RF suite 5/5 pass (this
  backfill's own re-run); PR #447 (2026-08-23) originally rebuilt the T3/suite to this pattern

## Selectors `[from screens/Royalty_Owner/royalty_owner_sow.md + royalty_owner_page.resource, confirmed live 2026-08-23 per PR #447]`

| Purpose | Selector |
|---|---|
| Open | search `Royalty Owner` → treeview link, or `Open EC Screen` (T1 common.resource) |
| Grid (rows) | `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`) |
| Insert (+) | hover `span.ui-icon-insert` → click "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | explicit — `Find Object Row By Filter`/`Clear Object Row Filter` (T2), wrapped as `Find/Clear Royalty Owner Row By Filter` in the T3 |

### New Object form (`objectForm`) — 3 mandatory fields, R:C addressed
- `R:0` **Royalty Owner Code*** — `tab:tabPanel:objectForm:form:G:0:R:0:C:1:in`
- `R:1` **Royalty Owner Name*** — `tab:tabPanel:objectForm:form:G:0:R:1:C:1:in`
- `R:2` **Start Date*** (date) — `tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input`

⚠️ **Field labels are screen-prefixed** — "Royalty Owner Code"/"Royalty Owner Name", NOT the
generic "Code"/"Name" that Bank/Object List use. Same convention as State/Calendar/County.
Confirmed live 2026-08-23 via a field-inventory scan of `objectForm`/`updateAttributes` (28
ECCell labels starting at Royalty Owner Code/Royalty Owner Name/Official Name...).

### Update tab (`updateAttributes`) — Code read-only, only Name editable in this suite's scope
- `Royalty Owner Code` (read-only) — `tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in`
- **`Royalty Owner Name`** (editable) — `tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in`
- Start Date/End Date are **NOT present** in `updateAttributes` — Insert-only / objectdates-only
  fields, matching Bank/State/Object List's convention.

### Delete (date-close) — `objectdates`
- **End Date** input — `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (Start Date at
  `R:0:C:1`, End Date label at `R:0:C:2`). Toolbar Delete is DISABLED for this object (date-
  effective master data) — the EC-correct delete is **End Date = Start Date → Save → GO**, which
  produces a TRUE delete (row leaves `OV_ROYALTY_OWNER`, DB-verified).

## Mandatory-yellow fields
Royalty Owner Code, Royalty Owner Name, Start Date (Insert only — all three, `objectForm`).
Update (`updateAttributes`) only exposes Royalty Owner Name as editable within this suite's scope
(Code is read-only post-create).

## Quirks
- Screen-prefixed labels ("Royalty Owner Code"/"Royalty Owner Name") — do not assume the generic
  Bank/Object List "Code"/"Name" labels apply; always confirm live per screen (same lesson as
  State/Calendar).
- Fixed test code `AUTOTEST_ROYALTY_OWNER` used by the RF suite (not per-run generated) — EC keeps
  deleted codes in the base table, so every run MUST complete TC05 (delete) to free the code for
  the next run.
- No navigator/BU-PU cascade — standard Bank-family timing, no lazy-redraw risk.
- Explicit grid-filter wiring (`Find/Clear Royalty Owner Row By Filter`) is present from the
  2026-08-23 rebuild — confirmed firing exactly once per test case (`output.xml` grep for
  `kw name="Find Royalty Owner Row By Filter"` = 5, re-verified 2026-08-28).

## Automation (code in ec-automation — this file is the MD selector reference)
- **RF:** T3 `pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource`
  (label-driven, properties-file-driven, reuses T2 `manage_object.resource` + T1
  `common.resource` as-is — no shared-file edits) + suite
  `tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot` → live 5/5 (2026-08-23 at
  PR #447, re-confirmed 5/5 2026-08-28 for this backfill).
- **Playwright:** pre-existing `screens/Configuration/Assets/Royalty_Objects/Royalty_Owner/playwright/ec_iud_royalty_owner.py`
  (predates the Universal Screen Engine decision; no new Playwright work required going forward
  per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- **Test data:** `testdata/royalty_owner_{insert,update,form_verify,grid_verify}.properties`.
- **DB self-clean check:** `SELECT COUNT(*) FROM OV_ROYALTY_OWNER WHERE CODE =
  'AUTOTEST_ROYALTY_OWNER'` via a fresh `oracledb` connection → 0 after TC05.
- **Full bundle:** `screens/Configuration/Assets/Royalty_Objects/Royalty_Owner/` (SOW, README,
  JOURNAL, CHECKLIST, evidence).
