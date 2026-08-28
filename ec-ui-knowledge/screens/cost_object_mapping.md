# Cost Object Mapping — KB selector map

**Nav path:** Configuration > Assets > Financial Objects > Cost Object Mapping
**DB view:** `OV_FIN_COST_OBJECT`
**Screen type:** Manage Object (OV), plain — no navigator (Bank-pattern, not Area-pattern).
**Delete semantics:** End Date = Start Date (true delete).
**Last verified:** 2026-08-28 (backfill; RF suite last live-run and merged 2026-08-23, PR #442,
Batch 4 of the Bank-pattern conversion project). EC env: local sandbox.

Source: transcribed from `pageobjects/Configuration/Assets/Financial_Objects/
cost_object_mapping_page.resource`'s own Documentation/Variables section — not re-scanned live for
this KB entry, per the backfill work order's "transcribe, don't re-discover" instruction.

## Grid
- Grid id: `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}` —
  not re-hardcoded locally).
- Grid columns: Code, Name, Start Date (3-column, Bank/Account/Country convention).

## Insert (`objectForm`)
Field order: Code, Alternative Code, Name, Start Date, End Date, Description, Object Type, Cost
Object, Line Item Type, Company, Node, Product, Distribution Object Type, Profit Centre.

**Mandatory (confirmed live via `MandatoryCellStyle` on the wrapping `<span>`):** Code, Name, plus
4 reference dropdowns:
- **Object Type** — options: Cost Center / Revenue Order / WBS Element.
- **Cost Object** — CASCADE dropdown; empty ("Dependent field 'Start Date' is empty" banner) until
  BOTH Start Date and Object Type are already set. Must be filled AFTER those two in any
  properties file (`PropertiesReader`/`Insert Object From Properties` fill in file order).
- **Company** — literal option `Acme Chemicals` used (avoids other options with internal
  double-spaces).
- **Distribution Object Type** — options: Country / Delivery Point / Field / Process Train / Well.

Line Item Type / Node / Product / Profit Centre exist but are NOT mandatory — omitted from the
insert properties file (IUD fills only needed fields).

All 4 mandatory dropdowns use REAL LITERAL option text on insert, never `__FIRST__` (the VAT Code
round-trip-verify gotcha — `__FIRST__` never resolves back to literal text for the TC02
Verify-Insert-Exists comparison).

## Update (`updateAttributes`)
Only fields that exist there may be listed: Name, Description (mirrors Bank/Customer's Name+
Description update pair). Code is read-only there; Start Date/End Date live only in `objectdates`.

## Delete (`objectdates`)
- Field id: `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (single row, End Date at C:3,
  Start Date at C:1 — same shape as Bank's/Customer's own DEL_ENDDATE row).
- Delete = set End Date = Start Date, Save (true delete from `OV_FIN_COST_OBJECT`).

## Test data used
Fixed test code `AUTOTEST_CMAP` (not per-run timestamped). Start Date/End Date `2003-01-01`.
Object Type=`Cost Center`, Cost Object=`AA` (cascade-populated), Company=`Acme Chemicals`,
Distribution Object Type=`Country`.

## Quirks
- Screen name says "Mapping" but this is a genuine Code/Name manage-object OV, NOT a
  linking-only grid — confirmed by live recon during PR #442 (same conclusion later reached for
  sibling-named screens Account Mapping and Sales Order).
- Insert/update labels are the GENERIC "Code"/"Name" (like Bank), not screen-prefixed (unlike
  Area/Tank's "Area Code"/"Tank Code" convention).
- Cost Object's cascade dependency is the main gotcha: filling it before Start Date + Object Type
  are set yields zero options.
- A legacy (2026-06-11) Playwright driver + investigation/ recon exist in
  `screens/Configuration/Assets/Financial_Objects/Cost_Object_Mapping/` as historical reference,
  predating the 2026-08-23 RF conversion — not the current automation for this screen.

## Equivalent RF files
- T3 page object: `pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource`
- Suite: `tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot`
- Test data: `testdata/cost_object_mapping_{insert,update,form_verify,grid_verify}.properties`
- Bundle: `screens/Configuration/Assets/Financial_Objects/Cost_Object_Mapping/`
