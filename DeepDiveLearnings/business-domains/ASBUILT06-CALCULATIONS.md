# Pluto As-Built 06 — Calculations (deep dive, 2026-06-13)
Source: `WSPLU_EC_AsBuilt06_Calculations_v1.0.docx` (105 pages). **Read: TOC + intro/design
decisions + the calc-variable read/write patterns + emissions & GHG calc structure (extraction).
NOT read line-by-line: every step's full formula (105pp) — captured the model + inventory +
data-flow, which is the durable value.**

## Calculation inventory (the ZWP_*/C_* libraries behind the flows)
- **Allocation**: ZWP_ALLOC_ONSHORE_DAY/MTH, ZWP_DAILY_MASS_BALANCE, ZWP_DAILY_MB_OFFSHORE,
  C_ALLOC_OFFSHORE_MTH, C_SCA_ALLOC_OFFSHORE_DAY/MTH (Pluto + Scarborough, daily + monthly).
- **Commercial**: ZWP_COMMERCIAL_MTH, ZWP_EMIS_COMM_MTH_CALC (onshore monthly emissions commercial).
- **Tax**: **C_PRRT** (Petroleum Resource Rent Tax) — Pluto PRRT Feed → Pluto Phase Points →
  Scarborough Phase Points.
- **Deferment**: C_DEF_RAU_CALC (Deferment + RAU = Rate of Average Uptime / restricted-avail).
- **Emissions** (the NGER implementation): ZWPC_EMISSION_DISCHARGE (Burrup LNG Park onshore,
  11 steps), ZWPC_EMISSION_DISCHARGE_OFFSHORE (Pluto Upstream), ZWPC_SCA_EMISSION_DISCHARGE
  (Scarborough).

## Component set (standard, allocation + emissions)
C1 · C2 · C3 · iC4 · **nC4** (holds C4 if only C4 given) · iC5 · **nC5** (holds C5/C5+ if only
those given). Single shared component set across allocation + emissions.

## Calc engine model (variables ↔ class.column — the concrete pattern)
Calcs read/write via named variables bound to a `CLASS.COLUMN` at a grain (stream/day,
contract/account/day, …). Examples (Table 15/22/26):
- READ: `InitialNMass(Stream,day) ← STRM_DAY_STREAM_DATA.THEOR_NET_MASS`;
  `WFrac(Stream,day,component) ← STRM_DAY_COMP_DATA.WT_FRAC`;
  `ZWP_rStrmTotCO2e(Stream,Day) ← ZWP_EMIS_STRM_DATA.EMIS_VALUE` (**custom class consolidating
  Emission-Module output**); `ZWP_CompConst_IdealGCV ← COMPONENT_CONSTANT.IDEAL_GCV`;
  system attrs ← `SYSTEM_ATTRIBUTE.ATTRIBUTE_VALUE`.
- WRITE: monthly stream `STRM_MTH_ALLOC.{NET_MASS,NET_VOL,ENERGY}` +
  `STRM_MTH_COMP_ALLOC.ALLOC_NET_MASS`; contract accounts
  `SCTR_ACC_DAY_STATUS / SCTR_ACC_DAY_CPY_STATUS.{MASS_QTY,VOL_QTY,ENERGY}` (+ company split).
- Everything carries **Mass / Volume / Energy / CO2e**; contract-account data tracked Daily /
  Monthly / **Cumulative** (total-till-date + year-till-date). Calendar year = Jan-Dec, but
  **lifting year = Apr-Mar** (good test-edge fact).

## Emissions calc (ZWPC_EMISSION_DISCHARGE) — 11 steps
Pre: write stream inputs to allocation tables → 1 init/read **Stream Component Analysis**/reset
→ 2 init activity by stream class+attr → 3 **Component Emission Factor** → 4 EF conversion →
5 Gas Emission → 6 Component Emission → 7 Component **CO2e** EF → 8 Component CO2e Emission →
9 Pollutant Emissions + custom energy → 10 **Emission Intensity** → 11 post-calc.
GHG allocation: compute CO2e mass per stream (from Emissions) → ratios per user group/user →
GHG quantity per the Onshore Allocation procedure; streams grouped via **Stream Set Lists**.

## 🔑 The full data-flow chain (ties ALL my work together)
PHD daily field data (I_IN_PHD_DAILY, As-Built 05) → **validations** (Issue_1052 / As-Built 09:
PHD-quality + missing-data + **component sum 98-102% rules 1156/1157**) → **Mass Balance** →
**Allocation** (ZWP_ALLOC_*) → **Emissions/CO2e** (ZWPC_EMISSION_*, consuming the SAME stream
component analysis the validations guard) → **Contract Accounts** (SCTR_ACC_*) + **PRRT** →
Reports. So Issue_1052's component-analysis validations are the quality gate protecting the
emissions + allocation calc inputs — not a standalone checker.

## Cross-links / decision
Deepens production.md (allocation), ASBUILT14 (flow), ASBUILT09 (validations), TEST-CASE-BACKLOG
(P-tier oracles can now name the write-tables: STRM_MTH_ALLOC, SCTR_ACC_DAY_STATUS, ZWP_EMIS_*).
As-Built series now read: 05, 06, 09, 14. Remaining: 01 SystemConfig, 02 Screens, 03 ObjectConfig,
07 Reports, 11 Notification (lower priority). Good session checkpoint.
