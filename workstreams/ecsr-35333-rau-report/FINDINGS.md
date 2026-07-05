# ECSR-35333 — Fact-Finding Findings

**Ticket:** ECSR-35333 (Critical) — *Pluto Hub Monthly Deferments and RAU Report issues* — RAU Performance Summary tab.
**Investigated on:** ECAASDEV (read-only) — DB `dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB`; web `https://dev.non-prod.plp.wde.ecaas.cloud/`.
**Report under test:** *Pluto Scarborough – RAU Performance Summary*, period **01–30 Jun 2026**, generated **16 Jun 2026 15:22**, LNG Train 1.
**Status:** Issue 1 root-caused (proven). Issue 2 linked to Issue 1. Issue 3 not yet investigated. One secondary data defect found. **No fix applied — fact-finding only; awaiting client re-test.**

---

## Issue 1 — Period Actual & YTD Actual are blank (RAU Performance Summary)

**Plain-English cause:**
> When the RAU calculation detects **any** deferment data **not "Verified"** for the selected month, the **RAU Calculation does not run** (as the As-Built DDS states). The Actual figures are therefore never produced, so the report comes out with **wrong/blank data** — Period Actual & YTD Actual empty for that facility.

**For LNG Train 1, June 2026:** **120 of its 150 daily deferment records are still "Pending" (`P`), not "Verified" (`V`)** — so the calc skipped LNG Train 1 and produced no actuals → report blank.

**Why the deferments weren't verified:** the report was run **mid-month (16 Jun)**, before June's deferments were verified (verification happens at month-end close). The calc checks the **whole month** (1st → last day), so any unverified day blocks it.

**The chain:**
1. Report's Period/YTD Actual read `ZWP_V_DEF_RAU_SUB_004.PERIOD_ACTUAL / YTD_ACTUAL` (Jasper subreport `RAU_SUB_04_LNG1_PERF_YR.jrxml`, filtered `DEF_FCTY_1_CODE='PLU_LNG_TRAIN1'`, `DAYTIME = month of report End Date`).
2. That view derives them from contract-account events `RAU_*_ACT` / `RAU_*_ACT_YTD` — **none exist** for `C_PLU_LNG_1` in June.
3. Those events are produced by the scheduled calc **`ZWP_RAU_CALC_PLUSCA` → `ZWP_P_DEF_RAU_CALC`**, which **skips a facility whose monthly deferments aren't all Verified**.

**Proven four independent ways:**
- **DDS §4.1.6 (Inputs):** *"the calculation will check that all daily deferment event statuses are 'Verified' … the RAU Calculation will not be executed … 'There are deferment events not verified'."*
- **Package code** (`R__0500_ZWP_P_DEF_RAU_CALC_body.sql`): counts `TV_ZWP_DEF_DAY_DETAIL` rows for the whole month where `APPROVAL_STATUS != 'V'`; if ≥ 1 it sets the message and skips the actual block (in the `ELSE`).
- **Live data:** `TV_ZWP_DEF_DAY_DETAIL` for LNG Train 1, June = 150 rows, **120 = `P`**, 30 = `V`, unverified rows on **all 30 days**.
- **The calc's own run record** (Schedules screen, 16 Jun run): revision text *"There are deferment events not verified for SCA_OFFSHORE."*

**Conclusion:** The report, view and calculation are all **behaving as designed**. Issue 1 is a **timing/data matter** — actuals only exist once deferments are Verified — **not a report/code defect**.

**Recommended action (operational):** verify the outstanding June deferment events for LNG Train 1 (and the other affected facilities — Condensate, Domestic Gas, PNI, and SCA Offshore), then re-run `ZWP_RAU_CALC_PLUSCA`. The Actual columns will then populate.

---

## Issue 2 — Missing actuals on the *Monthly Contract Account Events* screen
**Same root cause as Issue 1.** That screen shows only the `*_TRGT`, `*_TRGT_YTD`, `*_YEO` accounts because the calc never created the `*_ACT` / `*_ACT_YTD` accounts (deferments unverified). Verifying deferments + re-running the calc resolves both.

## Issue 3 — "Avg YEO" not matching "Report YEO"
**Not yet investigated.** Two YEO sources at different grains exist (`SUB_004.YEO` vs `ZWP_V_REP_RAU_PERF_MTH.YEO_TTD`); to be analysed in a follow-up.

## Secondary defect (separate from the ticket's 3 issues — flag to log)
**LNG Train 2** *did* get actuals (its deferments were all Verified), **but the values are wrong** — Utilisation Actual = **3130%**, Utilisation YEO = **309%** (impossible), and its `_ACT_YTD` qty is NULL. This points to a bad **Capacity** value from Train 2's `LNG_TRAIN_2_TECHMAX` capacity stream. The calc's capacity logic was recently changed (ECPR-30901 add-LNG-Techmax 19-Mar-2026; ECPR-31040 capacity/deferment fix 19-May-2026) — a likely lead.

---

## Reproduce (read-only, from `investigation/`)
Set env then run any script: `EC_DB_DSN=dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB EC_DB_USER=ECKERNEL_EC EC_DB_PWD=*** py <script>.py`
- `proof_train1_unverified.py` — the 120/150 unverified deferment rows (Issue 1 proof).
- `diag_calc_gate.py` — both trains: verified gate + Techmax capacity reference.
- `diag_train_qty.py` — raw `RAU_*` event values per train (shows Train 2's 3130%).
- `ecaasdev_rau_recon.py`, `check_june_target_actual.py`, `diag_train_eqpm_join.py`, `get_sub004_def.py`, `extract_cdefrau_dds.py` — supporting recon + the view DDL + DDS §4.1 extraction.

---

## ⭐ RE-OPENED RCA (2026-07-03) — THREE distinct root causes (supersedes the single-cause note above)

**Context:** the ticket was closed 2026-06-29 with the "unverified deferments" cause; **re-opened 2026-06-30 by Swapnil Thakur** — he verified SCA's deferments and re-ran the RAU calc (ran clean, no error) but Issues 1/2/3 persisted. Re-investigation (read-only, ECAASDEV) shows the ticket has **three** distinct causes across facilities, not one. Report/views/Jasper are correct — all three are upstream data/calc conditions.

**Per Equipment Facility (June 2026):**

| Equipment Facility | Deferment verified | Capacity | RAU Actual written | Report Actual | Cause |
|---|---|---|---|---|---|
| PLU_LNG_TRAIN1 (LNG Train 1) | 30/150 (120 Pending) | 73,166 t ✅ | none | blank | **1** (+3 latent) |
| PLU_PNI (Interconnector) | 30/116 (86 Pending) | ok | none | blank | 1 (+3) |
| PLU_COND (Condensate) | 31/91 (60 Pending) | ok | none | blank | 1 (+3) |
| PLU_DG (Pipeline Gas) | 31/61 (30 Pending) | ok | none | blank | 1 (+3) |
| SCA_OFFSHORE (Scarborough) | 31/31 ✅ | **0** | none | blank | **2** |
| PLU_LNG_TRAIN2 (LNG Train 2) | 30/30 ✅ | ok | garbage | Util 3127% | **3** |
| PLA_OFFSHORE (Pluto A) | 62/62 ✅ | ok | valid | populated ✓ | healthy |

**Cause 1 — Unverified deferments** (Train 1, Interconnector, Condensate, Pipeline Gas): calc verification gate (`ZWP_P_DEF_RAU_CALC` body line 137, `APPROVAL_STATUS != 'V'`) skips the actual write. 296 rows still Pending. Only SCA was verified in the 06-30 re-run, so these four were never addressed. **Fix:** verify the outstanding June deferment rows, then re-run `ZWP_RAU_CALC_PLUSCA`.

**Cause 2 — Zero capacity** (Scarborough): deferments fully Verified and the calc runs clean, but `p_capacity = 0` → the write is skipped (body line 409). Root cause traced end-to-end: `ZWP_DEF_DAY_SUMMARY.CAPACITY` ← `zwp_p_defer_custom.getCapacity('EQPM',…)` = 0 for SCA. getCapacity → `getStreamReferCapacity` (SCA has no capacity stream ref) → fallback `GetPlannedVolumes` → `getGroupForecastId(SCA,'CAPACITY')` = **NULL**. SCA has forecast facility-day rows but **no `ZWP_*_CAPACITY` values loaded** (`ZWP_T_FCST_FCTY_DAY`), so no valid CAPACITY forecast group resolves → capacity 0 every June day → blank actuals AND the SCA negative auto-deferments (deferment = 0 − production). **Fix (data/config):** load Scarborough's CAPACITY forecast (`ZWP_LNG_CAPACITY`) as the other facilities have.

**Cause 3 — Negative auto-deferments** (Train 2 = >100% garbage now; latent on all facilities, ~29 rows each): auto-variation deferments book *(reference − actual)*; on ambient-uprate days (LNG "Daily Variation (ambient temp/pressure)") and demand-driven export (gas/PNI/cond) actual exceeds reference, so `DEF_QTY_DER` is negative. The calc only **warns** ("There are negative auto deferments", lines 156–162) and still sums the negatives into `(Cap − Def)/Cap × 100` → **> 100%** (Train 2 Util 3127%) and skewed YEO (Issue 3). **Fix (calc logic — author Grant Hewton):** floor/exclude negative auto-deferments in the RAU actual calc, or in the auto-deferment derivation.

**LNG Train 1 note:** capacity is **healthy** (73,166 t via the `LNG_TRAIN_1_DEF_CAP` techmax stream) — its blank actuals are **Cause 1**, not capacity. But it also has 29 negative-auto-def rows (June deferment total −373,416), so after verifying it will likely emit >100% inflated actuals like Train 2 → needs Cause 3 too.

**Issue 2** = the same missing `_ACT`/`_ACT_YTD` writes (screen shows only TRGT/YEO). **Issue 3 (YEO)** = downstream of missing/garbage actuals + the two-source grain mismatch.

**Deployed calc:** `ZWP_P_DEF_RAU_CALC` PACKAGE + BODY both VALID, body recompiled 2026-06-10 09:29; deployed source matches the client repo (mod history ECPR-30797 / 30901 / 31040).

**Env & routing:** all analysis read-only on ECAASDEV. Fixes for Causes 1–2 are operational/data; Cause 3 is a calc-logic decision. Deploy env is NOT ECAASDEV — confirm target before any change.

**New investigation scripts (this session):** `ecaasdev_rau_recon2`, `def_verify_check`, `neg_autodef_trace`/`_trace2`, `sca_capacity_trace`/`_alldays`, `sca_forecast_trace`, `sca_streamref_trace`, `fcst_setup_cmp`, `getcapacity_trace`/`_body`, `getcap_helpers`, `getgroupfcst_src`, `plannedvol_body`, `valid_group_trace`, `train1_capacity_trace`, `eqpm_type`, `fcty_names`, `pkg_details`. All read creds from env (no hardcoded credentials).

---

## Follow-up Q (2026-07-05) — "Tab 4 always shows LNG Train 1, not COND/PNI"

**Answer: not a report defect.** (1) The generated xlsx contains ALL 8 facility sections on Tab 4 (rows 11/28/45/62/79/93/110/124 — verified in the ticket's own attachment). (2) All 24 Tab-4 subreport queries filter their OWN facility (`DEF_FCTY_1_CODE`/`FACILITY_CODE`/`FACILITY` per jrxml — no copy-paste bug). (3) Train1/Train2/Cond LOOK identical because the uploaded RAU **targets are literally the same values** (Rel 98.12 / Avail 88.12 across all three; verified in `DV_SCTR_ACC_MTH_EVENT`). (4) **PNI has ZERO target events for all of 2026** (`C_PLU_PNI` — no `RAU_*_TRGT` rows) → its section shows only the derived YEO ≈ 0.333 artifact → reads as "not loaded". Actual columns differ per the 3-cause RCA. **Data fixes: upload PNI RAU targets; correct Train1/2/Cond targets if they were meant to differ.** Trace: `investigation/target_compare_across_contracts.py` (read-only, ECAASDEV).
