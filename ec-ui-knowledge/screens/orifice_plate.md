# Screen: Orifice Plate

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`),
  plain (no navigator section). **Full Bank-pattern** (converted PR #463, Batch 8, 2026-08-23).
- **BF_CODE:** CO.0089 — **Treeview:** Configuration > Assets > Stream_Objects > Orifice Plate _(DB treeview JSON)_
- **DB view:** `OV_ORIFICE_PLATE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 — EC 14.2.4 — local sandbox — `robot --dryrun` 5/5, live
  `EC_HEADLESS=true robot` 5/5, DB self-clean confirmed via fresh `oracledb` connection.

## Selectors `[from pageobjects/.../orifice_plate_page.resource Variables, 2026-08-28]`
| Purpose | Selector / value |
|---|---|
| Open | search `Orifice Plate` -> `label.tv-link` "Orifice Plate" |
| Grid id | `manage_object_nav_nav:form:T_data` (`${OV_MANAGE_OBJECT_TABLE}`, T2 shared constant) — needs GO to load |
| Delete field (`objectdates`) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" (T1/T2 shared gesture) |
| Save / GO | shared T1/T2 keywords (no screen-specific override) |
| Grid filter | `Find Object Row By Filter` / `Clear Object Row Filter` (T2, `resources/manage_object.resource`),
  wrapped as `Find Orifice Plate Row By Filter` / `Clear Orifice Plate Row Filter` — wired into
  Update / Find / Verify-Found / Delete (NOT Verify-Removed / Does-Not-Exist, matching Bank/Berth). |

### Form field labels — screen-prefixed, resolved BY LABEL (no hardcoded field ids)
`@{ORIFICE_PLATE_FORM_LABELS}` = `Orifice Code`, `Orifice Name` (used by both TC02 insert-verify
and TC04 find-verify).

### New Object form (`objectForm`) — mandatory (yellow when empty)
**Orifice Code*** — **Orifice Name*** — **Start Date*** (date) — plus mandatory extras beyond the
plain Bank shape: **Material** (dropdown), **Diameter [mm]**, **Measurement Temp [°R]**. Other
optional dropdowns are skipped (not mandatory).

### Update (`updateAttributes`) / Delete (`objectdates`)
`Orifice Code` (read-only) — **`Orifice Name`** (mandatory, updatable). Delete: **`End Date`** =
Start Date -> row leaves `OV_ORIFICE_PLATE` (true delete).

## Automation (code in ec-automation)
- **RF T3:** `pageobjects/Configuration/Assets/Stream_Objects/orifice_plate_page.resource` —
  label-driven, NO hardcoded field ids, properties-file-driven insert/update
  (`Insert Object From Properties And Verify Code` / `Update Object From Properties`), explicit
  grid-filter wiring, dedicated credentials `ORIFICE_PLATE_EC_USER`/`ORIFICE_PLATE_EC_PASS`.
- **RF suite:** `tests/Configuration/Assets/Stream_Objects/orifice_plate_iud.robot` — TC01 Verify
  Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete. Fixed test code
  `AUTOTEST_ORIFICE_PLATE`. Live 5/5 (2026-08-23 PR #463; re-confirmed 2026-08-28).
- **Properties:** `testdata/orifice_plate_{insert,update,form_verify,grid_verify}.properties`.
- **Playwright** (pre-existing, out of scope for the RF pattern conversion and this backfill):
  `py/orifice_plate_iud.py` — last known 7/7 (2026-07-26); superseded going forward by the
  Universal Screen Engine per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H.

## Quirks
- Plain OV, no navigator — single implicit Date+GO load via the shared T2 manage-object nav.
- Grid-filter keyword deliberately NOT wired into Verify-Removed/Does-Not-Exist, matching the
  Account/Bank/Berth/State convention (owner, 2026-08-22).
- Mandatory extras beyond Code/Name/Start Date (Material, Diameter [mm], Measurement Temp [°R])
  are screen-specific — do not assume a "similar-looking" plain-OV screen shares this exact set.
