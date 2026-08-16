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
