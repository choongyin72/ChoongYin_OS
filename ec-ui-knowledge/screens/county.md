# Screen: County

- **Type:** OV (EC Object Configuration, date-effective), Manage Object, **no navigator section**
- **Treeview path:** Configuration > Assets > Basic Objects > County
- **Open via:** menu search
- **DB view (ground truth):** `OV_COUNTY` (key `CODE`; also `NAME`, `DESCRIPTION`, `API_CODE`, `STATE_CODE`)
- **Last verified:** 2026-08-24 (PR #489) · EC **14.2.4** · local sandbox · live I-U-D 5/5 DB-verified
  (re-confirmed 2026-08-28 as part of the lean-deliverable backfill: dryrun 5/5 + full-tree 883/883,
  live 5/5, DB self-clean 0 residual via fresh connection — automation itself unchanged)
- **Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated, pure screen-verify).
  Follows `bank_page.resource`/`bank_iud.robot` shape exactly.

## Selectors `[from county_page.resource Variables section]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (reused from T2's `${OV_MANAGE_OBJECT_TABLE}` constant, no navigator) |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, NOT label-driven — same C:3 shape as Bank; live-confirmed via an insert+delete probe round-trip, 2026-08-23) |
| Insert/Update/Find/Delete gestures | Delegated to shared T2 `resources/manage_object.resource` (`Insert Object From Properties And Verify Code`, `Update Object From Properties`, `Find Object Record`, `Delete Object Via End Date`, `Verify Object *`) — County's T3 only supplies labels/properties paths, no new gesture logic |
| Grid filter | `Find Object Row By Filter` / `Clear Object Row Filter` (shared T2), wrapped as `Find/Clear County Row By Filter` — output.xml confirms 5 hits across Update/Find/Verify-Found/Delete/Verify-Insert-Exists |

### Mandatory-yellow fields (Insert, `objectForm`)
`County Code`* , `County Name`* , `Start Date`* (confirmed live via `MandatoryCellStyle`).
**Screen-prefixed labels** — "County Code"/"County Name", NOT the generic "Code"/"Name" (same pattern
as State/Region). Passed as `code_label=County Code` through every T2 call.

### Non-mandatory fields present but NOT filled (IUD-fill-only-needed-fields convention)
Master System Code/Name (read-only display), Description (filled, non-mandatory but part of test data),
API Code, State dropdown.

### Update tab (`updateAttributes`)
Only County Name / Description — **no date fields at all** on this tab (live-confirmed 2026-08-23);
Start Date exists only on `objectForm` (Insert) and `objectdates` (Delete).

### Delete (date-close) — `objectdates`
Row R0: End Date `…R:0:C:3:da_input` (label 'End Date' at C:2, Start Date at C:1 — same packed-row
shape as Bank). **Delete = set End Date = Start Date → Save** (row leaves `OV_COUNTY`).

## Quirks
- Field labels are screen-prefixed ("County Code"/"County Name"), a live gotcha that differs from
  Bank's generic "Code"/"Name" — do not assume generic labels for this screen.
- `updateAttributes` has no date fields — do not try to screen-verify Start/End Date against that tab.
- **Pure screen-verify convention**: this suite deliberately has NO inline `DbVerify` keyword calls in
  `county_iud.robot` itself (removed in PR #489 to match `bank_iud.robot` exactly, owner decision
  2026-08-18). DB ground-truth for this screen is established via the shared T2 keywords' own
  `DbVerify` usage plus an out-of-suite fresh-connection check, not an in-suite DB read.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (maintained, current):** T3 `ec-automation/pageobjects/Configuration/Assets/Basic_Objects/county_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Basic_Objects/county_iud.robot` (T2 `manage_object.resource`
  + T1 `common.resource`). 5-TC suite (TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete).
  Live 5/5 PASS (PR #429 2026-08-23; PR #489 2026-08-24 alignment fix; re-confirmed 2026-08-28 backfill).
- **Playwright:** ORIGINAL 2026-06-11 reference only (`ec-automation/screens/.../County/playwright/ec_iud_county.py`),
  superseded — no new Playwright work per owner decision 2026-08-27 (Universal Screen Engine replaces this role).
- **Bundle docs:** `ec-automation/screens/Configuration/Assets/Basic_Objects/County/` (SOW/README/JOURNAL/
  evidence/CHECKLIST, backfilled 2026-08-28).
