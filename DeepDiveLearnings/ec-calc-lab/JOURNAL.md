# EC Calculation Lab — JOURNAL (feature/ec-calc-lab)

_2026-06-28, local sandbox (localhost:1521/ORCL + sysadmin web). Autonomous session._

## Goal
Lock EC Calculation SME by proving two hands-on muscles: (1) **build** a calc from a spec; (2) **trace/debug**
a calc error via the logs. Practice spec `AUTOTEST_DBL_VOL` (EC_PROD/DAY): read a measured value ->
`round(input*2)` -> write a scratch `_ALLOC` column.

## What got DONE (proven)
- **Full read-only recon (18 scripts)** — the entire calc CONFIG model + UI is now mapped:
  - Storage model: `CALCULATION` (EQUATIONS/PROCESS/..., scope, context, period, date-effective) ->
    `CALC_EQUATION` (MathML) -> context-scoped vars (`CALC_VARIABLE_LOCAL`, keyed `CALC_VAR_SIGNATURE`) ->
    DB bindings `CALC_VAR_READ_MAPPING`/`WRITE_MAPPING` (`CLS_NAME` + `SQL_SYNTAX` = the attribute).
  - Run path: Calculation Set/Collection framework; EC_PROD EQUATIONS results/log land in `ALLOC_JOB_LOG`
    (the "Calculation Log" screen). `PWEL_DAY_ALLOC` has 120 rows => the engine HAS run here.
  - Build UI: `Create Calculation` (context-gated grid; create = **copy** an existing calc via the VERSIONS
    area "Copy To New Calculation" button = `copybutton:form:B`) + `Maintain Calculation` (nav = Date +
    Context + **Calculation** + GO; tabs **Equations / Set Equations / Local Variables**).
  - Concrete spec locked: read cls `PWEL_DAY_DATA` attr `THEOR_GAS_RATE` -> write cls `PWEL_DAY_ALLOC`
    scratch col `VALUE_1`; test well + day 2003-01-01.
- **First write PROVEN + reversible:** created `AUTOTEST_DBL_VOL` (EQUATIONS/MAIN/EC_PROD/2003-01-01) by
  copy-create, then **deleted it cleanly** via "Delete Calculation" -> "Yes". Independent DB re-read:
  0 CALCULATION rows, **0 orphan equations, 0 orphan local vars** -> sandbox fully clean.
- **Bonus SME (trace muscle, unblocked):** traced the real `EC_DAILY_VOLUME` = PROCESS/MAIN/DAY calc =
  an **8-element / 7-transition flowchart** (CALC_PROCESS_ELEMENT + CALC_PROCESS_TRANSITION) — confirms the
  PROCESS-calc orchestration model.

## BLOCKER (parked for discussion — owner-directed)
**Authoring the equation + variable read/write mappings has no reliable automatable path right now:**
1. The equation is stored as **Equation-Editor-generated MathML**. Hand-authoring EC-dialect MathML
   (variable/function/literal `<m:ci type=...>` encodings) from scratch is high-risk.
2. **No DB-config template exists** — query found **0 EC_PROD calcs with both read + write var mappings**
   on local vars (the real calcs e.g. EC_DAILY_VOLUME are PROCESS-type with logic in sub-calcs; the
   EQUATIONS calcs are empty test stubs). So there's nothing clean to clone the mappings/MathML from.
3. The **Maintain Calculation Equation Editor** (Equations/Local Variables tabs) is a structured/graphical
   editor — reliably automating "author DblVol=round(GrossVol*2) + 2 vars + 2 read/write mappings"
   headless is a large, error-prone effort, not safe to grind unattended.

This is the genuine frontier — NOT a missing recon piece. Header create/delete works; the equation+mapping
authoring is the hands-on hard part.

## Resolution options (to discuss when we talk)
- **(A) Interactive headed Equation-Editor session** (recommended): run it headed so the graphical
  authoring (equation expression + local vars + read/write mappings) can be done/observed step by step.
  This is the authentic "build a calc" SME muscle.
- **(B) Guided MathML hand-authoring:** I author the equation MathML by analogy to a real equation that
  uses variables+functions (e.g. the EC_PAY_DD `BusinessDay[...](InvoiceReceivedDate,8)` equation), build
  the var + read/write-mapping INSERTs, you sanity-check before run. Faster but riskier.
- **(C) Re-scope** the practice calc to fit whatever a real EQUATIONS calc with mappings looks like in
  another context, then clone cross-context.

## Status of the SME goal
**Knowledge axis: ~complete** — architecture, config model, JEXL/MathML, run path, allocation, performance,
AND now the build UI + create/delete mechanics are all mapped. **Remaining gap = the single hands-on
equation-authoring + run + debug-trace**, which needs the interactive Equation-Editor session (option A).

## Cleanup / state
Sandbox CLEAN (AUTOTEST_DBL_VOL created + deleted + 0 residue verified). Recon DB creds env-var'd
(security-review follow-through). All 18 recon + build + cleanup scripts committed on `feature/ec-calc-lab`.
No PR raised (lab incomplete by design — resumes at the equation-authoring step).
