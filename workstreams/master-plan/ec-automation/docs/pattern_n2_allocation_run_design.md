# Pattern N2 — Allocation calc RUN + verify (HA.0002 Daily Allocation) — recon (2026-06-13)
The calculation heart of EC: run an allocation over an **Allocation Network** for a date(range),
which computes per-well/stream allocated quantities and writes them to `*_DAY_ALLOC` tables. Verify
with a **conservation oracle** (the calc-engine critique gave the invariants — see
DeepDiveLearnings/ecpedia-efk/calc-engine-insights.md).

## Screen
- **HA.0002 "Daily Allocation"** — URL `/com.ec.prod.ha.screens/edit_daily_alloc`. Main frame (no iframe).
- Navigator: **From Date** (`nav:form:G:0:R:1:C:0:da_input`) + **To Date** (`G:1`) +
  **Allocation Network Group/Network** (`G:2` dd) + **Allocation Network** (`G:3` dd) +
  **Calculation Job** (`G:4` dd). GO = `button:form:B`. dds are **date-filtered** (empty until a date set).
- Allocation networks (seed): AS1_MassNetwork, **AS2_Onshore**, AS3_Offsh_Daily1/2, AS3_Reservoir_Alloc,
  AS4_DILUENT, AS5_INJECTION, P1/PS7/PS11/Resv networks, FRMW/Chem networks.

## Data model (DB)
- Networks/jobs: `OV_ALLOC_NETWORK`, `OV_ALLOC_NETWORK_GROUP`, `ALLOC_NETWORK_JOB_CONN` (network↔job),
  `CALCULATION` (+`_VERSION`), `DEPENDENT_CALC_JOB`.
- **Results**: `PWEL_DAY_ALLOC` (per-well, key OBJECT_ID+DAYTIME) — cols `ALLOC_GAS_VOL`,
  `ALLOC_NET_OIL_VOL`, `ALLOC_COND_VOL`, `ALLOC_WATER_VOL`, `ALLOC_GL_VOL`, `ALLOC_*_MASS`,
  `ALLOC_GAS_ENERGY`, + `THEOR_*` / `PREC_THEOR_*` (theoretical basis the actuals are prorated onto).
  `STRM_DAY_ALLOC` + `STRM_DAY_{PC,CPY,COENT,COMP}_ALLOC` = stream allocation at profit-centre /
  company / co-entity / component grains (matches the dimensioned variables in the calc engine).
- Existing allocation data: PWEL_DAY_ALLOC has 2018–2021 (richest **2021-10-01 = 22 wells**);
  STRM_DAY_ALLOC sparse (2011-01-01). (No allocation exists for the 2003 seed dates.)

## ✅ RUN MECHANISM CRACKED (2026-06-13) — corrects an earlier wrong "PA-blocked" conclusion
The run is **synchronous via a "RUN CALCULATIONS" button**, NOT BPM. ("Process automation not
available" = the BPM bell only — a red herring; SME confirmed PA=BPM, skip until a BPM deep dive.)
Working flow on HA.0002:
1. Set **From/To Date**, pick **Allocation Network Group/Network** (G2), then the **Calculation Job**
   (G4) populates (e.g. P1 Dashboard → "Daily Well Volume" = EC_DAILY_VOLUME), GO.
   ⚠️ The network MUST have a calc job wired in `ALLOC_NETWORK_JOB_CONN` (AS2_Onshore has NONE → its
   job dd was empty; P1 Dashboard / P1 Day Allocation / Resv network / "Testing allocation RUN_NO" do).
2. Second row: **Job Start Time**, **Log Level**, **Simulate** (checkbox = run the calc flow but
   NEVER write to DB — per SME; ideal for safe iteration), then the green **RUN CALCULATIONS**
   button = **`ProdAllocButton:form:B`** (`PrimeFaces.ab`).
3. The job runs in ~1–2s and appears in **`log_list:form:T_data`** with Run No / Date / Duration /
   **Exit Status (Success/Failure)** + DOWNLOAD/VIEW the log. (`RunningJobs:form:T_data` shows
   in-flight WAITING; it moves to log_list on completion.)
**Runnable calc TYPES** (CALCULATION where CALC_SCOPE=MAIN): `EC_DAILY_VOLUME` (Daily Well Volume),
`EC_MONTHLY_VOLUME`, `EC_DAILY_RESV_ALLOC`/`EC_MONTHLY_RESV_ALLOC`, test `RUN_NO_TEST`.

### Current result: the test run FAILED (a real finding, not a block)
Ran EC_DAILY_VOLUME over **P1 Dashboard @ 2021-10-01** → Exit Status **Failure** in ~1s:
*"Failed to execute equation step … Failed to evaluate iteration/condition … Failed to calculate
and/or assign a value."* So the calc executes but **errors out** (likely missing input / config gap
for that network+date in this sandbox — consistent with the fragile-equation issues in the
calc-engine critique). No DB write because it failed. ⇒ the calc engine RUNS; this particular
allocation doesn't complete cleanly here.

### Next (use Simulate — no DB risk)
Find a calc/network/date that runs **Success** (try the dedicated **"Testing allocation RUN_NO" →
RUN_NO_TEST**, or a P1 date with complete input), iterating with **Simulate** checked (no writes).
On a clean Success, verify the conservation oracle on `PWEL_DAY_ALLOC`/`STRM_DAY_*_ALLOC`
(sum-to-total / no-neg / roll-up). The "Failure exit status" is itself a meaningful test signal
(an allocation that errors is a defect to catch).

## ✅ What IS doable now — the VERIFY half (conservation oracle on existing results)
Even without a fresh run, the meaningful allocation invariants can be DB-asserted against existing
`*_DAY_ALLOC` data (the test oracle from calc-engine-insights.md):
1. **No negatives** — VERIFIED on 2021-10-01: `COUNT(*)` of PWEL_DAY_ALLOC rows with any negative
   `ALLOC_*` = **0**. ✓ (invariant holds on real data; `tmp/scripts/pwel_alloc_struct.py`)
2. **Sum-to-total / conservation** — sum of per-well `ALLOC_GAS_VOL` (etc.) over a network's wells
   should equal the network's measured field/stream total; per-PC/company/component splits in
   `STRM_DAY_*_ALLOC` should sum to the stream total. (Needs the network→members→total mapping from
   `ALLOC_NETWORK_JOB_CONN` + the stream/field measured tables — next recon step to wire a real
   sum-check.)
3. **Multi-grain roll-up** — day rolls to month; dimensional splits sum to parent grain.

## Next steps
- **Unblock the RUN** (needs user): can Process Automation be enabled in the local sandbox, or what's
  the supported way to trigger an allocation calc here? (Then build the N2 RUN-verify suite:
  set network+job+date → run → assert conservation on `*_DAY_ALLOC`.)
- **Independent of the run**: build a `DbVerify` allocation-conservation helper (no-neg + sum-to-total
  + roll-up) and a read-only suite that asserts invariants on existing allocation data — a meaningful
  N2 test that needs no calc execution. (Mechanical; doable next.)

## ✅ BUILT + GREEN (2026-06-13) — N2 RUN-verify suite, 3/3 live (DB-verified, no DB write)
The N2 pattern is now a working, layered RF suite — the run mechanism is fully cracked and the
verify half is DB-grounded.

**Artifacts (layered T1→T3):**
- T2 `resources/allocation_run.resource` — cross-screen allocation-RUN mechanics: set date range,
  pick network (G:2) + calc job (G:4), apply navigator, enable **Simulate**, click RUN CALCULATIONS
  (`ProdAllocButton:form:B`), and poll `log_list` for the newest run's **Exit Status**.
- T3 `pageobjects/Production/ha0002_daily_allocation_page.resource` — screen name, result table
  (`PWEL_DAY_ALLOC`), and the scope data (the positive/negative cases).
- Suite `tests/Production/daily_allocation_run.robot` — TC01 positive Success, TC02 negative
  Failure, TC03 DB conservation oracle.
- `libraries/DbVerify.py` — added `allocation_row_count`, `allocation_negative_count`,
  `allocation_conservation_should_hold` (no-negatives oracle; fails on an empty day too).

**Proven scope (exact labels):**
- POSITIVE (Success): network **"Testing allocation RUN_NO"** → job **"01 Run No .test"** @ 2003-01-01.
- NEGATIVE (Failure): network **"P1 Dashboard"** → job **"Daily Well Volume"** @ 2021-10-01 (the calc
  errors on equation steps — a real calc-engine defect; the Failure status is the test signal).

**Run-mechanism details nailed during the build:**
- The network selector is navigator group **G:2** (lists the networks directly, e.g. "Testing
  allocation RUN_NO", "P1 Dashboard"); the calc-job dd is **G:4** (populated after the network pick).
- **Simulate** is a native `<input type=checkbox>` styled with class `ECCell ECCheckboxCell`, id
  **`dateStartJob:form:G:0:R:1:C:2:cb`**. There is NO separate `...:C:2` container element — clicking
  that id (a Browser-lib `Click`) times out. The reliable, headed-safe gesture is a **JS click on the
  input** (`i.click()` toggles `.checked` and fires EC's onclick; PrimeFaces serializes the checked
  state on the RUN ajax). Simulate ON = the calc runs but writes NOTHING to the DB (SME-confirmed) —
  **verified**: after both runs, PWEL_DAY_ALLOC @2021-10-01 still = 22 rows, 0 negatives (untouched).
- **`log_list:form:T_data`** row (newest = top, ri=0): cells = `[Timestamp, RunNo, User, Date,
  NETWORK(idx 4), Duration, Details, EXIT STATUS(idx 7), …]`. The reader polls the top row until its
  network cell matches the scope AND the status is terminal (Success/Failure/Error) — disambiguates
  the just-submitted run from a prior one.
- **Timing caveat**: Simulate runs complete synchronously (~1-2s) → log_list. The NON-simulate path
  goes through the Quartz executor (RunningJobs = WAITING→ACQUIRED) and can stall in this sandbox
  (observed >26s with no completion) — so functional RUN tests use Simulate; do not depend on a
  fresh non-simulate completion here.

**Conservation oracle — honest scope:** asserted (no-negatives + rows-exist) on REAL persisted
results (PWEL_DAY_ALLOC @ 2021-10-01, 22 wells produced by a prior real run). A fresh non-simulate
Success that writes new rows isn't reliably reproducible in this sandbox (executor stalls; the
RUN_NO_TEST calc doesn't write well allocations), so the oracle reads existing real output rather
than a freshly-triggered write. **sum-to-total** and **day→month roll-up** remain future extensions
(need the network→members→measured-total mapping from `ALLOC_NETWORK_JOB_CONN` + source totals).

## Sum-to-total / cross-column oracle — recon BLOCKER (2026-06-14)
Tried to extend the conservation oracle beyond no-negatives. **Not feasible on existing sandbox data:**
- **No co-present totals:** `STRM_DAY_ALLOC` has rows only on 2011-01-01 (8), NOT on 2021-10-01 where
  the 22 `PWEL_DAY_ALLOC` wells live — so there is no stream/field total to sum the per-well
  allocations up to. (`tmp/scripts/n2_sumtotal_recon.py`)
- **Sparse columns:** on 2021-10-01 only `ALLOC_GAS_VOL` (+ a few volumes) is populated;
  `ALLOC_NET_GAS_VOL`, `ALLOC_GAS_MASS`, `ALLOC_GAS_ENERGY`, `ALLOC_GAS_GCV` are **all NULL** — so the
  per-row physical invariants (NET≤GROSS gas, energy≈vol×GCV, mass-present-where-vol) have nothing to
  compare; they'd pass vacuously. (`tmp/scripts/n2_invariant_recon.py`) — deliberately NOT shipped.
- **Root cause:** the existing allocation rows are a sparse/partial (gross-volume-only) result. A
  meaningful sum-to-total / mass-energy oracle needs a *fresh full* allocation that writes the complete
  column set + co-present stream totals — which requires the **non-simulate** executor, and that stalls
  in this sandbox (ACQUIRED, see above). So `allocation_conservation_should_hold` (no-neg + rows-exist)
  remains the shippable oracle until a complete real allocation result exists.
- **To revisit when:** Process Automation / a working non-simulate run is available (then run a full
  allocation, and add sum-to-total via `ALLOC_NETWORK_JOB_CONN` network→members + the stream totals).
