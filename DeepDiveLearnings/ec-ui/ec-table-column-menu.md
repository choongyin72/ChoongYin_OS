# EC Table Column Menu (the "hamburger") — how to use it

**What it is:** a per-table menu available on **every EC screen whose data is shown in a table layout**
(1st-level grid, 2nd-level/detail grid, any nesting). Hover the mouse over the **first column header**
(e.g. "BF Code" on the Business Function screen) and a small **hamburger icon** appears; clicking it opens
the menu with the 8 items below. It controls **how YOU view/work with that table** (per-user personalisation),
not the underlying data — except **Paste from clipboard**, which can write into the grid.

> Source legend: **[V]** = verified firsthand on the local sandbox (this/earlier sessions).
> **[S]** = source-derived from the EC framework source (`C:\DEV\GIT\ec-application`, read-only) — how it is
> BUILT; still PENDING live confirm (the demo flips [S]->[V]).
> **[C]** = caption-based guess only, not yet confirmed.
> Honesty note: my live automation of the menu itself was unreliable (hover-revealed icon + scrollbar/frozen
> dual-DOM), so several per-item behaviours below are [S]/[C] and flagged for live confirmation on a clean grid.

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
2. **Use scrollbar** — **[S]** Toggles the table between **pager mode** (pagination buttons at the bottom) and
   **scrollbar mode** (a vertical scrollbar inside the grid). The caption is dynamic — "Use scrollbar" when
   paging is on, "Use pager" when it's off. Source: menu item `ups` → `TableScreenlet.togglePager()` flips the
   `pagingEnabled` flag, persists it, and jumps back to the selected row's page. The grid becomes `scrollable`
   when paging is off OR any column is frozen — which is why scrollbar/freeze mode splits the table into a
   frozen + scrollable DOM (the thing that made my headless automation harder).
3. **Freeze columns…** — **[S]** Opens an **overlay panel** with a **spinner**: enter how many left columns to
   freeze (1-based; `0` or the **Clear** button = unfreeze all), **Ok** applies. Frozen columns stay pinned while
   you scroll horizontally (keep BF Code/Name in view while reading far-right cols). Source: `changeFixedColumn()`
   stores the frozen column NAME under personalisation key `FIXED_COLUMN` and resets the DataTable; freezing >0
   forces the grid into scrollable mode (see item 2).
4. **Number of rows/page…** — **[V]** Opens a dialog to set the **page size** (rows shown per page). Increase it
   to load many/all rows on one page (fewer pages to step through). **✅ Live-verified 2026-06-19:** set `100`
   → grid shows up to 100 rows/page; paginator `(1 of 74)` → `(1 of 15)` (~1,471 rows). Pairs with filtering
   for reliable row-finding (filter to narrow, big page size to avoid pagination).
5. **Copy to clipboard** — **[S]** Copies **all rows × visible columns** of the grid to the system clipboard as
   **Excel-friendly TSV** (tab-separated, newline rows, includes header row(s); dates/numbers formatted). Source:
   menu item `ctc` → `onCopyToClipboardClicked()` → `TableScreenletUtils.copyToClipboard()` builds the TSV and runs
   JS `EC.clipboard.copyToClipboard(...)` (modern `navigator.clipboard.writeText`, with IE/legacy + internal-buffer
   fallback). Shows an "_N row(s) copied to clipboard_" message. Works as a **pair with Paste** (item 6).
6. **Paste from clipboard** — **[S]** ⚠️ Reads the clipboard (TSV) and writes the values **INTO the grid cells,
   STAGED IN MEMORY ONLY — it does NOT persist by itself** (a DB write happens only if you then click Save). Source:
   menu item `pfc` → JS `EC.clipboard.pasteToTableScreenlet()` reads the clipboard and posts it via remoteCommand
   `{id}_sendPasteData` (param `clipData`) → `onPasteFromClipboardClicked()` → `TableScreenletUtils.copyFromClipboard()`:
   it validates the header row matches the visible columns, then per row (**only up to the grid's CURRENT row count**
   — extra clipboard rows are ignored) writes each tab value into the cell, **skipping read-only/label cells**, with
   type-aware parsing (date pattern, locale number, dropdown). So it **edits existing rows in place; it does NOT add
   new rows.** Test rule: **observe only, NEVER Save, reload-verify clean** — and prove Copy+Paste together live.
7. **Show and hide columns…** — **[V]** Opens a dialog listing the table's columns with checkboxes; tick/untick
   to choose which are visible. **✅ Live-verified 2026-06-19:** unticking columns (App Space Cntx, URL) removed
   them from the grid (left BF Code / Name / Released). Note: on Business Function the dialog offered **only the
   5 defined columns** — no extra/hidden columns to reveal (so "reveal a hidden column" depends on the screen
   defining more columns than it shows).
8. **Reset personalisation for component** — **[S]** Clears **this screenlet's** per-user personalisation back to
   defaults. Source: menu item `rpc` → `resetPersonalisationForScreenlet()` → `resetPersonalisation()` which calls
   `screenletPersonalisation.clear()` and resets paging + filter to defaults. **Cleared keys:** `FIXED_COLUMN`
   (freeze), `HIDDEN_COLUMNS` (show/hide), `SORTED_COLUMNS`, column widths, paging (rows/page + scrollbar), filter
   state. Does **NOT** touch table DATA, and resets only this component (not the whole screen). **Stored server-side,
   per user, in DB table `CTRL_PERSONALISATION`** (entity `CtrlPersonalisationEntity`: `PRES_KEY` = screen#screenlet,
   `USER_ID` = user — a NULL-user row is the default for everyone, `PRES_CLOB_VALUE` = JSON state). Best run **LAST**
   in the demo — it cleans up all the view tweaks from the other items.

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

## Source-derived automation hooks (the 5 items) — **[S]** (confirm live)
Reverse-engineered 2026-06-20 from `ec-application` (read-only). Component XHTML:
`ec-web/src/main/webapp/resources/screenlet/tableScreenlet.xhtml`; backing bean
`frmw-pf-jsf/.../screenlet/table/TableScreenlet.java` (+ `AbstractTableScreenlet`, util `TableScreenletUtils`).
The menu items are children of the column menu `{screenlet}:form:cm_menu`; the hamburger button is `{screenlet}:form:cm`
(hover-installed via JS `EC.table.installOnHoverMenuHandler`). Leaf ids (full id = `{screenlet-id}:form:cm_menu:{leaf}`):
- **Use scrollbar:** item `ups` → `togglePager()`.
- **Freeze columns:** item `fc` opens overlay `freezePanel` (widgetVar `{uid}_fp_wv`); spinner `fcNum`, Ok `fcNumOk`, Clear `fcNumClear`.
- **Copy to clipboard:** item `ctc` → JS `EC.clipboard.copyToClipboard` (TSV).
- **Paste from clipboard:** item `pfc` → JS `EC.clipboard.pasteToTableScreenlet` → remoteCommand `{id}_sendPasteData` (param `clipData`).
- **Reset personalisation:** item `rpc` → `resetPersonalisationForScreenlet()`; persisted in DB `CTRL_PERSONALISATION`.

## TODO — flip [S]->[V] via the live you-drive / I-capture demo (Business Function)
All 5 remaining items (2,3,5,6,8) are now **[S]** (source-derived). Live-confirm each in the demo: Use scrollbar,
Freeze columns (spinner overlay), **Copy + Paste as a pair** (Paste = observe-only, NEVER Save, reload-verify
clean), Reset personalisation (run last). THEN the GATED decision: convert proven items into reusable RF common
keywords with honest per-keyword confidence (not committed until genuinely confident).

_Created 2026-06-19 (3/8 live). Updated 2026-06-20: items 2,3,5,6,8 reverse-engineered from `ec-application`
source (read-only) -> [S]; pending live confirm. Keep [S] honest until the demo flips them to [V]._
