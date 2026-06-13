# Pluto As-Built 07 — Reports (deep dive, 2026-06-13)
Source: `WSPLU_EC_AsBuilt07_Reports_v1.0.docx` (V1.1, 156pp). Read: full report list (TOC) +
intro. The allocation system's OUTPUTS = 35 reports, generated/approved/issued via Report
Administration (RP.0003). NOT read: each report's per-field layout (reference-grade).

## Report catalog (by theme)
**Daily allocation/asset**: R_PLU_SCA_DAILY_ASSET · R_PLU_DAILY_PARTNER · R_SCA_DAILY_PARTNER ·
R_BLP_DAILY_PROD_ALLOC_PLUTO · R_BLP_DAILY_PROD_ALLOC_SCARBOROUGH.
**Monthly allocation**: R_PLU_MONTHLY_PROD_ALLOC · R_SCA_MONTHLY_PROD_ALLOC ·
R_BLP_MONTHLY_ALLOC_PLUTO · R_BLP_MONTHLY_ALLOC_SCA · R_BLP_LNG_T1 / R_BLP_LNG_T2 (Train Manager).
**Regulatory / fiscal (Australian — big theme)**:
- R_BLP_PETROLEUM_STATISTIC (Australian Petroleum Statistics).
- R_PLU_NOPTA / R_SCA_NOPTA (**NOPTA** = National Offshore Petroleum Titles Administrator).
- R_PH_PRRT_PLUTO / R_PH_PRRT_SCARBOROUGH (**PRRT** tax reports — from C_PRRT calc).
- R_PH_RESERVES (reserves; marked insufficient info).
**Emissions / GHG (XEM + NGER scope)**: R_PH_MONTHLY_EMISSIONS · R_PH_ASSET_GHG (monthly) ·
R_PH_ANNUAL_EMISSIONS_NGER (**NGERS**) · R_PH_ANNUAL_NPI_EMISSIONS (**NPI** = National Pollutant
Inventory) · R_BLP_PLU_ANNUAL_EMISSIONS_SGM_PV / R_SCA_..._SGM_PV (**Safeguard Mechanism** PVs) ·
R_PH_MONTHLY_EMISSIONS_LIABILITIES · R_PH_ANNUAL_GHG_CHANGES · R_PH_EMISSIONS_RERUN ·
R_PH_ANNUAL_EMISSIONS (corporate).
**Deferment**: R_PH_MONTHLY_RAU (Deferments + RAU).
**Audit / governance**: R_PH_DAILY_PAT_MONITORING (system monitoring) · R_PH_DATA_CHANGES ·
R_PH_PERIOD_CONFIG_CHANGE_SUMMARY · R_PH_ACCESS_MANAGEMENT_CHANGE.
**Other**: R_BLP_MISMEASUREMENT · R_BLP_OFFTAKE.
**ON HOLD**: R_MONTHLY_WELL_ALLOC_REVIEW (Reconciliation Factor review) · R_PH_MONTHLY_CSA_PSA_
TOLLING_ACTUALS.

## Insight
Pluto's reporting is dominated by **Australian regulatory obligations** — NOPTA titles,
Petroleum Statistics, PRRT (profit tax), and a full emissions stack (NGER, NPI, Safeguard
Mechanism). This is the "why" behind the GHG/PRRT calc complexity in As-Built 06: the outputs
are statutory submissions, so the validations (As-Built 09) and calc accuracy matter legally.
Reports are the terminal stage of the daily/monthly flow (As-Built 14): data → validate →
allocate → emissions/PRRT → **report → QC approve → issue/publish**.

---
# CAPSTONE — Pluto As-Built series (read 02/05/06/07/09/14)
The end-to-end Pluto "Production Allocation System" now mapped:
```
MASTER DATA (As-Built 03 objects; screens cat. As-Built 02, SI units degC/MPa/Sm3)
  │
INBOUND (As-Built 05): I_IN_PHD_DAILY (OPC UA auto tag feed, Honeywell PHD) + DOMGAS/CARGO/TAS;
  manual Excel backups (ZWP_INTERIM_DATA_UPLOAD, I_IN_MISMEASURED_CORRECTED) ← the ECIS task
  │
VALIDATE (As-Built 09): V_DAILY_PHD/MISSING_DATA/SAMPLING (rules incl. 1156/1157, 1058-1074),
  via Validation Overview (CO.0203/0204) ← Issue_1052
  │
CALCULATE (As-Built 06): mass balance → ZWP_ALLOC_* → ZWPC_EMISSION_* (CO2e/NGER) → C_PRRT;
  component set C1-nC5; writes PWEL_DAY_ALLOC / STRM_MTH_ALLOC / SCTR_ACC_*
  │
PROCESS/GOVERN (As-Built 14): daily + monthly flows, QC2/3/4, P→V→A status, month lock
  │
REPORT (As-Built 07): 35 reports — daily/monthly allocation + NOPTA/PRRT/Petroleum-Statistics
  + NGER/NPI/Safeguard emissions + audit. Issued via RP.0003.
```
**My two live tasks sit inside this chain**: ECIS = the inbound manual-Excel backup; Issue_1052
= the validation gate. Everything I automate (Assets/Dispatching objects) = the master data it
runs on. Remaining As-Built (01 SystemConfig attrs, 03 ObjectConfig xlsx, 11 Notification) =
reference, lower priority. As-Built deep dive: SUBSTANTIVELY COMPLETE.
