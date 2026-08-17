# EC Knowledge Base

A small, growing collection of confirmed EC facts and concepts that don't belong to one specific
screen note (see `screens/*.md` for that) and aren't a debugging technique (see
`EC_BUG_TRACE_SOP.md` for that). Every entry here was verified live or via a real DB query before
being written down - nothing speculative. Organized by category; add a new category when a fact
doesn't fit an existing one.

**Rule for this file (per the project's no-trial-error standard):** before guessing at any EC
fact live, check here first. After confirming something new, add it here immediately.

---

## Category: Class config tables (how EC stores screen/field metadata)

Confirmed via real queries 2026-08-16 (investigating Universal Screen Engine open-items #4 gap b):

| Table | What it actually contains |
|---|---|
| `CLASS_REL_CNFG` | Clean, structured class-to-class relationships: `(CLASS_NAME, RELATION_NAME, REF_CLASS_NAME, RELATION_TYPE)`. Filter to `RELATION_TYPE='OBJECT'` for real FK-style dependencies (a field pointing to another class's record). `RELATION_TYPE='CODE_REF'` = simple `EC_CODES` lookup values, not object dependencies. |
| `CLASS_ATTR_PROPERTY_CNFG` | Per-class, per-attribute config properties. Key `PROPERTY_CODE` values: `PopupQueryURL` (which XML query builds a popup's option list - its path names the real EC module, e.g. `/com.ec.revn.sp/query/get_report_reference_popup.xml` = Report Reference), `PopupDependency` (scoping rule, e.g. `RetrieveArg.DATASET=Screen.this.currentRow.TRG_DATASET` = popup search is filtered by the current row's own Dataset field), `PopupReturnColumn`, `LABEL`. |
| `CLASS_DEPENDENCY_CNFG` | **NOT** field-level FK dependencies despite the name - confirmed empty for `COST_MAPPING`. Real content is class inheritance/polymorphism (`DEPENDENCY_TYPE='IMPLEMENTS'`, e.g. `ALLOCATEABLE_OBJECT implements FACILITY`). Don't trust this table for "does screen X depend on screen Y" questions. |

## Category: Field/dropdown behavior (general rules)

- **Never conclude a dropdown is broken/empty from its raw `.input_value()` alone** - always click
  it open and check the real panel options first. A blank displayed value can mean either genuinely
  no valid option, or a value that fails to auto-populate on render but is immediately available
  once opened (confirmed case: Project Data Mapping Setup's Reference field - blank on row-select,
  correct option retrievable and selectable, Save persists it correctly with zero data loss).
- Full technique for tracing a "field can't retrieve data" symptom: `EC_BUG_TRACE_SOP.md` section 9.

## Category: Popup/dialog behavior (general rules)

- **A popup/dialog picker can render mostly or fully BELOW the visible viewport** when triggered
  from a field far down a long insert/update form (confirmed live, Chemical Stream's mandatory
  "From Connection" picker: dialog title bar measured at y=889 on a 1080px-tall viewport). This
  shows up as Playwright reporting the target element "visible, enabled, stable" but "outside of
  the viewport" on every retry.
- **Neither page-level scrolling nor `element.scrollIntoView()` fixes this** - confirmed by direct
  measurement both ways: `window.scrollY` stayed at `0` and the dialog's own bounding box barely
  moved (9px) after a `scrollIntoView({block:'center'})` call. The dialog's position is
  independent of document scroll, unlike what its appearance in the page suggests.
- **The real fix: these are PrimeFaces `.ui-dialog` widgets, draggable via their own**
  **`.ui-dialog-titlebar.ui-draggable-handle` header** - a real mouse down/move/up sequence on the
  title bar repositions the whole dialog, exactly like a human dragging it. Confirmed live,
  reproduced multiple times across different data (different Start Dates): dragging the title bar
  to near the top of the screen makes the dialog's full content reachable by normal
  locator-based clicks - no bigger viewport, no raw-coordinate click hack needed.
- Reusable helper: `ensure_dialog_in_view(page)` in `workstreams/master-plan/ec-automation/py/
  engine.py` - no-ops if the dialog is already comfortably in the top 30% of the viewport, called
  automatically inside the engine's shared `_PopupHandle.pick_by_code()`. Screen-local custom
  popup handlers must call it themselves after the popup opens.

## Category: OV-GM navigator behavior (general rules)

- **Not every OV-GM screen's extra navigator columns are true parent-gated cascade children** -
  some screens (confirmed live, Service) render ALL their nav columns (`nav:form:G:*:R:1:C:1..3`)
  in the DOM upfront, independent of each other, rather than a child only appearing once its parent
  is chosen (contrast with Property, where Date and Business Unit sit in separate groups but are
  still genuinely independent - see the 2026-08-14 fix note in `apply_navigator()`'s docstring).
- **`engine.py`'s `apply_navigator(values=[...])` defaults `levels` to `len(values)`** (fixed
  2026-08-17, round-5 stability test) precisely because of this: on a screen with more nav columns
  than the caller lists, defaulting to a flat `levels=4` used to silently fill the EXTRA columns
  with `__FIRST__` too, even when the caller never asked for them - confirmed live on Service, this
  narrowed a 20-row grid down to 1 unrelated row, making a freshly-inserted object invisible with no
  error. Pass `levels=None` (the default) when mirroring a real hand-written driver that only ever
  touches as many columns as you list in `values`; only pass a higher `levels` explicitly if you
  genuinely intend to also touch further columns.

## Category: Project Data Mapping Setup (SP.0039, class COST_MAPPING)

- Navigator uses a NONSTANDARD scheme: `StandardNavigator:form:G:0:R:<row>:C:<col>:dd/da_input`
  (not the usual `nav:form:...` prefix). Real, visible GO button: `buttongo:form:B` (the hidden
  `StandardNavigator:form:defaultSubmit` is never actually rendered visible - clicking it times out).
- Navigator column layout confirmed live: `C:1`=Daytime(date), `C:3`=Dataset, `C:5`=Reference,
  `C:7`=Data Mapping (row 0); `C:1`=Project, `C:3`=Company, `C:5`=Inventory, `C:7`=Split Key (row 1).
- Dataset dropdown display-name -> code mapping (confirmed live, only 2 options exist):
  - "Monthly Royalty Calculation Test" = `MRC_TEST`
  - "CARE Insitu Mapping Test" = `CARE_INSITU_TEST`
- Real test row usable for read-only demos: `MRC_COST_CAPITAL_TEST` (Dataset=MRC_TEST,
  Reference/`REPORT_REF_CODE`=`MRC_COST_CAPITAL_TEST`, display name "Allowed Costs - Capital Test").
