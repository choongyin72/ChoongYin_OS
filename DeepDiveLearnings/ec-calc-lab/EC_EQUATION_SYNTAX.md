# EC Calculation — Equation Definition Syntax & Formula Editor (official doc)

_From `docs/EC/EC Calculation/Part II - Basic Functionality inside Equation 1.pdf` (Tieto, EC-11.2, 40pp).
The author-facing syntax + how the Formula Editor popup works. Pairs with the runtime side in
[[EC_CALC_FRAMEWORK_FROM_SOURCE]] (each construct here = a `*CalcNode`)._

## Equation = iterations + condition + equation
An equation has 3 parts: **Iterations** (optional, `∀ iterator ∈ set`), **Condition** (optional, a logical
expression), **Equation** (mandatory). Equation statement types:
| Type | Equation form |
|---|---|
| Variable assignment | `<obj-ident-list> variable = <arithmetic expression>` |
| User info message | `INFO = <string expression>` (→ calc log) |
| User warning | `WARNING = <string expression>` |
| User error | `ERROR = <string expression>` (stops the engine) |
| Macro call | `<macro call>` |
Equations run in EXEC_ORDER; an arithmetic expression may only appear on the RHS.

## Identifier scope
- **Calculation scope** — sets / inherited sets: known throughout the calc body from definition onward.
- **Equation scope** — `∀` iterators: known throughout the equation they're defined in (usable in condition + both sides).
- **Expression scope** — entities defined on an RHS sub-expression (e.g. a `sum` iterator) — only inside that sub-expr.
- **Global scope** — predefined for all calcs (`global` object, `this` set, global attributes).

## Basic elements
- **Identifiers:** variable / attribute / set / object(iterator) / predefined (`objects` = all calc objects;
  `global` = owner of global attributes; `this` = current calc object).
- **Literals:** numeric, text, `null`.
- **Operators:** comparison, logical, arithmetic. **Functions:** numeric, set, date.
- **Iteration construct:** `∀ iterator ∈ set-identifier` (iterator must be new; set must be in scope).

## Logical expressions (conditions, set filters)
- Comparison: `=` `≠` `>` `≥` `<` `≤` (binary, type-compatible). Function: `isValid(?)` → TRUE if input has a valid value.
- Combine with `∧` (and), `∨` (or), `¬` (not). e.g. `Phase[s]='OIL' ∨ Phase[s]='GAS'`.

## Arithmetic expressions (RHS)
- Operators: `+ - · /` and power. Precedence is standard; parentheses override.
- Numeric functions: `min(a,b)`, `max(a,b)`, `abs(x)`, `mod(a,b)`, `log(x)` (base-10), `floor(x)`, `arctan(x)`,
  **`sum`** (over an iteration), **`round`** — 1-arg (default precision), 2-arg (value, decimals), 2-arg
  (value, mode), 3-arg (value, decimals, mode). Rounding modes: `HALF_EVEN` (default), `HALF_UP`, `TRUNC`
  (Config→Preferences→Maintain System Setting → Calculation Rounding Mode).
- Index/iter: `argmin`/`argmax` (N subscripts + variable + iterator → iterator at min/max).
- Date: `addDays(d,n)`, `addMonths(d,n)`, `addSubDay(subdate,n,periodcode)`, `midnight(d)`, `firstOfMonth(d)`,
  `firstOfYear(d)`, `toDay/toMonth/toYear/toSubDay(x)`.

## Sets
- **Filter syntax:** `set = { ∀ iterator ∈ set | logical-expression }` (keep members satisfying the filter).
  e.g. `streams = { ∀ o ∈ objects | ObjectType[o]='STREAM' }`.
- **Expression syntax:** `set = <set-expression>` with `∪` union, `∩` intersect, `\` difference.
- Set functions: **`lookup('ObjectType','COMPONENT')`** (preferred over filtering `objects`), `days(from,to)`,
  `months(from,to)`, `years(from,to)` (to-exclusive), `interval([a,b>)` (typed ranges incl SUB_DAY), `args(var,iter)`
  (objects actually used in a dimension — perf for sparse data; `*` = iterate all values of a subscript), `elementAt`.

## Formula Editor popup — HOW TO AUTHOR (this resolves the "parked" editor)
- The editor builds formulas by **selecting syntactical elements from a RIGHT-CLICK context menu** — you do
  **NOT free-type** (that's why typing "INFO" earlier popped the Insert-Iterator popup). **`?` = an unidentified
  placeholder**; left-click an element/`?`, then pick a menu action (acts before/under/after per cursor position).
  **OK** accepts, **Cancel** discards.
- Context-menu tree (filtered by cursor context): **Operands** (Insert variable / set / attribute / iterator /
  constant number / constant text / global attribute / parentheses / placeholder); **Insert iteration**;
  **Insert assignment** (`=`); **Arithmetic operators** (+ − · /); **Arithmetic functions** (sum, cardinality |?|,
  power, min, max, mod, floor, abs, arctan, round(?), round(?,?), round(?,?,?)); **Set operators** (union/intersect/
  set-minus); **Set functions** (set filter, interval, lookup, component list, days/months/years, argmin/argmax,
  sortAsc/Desc, args, elementAt); **Comparison operators**; **Logical operators** (or/and/not) + **isValid**;
  **Date functions** (addDays/addMonths/midnight/firstOfMonth/firstOfYear/toDay/toMonth/toYear); **Flow control**
  (LABEL / GOTO / macro call); **Log message** (INFO / ERROR).
- **Worked example — author `INFO = 'text'`:** right-click the empty Equation → **Log message → Insert 'INFO'**
  → left-click the resulting `?` → **Operands → Insert constant text...** → type the message → OK → Save.
- **Worked example — `var = expr`:** **Operands → Insert variable...** (LHS, gets one `?` subscript per dimension)
  → **Insert assignment** (`=`) → build the RHS (constants/variables/operators/functions) by filling each `?`.
- Sub-popups: Insert constant number/text, Insert iterator (names a variable/attr subscript), Insert variable
  (lists public/private vars), Insert attribute, Insert global attribute, Insert number-of-iterations (argmin/max).

## Global attributes (predefined, scope `global`)
`Period`, `Method`, `PeriodStartDate`, `PeriodEndDate`, `IncrementStartDate`, `IncrementEndDate`. For a daily
alloc PeriodStart=IncrementStart; for monthly, Period spans the month while Increment advances per-day pass.

## Cross-reference
Runtime backing of every construct = the CalcNodes in [[EC_CALC_FRAMEWORK_FROM_SOURCE]] (e.g. INFO→UserLogMsg,
`=`→AssignVariable, `∀ ∈`→ElementOf, sum→Sum, isValid→IsValid, lookup→Lookup, args→Args, round→Round).
Other docs in the set: `Calculation functions.docx`, `documentation-14.2.5/`, `ec_calculation.md`, `online-help-14.2.5/`.
