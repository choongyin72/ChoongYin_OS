# Financial Item Template (BF FI.0002) - selector map

**Nav path:** EC Revenue > Financial Item > Financial Item Template
**DB base:** `FINANCIAL_ITEM_TEMPLATE` (column `TEMPLATE_CODE`, not `CODE`)
**Type:** TV, inline-editable grid, physical delete.
**Last verified:** 2026-08-16, local sandbox `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`.

## Grid
Grid tbody id: `templ:form:T_data` (a second grid `templ_row:form:T_data` also exists - not used
by this IUD cycle). Toolbar Insert/Delete flyout text is **"Template"**, NOT "Financial Item
Template" - same "flyout text != screen title" gotcha already seen on Language.

## Insert
1. Toolbar Insert (icon='insert') -> "Template" -> a new blank row appears.
2. **Resolving the new row is a real gotcha**: don't use a plain "find a row with any blank cell"
   check - an EXISTING row's blank optional column (e.g. blank Contract Area) matches that just as
   well, landing edits on the wrong row (confirmed live: new row landed at index 1, not the grid's
   end; a naive check matched index 0 instead). Resolve by requiring BOTH the Code cell AND the
   Name cell empty - that's the genuine signature of the new row.
3. Fill by grid_cell (label): `Financial Item Template Code`, `Financial Item Template Name`,
   `Valid From` (date, DAYTIME column - NOT NULL in DB, mandatory despite not being visually
   flagged). Business Unit/Contract Area/Date navigator fields are optional filters, not mandatory.
4. Save.

## Update
Re-resolve the row by Code (`find_grid_row`, never a remembered index - Save can re-sort rows) ->
edit Name cell -> Save.

## Delete
Select the row (`select_grid_row`) -> toolbar Delete (icon='delete') -> "Template" -> Save. This is
a **physical** row removal (no End Date=Start Date convention - that's OV/OV-GM only).

## See also
- `workstreams/master-plan/ec-automation/screens/EC_Revenue/Financial_Item/Financial_Item_Template/`
- `docs/universal_screen_engine_design.md` section 23 (Phase 4 Pilot 2 - first-ever TV generator, 3 real gaps found here).
