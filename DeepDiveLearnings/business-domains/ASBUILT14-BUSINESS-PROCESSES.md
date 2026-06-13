# Pluto As-Built 14 — Business Processes (deep dive, 2026-06-13)

Source: `WSPLU_EC_AsBuilt14_BusinessProcesses_v1.2.docx` (Woodside Doc XA0000SG1401816029
rev D; supplier WSPH_EC_DDS 14 v1.2, 13-May-2026). **Read so far: cover + Key Design
Decisions (§1.3) + full TOC + the COMPLETE Daily Production Allocation process (§2.1.1).
NOT yet read: monthly onshore/offshore (§2.1.3-2.1.5), mismeasurement/misallocation
(§2.1.6-7), monthly lock (§2.1.8), deferment (§2.2), reservoir mgmt (§2.3), GHG/Emissions
detail (§2.4) — next reading session.**

## Pluto = a PRODUCTION ALLOCATION system (official scope)
The whole EC implementation is "Pluto Hub Production Allocation System". Business processes:
- **2.1 Production Allocation** (core): Daily (Pluto+Scarborough) · Pre-Month-End · Monthly
  Onshore (Burrup LNG Park) · Monthly Pluto Offshore · Monthly Scarborough Offshore ·
  Mismeasurement · Misallocation · Monthly Lock (allocation + emission data)
- **2.2 Deferment**: Deferment Data Entry & Review
- **2.3 Production/Reservoir Mgmt**: Well Theoretical Method Mgmt · Well Alignment ·
  Monthly Pluto Reservoir Review
- **2.4 GHG/Emissions**: Monthly Emissions Actuals · Annual Emissions Reporting

Three asset scopes recur: **Burrup LNG Park (Pluto Onshore)** · **Pluto Upstream (Offshore)**
· **Scarborough Upstream (Offshore)**. Pluto Onshore has GHG allocation; Scarborough doesn't.

## Key design decisions (§1.3) — load-bearing facts
- **ZWP extension**: all Pluto-specific config is bundled in extension code **ZWP** (Z=project,
  WP=Woodside Pluto). Attributes/objects with Context Code ZWP are project-specific. (Confirms
  every ZWP_* object I've seen — calc libs, validations, packages — is custom Pluto config.)
- **Date-sensitivity** via valid-from-date mechanism (the object versioning I keep hitting).
- **GHG = EC Environmental module XEM 4.1.1 + CUSTOM NGER calcs** (Australian NGER
  Measurement Determination 2008): product calcs NGER §2.22 (fuel combustion EF), §3.87/§3.87A
  (flare CO2/CH4/N2O); custom calcs §3.73NB (produced-water CH4), §3.73F (offshore CO2/CH4),
  Ch.6 (component energy). Detail in As-Built 06.
- Scarborough emissions inherit Pluto's calc libraries as-is (no GHG allocation for Scarborough).
- `ZWP_TEMP_CALC` system attribute = short-term GCV/density calc for Scarborough until Meter
  Suite long-term solution (set "N" to disable later). `ZWP_*` system attributes are the
  config switches.
- Daily emissions calc also absorbs monthly inputs on the 1st and annual on 1-Dec.

## Daily Production Allocation flow (§2.1.1) — fully mapped
Swimlanes: Energy Components · Operator · IT Support · OIM · PAE. The loop:
1. **Review/Update/Insert data** — well/stream/tank/equipment daily-status screens (see map).
2. **Run Daily Mass Balance** (offshore `ZWP_DAILY_MB_OFFSHORE_V0` + onshore
   `ZWP_DAILY_MASS_BALANCE_V0`) → balanced? loop until yes.
3. **Run Daily Onshore Allocation** `ZWP_ALLOC_ONSHORE_DAY_V0` + **Daily Offshore Allocation**
   `ZWP_ALLOC_SCA_OFFSHORE_DAY_V0` (Pluto+Scarborough) via **Daily Allocation (HA.0002)**.
4. **Review allocation results** → **Generate reports** (RP.0003) → **QC2 approve** → set input
   data **Verified** (Daily Data Status Processes HA.0001) → **issue/publish** asset+partner
   reports. QC3 notification (N_QC3_NOTIFCATION) every 15 days.

### Screens (codes I can now map to the treeview)
HA.0002 Daily Allocation · HA.0001 Daily Data Status Processes (P/V/A) · PO.0002 Daily Gas
Stream Status · PO.0085/PO.0001 Daily Liquid Stream · PO.0066 Daily Electrical Stream ·
PO.0003 Daily Water Stream · PO.0020/PO.0019 Stream Gas/Liquid Component Analysis · PO.0005.02
Daily Tank Status VCF · CO.0011 Daily Equipment Status · WR.0001 Daily Production Well Status 1
(**Pluto wells**) · WR.0027 Daily Production Well Status 2 (**Scarborough wells**) · WR.0010.01
Well Gas Component Analysis · CO.0250 Manage Well · CO.0086/CO.0156 Stream/Well Reference Value ·
CO.0211 Swing Well Connection · CO.0204 **Validation Overview Pluto Scarborough** ·
**CO.0130 Schedules** · **IS.0006 Upload Files** · XEM.0001 Stream Emissions Daily · SA.* contract
account/equity/parties screens · ZZ.0001/ZZ.0002 Deferment · TO.0017 BL/MR Light · RP.0003 Report Admin.

### Interfaces
Inbound: **I_IN_PHD_DAILY** (PHD Field Data Ingest — THE PHD interface behind the ECIS task!) ·
I_IN_DOMGAS · I_IN_CARGO_JV_ENT_DAILY · I_IN_TAS (truck LNG). Outbound: I_OUT_EDP_NON_CORP ·
I_OUT_EDP_CORP_DAILY · I_OUT_PPML (reports). Detail in As-Built 05 Interfaces.

### Validations (the Issue_1052 family — now in business context!)
- **V_DAILY_SAMPLING_VALIDATION** — component-analysis quality (% within range = MY sum-check
  rules 1156/1157; mandatory fields).
- **V_DAILY_PHD_VALIDATION** — imported PHD quality (no negative pressure/mass; onstream=0 if
  shut-in = the frozen/threshold checks).
- V_IN_PHD_THRESHOLD · V_DLY_MISSING_DATA_VALIDATION (the missing-data layer I flagged in
  Issue_1052!) · V_DEF_MANDATORY · V_DOMGAS · V_CARGO. All surfaced via **CO.0204** = the exact
  screen my validation_overview automation drives.

## 🔑 Direct ties to my work (why this matters)
- **Issue_1052** = the Validations section of the daily allocation process. CO.0204 +
  V_DAILY_PHD_VALIDATION + V_DAILY_SAMPLING_VALIDATION + V_DLY_MISSING_DATA_VALIDATION are
  exactly what I've been validating. The "missing data" layer I identified maps to
  V_DLY_MISSING_DATA_VALIDATION.
- **ECIS PHD-backup task** = a backup path for **I_IN_PHD_DAILY** (PHD Field Data Ingest),
  run via CO.0130 Schedules with files through IS.0006 Upload Files — the exact screens I
  built CLAUDE_WELL_TEST on. The real interface to study is in As-Built 05.
- **My TEST-CASE-BACKLOG** can now be re-grounded in the REAL Pluto process names (e.g. P1
  daily-cycle smoke = this §2.1.1 flow; the oracle screens/calcs are named here).

## Validations detail (§2.1.1.8, confirmed) — Issue_1052 spec, verbatim
- **V_DLY_MISSING_DATA_VALIDATION**: "enforces the PRESENCE of imported PHD data; throws an
  error if a data element is missing." → this is EXACTLY the missing-data layer I flagged in
  Issue_1052. Now I have the official name + intent.
- **V_IN_PHD_THRESHOLD**: errors if imported quantity < threshold % (e.g. 90% of a day's data
  elements) — a completeness gate distinct from per-value quality.
- V_DAILY_PHD_VALIDATION (no negative pressure/mass; onstream=0 if shut-in),
  V_DAILY_SAMPLING_VALIDATION (component % in range + mandatory), V_DEF_MANDATORY
  (Unplanned deferment needs Trip/Slowdown+Cause+Sub-Cause), V_DOMGAS, V_CARGO.
- **Full validation detail lives in As-Built 09 Validations** ← the Issue_1052 reference doc.

## Roles + QC gates (§2.1.1.9-10)
Roles: **PAE / ALLOC_PROC** (verify+approve after QC2) · **OIM / SUPERVISOR** (verify+approve
up to QC2) · **Operator / OPERATOR** (data entry, run calcs, provisional reports) ·
**IT Support / SUPPORT_ADM** (PHD import issues, rerun PHD interface). QC2 = a set of
status processes `SP_IN_{ONSH|OFFSH}_{METERLIMS|EMIS|TOPS|WELL}_{PLU|SCA}_P_V` lifting input
data P→V per data category/asset. Detail: As-Built 12 (Roles) + As-Built 15 (Status Process).

## Newly-discovered sibling As-Built docs to fetch
- **As-Built 09 Validations** — the Issue_1052 home (V_* rule definitions).
- As-Built 12 Roles and Access · As-Built 15 Status Process.
(Add these to PLUTO-ASBUILT-INDEX — the series has >14 volumes incl. 09/12/15.)

## Monthly Allocation + GHG/Emissions + PRRT (§2.1.3-2.4, extracted 2026-06-13)
Read via keyword extraction of the saved doc (monthly + emissions swimlanes). New calc
libraries + governance beyond the daily flow:
- **Monthly calc libraries**: `ZWP_ALLOC_ONSHORE_MTH_V0` (monthly onshore allocation),
  `ZWP_COMMERCIAL_MTH_V0` (monthly commercial calc), `ZWPC_EMISSION_DISCHARGE` (monthly
  emission+discharge, run on **Daily Allocation HA.0002**), **`ZWP_PRRT_MTH_V0`** (PRRT =
  **Petroleum Resource Rent Tax** — Australian tax calc!). Run via **Monthly Allocation
  (HA.0003)**; status via **Monthly Data Status Processes (HA.0004)**.
- **Emissions screens**: **Stream Emissions Daily (XEM.0001)** (results store/visualize) +
  **Stream Emission Configuration (XEM.0002)** (per-stream emission setup — # stations,
  methane EF, GCV/density/composition refs). Monthly Onshore Emissions runs **for Pluto only**
  (Scarborough inherits Pluto's libs, no GHG allocation).
- **GHG = XEM 4.1.1 product calcs + custom NGER** (Australian NGER Measurement Determination
  2008): product NGER §2.22 (fuel-combustion EF), §3.87/§3.87A (flare CO2 / CH4+N2O); **custom**
  §3.73NB (produced-water CH4), §3.73F (offshore CO2+CH4), Ch.6 (component energy). Detail =
  As-Built 06. Custom calcs survive XEM upgrades but need stream-emission-config rework if
  Woodside later adopts product NGER calcs.
- **Monthly governance**: QC3 (set input Approved) → run calcs → **QC4** → Final PAA reports;
  WD1/WD5 working-day milestones; revert-to-Provisional path for corrections; status processes
  `SP_IN_ONSH_{TRUCK|EMIS}_*_V_A` (V→A) and `SP_OUT_ONSH_{ALLOC|EMIS|COMM}_CALC_PLU_P_V` (output
  P→V). Monthly inputs via Excel: **I_IN_UPLOAD_GAS_OIL_GREASE** (→ Monthly Gas/Liquid Stream
  Status PO.0024/PO.0041; goes Provisional→Approved after review) — another manual-Excel
  interface alongside the As-Built 05 set.

## EFK A4 (Environment/GHG) — blocker + resolution (2026-06-13)
EFK's "EC Environment Management" page only links to a legacy Tieto space
(ecpedia.eu.tieto.com/display/XEM — not reachable via this MCP) and its child is an empty
training template. **Resolved by redirecting GHG learning to the Pluto As-Built (this doc
§2.4 + As-Built 06 Calculations)** — Pluto-specific and reachable, higher value. So EFK A4 =
covered-by-redirect, no separate EFK content exists.

## Next reads (As-Built 14 remainder + siblings)
1. §2.4 GHG/Emissions (new scope — XEM + NGER; affects emission test cases).
2. §2.1.3-2.1.5 monthly allocation (the month-end + lock governance).
3. §2.2 Deferment execution steps.
4. **As-Built 05 Interfaces** (I_IN_PHD_DAILY design = directly feeds the ECIS real task).
5. **As-Built 06 Calculations** (ZWP_ALLOC_* + NGER custom calcs).
