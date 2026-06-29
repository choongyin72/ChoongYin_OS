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

## 5. Best-practice WHEN / HOW (ECpedia BPR — *Calculation Design* hub, read 2026-06-30)
_This is the practitioner judgment layer — WHEN to create vs reuse, HOW to use each component well —
from the SME-approved BPR best-practice pages (the "Calculation Data Model Best Practices",
"Naming conventions variables", "Naming Conventions Sets and Iterators", "Generic vs specific")._

### 5.1 Variable Definitions — THREE kinds, each with a distinct WHEN
The best-practice page splits variables into three (this is the key clarification over "a variable is a value holder"):
| Kind | WHEN to use | Naming / HOW |
|---|---|---|
| **Database variable** (the *Variable Definitions* screen) | the value must be **read from or written to the DB**. Product ships many; **projects routinely create new ones**. | prefix with extension code + **`r`** (read) or **`w`** (write): `ZXC_rDensity[Stream,Daytime]`, `ZXC_wYieldFactor[Stream,Daytime,Component]`. EC module vars use `EM_r`/`EM_w` etc. |
| **Global variable** | a value to be **shared across equation blocks / levels / libraries**. Declare **as high as possible**. Best-practice flow: **read → assign to global → process on globals → assign back to write var**. | `gn`=global numeric, `gv`=global varchar, `gd`=global date (e.g. `gnNMass`, `gnNStdVol`). |
| **Local variable** | hold an **intermediate result** (sum/avg) **inside ONE equation block** — never passed up/down. | `ln`/`lv`/`ld`/`ls` (local set). Clean up unused ones. |
**Critical HOW rules for Database variables:**
- **Either read OR write per data class — not both.** A var with both read+write mappings to the *same* data class risks cache-integrity bugs; if you must, the two mappings **must point to different classes**. Safest = don't.
- **Consistent dimensions per class.** The engine builds the read WHERE-clause from the *first* variable seen on a class → **all variables on the same class must share the same dimensions in the same order** (always `(s,d,c)`, never a mix; always `OBJECT_ID`, never sometimes `OBJECT_CODE`).
- **Consistent Validity Period Type per class** — mixing period types on one class **doubles** the read time.
- **Process on date-dimensionless globals** (read into `gnInitialNStdVol(s)`, compute, then a library maps globals → day/month-indexed write vars) → same logic reused for sub-daily/daily/monthly.
- **Engine is dynamically typed** — a var's type (num/string/date) is fixed at **first assignment**, not by the definition. (So the `CALC_VAR_DATA_TYPE` column is the definition hint; runtime is dynamic.)
- **Honor-the-agreement** > technical elegance: for commercial calcs, name vars after the contract's own terms even if less efficient (transparency / no dispute), accepting it may block standard library reuse.

### 5.2 Database Object Types — WHEN/HOW (via sets + iterators)
You rarely "use" an object type directly; you **iterate a SET of its members** with a standard **iterator**:
- **Build sets, don't hardcode objects.** Base set at calc root = `<Object>All` (e.g. `StreamsAll`, `NodesDB`); derive subsets with set operators (`StreamsGas`, `StreamsMeasured`, `WellNodes`). Make a set **only if used ≥2 times**.
- **Standard iterator abbreviations (2–4 char, lowercase, used for BOTH set names and iterators):** `s`=Streams, `n`=Nodes, `c`=Hydrocarbon Components, `pc`=Profit Centres, `cntr`=Contracts, `acc`=Contract Account, `dp`=Delivery Point, `np`=Nomination Points, `stor`=Storages, `la`=Lifting Account, `pint`=Perf Interval, `p`=Phase, `prod`=Products… Reserve `d`/`m`/`h` for **date iterators only — never define a set `d`** (use `DaysInPeriod`/`DaysToIterate`/`Month`).
- **Which set type:** prefer the simpler **Object-Type set combinations** over a set *equation* (easier to read); only use an equation for complex sets.
- **Performance:** add **object-specific local sets** to avoid iterating huge sets with a condition; use **`args(...)`** to build **dynamic sets** of only the objects that actually have data (e.g. `lsProfitCentresUsed = args(gnNMass(s, pc in *), pc)`) — but only after the data is read.

### 5.3 Simple Object Types — WHEN
Use a **`LITERAL(...)`** simple type when the dimension key is **not a persisted EC entity** but a code/enum/classifier (phase, analysis code, offset, identifier). It gives you a non-DB dimension to index a variable by without standing up a DB class.

### 5.4 Global Attributes — WHEN/HOW
The product-predefined globals (`Period`, `Method`, `PeriodStartDate/EndDate`, `IncrementStartDate/EndDate`) drive **period/run context**. Best-practice usage shows up in the date sets: `DaysInPeriod` (1 day if daily, all days if monthly), `DaysToIterate` (1 day unless monthly `LOOP_DAYS`), `Month = toMonth(PeriodStartDate(global))`. So `Method` + `Period*` globals are what let ONE calc serve daily and monthly runs.

### 5.5 The data-model rule that governs read/write mappings (the "create new vs reuse" answer)
This was my biggest gap; the **Calculation Data Model Best Practices** page answers it directly:
- **NEVER read/write screen classes directly** → severe performance hits. Bind variables to **dedicated allocation classes**: reads from **`_DATA`** classes (DB-view-based, read-only — `PWEL_DAY_DATA`, `STRM_DAY_STREAM_DATA`), writes to **`_ALLOC`** classes (own write tables — `PWEL_DAY_ALLOC`, `STRM_DAY_ALLOC`).
- **Decision ladder (both read & write): reuse → extend → create new.**
  1. **Reuse** an existing `_DATA`/`_ALLOC` class for existing attributes.
  2. **Extend** an existing class via extensions for project-specific attributes — *never create a whole new class just for a new attribute*.
  3. **Create new** only for genuinely new tables: read class = read-only, **based on a DB view**, suffixed `_DATA`; write class = on a **new base table**, suffixed `_ALLOC`.

## Further reading (ECpedia / docs — for best-practice depth)
- **ECpedia BPR — *Calculation Design* hub** (id 279511052) and its children: *Naming conventions variables* (374866070),
  *Naming Conventions Sets and Iterators* (297107526), *Equation Blocks, Equation standards, and logging* (297107563),
  *Calculation Data Model Best Practices* (337051706), *Object versions in EC calculations* (374800538),
  *Generic vs specific calculations* (374800456), *Library Calculations* set (290881537 + children). **These are the SME-approved practitioner rules.**
- ECpedia EFK: *Calculation Framework*, *EC Calculation Overview* (mostly stubs); HYPAS *EC Calculation Architecture (Technical)*.
- Local HTML docs: `docs/EC/EC Calculation/documentation-14.2.5/`. Online-help screens: `01 Calculation Objects` (CO_* codes).
