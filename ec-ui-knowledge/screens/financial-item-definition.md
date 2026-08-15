# Financial Item Definition (BF FI.0001) - selector map

**Nav path:** EC Revenue > Financial Item > Financial Item Definition
**DB view:** `OV_FINANCIAL_ITEM`   **Base:** `FINANCIAL_ITEM`
**Type:** OV, custom-URL, no navigator, date-effective.
**Last verified:** 2026-08-16, local sandbox `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`.

## Grid
Grid tbody id: `manageObject:form:T_data`. 24+ existing rows (paginates past 20/page - use
`Engine.row_exists()`/`select_row()`, which walk all pages, not a current-page-only check). Cells
render as readonly `<input value="...">`, not `<span>` text - resolve by input value OR text.

## Insert (New Object form)
Mandatory fields, by label (confirmed via `Engine.field_inventory()` on the empty form):
- `Item Code` (text), `Item Name` (text), `Start Date` (date)
- `Item Type` (dropdown) - value used: "Cost"
- `Default Cost Object Type` (dropdown) - value used: "Cost Center"
- `Format Mask` (dropdown) - use `__FIRST__`, exact mask strings don't reliably substring-match
- `Data Fallback Method` (dropdown) - value used: "Overridden-Calculated-Interfaced"

Optional, left blank: Contract Area, Currency/UOM, Comment, Description, Pre-defined Object Link
(Type), Unit Type.

## Update
Row-select -> edit `Item Name` by label -> Save.

## Delete
End Date = Start Date (standard OV date-effective true delete). Toolbar Delete icon is disabled by
design (same convention as Bank) - deletion is via the date-effective close, not a toolbar click.

## See also
- `workstreams/master-plan/ec-automation/screens/EC_Revenue/Financial_Item/Financial_Item_Definition/`
- `docs/universal_screen_engine_design.md` section 23 (Phase 4 Pilot 1 - 3 real engine gaps found here).
