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
