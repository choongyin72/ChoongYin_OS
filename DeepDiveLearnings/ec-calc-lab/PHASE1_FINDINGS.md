# EC Calculation Lab — Phase 1 (read-only recon) FINDINGS + resume plan

_2026-06-28, local sandbox (localhost:1521/ORCL + sysadmin web). Pure read-only — no writes, nothing to clean._

## Objective (unchanged)
Lock EC Calculation SME by proving two muscles on a disposable target: (1) **build** a calc from a spec;
(2) **trace/debug** a calc error via the calc logs. Spec = `AUTOTEST_DBL_VOL`: read a measured gross volume
-> `output = round(input*2)` -> write a scratch `_ALLOC`, context **EC_PROD**.

## Calc data model — CONFIRMED (how a calc is actually stored)
- **`CALCULATION`** = the calc object (date-effective): `OBJECT_CODE`, `CALC_TYPE` (EQUATIONS/PROCESS/LIBRARY/...),
  `CALC_SCOPE` (MAIN/PUBLIC_SUB/...), `CALC_CONTEXT_ID`, `CALC_PERIOD` (e.g. DAY), `START_DATE/END_DATE`.
- **`CALC_EQUATION`** (keyed by calc `OBJECT_ID`): `EXEC_ORDER`, `DESCRIPTION`(CLOB), `CONDITION`(CLOB MathML),
  `EQUATION`(CLOB MathML), `ITERATIONS`. Equations are readable once MathML tags are stripped, e.g. template
  `EC_PAY_DD_LNG_DES_PREL_EST`: `[1] DueDate = PeriodStartDate(global)`; `[2] cond isValid(InvoiceReceivedDate)
  -> DueDate = BusinessDay[DAY,LITERAL(OFFSET)](InvoiceReceivedDate, 8)`.
- **Variables** are **context-scoped**, keyed by `CALC_VAR_SIGNATURE`, referenced in equations by `NAME`:
  `CALC_VARIABLE` / `CALC_VARIABLE_LOCAL` (`CALC_CONTEXT_ID`, `NAME`, `CALC_VAR_DATA_TYPE`, alias fields).
- **DB bindings = the read/write mappings** (keyed by `CALC_VAR_SIGNATURE`):
  - `CALC_VAR_READ_MAPPING`: `CLS_NAME` + `SQL_SYNTAX` (+ `CALC_DATE_HANDLING`, `PROD_DAY_ATTR_NAME`,
    `VALID_FROM/TO_ATTR_NAME`, `SUB_DAILY_IND`) = WHERE the input value is read from.
  - `CALC_VAR_WRITE_MAPPING`: `CLS_NAME` + `SQL_SYNTAX` (+ `ALWAYS_INSERT_IND`, `PROD_DAY_ATTR_NAME`) = WHERE
    the output is written.
- **`CALC_CONTEXT`** (14 on sandbox). Target = **`EC_PROD`** ("Well, sub-surface and production ownership
  allocations", id `96D6E0ED1D5A0571E053020011ACE2E9`).
- EC_PROD EQUATIONS/MAIN calcs are mostly EC product **test stubs** (RUN_NO_TEST, PROXY_TEST_*,
  01_TEST_CALCULATION [logging-only], EQUATION_LOOP_TEST, ARGS_FUNC_TEST) — no clean small real read->write
  arithmetic exemplar. So the build patterns the *structure* from the template + the mapping tables above,
  not a single clone.

## Build recipe for `AUTOTEST_DBL_VOL` (for the build session)
1. `CALCULATION`: code `AUTOTEST_DBL_VOL`, EQUATIONS/MAIN, context EC_PROD, period DAY, far-past start.
2. Input var (e.g. `GrossVol`) + `CALC_VAR_READ_MAPPING` to a measured gross-volume dataset for a test well/day.
3. Output var (e.g. `DblVol`) + `CALC_VAR_WRITE_MAPPING` to a scratch `_ALLOC` column.
4. `CALC_EQUATION` exec_order 1: `DblVol = round(GrossVol * 2)`.
Author via **Equation Editor UI first**; fall back to `CALC_*` SQL if the UI blocks (user decision 2026-06-28).

## *** FEASIBILITY GATE — resolve FIRST in the build session ***
**All run-log tables are EMPTY** — `CALC_BATCH_LOG` = `CALC_PROCESS_LOG` = `CALC_PROCESS_DETAIL_LOG` = **0 rows**.
No calc has ever been run on this sandbox. Engine package `EC4E_CALCULATION` IS present (spec+body).
`DEPENDENT_CALC_JOB` has 1 row; no `CALC_JOB` table; `EC4E_ALLOC_JOB_LOG` is a package not a table.
=> **Before building anything, establish + verify a RUN trigger that populates those logs** (options to probe:
the Maintain/Run Calculation web screen, a Calculation Job / scheduler, or an `EC4E_CALCULATION` run entry).
If a calc cannot be run + logged here, Phase 3 (run) and Phase 4 (trace-the-error — the core SME proof) cannot
be demonstrated on this sandbox, and we either find the right run path or move the run/debug to a calc-enabled
env. **This is the make-or-break; do it before authoring config.**

## Still to confirm in the build session
- The exact **read source** (a measured gross-volume class/`SQL_SYNTAX` for a test well on an unused far-past day).
- A safe **scratch `_ALLOC` write target** + its key columns + that it's cleanly nullable/deletable.
- The **run trigger** (per the gate above) + that it writes `CALC_PROCESS_DETAIL_LOG` (needed for the debug drill).
- Clean-delete path for a calc (CALCULATION + equations + vars + mappings) — confirm fully reversible before build.

## RUN-PATH GATE — RESOLVED (read-only, 2026-06-28)
The run path exists and is UI/collection-based (not a standalone proc). Confirmed live menu screens:
- **Build:** `Create Calculation` + `Maintain Calculation` (+ `Calculation Equation` = the Equation Editor),
  `Calculation Context`, `Calculation Library`, `Calculation Group Setup` / `Calculation Group Context`.
- **Run:** per-context calc screens — e.g. production/contract/financial run screens + the Calculation
  Set/Group framework (`CALC_COLLECTION`, 53 sets; `CALC_BATCH_LOG` keys on collection). `Calculate Forecast`,
  `Period Process Calculations` etc. are run actions.
- **Result/log:** `Calculation Log` screen; EC_PROD calc results/log land in **`ALLOC_JOB_LOG`** (class
  `CALC_DAY_PROD_LOG` = "Daily Production Calculation Log"). `CALC_PROCESS_*_LOG` empty = those are for
  PROCESS-type calcs; EQUATIONS-calc runs in EC_PROD log to ALLOC_JOB_LOG.
=> Engine is present + runnable here; the trigger is the EC web UI. **Phase-4 trace target = `ALLOC_JOB_LOG`
+ `CALC_BATCH_LOG` (+ the Calculation Log screen), not CALC_PROCESS_DETAIL_LOG, for an EC_PROD EQUATIONS calc.**

## NEXT ACTION = Phase 2 build (a WRITE, hardest EC UI = Equation Editor)
Recon is COMPLETE. The remaining work is the live build in `Create Calculation`/`Maintain Calculation` +
Equation Editor (author the calc, vars, read/write mappings), then run via the production calc/Set screen,
verify ALLOC_JOB_LOG + the output `_ALLOC`, then the inject-fault debug drill. This is the write half and the
single hardest EC UI — best with clean budget (the dedicated-session rationale; NOT a blocker).

## Phase-2 ENTRY mapped (read-only) — BUILD IS TEED UP
`Create Calculation` screen = context-gated multi-panel:
- Navigator: date `nav:form:G:0:R:1:C:0:da_input` + **context dd `nav:form:G:1:R:1:C:0:dd`** + GO `button:form:B`.
  **Context dd option for EC_PROD = `'Production Allocation'`** (the 14 options map to the 14 CALC_CONTEXTs).
- After GO: panels `calculation:form` (the calc header), `calculation_version:form` (versions),
  `static_param:form` (static params). The **Equation Editor** is a deeper screen (`Calculation Equation` /
  `Maintain Calculation`) for authoring the equation + variable read/write mappings.

### First build steps (resume here)
1. Open `Create Calculation` -> set a far-past date + context `Production Allocation` -> GO.
2. Create the calc header in `calculation:form` (code `AUTOTEST_DBL_VOL`, type EQUATIONS, scope MAIN, period DAY).
3. Add the equation (`Calculation Equation`/Equation Editor): `DblVol = round(GrossVol * 2)`.
4. Define input var `GrossVol` + `CALC_VAR_READ_MAPPING` (a measured gross-vol source for a test well/day);
   output var `DblVol` + `CALC_VAR_WRITE_MAPPING` (scratch `_ALLOC`).
5. **Confirm clean-delete path for the calc BEFORE step 2** (so it's reversible). If UI authoring of the
   equation/mappings proves impractical, fall back to DB-config `CALC_*` SQL (user-approved option 2).
6. Run via a Production Allocation run screen / Calculation Set -> verify `ALLOC_JOB_LOG` + output -> debug drill.

**Checkpointed before step 2 (first write) per the clean-reversibility + token-budget STOP rules: a first-ever
calc write should start with clean budget so it completes + self-cleans in one pass.** Resume = run steps 1-6.

## Resume plan
Dedicated focused session -> (a) crack the RUN-PATH gate first; (b) build via Equation Editor UI (DB-config
fallback); (c) run + DB-verify output = 2x input + read clean log; (d) inject fault -> trace via
`CALC_PROCESS_DETAIL_LOG` -> fix -> re-run green; (e) self-clean to zero residual + finish this bundle's JOURNAL.
Recon scripts: `investigation/recon01_clone_template.py`, `recon02_structure.py`, `recon03_recipe_and_feasibility.py`.
Branch `feature/ec-calc-lab`, worktree `/c/tmp/wt-calclab`.
