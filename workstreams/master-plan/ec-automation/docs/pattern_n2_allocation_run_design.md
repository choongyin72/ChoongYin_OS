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

## ⛔ BLOCKER — the allocation RUN is not executable in this sandbox (honest)
Attempted (user-authorised; local DB refreshable): set dates + AS2_Onshore network + GO. Result:
- G3 (Allocation Network) and G4 (Calculation Job) dds stayed **empty** after selecting the G2
  network; GO surfaced **no Run/Calculate control**; no allocation row was created
  (`PWEL_DAY_ALLOC` @2003-01-01 stayed 0); no error.
- The screen toolbar persistently shows **"Process automation not available."**
→ Conclusion: the allocation calc is **submitted to the Process Automation engine**, which is **not
available** in this local sandbox (separate from the Quartz scheduler the user restarted). So a
fresh allocation can't be triggered from this screen here. **NOT yet cracked** (unlike N1). This is
environmental — needs Process Automation enabled, OR a known alternative run path (e.g. backend calc
trigger / batch), which requires SME guidance. ⇒ Open question logged for the user.

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
