# EC Calculation Framework — from the source code (`frmw-calc`)

_Read directly from EC product source `C:\DEV\GIT\ec-application\frmw-calc` (READ-ONLY), package
`com.ec.frmw.bs.calc`. 232 Java files / ~42k LOC. This is the authoritative "how it really works" SME reference._

## 0. Where the code is
- Module: `C:\DEV\GIT\ec-application\frmw-calc` (Maven; pkg `com.ec.frmw.bs.calc`).
  - `engine` + `engine/calculation` (+ `.../process`) — the **executor**.
  - `mathml` + `mathml/calcnode` — the **equation language** (parser + node tree).
  - `common` + `common/calcvalue` — the **value/data model**.
  - `xls` — the **Excel-workbook** calc type.
  - `src/test/resources/mathml` — sample equations.
- DB-side engine = `ECKERNEL_EC` PL/SQL (3,288 `EC4E_*` object pkgs + 560 CALC/ALLOC bodies). See [[reference_ec_calc_source_code]].

## 1. Execution pipeline (how a calc runs)
`CalcAction` (BusinessAction; maps jobid→calc, sets period/context from `OV_CALCULATION`)
→ **`CalculationAction`** ("main entry point"; inits `EngineParameters`, defaults SIMULATE/LOG_LEVEL/TRANSACTION_MODE/DATASET,
   **splits the date range into per-period sub-transactions**, loops one run per period)
→ `CalculationRunnerImpl` (one **txn + log row** per period; maps result→OK/ERROR, finish log, stats)
→ `CalculationEngineEJB` (`REQUIRES_NEW` JTA txn — **the rollback boundary**; one period = one txn)
→ **`CalculationEngineImpl.run(ctx)`** — the lifecycle, in strict order:
  1. `readCalculation()` — load the calc tree (`CalculationReader`: `OV_CALCULATION`, `OV_CALC_PROCESS_ELEMENT`
     CONNECT-BY recursion, `DV_CALC_EQUATION` CLOBs, transitions, iterations; compiles each equation's MathML).
  2-6. init Object/Set/Variable **metadata + caches** (`ObjectMeta/Cache`, `SetMeta/Cache`, `VariableMeta/Cache`).
  7. compute `PERIOD_START/END` globals. 8. root logger. 9. register referenced variable signatures.
  10. **`calculation.execute(ctx)`** — the actual computation (recursive).
  11. optional `CalculationPreSaveValidator.validate(ctx)` (whitelisted) → `VALIDATION_STATUS`.
  12. **`varCache.write()`** — ONLY if **not SIMULATE** and validation passed (so Simulate = compute + log, no write).
  13. if `LINK_TO_EVENT=Y`: create `TV_CALCULATION_EVENT` + `EVT_TRAN_DATA_CON` rows for touched records.
- Any throwable → log + rollback (`EngineException`).

## 2. PROCESS vs EQUATIONS vs WORKBOOK (`engine/process`)
All implement `ICalculation.execute()` via `CalculationBase` (template: log enter/leave + `eval()`).
Types: `PROCESS | EQUATIONS | WORKBOOK | EXTERNAL_OPTIMISER`; scopes `MAIN | PUBLIC_SUB | PRIVATE_SUB`.
- **EQUATIONS** (`Equations.eval`): ordered `List<Statement>{execOrder, CompiledMathml}`. Walked by an **index loop**
  (`i = ictx.getNextEquationNum()`) so LOOP nodes can jump. CONDITION + ITERATIONS are compiled *into* each
  statement's MathML (evaluated by the interpreter, not the engine loop). `preProcessLoops()` pre-links
  LOOP-START/NEXT/EXIT/CONTINUE to equation indices.
- **PROCESS** (`Process.eval`): a flowchart — `EntryElement` → walk `getNextElement()` chain. A **STEP**
  (`ProcessElement`) recurses into its implementing sub-calc in a **child context**; if it has iterations it loops
  the sub-calc over a set (`NestedProcessElementIterator`, per `groupVersions`). A **DECISION** runs its impl, reads a
  synthetic `DecisionValue` STRING var, and branches via its transition map (`DEFAULT` fallback). ENTRY/EXIT are anchors.
  → **PROCESS orchestrates; the leaf STEPs (EQUATIONS/WORKBOOK) do the math.** (Matches the FLOWCHART tab: Start→Step→Stop.)
- **WORKBOOK** (`Spreadsheet.eval`): runs an Aspose.Cells `.xlsx` over cache adapters (see §5).

## 3. The equation language (`mathml` + `mathml/calcnode`)  ← this cracks the equation editor
An equation = a **MathML doc compiled into a tree of `CalculationNode` objects** (`MathmlInterpreter.buildCalculationTree`).
Each node is one operation; `eval(InterpreterContext)` walks depth-first returning a `CalculationValue`.
Bases: `CalculationNode` (root), `CalculationNodeBase` (generic param list), `FunctionCalcNodeBase` (csymbol fns:
subscripts vs arguments). The editor's "Insert Iterator", functions, etc. are exactly these node types:

| Author types (editor) | MathML | Backing CalcNode |
|---|---|---|
| `+ - * / ^ mod`, `abs floor log ln arctan`, `min max`, `round` | plus/minus/times/divide/power/rem/… | Addition/Subtraction/Multiplication/Division/Power/Mod/Abs/Floor/Logarithm/ArcusTan/MinMax/Round |
| `= <> < <= > >=`, `and or not`, `isValid(x)`, `isZero(x)` | eq/neq/lt/…/and/or/not/isValid/isZero | Compare/And/Or/Not/IsValid/IsZero |
| `var = expr` / `set = expr` / `RESPONSE[..]=` / log msg / LABEL,GOTO | `<eq/>` + `<ci type=...>` | AssignVariable/AssignSet/AssignResponseParam/UserLogMsg/SpecialIdentifier |
| **iterator** `c in S` / iterations (forall) | `<in/>` `<ci type=iterator>` / `<forall>` | **ElementOfCalcNode** / IterationsCalcNode (the "Insert Iterator" dialog!) |
| `sum[i in S](e)`, `argmin/argmax`, `sortAsc/Desc`, `card`, `elementAt` | sum/argmin/…/card/elementAt | Sum/ArgMinMax/Sort/Cardinality/ElementAt |
| `engineParameter(n)`, `lookup(i,v)`, `args(var,it)`, `snapshot`, `expand` | csymbol fns | EngineParameter/Lookup/Args/Snapshot/Expand |
| **`extfn("com.ec...X", v)`** (external Java) | csymbol `extfn` | **ExternalFunctionCalcNode** (reflectively loads `ExternalFunction`, `init`+`execute`) |
| set ops `union intersect setdiff`, relations subset/superset/eq, `{x in S: cond}` | union/intersect/… / `<set><condition>` | Union/Intersect/SetSubtraction/SetCompare/SetFilter (+ Arbitrary{Union,Intersect}) |
| dates `addDays addMonths addSubDays days months years toDay/Month/Year midnight firstOf…` | csymbol date fns | AddDays/AddMonths/AddSubDays/DaysMonthsYears/DateCast/DateTrunc |
| `LOOP-START/NEXT/EXIT/CONTINUE` | `<ci type=loop-identifier>` | Loop{Start,Next,Exit,Continue}CalcNode |
| var/set/iterator/attribute ref, literal/`e` | `<ci type=...>` / `<cn>` / `<exponentiale/>` | Resolve{Variable,Set,Iterator,Attribute} / Constant |

`MathmlInterpreter` grammar map is in its header (lines 29-98); dispatch in `buildApplyOperatorCalcTree` /
`buildCSymbolFunctionCalcTree` / `buildVariableAssignmentTree`. **So to author an equation I build this node tree;
the canvas editor is just a structured front-end for it** — the walk-through now only needs the editor's gestures,
not the grammar (which we have).

## 4. Value & data model (`common/calcvalue`)
- **`CalculationValue` has 3 interchangeable forms** (never Java-cast — convert): `toScalarValue()` / `toSetValue()`
  / `toIterationValue()`. Scalar↔1-element-set interchangeable; iteration only from native iterations.
- Scalars: `RealValue` (→`ECRealNumber`/BigDecimal, scale 15, configurable rounding; 0/0=0, tiny divisor=0),
  `StringValue`, `DateValue` (DAY/MTH/YR/SUB_DAY; SUB_DAY carries S/W DST flag), `BooleanValue` (renders Y/N),
  **`MissingValue`** (= 0 in +/−, **propagates** in ×/÷ — lets sparse sets sum correctly), `NullValue` (validate-mode).
- **Dimensions live on the VARIABLE, not the value** (`CalculationVariable`): N dims each typed by an object type
  (= DIM1..DIM5); value store = nested `Map` tree keyed by per-dim index strings → leaf `CalculationValue`. A
  "multi-dimensional value" = variable + index tuple → scalar.
- **Versioning is first-class**: `VersionKeyValue` (one version + `Timespan` lifetime), `MultiVersionKeyValue`
  (all versions of an object; binary-search `getVersionKeyValue(daytime)`), `equalsIgnoreType` = "calc equality"
  across versions. `Timespan` = half-open `[start,end>`.
- `CalculationValueHelper` = the central static ops library (arithmetic with MissingValue semantics, set algebra,
  date fns, comparisons, conversions). `ExternalFunction` (`init`+`execute`) = SPI for custom MathML functions.

## 5. Variable I/O binding (`engine/calculation` VariableMeta + VariableCache)
- **`VariableMeta`** loads `CALC_VARIABLE` + `CALC_VAR_READ_MAPPING` / `WRITE_MAPPING` (each = `CLS_NAME` class +
  `SQL_SYNTAX` attribute + date-handling + sub-daily attrs) + `CALC_VAR_KEY_*_MAPPING` (binds each DB key column to a
  variable DIMENSION / SCREEN_PARAMETER / CONSTANT / IGNORE). Reads go via the class **VIEW**; writes go to the
  **TABLE** only if `CALC_ENGINE_TABLE_WRITE_IND='Y'`, else the view. (Confirms the trace: mappings are context-level.)
- **`VariableCache`** = recursive (lexical scope). **Reads are lazy/on-access** (one SELECT per "readTraits" group
  populates many values), with object-version-validity checks. **Writes are deferred**: `write()` (root only) groups
  values into records (`ResultRecordGrouper`/`ResultRecordBatch`) and batches INSERT/UPDATE.
- **`ExecutionContext`** = the hub; `createChildContext` shares meta/object-cache but gives child variable/set/iterator
  caches (so STEP sub-calcs get scoped variables + a pushdown `IteratorCacheImpl`).

## 6. Excel-workbook calc type (`xls`)
Calc Type = Excel workbook → logic in a stored `.xlsx`, evaluated by **Aspose.Cells** (no Office). A **mapping
worksheet** declares per-cell: `READ`/`PARAMETER`/`ATTRIBUTE`/`ITERATOR`/`SET` (engine→cell), `WRITE`/`RESPONSE`
(cell→engine), `INFO`/`WARN`/`ERROR` (cell→log; ERROR aborts). `DataAccessHandler` pushes inputs → Aspose recalculates
(`CustomCalcEngine` handles VBA/custom fns via a `ServiceProvider` SPI) → reads outputs back. Keys cross the cell
boundary as strings via `ObjectCacheAdapter` (`[OBJ]`/`[VER]` prefixes).

## 7. SME takeaways
- Calc engine = **read definition → init caches → execute tree → write** (one JTA txn per period; Simulate skips write).
- PROCESS = orchestration flowchart; EQUATIONS = ordered MathML statements (with COND/ITERATIONS/LOOP baked in);
  WORKBOOK = Aspose xlsx; EXTERNAL_OPTIMISER = plugged solver.
- The **equation language is a fixed set of ~60 CalcNode operators** (catalogued above) over a scalar/set/iteration
  value model; variables carry the dimensions; MissingValue makes sparse sums work; versioning is first-class.
- **Variable DB I/O = context-level read/write/key mappings** (CLS_NAME + SQL_SYNTAX), lazy reads + batched writes.
- **Equation editor (parked) is now de-risked**: its constructs map 1:1 to the CalcNodes in §3 — the walk-through only
  needs the editor's click gestures, not the grammar.
