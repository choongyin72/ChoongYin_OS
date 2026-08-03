# Screen: Production Day Table

- **Type:** TV-style inline-editable grid, no navigator (`CLASS_TYPE=OBJECT`/`TIME_SCOPE_CODE=INVARIANT`).
- **BF_CODE:** CO.1033 - **Treeview:** Configuration > System > Production Day Table
- **DB base table:** `PRODUCTION_DAY_TABLE` (no version table)
- **DB view:** `OV_PRODUCTION_DAY` (key `CODE`)
- **Last verified:** 2026-08-03 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS
  (RF 1/1 pass + Playwright 5/5) - **Insert only. No Update, no Delete, no self-clean possible.**

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Production Day Table` -> `label.tv-link` "Production Day Table" |
| Grid | `production_day:form:T_data` (no navigator - loads immediately, 28 real rows, 2 pages) |
| Insert | hover `//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]` -> click `.../a[normalize-space(.)='Production Days']` (already correctly title-cased) |
| Blank row lookup | match `input[id^="production_day:form:T:"][id$=":C0_in"]` with value `''` |
| Cell ids | `production_day:form:T:{row}:C0_in` (Object Code) / `C1_dd_input` (Time Zone, dropdown) / `C2_da_input` (Start Date) / `C3_da_input` (End Date - NOT a delete trigger) / `C4_in` (Name) / `C5_cb` (Default) / `C6`-`C12` (offsets/description, optional) |
| Save | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` |

## Quirks (3 distinct root causes found this session - NOT the same as Constant Standard/Stream Item)
- **The Insert menu item's text is already correctly title-cased ("Production Days")** - no CSS
  `text-transform` illusion here, unlike Constant Standard. Insert worked on the very first click
  once the real blocker (below) was found.
- **Filling Object Code via `.fill()`/synthetic-set silently breaks the NEXT cell's dropdown from
  ever rendering.** Confirmed reproducible: fill C0 with `.fill()` first -> Time Zone's `_dd_panel`
  never appears (0 options, times out); skip the `.fill()`, use real keystrokes + Tab instead
  (`Type Cell By Id`), and the SAME panel has 9 real options. Root cause at the DOM level not fully
  isolated, but the fix is exactly this project's own established inline-grid convention - never use
  a form-field-style `.fill()` on an inline grid cell.
- **DELETE DOES NOT EXIST ON THIS SCREEN - permanent business-process decision, owner-confirmed
  live 2026-08-03.** The toolbar Delete icon never enables for ANY row (tested against 3+
  pre-existing real rows, not just test data, via 6+ distinct selection gestures - cell click, td
  click, tr click, edge click, fresh-reload-then-click - none worked). Setting End Date = Start Date
  does NOT remove a row from `OV_PRODUCTION_DAY` either (confirmed via DB - the view has no
  date-range filter, consistent with `TIME_SCOPE_CODE=INVARIANT`). Owner, checked live directly:
  "no deletion is allow in Production Day Table screen... Production Day Table set object end date
  its not trigger delete record as its implementation are different than other objects
  implementation." **Do not attempt to build a Delete path for this screen - there isn't one.**
- **Self-clean is impossible by design.** Every Insert (including every future test run) permanently
  accumulates a row. Owner decision 2026-08-03: accept this as a permanent, disclosed exception (same
  precedent as Royalty Contract's residual `CNTR_PG_SETUP` rows). **Run the RF suite/Playwright
  driver SPARINGLY** - each run adds one more permanent `AUTOTEST_PDT_*` row; 8 exist as of this build.
- **DB commit visibility measured ~8s slower than every other screen built so far.** A direct timed
  test (checking presence at t+0/1/2/3/5/8s after Save) showed the row was not visible to a fresh DB
  session until 8 seconds had passed. Wait generously (10s used here) before any DB assert on this
  screen specifically - shorter waits (tried 1.2s) produce a false-negative "not in view" failure on
  a row that DID persist correctly.
- **RF Browser library's `Evaluate JavaScript` trailing-argument form does not thread values into
  the JS function on this project's setup** - `Evaluate JavaScript ${None} (code) => {...} ${code}`
  silently receives `code=undefined` inside the browser. This project's own convention (see
  `allocation_run.resource`/`popup.resource`) is to inline the value via RF's own `${VARIABLE}`
  string substitution directly into the JS source (`const want = '${code}';`), not as a trailing
  function argument. Caused one full live RF failure ("No blank row after Insert") on a row that
  genuinely existed - isolated via a standalone debug script dumping all grid values.

## Automation (code in ec-automation)
- **Playwright:** `py/production_day_table_iud.py` (bespoke driver, Insert-only; real keystrokes +
  Tab for every cell; 10s post-Save wait for commit-visibility).
- **RF:** T3 `pageobjects/Configuration/System/production_day_table_page.resource` + suite
  `tests/Configuration/System/production_day_table_iud.robot` (1 test case: insert). Reuses shared
  T1 keywords `Type Cell By Id`/`Select First EC Dropdown Option`/`Save` from `table.resource`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.
