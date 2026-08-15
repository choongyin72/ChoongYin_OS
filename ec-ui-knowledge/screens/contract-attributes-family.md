# Contract Attributes screen family — Sale / Revenue / Transport (generalized, cross-environment)

**Verified 2026-08-09 on TWO independent environments** (CLP ECaaS TEST + this repo's local
sandbox `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`): **Sale Contract Attributes**,
**Revenue Contract Attributes**, and **Transport Contract Attributes** are the SAME underlying JSF
component:

```
com.ec.tran.co.screens/contract_attribute/ACCESS_COLUMN/<SALE_CODE|REVN_CODE|TRAN_CODE>
```

Everything below — grid id, toolbar structure, edit-field ids, the never-before-set mechanism, the
protected-attribute wall, and the unsaved-changes trap — is confirmed byte-for-byte identical
across all three screens and both environments. **This is the general solution**, not a
CLP/Sale-specific one. Reusable Python module:
`workstreams/master-plan/ec-automation/libraries/contract_attribute_helpers.py`
(`set_attribute_value()`, `delete_attribute_value()`, `find_contract_attribute_frame()`,
`AttributeProtectedError`).

## Screen shape
- Nav: Date, Business Unit (`nav:form:G:0:R:1:C:1:dd`), Contract Area (`...C:2:dd`), Contract
  (`...C:3:dd`), GO (`button:form:B`).
- Grid tbody id: **`attribute:form:T_data`**. Each `tr` = one attribute row, `td` 0 = label, `td` 1
  = value. Row order/count is fixed per contract template, NOT per screen type.

## Editing an EXISTING value
Click the row's `td` index 1 — reveals an editable field at a FIXED id regardless of row:
**`version:form:T:0:C1_...`** (id never changes; only the field TYPE does, per the attribute's
data type):
- **Text/numeric**: plain input, id `version:form:T:0:C1_in`.
- **Object-reference** (dropdown): `version:form:T:0:C1_dd_input` + `_dd_button` + `_dd_panel`
  (match option rows by `data-item-label`, substring match is fine).
- **Boolean**: a real **checkbox**, id `version:form:T:0:C1_cb` (`is_checked()`/`.click()` — NOT a
  dropdown, despite the grid showing "Y"/"N" text).

## Setting a NEVER-BEFORE-SET value (no existing version row)
Clicking the cell selects the row but reveals none of the above fields — the mini version panel
shows "No records found" instead. Mechanism:
1. Click the row's `td` index 1 to select it.
2. Toolbar **Insert (+)**: `screenToolbar:form:menuBar`'s child `<a>` at index **2** (icon class
   `ui-icon-insert`, has a submenu). Hover it.
3. Click submenu item **"Attribute Version"** — index **3** in the same list. This creates a new
   version row; the edit field now appears at the same fixed `version:form:T:0:C1_...` id.
   *(Index 4/5 = Dimension / Dimension Attribute Version, usually disabled — not this pattern.)*
4. **PROTECTED ATTRIBUTE CHECK — do this before assuming success:** some attributes are flagged
   protected in the EC config and CANNOT be inserted this way at all. Step 3 instead throws a
   dialog: **"Not allowed to insert protected attributes."** (dismiss via its OK button — the real
   button text is "Ok", mixed case; a case-sensitive XPath `contains(., 'OK')` will silently never
   match it in RF, use Browser library's case-insensitive `text=Ok` instead). This is a genuine
   business rule, not a bug, and it is **queryable in advance — not just discoverable by trial**
   (see "Protection is queryable in advance" below). The helper module raises
   `AttributeProtectedError` here — callers MUST catch and report this, never retry blindly.
5. **Also fill Daytime** — `version:form:T:0:C0_da_input` (date input). MANDATORY for a first-time
   version, easy to miss (not visually flagged "mandatory" the way yellow-cell OV screens are).
   **Skipping it makes Save silently no-op** — no error, but the value never actually persists;
   only caught by a subsequent Refresh throwing an "UNSAVED CHANGES" modal, which proves the earlier
   Save never actually committed anything.
6. Fill the value field (per its type, same as the "existing value" section above), Tab out.
7. Save via toolbar `menuBar` index **0** (title-based xpath `//a[@title="Save [Ctrl+s]" and
   not(contains(@class,"ui-state-disabled"))]` is unreliable on this toolbar — prefer clicking by
   position).
8. Verify by reading the grid row's `td` index 1 text — should show the new value.

## Protection is queryable in advance (2026-08-09 discovery — supersedes "not guessable")
The **Contract Template** screen (`com.ec.tran.co.screens/contract_service_template`) shows, per
template, a Hidden/Edit/Protected column for EACH of Sale/Revenue/Transport for every attribute.
This is backed by table **`TV_CNTR_TEMPLATE_ATTRIBUTE`** — columns `SALE_CODE`/`REVN_CODE`/
`TRAN_CODE` hold exactly `HIDDEN`/`EDIT`/`PROTECTED`, keyed by `TEMPLATE_CODE` + `ATTRIBUTE_NAME`.
A contract's template is `OV_CONTRACT.TEMPLATE_CODE`. So the FULL protection matrix for any
contract, on any of the 3 screens, is one join away — no live UI trial needed:
```sql
SELECT ta.attribute_name, ta.label, ta.sale_code, ta.revn_code, ta.tran_code, ta.sort_order
FROM TV_CNTR_TEMPLATE_ATTRIBUTE ta
JOIN OV_CONTRACT c ON c.template_code = ta.template_code
WHERE c.code = '<contract_code>'
ORDER BY ta.sort_order
```
`SORT_ORDER` also predicts the grid's row order (matches what's rendered live) — so this single
query can drive BOTH "is this attribute protected on screen X" and "what row index is it at",
removing the need to dump the live grid first just to find a row. Verified 2026-08-09: predicted
`DCQ` (Daily Contract Quantity) as the one PROTECTED attribute on Sale for SS1_Contract_A's
`DEFAULT` template (every sibling attribute = EDIT) — confirmed live, dialog appeared exactly as
predicted, no other row triggered it.
Cross-check the actual stored value via **`DV_CONTRACT_ATTRIBUTE`** (`OBJECT_CODE` = contract code,
`ATTRIBUTE_NAME`, value in `ATTRIBUTE_STRING`/`ATTRIBUTE_NUMBER`/`ATTRIBUTE_DATE`, `DAYTIME`/
`END_DATE` = the date-effective version window — this is the same "Daytime" field filled in the
UI). No row in this table for a given attribute = genuinely never-set (matches a blank grid cell).
Note: this table can hold values for attributes no longer present in the CURRENT template
definition (seen live: `TOTAL_CONTRACT_QTY` had a stored value but wasn't in the template's
attribute list at all) — a leftover from an earlier template revision; harmless, just don't be
surprised by it.
**Still use the live UI as the actual write path and the dialog-catch as a safety net** — this SQL
query is for planning/prediction (and for building smarter test data / row-index resolution), not
a replacement for verifying what actually happens when you click Save.

## Deleting a value / restoring never-set state (self-clean)
Mirrors Insert exactly. Select the row (click `td` index 1), hover toolbar **Delete (-)** at
`menuBar` index **6** (has a submenu, same shape as Insert), click submenu **"Attribute Version"**
at index **7**. This item is **disabled** if the row currently has no version to remove (a real
guard, useful for detecting current state) and **enabled** once a version exists. A YES/NO confirm
may appear — click YES. Save via index 0. Verified round-trip (set → delete → blank again) live on
2026-08-09.

## The "unsaved changes" trap
Clicking into a DIFFERENT row while a previous edit is unsaved throws a `confirmationForm` modal:
**"UNSAVED CHANGES — There are unsaved changes in Attribute Version. Do you want to save these
changes?"** — YES / NO buttons, plus a separate **Cancel** button at
`confirmationForm:cancelbtn` (stays on the current screen state without committing or discarding —
useful if you want to keep editing the same row). Click **NO** to cleanly discard just that one
field's edit; confirmed this doesn't affect anything already saved. Safe practice: Save after every
single row edit before moving to the next, to avoid this modal appearing at all.

## Don't assume — verify per contract/screen
- Field TYPE (text/dropdown/checkbox) is a property of the attribute's data type, not the screen —
  don't hardcode which rows are which type; detect live (`_in`/`_cb`/`_dd_button` presence).
- Row ORDER/COUNT is fixed per contract TEMPLATE, not globally — different templates on the same
  screen type can have entirely different attribute sets. Don't hardcode row indices across
  different contracts without re-verifying.
- Whether an attribute is PROTECTED is per attribute-definition and must be discovered live (try
  the Insert, catch the dialog) — never assumed from the attribute's name or apparent purpose.
