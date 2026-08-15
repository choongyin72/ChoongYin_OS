---
name: ec-contract-attribute-iud
description: Use when reading, setting, inserting, or deleting values on ANY EC Contract Attribute screen - Sale Contract Attributes, Revenue Contract Attributes, or Transport Contract Attributes (all three are the SAME underlying screen). Covers the never-before-set-attribute mechanism, protected-attribute detection (queryable in advance via SQL), and both a Playwright module and a Robot Framework resource, live-verified on two independent EC environments (CLP ECaaS TEST and this repo's local sandbox).
---

# EC Contract Attribute screens - Sale / Revenue / Transport (proven, DB-verified)

Apply this instead of re-discovering the mechanism live. Full narrative + every verification is in
`ec-ui-knowledge/screens/contract-attributes-family.md` - read that if you need the "why" behind
any step below; this file is the fast operational reference.

## 0. All three screens are ONE screen
Sale Contract Attributes, Revenue Contract Attributes, Transport Contract Attributes are the exact
same JSF component: `com.ec.tran.co.screens/contract_attribute/ACCESS_COLUMN/<SALE_CODE|REVN_CODE|TRAN_CODE>`.
Same grid id, same toolbar structure, same edit-field ids - proven byte-for-byte identical across
CLP TEST and the local sandbox. Whatever screen you're asked about, the mechanism below applies.

## 1. Look up the protection/row-index matrix BEFORE touching the UI (SQL-first)
Don't probe live to discover which attributes are editable. Query it:
```sql
SELECT ta.attribute_name, ta.label, ta.sale_code, ta.revn_code, ta.tran_code, ta.sort_order
FROM TV_CNTR_TEMPLATE_ATTRIBUTE ta
JOIN OV_CONTRACT c ON c.template_code = ta.template_code
WHERE c.code = '<contract_code>'
ORDER BY ta.sort_order
```
`SALE_CODE`/`REVN_CODE`/`TRAN_CODE` = `HIDDEN`/`EDIT`/`PROTECTED` per screen. `SORT_ORDER` predicts
the live grid's row order. Cross-check actual stored values via `DV_CONTRACT_ATTRIBUTE`
(`OBJECT_CODE`=contract code, `ATTRIBUTE_NAME`, value in `ATTRIBUTE_STRING`/`_NUMBER`/`_DATE`,
`DAYTIME`/`END_DATE`=the date-effective window) - no row there = genuinely never-set. This SQL is
for planning only; still verify live via the actual Save + a DB re-read, never trust the query alone
as proof of a write.

## 2. The live UI mechanism
- Grid tbody id: `attribute:form:T_data`. `td` 0 = label, `td` 1 = value.
- **Existing value**: click `td` index 1 -> edit field appears at the FIXED id
  `version:form:T:0:C1_...` (id never changes; only TYPE does): `_in` (text), `_dd_button`/`_dd_panel`
  (dropdown, match by `data-item-label` substring), `_cb` (checkbox - real checkbox element, not a
  dropdown despite showing Y/N text).
- **Never-before-set value**: clicking the cell selects it but shows NO edit field (mini panel says
  "No records found"). Fix: toolbar Insert(+) = `screenToolbar:form:menuBar` child `<a>` index **2**
  (hover) -> submenu "Attribute Version" index **3** (click). NOW the edit field appears at the same
  fixed id. Then **fill Daytime** (`version:form:T:0:C0_da_input`) - skip this and Save silently
  no-ops (no error, but nothing persists; only caught by a later Refresh throwing an unsaved-changes
  modal). Then fill the value, Save.
- **Protected attribute**: Insert throws "Not allowed to insert protected attributes." - dismiss via
  its button (real text is **"Ok"**, mixed case - a case-sensitive match will silently miss it, use
  a case-insensitive selector). This is a real business rule (see section 1), not a bug - never retry.
- **Delete/restore blank**: mirrors Insert - toolbar Delete(-) index **6** (hover) -> submenu
  "Attribute Version" index **7** (click; disabled if no version exists to remove - a real guard).
  Confirm any YES prompt, Save. Verified round-trip (set -> delete -> blank again).
- **Save** = `menuBar` link index **0** (title-based xpath is unreliable on this toolbar - use position).
- **Unsaved-changes trap**: switching rows mid-edit throws a `confirmationForm` modal (YES/NO, plus
  a separate Cancel at `confirmationForm:cancelbtn`). Save after every row to avoid it.

## 3. Reusable code - don't rewrite this, import/call it
- **Playwright**: `workstreams/master-plan/ec-automation/libraries/contract_attribute_helpers.py`
  - `set_attribute_value(page, fr, row_idx, value, daytime=None)`,
  `delete_attribute_value(page, fr, row_idx)`, `find_contract_attribute_frame(page)`,
  `AttributeProtectedError`.
- **Robot Framework**: `workstreams/master-plan/ec-automation/resources/contract_attribute.resource`
  - keywords `Set Contract Attribute Navigator`, `Set Contract Attribute Value`,
  `Delete Contract Attribute Value`, `Contract Attribute Edit Field Kind`,
  `Get Contract Attribute Row Value`/`Label`. Both return/RETURN `PROTECTED` (not an exception in
  RF) when EC refuses the insert - assert on it, don't assume `OK`.
- Live-proof suite (all 3 field types + insert + delete + protected, 5/5 PASS):
  `workstreams/master-plan/ec-automation/tests/contract_attribute_rf_smoketest.robot`.

## 4. Verification discipline (non-negotiable)
- Read the grid cell's `td` index 1 text AFTER Save - never trust the optimistic client state.
- For anything beyond a quick check, also DB-verify via `DV_CONTRACT_ATTRIBUTE` (see section 1).
- Self-clean test data via `delete_attribute_value`/`Delete Contract Attribute Value`, then verify
  blank again - don't leave pre-existing (non-AUTOTEST) contracts modified.
- Never click CREATE CONTRACT / re-run a creation flow to "redo" a state for evidence - flip the
  relevant status field via the correct BASE table (not the view, if a view UPDATE is blocked) and
  screenshot instead.

## 5. Known gaps (say so, don't overclaim)
- Never-before-set + checkbox combined (Insert -> then toggle) is proven in Python (CLP) but not yet
  independently re-run in RF - no naturally blank checkbox has been found in either environment.
- Delete has only been proven on a dropdown-type value; text/checkbox-type deletes are the same
  code path but not independently re-confirmed.
- Scope is the attribute GRID only - Copy Contract, Contract Properties (lock), price objects are
  different screens/mechanisms, not covered here.
