# SOW - Production Day Table (CO.1033)

## 1. Screen identity
- **BF Code:** CO.1033
- **Treeview path:** Configuration > System > Production Day Table
- **Type:** TV-style inline-editable grid, no navigator (`CLASS_TYPE=OBJECT`, `TIME_SCOPE_CODE=INVARIANT`).
- **DB base table:** `PRODUCTION_DAY_TABLE` (no version table).
- **DB view:** `OV_PRODUCTION_DAY`.

## 2. Scope: INSERT ONLY (owner-confirmed 2026-08-03)
This screen supports Insert only. Update and Delete are **permanently out of scope**:

> "its business process logic flow.... no deletion is allow in Production Day Table screen. such
> feature been disabled. Production Day Table set object end date its not trigger delete record as
> its implementation are different than other objects implementation" - owner, checked live directly.

Confirmed independently before the owner's check: the toolbar Delete icon never enables for ANY row
(tried on 3+ pre-existing real rows, not just test data), and setting End Date = Start Date does NOT
remove a row from `OV_PRODUCTION_DAY` (confirmed via DB - the view has no date-range filter,
consistent with `TIME_SCOPE_CODE=INVARIANT`).

## 3. Self-clean: IMPOSSIBLE BY DESIGN (owner decision 2026-08-03)
Since there is no Delete mechanism, every Insert - including every future live run of the RF suite
or the Playwright driver - permanently accumulates one `AUTOTEST_PDT_<timestamp>` row in
`OV_PRODUCTION_DAY` with no way to remove it via the UI. **Owner decision: accept this as a
permanent, disclosed exception**, matching the precedent set on Royalty Contract's residual
`CNTR_PG_SETUP` rows. As of this build, 8 `AUTOTEST_PDT_*` rows exist permanently in the sandbox from
this investigation + build session. **Run this suite/driver sparingly** - not as part of routine
regression sweeps - since every run adds one more permanent row.

## 4. Insert mechanism
Hover the Insert toolbar icon's own `<li>` -> click the menu item "Production Days" (already
correctly title-cased on this screen - **not** a CSS-uppercase illusion like Constant Standard's
original blocker) -> a blank row appears. Columns (label -> cell id):
- Object Code -> `C0_in` (text, mandatory)
- Time Zone -> `C1_dd_input` (autocomplete dropdown, `__FIRST__` picks the first option)
- Start Date -> `C2_da_input` (date)
- End Date -> `C3_da_input` (date, NOT a delete trigger - see §2)
- Name -> `C4_in` (text; persists exactly as typed, NOT server-derived like Stream Item's Name)
- Default -> `C5_cb` (checkbox, optional)
- 6 more offset/description columns (`C6`-`C12`), all optional for a minimal insert.

## 5. Critical gotcha: cell-fill method matters
Filling `C0_in` (Object Code) via a plain `.fill()`/synthetic-set (this project's
`ec.fill_field()`, designed for object-FORM screens) **silently breaks the NEXT cell's
autocomplete dropdown panel from ever rendering** - confirmed reproducible: with `.fill()` on C0
first, the Time Zone dropdown's `_dd_panel` never appears (times out with 0 options), even though
the panel genuinely has 9 real options when opened without a preceding `.fill()`. Root cause not
further isolated (likely a partial re-render race specific to inline-grid cells), but the fix is
straightforward: use REAL KEYSTROKES + Tab for every cell (this project's own `Type Cell By Id`
convention, already proven on Constant Standard) instead of `ec.fill_field()`. This is the actual
per-screen fix - **not** a case-sensitivity bug like Constant Standard's original blocker.

## 6. DB commit visibility - measured slow (~8s)
This screen's Save commit is NOT immediately visible to a fresh DB session - measured
reproducibly at ~8 seconds (0-5s: not visible; 8s: visible), unlike every other screen built so far
where the commit is instant. The driver/T3 both use a generous 10s wait after Save before any DB
assertion, to avoid a false-negative.

## 7. RF-specific gotcha: `Evaluate JavaScript` argument passing
Passing a value as a TRAILING positional argument to the RF Browser library's `Evaluate JavaScript`
keyword (`Evaluate JavaScript    ${None}    (code) => {...}    ${code}`) does **not** thread the
value into the JS function the way it does in raw Playwright - the parameter arrives as `undefined`
inside the browser, causing every comparison to silently fail. This project's own convention
(confirmed via `allocation_run.resource`/`popup.resource`) is to inline the value via RF's own
`${VARIABLE}` string substitution directly into the JS source (e.g. `const want = '${code}';`), not
as a separate function argument. Cost one full live RF failure round ("No blank row after Insert")
before this was isolated via direct debug scripts.
