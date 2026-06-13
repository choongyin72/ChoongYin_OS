# Pluto As-Built 09 — Validations (deep dive, 2026-06-13) — THE Issue_1052 spec
Source: `WSPLU_EC_AsBuilt09_Validations_v1.0.xlsx` (read in full via read_resource).
The authoritative catalog of every Pluto validation rule, its object/attribute, type, severity,
and **Check Rule ID** — directly the Issue_1052 reference. Confirms my prior findings.

## 🔑 Three validation LAYERS (confirms my "2 missed layers" Issue_1052 note)
Each rule is tagged across 3 columns: **Validated By Screen** / **Validated by Check Rule** /
**Validation by Calculation**. So a rule can be enforced at the screen (on-save), as a
CTRL check-rule (Validation Overview / batch), and/or inside an allocation calculation.
Validation Type values seen: `SCREEN, CHECK_RULE` (both) · `CHECK_RULE` only · (calc rules: NA).

## Validation groups + Check Rule IDs (the catalog)
**V_DAILY_PHD_VALIDATION** (PHD data quality) — STRM_DAY_STREAM_MEAS_GAS:
- 1040 GRS_MASS ≥0 (ERROR, screen+rule) · 1039 GRS_VOL ≥0 · 1041 MEASURED_ENERGY ≥0
- + per-object: onstream-hrs=0 if SHUT IN (WARNING), mass rates=0 if hours online=0, hours 0-24,
  **Frozen Value (1-day default)**, **Std-Dev band (±X σ over previous Y, optional min threshold)**,
  **% Difference vs Previous** (configurable). (These = the frozen/stddev/threshold checks.)

**V_DAILY_MISSING_DATA_VALIDATION** ("All PHD input values mandatory, else Error") — the
mandatory-presence layer I flagged. Check Rule IDs + attributes:
- 1058 STRM_DAY_STREAM_MEAS_GAS.GRS_MASS · 1068 STRM_DAY_STREAM_MEAS_WAT.GRS_VOL_WAT ·
  1069 STRM_SUB_DAY_STATUS_GAS.GRS_MASS · 1073 STRM_DAY_STREAM_MEAS_ELE.POWER_CONSUMPTION ·
  1074 TANK_DAY_INV_OIL.CLOSING_GRS_VOL
- **PWEL_DAY_STATUS 1059-1067**: ON_STREAM_HRS, AVG_FLOW_MASS, AVG_COND_MASS, AVG_GAS_MASS,
  AVG_WATER_MASS, AVG_BH_PRESS, AVG_BH_TEMP, AVG_WH_PRESS, AVG_WH_TEMP (all mandatory).
- (sheet note on 1058: "covered by row 82… Tushar please verify" — an open authoring TODO.)

**V_DAILY_SAMPLING_VALIDATION** (component analysis) — WELL_GAS_COMPONENT + STRM_GAS_COMPONENT:
- min/max range per component (0-100 if unset); **sum 98-102% pre-normalisation else ERROR**;
  missing-mandatory; **Frozen State**; **% diff vs previous**; **Std Dev**.
- IDs: WELL_GAS_COMPONENT 1081-1086; STRM_GAS_COMPONENT 1075-1080, 1122;
  **1156 = Stream Gas Component Analysis COMP_MOL_PCT sum 98-102%**,
  **1157 = Well Gas Component Analysis COMP_MOL_PCT sum 98-102%** ← MY Issue_1052 rules, confirmed.
  (WT% sum checks are the COMP_WT_PCT rows 1076/1077 etc.)
- V_SAMPLING_VALIDATION (CARGO_ANALYSIS_COMPONENT): BoL composition sums to 100% for cargo loadings.

**V_DEF_NEGATIVE / V_DEF_MANDATORY** (ZWP_DEF_DAY_DETAIL deferment): DEF_QTY_DER negative-on-auto
highlight; TRIP_SLOWDOWN/CAUSE/SUB_CAUSE mandatory if Category=Unplanned (else error).

**Allocation/calc validations** (Daily/Monthly Allocation Screen; Validation by CALCULATION):
- V_MASS_BALANCE_DAY/MTH: imbalance > overall uncertainty (M_MassBalImbalance vs M_OverallUncert).
- V_ALLOC_ONSHORE_DAY/MTH, V_ALLOC_OFFSHORE_MTH: allocated values ≥0 (except Net Condensate
  Crossover); product-allocation % sums to 100%; mass fractions sum to 1; |Reconciliation Factor|
  > preconfigured → WARNING (Condensate/Export LNG/Well RFs); trucked BoL mass = PHD mass ±tol.
- V_REALLOC_EVENT: a reallocation event must exist before reallocation runs.

**Governance/monthly**:
- V_DAILY_DATA_APPROVED: all daily records must be Approved before the monthly provisional BPM
  can start (PWEL/STRM day status, IDs incl. 1125-1141).
- V_MONTHLY_COMPLETENESS_CHECK (STRM_MTH_LIQ_DERIVED, STRM_DAY_STREAM_DER_GAS/OIL),
  V_MONTHLY_MISSING_DATA_VALIDATION (STRM_MTH_LIQ), V_MONTHLY_INPUT_DATA (DV_STOR_DAY_EXPORT_STATUS;
  part-lifting EXPORTED_QTY/QTY2 mandatory ≥0).
- **Emissions validations**: GRS_MASS/GRS_VOL/ENERGY ≥0 **AND `ZWP_INC_IN_EM_VAL='Y'` AND
  `*_METHOD IS NOT NULL`** (only streams flagged "Include in Emissions Validation").

## Ties to Issue_1052 (live task) — actionable
- My committed work (sum/MOL% rules 1156/1157) = confirmed correct + located in the catalog.
- The **missing-data layer** I flagged = V_DAILY_MISSING_DATA_VALIDATION, IDs 1058-1074 (full
  attribute list above) — now I have the exact rule IDs + attributes to build/verify.
- The **Class Validation / SCREEN layer** = the "Validated By Screen" column (SCREEN,CHECK_RULE
  rows) — the second missed layer; the catalog says which rules fire on-screen vs batch.
- Frozen/StdDev/%-diff checks all catalogued with IDs → maps to my frozen-check + ZWP_P_VALIDATION work.
- The "Tushar please verify (1058)" note = an open spec ambiguity to raise.

## Decision
As-Built 09 = highest-value live-task read this session. Issue_1052 resume memory updated.
Remaining As-Built: 06 Calculations (the calc formulas behind these), finish 14 monthly detail.
