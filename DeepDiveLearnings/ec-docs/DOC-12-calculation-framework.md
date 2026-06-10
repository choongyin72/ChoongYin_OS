# DOC-12 — EC Calculation Framework Deep Dive (2026-06-10)

Sources: 9 EC 14.2.x doc extracts (root `ec_doc_calc_*.txt`, `ec_doc_p06_calc_framework.txt`),
ECpedia BPR space (25 calc/allocation best-practice pages), live plutodev DB recon
(`tmp/logs/calc_recon_plutodev.txt`), Woodside repo `Pluto_Config/.../080_Calculations/`.

## 1. The mental model

A **Calculation** is configurable business logic stored as DATA in the DB — a process
diagram of steps (equation blocks, sub-processes, library calls, decisions), with equations
stored as MathML. No compiler; the **Calculation Execution Framework** interprets it.
Everything is config: deployable via Flyway MERGE/INSERT scripts, versionable, date-effective.

Two halves: **Definition** (Create Calculation → Maintain Calculation flowchart editor)
and **Execution** (calculation groups / allocation network jobs run them per period).

## 2. Building blocks

| Concept | What it is |
|---|---|
| Calculation | Process diagram; CALC_TYPE = EQUATIONS / PROCESS / LIBRARY / PROXY; CALC_SCOPE = MAIN / PUBLIC_SUB / PRIVATE_SUB; CALC_PERIOD = DAY / MTH / etc. |
| Equation block | Logical group of equations; naming standard: `[index] Name (iterators)` e.g. `[20,20] Read Daily Stream Data (d=daysInPeriod, s=StreamsMeasured)`; keep <50 equations |
| Variable | Data container, multi-dimensional via signature `Name[DIM1,DIM2,...]` |
| Set | Group of objects to iterate (StreamsMeasured, NodesASC, ComponentsUsed); global (CamelCase) vs local (lowerCamel, 4-char type prefix) vs dynamic (Args()) |
| Iterator | Steps through a set; reserved letters: d=day m=month s=stream n=node c=component p=phase pc=profit-centre |
| Condition | Guard on equation (isValid(), div-by-zero protection) |
| Library Calculation | Reusable calc with pseudo-signature (Expected Inherited Sets/Variables); no recursion; context-bound |
| Calculation Group | WHAT objects × WHICH calcs × WHEN (period/job schedule); 5 OOB contexts: Allocation Network, Contract, Financial Item, Price, Product Stream |

## 3. Variable Definition — the data contract (the part that matters most)

Variables are the ONLY bridge between DB and engine. Four config tables (all have DV_ views,
deployed via `080_Calculations/01_Variables/` scripts):

| Table | Role | Key columns |
|---|---|---|
| CALC_VARIABLE | declares variable + dimensions | CALC_VAR_SIGNATURE `ZWP_rCntrX1QtyYTD[CONTRACT,ACCOUNT_LIST,MTH]`, DIM1..4_OBJECT_TYPE_CODE, CALC_VAR_DATA_TYPE |
| CALC_VAR_READ_MAPPING | where reads come from | CLS_NAME_MAPPING (class/view), SQL_SYNTAX (column), CALC_DATE_HANDLING (FIXED_INTERVALS / VALID_UNTIL_NEXT / VARIABLE_PERIOD), VALID_FROM/TO_ATTR |
| CALC_VAR_WRITE_MAPPING | where results land | CLS_NAME_MAPPING, SQL_SYNTAX, ALWAYS_INSERT_IND, DIMn_TRIGGER_IND |
| CALC_VAR_KEY_RD/WR_MAPPING | binds key columns to dimensions | SQL_SYNTAX (e.g. OBJECT_ID, DAYTIME), CALC_DIM_MAPPING_CODE = DIMENSION(n) or CONSTANT('MTH') |

Naming: `g`/`l` prefix global/local; r=read w=write in Woodside names (ZWP_rXxx, ZWP_wXxx).

**Iron rule (docs + ECpedia + Woodside all agree):** read from `*_DATA` classes
(view-based, read-only: STRM_DAY_STREAM_DATA, PWEL_DAY_DATA, RBF_DAY_DATA), write to
`*_ALLOC` classes (dedicated result tables: PWEL_DAY/MTH_ALLOC, STRM_DAY/MTH_ALLOC).
NEVER read/write screen classes — performance death. Extend existing _DATA/_ALLOC classes
for project attributes; only create new ones (with the suffix) as last resort.

## 4. Execution & logging

- Runs per **calculation group** (or allocation-network job): manual (screen), scheduled
  (Calculation Job Connection tab), or workflow/BPM-triggered.
- Logging: 3 profiles (No Detail default / Medium / Full-debug); semicolon-delimited INFO
  lines for Excel import; Warning < Error (stops after showing all) < Fatal (immediate);
  ErrorCount auto-populated and testable. Always log the block index.
- Performance: built-in Performance Report in the calc screen log (≥12.2.10; old standalone
  Log Analyser exe is deprecated).

## 5. Screens (CO area)

Maintain Calculation (CO.1010, flowchart + equation editor) · Create Calculation ·
Variable Definition · Calculation Library (CO.1060) · Create/Maintain Library Calculation
(CO.1061/62) · Calculation Group Context · Calculation Group Setup (3 tabs: Group / List /
Job Connection) · Stream Node Diagram editor (network modelling).

## 6. Live plutodev footprint (recon 2026-06-10)

- 1,652 calculations / versions; 10,092 equations; 1,713 sets; 3,328 local variables.
- 1,373 declared variables: 819 product, 371 XEM (emissions), **183 ZWP (Woodside)**.
- 14 calc contexts; 5 libraries; 6 calc groups (CALC_GRP_CONTEXT); 3 log profiles.
- Read mappings top sources: TRANS_INVENTORY_TRANS (Revenue TI), XEM_* (emissions),
  RBF/PERF/PWEL/STRM _DAY_DATA. Write mappings top targets: TRANS_INVENTORY_TRANS/BALANCE,
  PWEL_DAY/MTH_ALLOC (54 each), STRM_*_ALLOC, XEM_* — textbook _DATA→_ALLOC pattern.
- 9 alloc-network job connections across 4 networks (PLU_EMISSION, PLU_OFFSHORE_ALLOC,
  PLU_ONSHORE_ALLOC, SCA_OFFSHORE_ALLOC).

## 7. Woodside implementation pattern (repo 080_Calculations/)

Folder convention: `00_DB_Object_types` → `01_Variables` → `02_Calculation/01_Library` →
`02_Calculation/02_Main` → `03_Network` (deploy order matters).

Architecture: thin **PROXY wrappers** (C_ALLOC_ONSHORE_DAY/MTH, C_ALLOC_OFFSHORE_MTH,
C_MASS_BALANCE_DAY/MTH, C_PRRT, C_SCA_ALLOC_OFFSHORE_DAY/MTH) wired to allocation networks,
each pointing at a versioned implementation (**ZWP_*_V0**: ZWP_ALLOC_ONSHORE_MTH_V0 etc.,
plus ZWPC_EMISSION_DISCHARGE). Patches arrive as new ECPR-numbered calc scripts.
Helper libraries: ZWP_LIB_* (READ_CARGO, DATA_LOG_DAY/MTH, MASS_BAL).

Note: ECpedia best practice (draft) says "use Library, not Proxy" for the prelim-daily /
final-monthly reuse pattern — Woodside predates/diverges from this; the V0-behind-proxy
gives them version swapping instead.

## 8. ECpedia map (BPR space — calc/allocation pages)

Approved: Production allocation (+ PFA Questionlist) · Well allocation · Component
allocation · Subsurface allocation · Ownership allocation · Multi-level allocation networks ·
Generic vs specific calculations · EC formulas vs Excel · Allocation flowchart modelling ·
Allocation pre-processing · Object versions in EC calculations.
2026-refreshed: Calculation Data Model Best Practices · Library Calculation
Basics/Design/Creating/Working-with · PSLC (product standard library calcs) · Naming
conventions variables · Sets/Variables/Iterators for libraries.
Draft: EC Calculation Library feature (library-vs-proxy guidance).
Tooling: EC Calculation Log Analyser (deprecated → built-in Performance Report).
Sandbox: Polar Bear — Production Allocation (worked example env).

## 9. Cross-links to prior sessions

- DOC-02/DOC-04: _DATA/_ALLOC classes are View-Generator classes — same class-config
  machinery as everything else (one spine).
- ECPR-31011: screen theo value vs calc theo value (`zwp_prod_well_theoretical` vs
  `ecbp_well_theoretical.getGasStdRateDay`) is a READ-side discrepancy between a class
  FUNCTION attribute and the calc's variable mapping — the exact class of bug this
  data-contract layer creates when two paths compute "the same" number.
- Issue_1052: check rules validate the INPUT side of this pipeline (PHD → screen classes →
  _DATA reads); calc results land in _ALLOC and feed the reports under UAT.
