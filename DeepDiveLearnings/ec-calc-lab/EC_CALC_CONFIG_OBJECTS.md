# EC Calculation — Configuration → Assets → Calculation Objects (the config vocabulary)

_Deep-dive of the **Calculation Objects** config folder (Calculation Context · Database Object Types · Simple
Object Types · Variable Definitions · Global Attributes). Reference-first: DB ground-truth (ECKERNEL_EC config
tables) + official context descriptions + the equation doc + source. This is the **vocabulary layer** a context
provides BEFORE equations are written — it sits beneath the engine ([[EC_CALC_FRAMEWORK_FROM_SOURCE]]) and the
equation editor ([[EC_EQUATION_SYNTAX]])._

## The big picture
A **Calculation Context** defines a calc domain and its vocabulary: the **Object Types** it works over, the
**Variable Definitions** (dimensioned value holders) equations read/write, and the **Global Attributes** every
equation can use. Equations (in calcs assigned to the context) reference these by name; the context's
read/write **mappings** then bind variables to real DB class.attributes for I/O.

## 1. Calculation Context  (`CALC_CONTEXT`, date-effective)
A named, date-effective calc domain. **14 contexts** (sandbox), grouped by EC module — official descriptions:
| Context | Description |
|---|---|
| **EC_PROD** | Well, sub-surface and production ownership allocations |
| EC_PROD_DC | Production deferment calculations |
| EC_PROD_FC | Forecasted allocation in production |
| **EC_TRAN** | Ownership allocation in transport/processing networks (Transport Dispatching) |
| EC_TRAN_CP | Generation of lifting schedules |
| EC_TRAN_FC | Forecasted allocation in transport/processing networks |
| EC_TRAN_TO | Gross/Net and UOM conversion of load/unload measurements |
| EC_REVN_DD | Due-date calc from contract terms + calendars |
| EC_REVN_FI | Financial Item calculations |
| EC_REVN_LI | Individual invoice line items |
| EC_REVN_TI | Transactional Inventory calculations for revenue |
| EC_REVN_VO | Stream item volumes |
| EC_SALE_PR | Unit price calculations from price indices |
| EC_SALE_SA | Categorisation, penalty & other contract calcs (incl. PSA) |
A calc (`CALCULATION.calc_context_id`) belongs to exactly one context; the context's variables/object types/
global attributes are in scope for its equations. (Matches the per-context I/O in [[EC_CALC_CONTEXT_IO.md]].)

## 2. Object Types  (`CALC_OBJECT_TYPE.CALC_OBJ_TYPE_CATEGORY` = the discriminator)
The **type system** for variable dimensions and iterators. Three categories (sandbox counts):
- **Database Object Types — `DB` (98):** backed by EC's object model / a DB class — the real business entities
  a calc iterates and dimensions over: `ALLOC_NODE`, `ALLOC_STREAM`, `CONTRACT`, `COMPANY`, `LIFTING_ACCOUNT`,
  `PERF_INTERVAL`, `PRODUCTION_DAY`, `PROFIT_CENTRE`, `STORAGE`, `HYDROCARBON_COMPONENT`, … (key `DATA_TYPE`
  usually STRING). The "Database Object Types" screen.
- **Simple Object Types — `SIMPLE` (69):** NOT DB-backed — `LITERAL(...)` string/code identifiers and
  enumerations used as literal dimension keys/classifiers: `LITERAL(ANALYSIS_CODE)`, `LITERAL(EVENT_NO)`,
  `LITERAL(PHASE)`, `LITERAL(INJECTION_TYPE)`, `LITERAL(NUMBER)`, `LITERAL(IDENTIFIER)`, … The "Simple Object
  Types" screen.
- **Predefined (65):** built-in time/system types: `DAY`, `MTH`, `YR`, `SUB_DAY`, `SYSTEM` (product-shipped, not
  user-created).
Object types are referenced as variable dimensions and as iterator domains (`∀ s ∈ streams`).

## 3. Variable Definitions  (`CALC_VARIABLE`, ~1,022 defs)
A **named, typed, dimensioned value holder** that equations read and write. Key columns:
- `NAME` (referenced in equations), `CALC_VAR_DATA_TYPE` (NUMBER/STRING/DATE), `CALC_OBJECT_TYPE_CODE` (the
  value's object type, if it returns an object key), `DEFAULT_PRECISION`, `ACTIVE_IND`.
- **`DIM1..DIM5_OBJECT_TYPE_CODE`** = the dimensions, each typed by an object type. e.g. `CO2_NStdVol` is NUMBER
  dimensioned `[ALLOC_NODE, DAY]` and `[ALLOC_NODE, MTH]`; equations subscript it: `CO2_NStdVol[node, d]`.
- `ALIAS_IND` / `ALIAS_CLASS_NAME` / `ALIAS_SQL_SYNTAX` = optional direct DB binding for the variable.
- Runtime metadata is resolved in **`CALC_VARIABLE_META`** (`CLASS_NAME` + `SQL_SYNTAX` + `ACCESS_MODE` +
  `DATE_HANDLING_PROPS` + `TIME_SCOPE_CODE` + `DATASETS`), and the actual DB I/O binding is the context-level
  **`CALC_VAR_READ_MAPPING`/`WRITE_MAPPING`** (`CLS_NAME` + attribute) — see [[EC_CALC_ARCHITECTURE_TRACE]].
So: a variable = "a number/string/date indexed by these object-type dimensions"; the mapping says where it
lives in the DB; the equation just uses its NAME + subscripts.

## 4. Global Attributes
Product-**predefined** attributes available in EVERY equation via the predefined `global` object (no per-row
config in this sandbox — `CALC_CONTEXT_ATTRIBUTE` is empty; `CALC_CONTEXT_ATTRIBUTE` is where context-specific
extras would be defined, `DEFINED_BY` marking product vs custom). The standard set (from the equation doc
Appendix B): **`Period`, `Method`, `PeriodStartDate`, `PeriodEndDate`, `IncrementStartDate`, `IncrementEndDate`**.
Used like `PeriodStartDate[global]`. For a daily run PeriodStart=IncrementStart; for monthly, Period spans the
month while Increment advances per-day.

## How the pieces connect (config → equation → run)
```
Calculation Context (domain, e.g. EC_PROD)
  ├─ Object Types        : DB entities (ALLOC_NODE, STREAM, CONTRACT...) + Simple literals + Predefined (DAY/MTH...)
  ├─ Variable Definitions: NAME : DATA_TYPE  indexed by [DIMn object types]   (e.g. CO2_NStdVol[ALLOC_NODE,DAY])
  ├─ Global Attributes   : Period / PeriodStartDate / Method / ...  (via `global`)
  └─ Read/Write Mappings : variable  <->  DB class.attribute   (context-level; CLS_NAME + SQL_SYNTAX)
        |
        v
Equations (in a calc assigned to the context) reference variables/objects/globals by name (see EC_EQUATION_SYNTAX)
        |
        v
Engine run: reads inputs via read-mappings -> evaluates equations -> writes outputs via write-mappings (EC_CALC_FRAMEWORK_FROM_SOURCE)
```

## Config tables (ECKERNEL_EC)
`CALC_CONTEXT` (+ `_VERSION`, `_ATTRIBUTE`), `CALC_OBJECT_TYPE` (+ `_META`, `CALC_OBJECT_ATTRIBUTE`,
`CALC_OBJECT_FILTER`), `CALC_VARIABLE` (+ `_LOCAL`, `_META`), `CALC_ATTRIBUTE_META`.

## Further reading (ECpedia / docs — for best-practice depth)
- ECpedia: *Calculation Framework*, *EC Calculation Overview*, *EC Calculation Architecture (Technical)*,
  *EC Concepts - Calculations*, *Calculation Data Model Best Practices* (links in `docs/EC/EC Calculation/ec_calculation.md`).
- Local HTML docs: `docs/EC/EC Calculation/documentation-14.2.5/`. Online-help screens: `01 Calculation Objects` (CO_* codes).
