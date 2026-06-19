# EC Table Column Menu (the "hamburger") — how to use it

**What it is:** a per-table menu available on **every EC screen whose data is shown in a table layout**
(1st-level grid, 2nd-level/detail grid, any nesting). Hover the mouse over the **first column header**
(e.g. "BF Code" on the Business Function screen) and a small **hamburger icon** appears; clicking it opens
the menu with the 8 items below. It controls **how YOU view/work with that table** (per-user personalisation),
not the underlying data — except **Paste from clipboard**, which can write into the grid.

> Source legend: **[V]** = verified firsthand on the local sandbox (this/earlier sessions).
> **[C]** = caption-based + standard EC behaviour, **NOT yet live-confirmed by me** — confirm before relying.
> Honesty note: my live automation of the menu itself was unreliable (hover-revealed icon + scrollbar/frozen
> dual-DOM), so several per-item behaviours below are [C] and flagged for live confirmation on a clean grid.

## The 8 menu items
1. **Turn filtering on / off** — **[V]** Adds a **filter row directly under the column headers** — one control
   per column: a **text box** for text columns (BF Code, Name, URL) and a **multi-select dropdown** for
   fixed-value columns (App Space Cntx). Type/pick a value → the table **narrows to matching rows** (great for
   jumping to a row in a big, multi-page table instead of paging). The caption toggles to "Turn filtering off",
   which **removes the filter row and clears active filters** → full list again.
   **✅ Live-verified 2026-06-19 (user-driven demo on Business Function, 74 pages):** ON → filter row appears
   (text boxes + an App Space **funnel** multi-select). `BF Code = CD.0021` → **1 row** (Bank). `Name = Bank`
   → **4 rows** (Bank / Bank Account / Bank Usage / Bank Account Usage) = **partial "contains" match**.
   App Space funnel → tick `EC Sale` → **`(1 of 9)`** (~180 rows). **Multiple column filters AND-combine.**
   "Turn filtering off" → filter row removed, filters cleared, back to **`(1 of 74)`**.
2. **Use scrollbar** — **[C]** Switches the table to a **fixed-height scrollable view** (scroll within the grid)
   instead of/with paging. _Side effect I did observe:_ scrollbar/freeze mode splits the table into frozen +
   scrollable DOM, which is what made headless automation of the grid harder.
3. **Freeze columns…** — **[C]** Opens a dialog to **lock the left N columns** so they stay visible while you
   scroll the table horizontally (keep BF Code/Name in view while reading far-right columns like URL).
4. **Number of rows/page…** — **[V]** Opens a dialog to set the **page size** (rows shown per page). Increase it
   to load many/all rows on one page (fewer pages to step through). **✅ Live-verified 2026-06-19:** set `100`
   → grid shows up to 100 rows/page; paginator `(1 of 74)` → `(1 of 15)` (~1,471 rows). Pairs with filtering
   for reliable row-finding (filter to narrow, big page size to avoid pagination).
5. **Copy to clipboard** — **[C]** Copies the table's data (visible/selected) to the clipboard, e.g. to paste
   into Excel. (Related ECpedia: "How to Import Excel Files".)
6. **Paste from clipboard** — **[C]** ⚠️ Pastes tabular data **from the clipboard INTO the grid** (bulk entry).
   This can **stage/modify data** — in tests/automation, do NOT use it unless intended, and never commit a paste.
7. **Show and hide columns…** — **[V]** Opens a dialog listing the table's columns with checkboxes; tick/untick
   to choose which are visible. **✅ Live-verified 2026-06-19:** unticking columns (App Space Cntx, URL) removed
   them from the grid (left BF Code / Name / Released). Note: on Business Function the dialog offered **only the
   5 defined columns** — no extra/hidden columns to reveal (so "reveal a hidden column" depends on the screen
   defining more columns than it shows).
8. **Reset personalisation for component** — **[V/doc]** Resets **this table's** personalisations (filter state,
   freeze, visible columns, rows-per-page, scrollbar) back to defaults. EC personalisation is **saved per user**
   (DOC-01: "set or reset user defaults"); a screen-level reset also exists under the screen's Settings.

## Verified automation hooks (for later RF/Playwright use) — **[V]**
- Grid body id pattern: `…:T_data` (e.g. `bf:form:T_data`); base `…:T`.
- **Filter toggle:** `{base}:tfo` — an `<a>` hidden until the header is hovered; turning it on renders the filter row.
- **Filter inputs (after filtering on):** text column → `{base}:sfilter{colIndex}_ft_filter`;
  fixed-value column → `{base}:sfilter{colIndex}_cb_filter` (multi-select). Column index = left-to-right (0-based):
  on Business Function — BF Code=0, Name=1, App Space Cntx=2, Released=3, URL=4.
- Prior firsthand use: `pageobjects/…/Validation/validation_overview_pluto_scarborough.resource` (Message column
  multi-select `sfilter3_cb_filter`); `DeepDiveLearnings/deep_dive/PW-04/ec_patterns_guide.md` Pattern 6
  (text filter `sfilter0_ft_filter`).
- ⚠️ Automation caveats: the hamburger is **hover-revealed** (headless hover is flaky → may need a real/headed
  hover, or drive the `:tfo` toggle directly); scrollbar/frozen grids duplicate the DOM (target the right copy);
  filter inputs may need a real keypress/Enter to trigger the PrimeFaces filter AJAX.

## TODO to fully verify (do on a clean, non-scrollbar grid e.g. Bank, headed)
Confirm live the exact behaviour of items 2–7 (currently **[C]**) and capture the dialog ids for Freeze /
Rows-per-page / Show-hide; then promote a reusable `Filter Grid Column By Value` keyword once filtering is
proven end-to-end on a clean grid.

_Created 2026-06-19 during the table-menu deep-dive. Keep [C] items honest until live-confirmed._
