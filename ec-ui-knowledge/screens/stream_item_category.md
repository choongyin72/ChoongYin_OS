# Screen: Stream Item Category

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`);
  plain (optional dropdowns only, none mandatory). Full "Bank pattern" since PR #473 (2026-08-23,
  Batch 10 of the Bank-pattern conversion project): properties-file-driven insert/update/verify +
  explicit grid-filter wiring, T2-consolidated.
- **BF_CODE:** CD.0016 - **Treeview:** Configuration > Assets > Stream_Objects > Stream Item
  Category _(DB treeview JSON)_
- **DB view:** `OV_STREAM_ITEM_CATEGORY` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Distinct from:** "Stream Item Category Split Key" (BF_CODE CD.0042, class `SPLIT_KEY`,
  shared view `OV_SPLIT_KEY`, page object `stream_item_category_split_key_page.resource` under
  `Configuration/Assets/Revenue_Split_Keys/`) - a sibling screen built separately. Always confirm
  the real `_page.resource` file path (grep, excluding `split_key`) before acting on either.
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - dryrun 5/5, LIVE RF 5/5 (first
  attempt, no retry), DB self-clean 0 residual (this backfill's own re-run confirmation, on top
  of PR #473's original live 5/5 at merge time 2026-08-23).

## Selectors `[from PR #473 body + stream_item_category_page.resource Variables section]`
| Purpose | Selector |
|---|---|
| Open | search `Stream Item Category` -> `label.tv-link` "Stream Item Category" |
| Grid | shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`); needs GO to populate (no default rows on open) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | `Find Stream Item Category Row By Filter` / `Clear Stream Item Category Row Filter` (thin T3 wrappers around shared T2 `Find Object Row By Filter` / `Clear Object Row Filter`), wired into Update/Find/Verify-Found/Delete |
| Delete End Date field id | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded per Bank/Berth's own documented precedent - same framework-invariant objectdates row shape) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, GENERIC not screen-prefixed)
**Code*** - **Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory-
yellow-and-empty)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Code` (read-only) - **`Name`** (only field updated). Start Date lives only in objectForm at
Insert time, not present in updateAttributes. Delete: **`End Date`** = Start Date -> true delete,
row leaves `OV_STREAM_ITEM_CATEGORY`.

## Test data
Fixed test code `AUTOTEST_SIC` (moved off the original generated/timestamped-code convention at
PR #473, to match Bank's fixed-code convention). Confirmed free in `OV_STREAM_ITEM_CATEGORY`
before each run; every run completes TC05 (delete) so the code stays free for the next run.

## Automation (code in ec-automation)
- **Playwright:** `py/stream_item_category_iud.py` -> 7/7 at original 2026-07-26 build (update
  Name). Untouched/unrebuilt since - permanently waived per the 2026-08-27 owner decision
  (Universal Screen Engine replaces this role going forward).
- **RF:** T3 `pageobjects/Configuration/Assets/Stream_Objects/stream_item_category_page.resource`
  (**label-driven, NO hardcoded ids** except the documented Delete End Date constant above) +
  suite `tests/.../stream_item_category_iud.robot` -> 5 TCs (clean-state/insert/update/find/
  delete), per-TC login/logout, live 5/5 both at PR #473's merge and at this backfill's
  confirmation re-run.
- **Testdata:** `testdata/stream_item_category_{insert,update,form_verify,grid_verify}.properties`
- **Credentials:** dedicated `STREAM_ITEM_CATEGORY_EC_USER`/`STREAM_ITEM_CATEGORY_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine/shared T2 handles appear/absent/pagination
  with zero screen-specific tuning.
- GENERIC "Code"/"Name" labels (NOT screen-prefixed) - confirmed via direct grep per PR #473's
  Batch 10 shared findings; do not assume a "Stream Item Category ..." prefixed label exists.
- Disambiguation risk is real, not hypothetical: 6 sibling "* Split Key" screens (Product/
  Company/Field/Stream Item Category/Other/Stream Item) share the view `OV_SPLIT_KEY` and can be
  confused with this plain screen by name alone (especially "Stream Item Category Split Key").
  Always confirm the real file path via grep, excluding any `split_key` hit, before touching
  either screen's files.
- 2026-08-25 alignment fix: removed direct `Code Should Be Present In View`/`Field Should Equal
  In View`/`Code Should Be Absent In View` calls from TC02/TC03/TC05 - these violated Bank's
  pure-screen-only verification convention (2026-08-18), the same deviation class as DOA Credit
  Limit (PR #503).
