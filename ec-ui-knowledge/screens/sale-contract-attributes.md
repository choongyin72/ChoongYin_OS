# Sale Contract Attributes — edit pattern (CLP ULSD)

**See [[contract-attributes-family]] for the GENERALIZED, cross-screen, cross-environment version of
everything below** (also covers Revenue/Transport Contract Attributes, the protected-attribute wall,
and the reusable `contract_attribute_helpers.py` module — verified 2026-08-09). This doc keeps the
CLP-specific attribute-name-to-row-index mapping and the Price Index incident notes.

Screen: `com.ec.tran.co.screens/contract_attribute` (URL contains `contract_attribute`).
Nav: Date / Business Unit (`nav:form:G:0:R:1:C:1:dd`) / Contract Area (`...C:2:dd`) / Contract (`...C:3:dd`) / GO (`button:form:B`).

## The attribute grid
- Grid tbody id: **`attribute:form:T_data`**. Each `tr` = one attribute row, `td` 0 = label, `td` 1 = value.
- Row order is fixed per contract template (same template = same row indices every time). For CT_OIL_SPA
  (ULSD SPA), verified row indices: 6=Premium Barge Delivery, 7=Premium Truck Delivery, 9=Price Index
  (base/MOPS), 11=MR Price Index, 12=MR Applicability, 13=MT-to-BBL conversion Factor, 14=Exchange Rate,
  15=Inner Decimal Precision, 16=Outer Decimal Precision, 17=Final Decimal Precision.
- **Cells are read-only text until clicked.** Click the row's `td` index 1 (the value cell) — this reveals
  an editable field at a FIXED id regardless of which row you clicked: **`version:form:T:0:C1_...`**
  (the id doesn't change per row; only the field TYPE and current value do, based on the attribute's
  data type).

## Field types you'll encounter at `version:form:T:0:C1_...`
- **Text/numeric attribute** (Premium, MT-to-BBL, Exchange Rate, Decimal Precision fields): plain input,
  id `version:form:T:0:C1_in`. Click it, `Ctrl+A`, `Delete`, type new value, `Tab`.
- **Object-reference attribute** (Price Index, MR Price Index — both reference the PRICE_INDEX class):
  dropdown, id `version:form:T:0:C1_dd_input` + `version:form:T:0:C1_dd_button`. Click the `_dd_button`,
  wait, then click the matching row in `version:form:T:0:C1_dd_panel` by `data-item-label` (partial match
  is fine — labels can have unusual dash characters).
- **Boolean attribute** (MR Applicability): a real **checkbox**, id `version:form:T:0:C1_cb`
  (`is_checked()`/`.click()` to toggle — NOT a dropdown despite the grid showing "Y"/"N" text values).
  Corrected 2026-08-09 after live verification; an earlier version of this doc wrongly assumed a dropdown.

## Save + the "unsaved changes" trap
- After editing one row, clicking into a DIFFERENT row while the previous edit is still un-saved throws
  a modal: **"UNSAVED CHANGES — There are unsaved changes in Attribute Version. Do you want to save these
  changes?"** (YES/NO buttons in `confirmationForm`). This blocks all further clicks until dismissed.
- Two safe strategies: (a) click the toolbar Save (`Save [Ctrl+s]`) after EVERY single row edit before
  moving to the next row, or (b) if you actually want to discard a specific edit (e.g. it was a mistake),
  click **NO** on this modal — confirmed to cleanly revert that one field back to its pre-edit value
  without affecting anything else already saved.
- Real incident (2026-08-08): accidentally changed "Price Index" (row 9, the base/MOPS index) to AAOVC00
  when only "MR Price Index" (row 11) should have been touched — the user's Copy Contract prepare form
  had legitimately set base Price Index to TCADI00 for this scenario, don't second-guess it without
  asking. Caught via the unsaved-changes modal before it saved; clicked NO to discard cleanly.

## Never-before-set attribute (no existing version row) — DIFFERENT mechanism
If an attribute has NEVER had a value (no prior DAYTIME/version row — e.g. a blank attribute on a
freshly copy-created contract), clicking its `td` index 1 does **NOT** reveal the `version:form:T:0:C1_...`
edit field. Instead: the row highlights/selects, the right-side mini panel header shows the attribute
name, but the version list shows **"No records found"** and `version:form:T:0:C1_dd_button` /
`_in` do not exist (`count() == 0`).

**Fix — Insert -> Attribute Version:**
1. Click the never-set row's `td` index 1 to select it (same click as above — selects but doesn't open an editor).
2. Hover/click the toolbar **Insert** icon: it's `screenToolbar:form:menuBar`'s child `<a>` at index **2**
   (icon class `ui-icon-insert`, has a submenu — a `ui-icon-triangle-1-s` sibling span). Do NOT confuse
   with index 0 (Save) or index 1 (Refresh).
3. Click the submenu item **"Attribute Version"** — index **3** in the same `menuBar` `<a>` list (text
   `ATTRIBUTE VERSION`, enabled). (Index 4/5 = Dimension / Dimension Attribute Version, usually disabled
   for this attribute grid — not needed here.) This creates a brand-new version row and the edit field
   NOW appears at the same fixed id `version:form:T:0:C1_...` (dropdown or plain input, per data type —
   see field-type section above).
4. **Also fill Daytime** — `version:form:T:0:C0_da_input` (a date-type input, next to the value field,
   same fixed-row pattern). This field is MANDATORY for a first-time version and is easy to miss (it's
   not highlighted/yellow in the way OV "yellow=mandatory" screens are). **If you Save without filling
   it, the Save appears to run with no error, but the grid cell stays blank / the value silently does
   NOT persist** — confirmed via a Refresh producing an "UNSAVED CHANGES" modal (meaning the edit was
   never actually committed) even though Save had been clicked. Fill Daytime with the contract's
   effective start date convention (e.g. `2026-01-01`), Tab out, THEN click Save.
5. Save via the toolbar (`Save [Ctrl+s]` — same `menuBar` index 0 `<a>`, or the title-based xpath
   `//a[@title="Save [Ctrl+s]" and not(contains(@class,"ui-state-disabled"))]` when that title attribute
   is actually present; if the title-based locator returns 0 matches, fall back to clicking `menuBar`
   index 0 directly by position — the title attribute is not always reliably queryable via Playwright on
   this particular toolbar).
6. Verify by reading `attribute:form:T_data` row's `td` index 1 text — should now show the saved value
   (e.g. "Clean Singapore-Hong Kong 30kt MR $/mt" for MR Price Index).

This is the general "first value" mechanism for ANY attribute row that starts blank on this screen —
applies to MR Price Index, MR Applicability, MT-to-BBL Conversion Factor, Exchange Rate, and the three
Decimal Precision rows alike, whenever they've never been set on that particular contract before.

**Confirmed live end-to-end on SIN2000-00 (2026-08-09):** all 6 never-before-set rows (MR Price Index,
MR Applicability, MT-to-BBL, Exchange Rate, Inner/Outer/Final Decimal Precision) succeeded first-try
using this exact sequence (click row -> detect missing `_in`/`_cb`/`_dd_button` -> Insert(idx2)->
Attribute Version(idx3) -> fill Daytime if blank -> fill/toggle the value field -> Save via menuBar
idx0) once the Daytime requirement was known. Before that discovery, 3 separate investigation rounds
were needed (checking `[title]` elements, `screenToolbar:form:menuBar` ids, then the submenu items) —
this doc now has the answer so it should NOT take multiple rounds again.

## Don't assume — verify per contract
Different contracts on the same template can have genuinely different intended base Price Index /
MR Price Index values depending on the test scenario (e.g. SIN2000-00's Full Generic scenario may
deliberately set base Price Index to the MR index for a specific test point). Always ask before
"correcting" a value that looks unusual rather than assuming it's a data-entry mistake.
