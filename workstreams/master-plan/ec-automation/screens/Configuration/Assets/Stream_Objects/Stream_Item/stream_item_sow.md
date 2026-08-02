# SOW - Stream Item (CD.0008)

## 1. Screen identity
- **BF Code:** CD.0008
- **Treeview path:** Configuration > Assets > Stream Objects > Stream Item (confirmed via EC's own
  online help page: "Business Function Path: Configuration>Assets>Stream Objects>Stream Item").
- **Type:** Custom-URL OV (Manage-Object), date-effective (`CLASS_TYPE=OBJECT`, `TIME_SCOPE_CODE=VERSIONED`).
- **DB base/version:** `STREAM_ITEM` / `STREAM_ITEM_VERSION` (Start/End Date live on the base table,
  not the version table - confirmed via `USER_TAB_COLUMNS`).
- **DB view:** `OV_STREAM_ITEM`.

## 2. Navigator
- Filter navigator (Code / Category / Product / Field / Well / Company / Node) + a GO button with the
  **non-standard id `buttongo:form:B`** (not the generic `button:form:B` the shared engine's
  `click_go()` expects) - the T3 defines its own `Stream Item Apply Navigator` keyword for this.
- Grid id: `nav:form:T_data` (custom-URL OV pattern, confirmed live).

## 3. Insert (New Object form)
Mandatory fields: Stream Item Code, Start Date, and 12 reference fields that resolve as ordinary
**autocomplete dropdowns** (not "Pick from EC Object" popups, despite the Save-error message's
`[..._POPUP]` bracket naming): Stream Item Category, Product, Field, Company, Stream, Measurement
Node, Calc. Method, Conversion Method, Master UOM Group, Daily Accrual Method, Monthly Accrual
Method, Reporting Category. Name is also mandatory-to-Save but is **server-derived** - see §5.

Start Date must be `>= 2020-01-01`-class (used `2003-01-01` here, matching the existing
`TEST_START_DATE_REFDD` constant) - earlier dates leave the reference dropdowns legitimately empty
("No records found"), not a selector bug. See [[feedback_child_object_date_must_follow_parent]].

## 4. Update - OUT OF SCOPE (owner instruction 2026-08-02)
Any Save on `updateAttributes` (even an unrelated field like Description) fails with EC's own error:
*"Cannot run schedule job UpdateStreamItem because it has not been configured. Please configure the
job before you continue."* Confirmed against EC's own online help page for this screen: changing a
Stream Item's core attributes (Calculation Method / Formula / Split Key / Conversion Method) can kick
off a background scheduler job (**BF VO.0031 - Daily SI Pending Calculation**) to recalculate all
instantiated Stream Items affected by the change - this job is not configured/enabled in this sandbox.
Reproduced live 3x (headed, owner-observed) before concluding this is a genuine environment gap, not a
code defect. Insert + Delete are covered; Update is explicitly skipped.

## 5. Name auto-derivation (documented EC behavior, not a bug)
EC's own online help: *"When creating a new Stream Item object, the Name attribute can be left blank
for the system to automatically generate the Name... Name of Stream Item Category / Name of Product /
Code of Field / [Code of Well /] Code of Company."* Confirmed live 3x: any manually-typed Name value is
discarded on Save and replaced with this derived string. The driver/T3 still fill Name (any text) only
because the field is mandatory-to-Save, not because the value persists.

## 6. Delete
Standard EC delete for a `VERSIONED` object: End Date = Start Date (zero-length window), via the
`objectdates` tab's fixed cell id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.

## 7. Known risks / gotchas
- `buttongo:form:B` (not `button:form:B`) - both the driver and the T3 use their own local
  navigator-GO wrapper instead of the shared engine's `click_go()`/`Apply Navigator`.
- The 12 "popup"-looking mandatory fields are genuinely dropdowns; `__FIRST__` picks the first
  available option on each.
- Start Date must be late enough (used `2003-01-01`) for the reference dropdowns to have options.
