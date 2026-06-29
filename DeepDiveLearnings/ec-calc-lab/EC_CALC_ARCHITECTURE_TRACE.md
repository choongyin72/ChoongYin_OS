# EC Calculation — Architecture, traced from the real DB (read-only, 2026-06-29)

_Sandbox ECKERNEL_EC. Verified by querying the live calc tables; figures are this sandbox's actuals._

## The object model
- **`CALCULATION`** = the calc object (date-effective): `OBJECT_ID`, `OBJECT_CODE`, **`CALC_TYPE`**
  (PROCESS / EQUATIONS / LIBRARY / PROXY), **`CALC_SCOPE`** (MAIN/PUBLIC_SUB/...), `CALC_CONTEXT_ID`,
  `CALC_PERIOD` (DAY/MONTH), START/END_DATE.
- Two working types:
  - **PROCESS** = an orchestration flowchart (e.g. `EC_DAILY_VOLUME`, MAIN/EC_PROD/DAY).
  - **EQUATIONS** = the actual compute (ordered equation list). 5,523 equation rows across 512 calcs here.

## PROCESS calcs = a flowchart (orchestration)
- **`CALC_PROCESS_ELEMENT`** (keyed by `CALCULATION_ID` = the parent process calc) = the step boxes
  (Start / Step N / Stop). `EC_DAILY_VOLUME` has 8 elements. Element codes are GUIDs; the boxes are flow
  nodes (no inline equations on the MAIN process calc itself).
- **`CALC_PROCESS_TRANSITION`** (keyed by `CALCULATION_ID`) = the arrows/flow between elements.
- A step is given logic by **"Implement as Equations"** (right-click the box in the FLOWCHART tab) -> it
  becomes an Equations sub-element you **drill into** to edit its EQUATIONS grid. (See
  [[EC_CALC_SCREENS_REFERENCE]] section 2 for the exact gestures.)

## EQUATIONS = ordered variable assignments
- **`CALC_EQUATION`** (keyed by the calc/element `OBJECT_ID`): `EXEC_ORDER`, `DESCRIPTION`, `CONDITION`
  (MathML), `EQUATION` (MathML), `ITERATIONS`. Equations run in EXEC_ORDER; each assigns a variable.
- Real patterns seen (e.g. a REVN inventory calc, 97 eqs): plain assignment (`IsQty = 'N'`), **conditional**
  (`COND(isValid ...) => IsQty = 'Y'`), **external Java functions**
  (`extfn com.ec.revn.calc.extfn.GetDimension`), and `REMARK` rows (inline documentation).
- The formula is stored as **MathML**; it is authored in the **canvas equation editor** (structured, not
  free-text — keystrokes map to constructs; see the PARKED note in the screens reference).

## Variables + DB I/O = defined PER CONTEXT (not per calc)  ← key architecture fact
- **`CALC_VARIABLE_LOCAL`** (keyed `OBJECT_ID` + `CALC_VAR_SIGNATURE`) = the variables; equations reference
  them by NAME.
- **`CALC_VAR_READ_MAPPING`** / **`CALC_VAR_WRITE_MAPPING`** (`CLS_NAME` + `SQL_SYNTAX` = the class.attribute)
  define where a variable's value is **read from** / **written to**. These are keyed by the **CONTEXT**
  `OBJECT_ID`, so they are **shared by every calc in that context** — not redefined per calc.
- Exactly **12 contexts** carry mappings here: `EC_PROD`, `EC_PROD_DC`, `EC_SALE_PR`, `EC_SALE_SA`,
  `EC_TRAN`, `EC_TRAN_CP`, `EC_TRAN_TO`, `EC_TRAN_FC`, `EC_REVN_DD`, `EC_REVN_FI`, `EC_REVN_TI`, `EC_REVN_LI`.

## Concrete end-to-end: the EC_PROD (Production Allocation) context
- **READS — 72 mappings**, e.g.:
  - `PWEL_DAY_DATA` . THEOR_CO2_RATE / THEOR_COND_MASS / THEOR_COND_RATE / THEOR_DILUENT_RATE (theoretical well rates)
  - `PWEL_DAY_PREC_DATA` . PREC_THEOR_* (preceding/precision theoretical)
  - `PERF_DAY_DATA` . ALLOC_COND_MASS / ALLOC_COND_PROD_VOL / COND_FRAC / ALLOC_GAS_INJ_VOL (perforation-level measured/allocated)
- **WRITES — 180 mappings**, e.g.:
  - `PWEL_DAY_ALLOC` . THEOR_CO2_RATE / ALLOC_CO2_VOL / CO2_VOL_FACTOR / THEOR_COND_MASS ... (well **daily** allocation)
  - `PWEL_MTH_ALLOC` . same attributes (well **monthly** allocation — the daily->monthly rollup)
- **Pattern:** read theoretical + measured rates/volumes -> compute allocation (equations) -> write allocated
  volumes + factors to the `_ALLOC` tables, both daily (`PWEL_DAY_ALLOC`) and monthly (`PWEL_MTH_ALLOC`).

## The run path (how a calc executes)
1. Connect the calc as a **Calculation Job** on an allocation network -> `tv_alloc_network_job_conn`
   ([[EC_CALC_SCREENS_REFERENCE]] section 3).
2. Run it from **Daily Allocation** (Simulate = dry-run, no real write) -> results/log land in `ALLOC_JOB_LOG`.

## SME takeaways
- PROCESS = orchestration (flowchart of steps); EQUATIONS = the math (ordered, conditional, function-using).
- **Variable read/write mappings are a CONTEXT-level asset**, shared across that context's calcs — so a calc's
  equations just reference variable NAMEs; the context says where those read from / write to in the DB.
- EC_PROD turns measured/theoretical well + perforation data into allocated daily & monthly volumes.
- This sandbox's compute calcs are largely orchestration shells / test stubs (no single calc had both read &
  write mappings on its own object_id — the mappings sit on the context), so deep equation logic is sparse
  here vs a full client (e.g. Woodside Pluto).
