# DOC-04 — EC Production
**Source:** EC 14.2.4 `prod` (22 pages) · **Read:** 2026-06-06 (pages 1–17 deep; 18–22 by title)

> 🟢 **Highest Woodside relevance** — Pluto is a Production/Allocation implementation. This is the operational core.

## 1. Record Status Processes (P→V→A engine)
The job that lifts **record status** (the lifecycle from DOC-01): **P**rovisional (manual insert, lowest) → **V**erified (process) → **A**pproved (monthly process, highest). Bidirectional, revision-tracked; **won't run on a locked month**. Defined in **Status Processes (CO.0076)** as an UPDATE with a **WHERE formula** (same formula engine as Check Rules: keywords + `${var}` constants/RV-attributes/function calls/subqueries). *(Ties DOC-01 status + DOC-03 check rules.)*

## 2. Deferment (PD.0020) — current version
A deferment = event where production/injection misses plan. **PD.0020 (Well Deferment) is current**; PD.0001/0001.02/0006 obsolete; PD.0004 (Daily Deferment Master) still exists. Controlled by system attr `DEFERMENT_VERSION`.
- **Down** deferment (full shut-in) vs **Constraint** deferment (reduced rate).
- Scope: single well · group (no linked wells) · group with linked wells (parent = Operator Route / Collection Point / Facility / Well Hookup / Equipment / Tank). Wells must be 'Open Normal' (WR.0088).
- **Event loss calc:** Loss = Loss Rate × Downtime if no Loss Volume; else = Loss Volume. Precedence: Down > Constraint; earlier start; Unscheduled > Scheduled; Single > Group. Run via "Calculate Deferment" button (`DefermentRecalculation` business action) or PD.0010 (`EcDp_Deferment.periodDefermentCalc`). Skips locked months.

## 3. 🟢 Hydrocarbon Accounting / Allocation (the heart of Production)
**Reconciliation** = balance fluids: sum of incoming streams adjusted to equal outgoing per phase, per calculation node. **Well allocation** = same but incoming "streams" are wells. Daily + monthly; volumetric default (mass/component supported).
- Allocates delivery-point measurements back to **production wells**; master injection → injection wells; gas-lift → gas-lifted wells; diluent → diluted wells.
- Operates over an **allocation network** (= a *calculation* network — also does PSA, deferment calcs): **nodes** (wells, platforms, terminals) + **streams** (flows). Edited in **Allocation Network (CO.0084)**; nodes added via **Calculation Group Setup (CO.0246)**.
- Three calc types: **equation-based** (EC MathML syntax), **Excel workbook**, **calculation library** (DOC-03). Uses daily/monthly **reconciliation factors** (pro-rating).
- **Allocation result tables** (key for queries): `STRM_DAY_ALLOC`, `PWEL_DAY_ALLOC` (producing well), `IWEL_DAY_ALLOC` (injection well), `PERF_DAY_ALLOC` (perforation interval) + `_MTH_` monthly + `_COMP_`/`_PROD_`/`_CPY_` variants + `OBJECT_DAY/MTH_DIMn_ALLOC`.
- **Ghost data** = stale allocation rows after config change (e.g. well producer→injector). Clean via `EcDp_Allocation.dataCleanup` (in the BPM optional block) or UE_CALC_ENGINE user exit.

## 4. 🟢 Allocation BPM Workflows (daily & monthly) — "Work by Exception"
EC automates allocation via **BPMN** processes — user only intervenes on exceptions. Deploy the **`prod-bpm-building-blocks`** artifact (from EC hub/nexus, `com.ec.bpm`) via **Project Management** business function → run via **Process Execution**.
Standard subprocesses (each optional/configurable): input init → input validation → **pre-checks** (check rules + class/object validation) → **data verification** (P→V status process) → **run allocation** → **ghost data cleanup** → **report** (Jasper/Excel/BO, optional verify/approve/email) → **approve allocation** (V→A) → (monthly) **Month Lock** user task. Params: Static (in template) vs Dynamic (entered at run).
Other prod BPMs: **Analytics Integration** (EC ↔ Analytics Manager ↔ external simulators HYSYS/PROSPER/PREVISO, via GraphQL extract + user-exit save), **Analysis Data Management** (bulk Mol↔WT↔Energy, normalization).

## 5. Stream Node Diagram
Visual tool to define/view allocation stream-node networks (Configuration → Assets → Calculation Objects). Pick date + network → Go. Read-only (view/export) vs edit (layout, add objects, save). Context menu for actions. (DOC-01 calc framework Stream/Node concept made visual.)

## 6. Well Testing (PT.* screens)
- **Multi Well Testing** (EC 13.0+): Production Test Define (PT.0005/0006) → Stable Period & Summarise (PT.0009, high-freq PI data, stability criteria) → Production Test Results (PT.0010) → Production Test Combination (PT.0011) → Enhanced Validation (PT.0025, accept/reject vs previous).
- **PreProcess & Calculate PVT** (PT.0010): triangular conversions (start/end/duration; vol/rate/duration; vol-rate/mass-rate/density — need 2 of 3); mass-transfer between phases (purify oil of water/diluent, gas of lift-gas); shrinkage/expansion to standard conditions. Error codes A/B/C in `ptst_result.preprocess_log`.
- **Single Production Well Test (PT.0013)**: single result; test device by Instrumentation Type 1–4 (data classes TDEV_PT_0013_1..4); rates at standard conditions via shrinkage.

## 7. System Attributes (CO.1012) — set per install
Key ones: `DEFERMENT_VERSION` (PD.0020) · `ALLOW_ALLOC_LOCK_MONTH` (N) · `DAILY_DEFERMENT_LEVEL` (FCTY_CLASS_1) · `ADJUST_POTENTIAL_DST` · API density/blend-shrinkage params (`API_CALC_*`, BITUMEN_DENSITY) · `REF_TEMP_TANK_SHELL`. **Check & set all on a new install.**

## 8. Other
- **API Measurement Standards** (MPMS Ch 12.1.1): tank **GOV** = (TOV − free water) × shell-temp correction CTSh × floating-roof adj. Tank material expansion coeff, TShREF (default 15°C). Configured in **Manage Tank (CO.0252)**.
- **Operation Mode** (EC 13.1+): quick per-day well production-mode override without a new config version (daily Well only; affects sub-daily calcs). Well Mode Attributes (CO.0255) + Well Mode (CO.0256).
- **Default Client Value**: class-attr property for new-insert date defaults — `NULL` / `NOW` / `YESTERDAY` / `PROD_DAY_START` (+offset) / `TO_DATE_PROD_START`. *(Relevant: when I inserted records, date fields defaulted — this is the mechanism.)*
- **Dashboard widgets** (`CTRL_DASHBOARD`): Top-5 producers, Actual vs Planned, reconciliation factor, well-on-stream — populated after a successful allocation run (e.g. `pwel_day_alloc.alloc_net_oil_vol`).

## 9. Pages 18–22 (by title)
Well Performance Curve · Well Decline Curve · **Production Forecasting** · Forecasting Upgrade Guide · **EC Chemistry** (chemical inventory, lab integration, injection optimization). → revisit on demand.

---

## Cross-links
- Status Processes = the P/V/A engine behind `RECORD_STATUS` I saw in OV_BANK/OV_EQPM.
- Allocation tables (`PWEL_DAY_ALLOC` etc.) = the production result data I could query next.
- Deferment / allocation screens are **data-grid + group-model-navigator** screens (DOC-01/02 patterns) — IUD automation would target these.
- Allocation BPM uses check rules (DOC-03) + status processes + calc library (DOC-03).
- Next: **DOC-05 Revenue + Sales**.
