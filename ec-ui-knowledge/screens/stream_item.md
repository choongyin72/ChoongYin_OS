# Screen: Stream Item

- **Type:** Custom-URL OV (Manage-Object), date-effective (`CLASS_TYPE=OBJECT`/`TIME_SCOPE_CODE=VERSIONED`).
- **BF_CODE:** CD.0008 - **Treeview:** Configuration > Assets > Stream Objects > Stream Item
  (confirmed via EC's own online help page for this screen)
- **DB base/version:** `STREAM_ITEM` / `STREAM_ITEM_VERSION` - Start/End Date live on the BASE table,
  not the version table (checked `USER_TAB_COLUMNS` directly - version table has no START_DATE column)
- **DB view:** `OV_STREAM_ITEM` (key `CODE`)
- **Last verified:** 2026-08-03 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS
  (RF 3/3 pass + Playwright 6/6, DB-verified, self-cleaning) - **Insert + Delete only, Update out of scope**

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Stream Item` -> `label.tv-link` "Stream Item" |
| Navigator GO | `buttongo:form:B` (NON-STANDARD - not the generic `button:form:B`; both driver + T3 use a local wrapper instead of the shared engine's `click_go()`/`Apply Navigator`) |
| Grid | `nav:form:T_data` (custom-URL OV, 14 pages of real pre-existing data on this sandbox) |
| Insert | standard `ec._open_new_object()` (Insert icon -> title-case "New Object"/"New Version" - already correctly cased, NOT a Constant-Standard-style CSS-uppercase illusion) |
| Insert mandatory fields | Stream Item Code (text), Start Date (date, must be late enough - see Quirks), 12 reference DROPDOWNS (not popups - see Quirks), Name (text, mandatory but discarded - see Quirks) |
| Delete | `objectdates` End Date = Start Date, fixed cell id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |

## Quirks
- **The 12 fields the Save-error lists as `[..._POPUP]`-bracketed are ordinary autocomplete
  DROPDOWNS on the live DOM (`dd_input`), not "Pick from EC Object" popups (`pin`).** The error
  message's bracket naming convention is misleading - always confirm field kind via DOM inspection,
  not the error text. Affected fields: Stream Item Category, Product, Field, Company, Stream,
  Measurement Node, Calc. Method, Conversion Method, Master UOM Group, Daily Accrual Method, Monthly
  Accrual Method, Reporting Category. `__FIRST__` on each satisfies Save.
- **Name is server-derived - EC-documented, not a bug.** EC's own online help: *"When creating a new
  Stream Item object, the Name attribute can be left blank for the system to automatically generate
  the Name... Name of Stream Item Category / Name of Product / Code of Field / [Code of Well /] Code
  of Company."* Confirmed live 3x (including typing Name LAST, immediately before Save) that any
  manually-typed value is discarded and replaced with this derived string. Still fill Name with any
  text - it is mandatory-TO-SAVE even though the value never sticks.
- **UPDATE IS BLOCKED by an unconfigured EC scheduler job - genuine sandbox gap, not a code defect.**
  Any Save on `updateAttributes` fails with EC's own error: *"Cannot run schedule job
  UpdateStreamItem because it has not been configured."* EC's online help documents this as a real
  feature (BF VO.0031 - Daily SI Pending Calculation - a background job that recalculates instantiated
  Stream Items when core attributes change); this sandbox's job simply isn't configured. Reproduced
  live 3x, twice with the owner watching a headed browser directly. **Owner instruction 2026-08-02:
  skip Update, cover Insert + Delete only** for this screen.
- **The navigator GO button has id `buttongo:form:B`, not the generic `button:form:B`** the shared
  engine's `click_go()`/RF's `Apply Navigator` expect. Their fallback (toolbar Refresh) doesn't throw
  an error but ALSO doesn't reliably re-list a just-inserted row on this screen's grid tab - looks like
  "insert failed" in verification when the insert actually succeeded. Both the Python driver and the
  T3 define their own local navigator-GO wrapper (clicks `buttongo:form:B` directly) instead of relying
  on the shared fallback.
- **Start Date must be late enough for the 12 reference dropdowns to have options** - this screen
  qualifies as a "reference-dropdown screen" per [[feedback_child_object_date_must_follow_parent]] (4th
  confirmed instance of this exact bug class). Used `2003-01-01` (matching the framework's
  `TEST_START_DATE_REFDD` constant); the owner's simplified standing recommendation going forward is
  `2020-01-01`. **If a dropdown-select step times out, read the actual failure screenshot before
  assuming a selector/timing bug** - a panel showing "No records found" is unmistakable proof of a
  date-scope issue, not something a longer timeout will ever fix (cost 2 live RF failures here before
  this was caught).
- This screen's earlier park history (2026-07-27, re-attempted 2026-08-02) wrongly assumed a
  Copy-based insert mechanism (same wrong turn as the original Constant Standard investigation) - the
  real Insert path is the standard `ec._open_new_object()` flow, already correctly cased on this
  screen (unlike Constant Standard's CSS-uppercase illusion).

## Automation (code in ec-automation)
- **Playwright:** `py/stream_item_iud.py` (thin driver reusing the shared engine, with 2 local
  wrappers `_insert`/`_close` for the non-standard GO button id). Insert + Delete only.
- **RF:** T3 `pageobjects/Configuration/Assets/Stream_Objects/stream_item_page.resource` + suite
  `tests/Configuration/Assets/Stream_Objects/stream_item_iud.robot` (3 test cases, no update). Reuses
  shared T2 label-driven keywords `Fill OV Field/Date/Dropdown By Label` (`manage_object.resource`).
- **Gate:** `verify_screen.py` -> OVERALL PASS.
