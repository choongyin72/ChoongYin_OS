# EC Business Glossary — industry meaning ↔ EC meaning ↔ tables
Cumulative, grows per domain dive. (Started 2026-06-13.)
Canonical full industry acronym list = **EC Vocabulary** (EFK `1844980`); this glossary keeps only
terms that tie to EC tables/screens I touch or are EC-specific — cross-checked vs EC Vocabulary 2026-06-14.

| Term | Industry meaning | In EC | Key tables/screens |
|---|---|---|---|
| **Production day** | The 24h operational day (often not midnight-midnight) | InitiateDay instantiates each day's empty status rows; Production Day Definition objects set day-start | SYSTEM_DAYS, PROD_DAY defs |
| **Daily status** | The day's measured/entered values per object | `*_DAY_STATUS` rows per well/equipment/stream/tank, record status P | PWEL_DAY_STATUS etc. |
| **Allocation / reconciliation** | Splitting commingled production back to contributing wells so each owner gets its share | Calculation over an allocation NETWORK (nodes+streams); daily + monthly; writes `*_DAY_ALLOC` | PWEL_DAY_ALLOC, STRM_DAY_ALLOC; CO.0084 |
| **Theoretical rate** | A well's expected rate from its last test | Well test results feed allocation basis | PWEL_RESULT, PT.* screens |
| **Deferment / LPO** | Production lost vs plan (downtime/constraint); "Lost Production Opportunity" | PD.0020 events; Loss = rate×downtime or volume; precedence rules | DEFERMENT_EVENT, DEFER_LOSS_* |
| **Record status P/V/A** | Data quality ladder: provisional → verified → approved | Status Processes (CO.0076) lift statuses; month lock freezes | RECORD_STATUS col everywhere |
| **Month lock** | Closing the books for a month — no further changes | Monthly Data Locking screens; processes refuse locked months | HCA section |
| **Nomination** | A shipper's request to move/take gas on a day (with renomination cycles during the day) | Nomination Entry/Daily Nomination; cycles TIMELY/EVENING/ID1.. define deadline times | NOMPNT_DAY_NOMINATION, NOMINATION_CYCLE |
| **Gas day offset (D-1/D)** | Whether a nomination deadline falls the day before (D-1) or on the gas day (D) | Gas Day Offset dd on Nomination Cycle | NOMINATION_CYCLE.GAS_DAY_OFFSET |
| **Entitlement** | What an owner is contractually allowed to lift (accrues with production share) | Lifting Account daily forecast/official balances | LIFT_ACC_DAY_* |
| **Lifting / cargo** | Physically taking product by tanker | Cargo status ladder T→R→C→A on top of record status; nomination→instruction→BL/MR | CARGO_TRANSPORT, VOY_CARGO_ACT |
| **BL/MR** | Bill of Lading / Measurement Report — official loaded quantities | TO.0005 closes the cargo and sets official quantities | LOAD qty → Revenue |
| **Demurrage / laytime** | Penalty when loading exceeds agreed port time | TO.0007/0015 with dynamic form layout (Create buttons!) | — |
| **Take-or-Pay** | Buyer pays for a minimum quantity even if not taken | Contract Account quantity computed by sales calc rules | CNTRACC_* |
| **Price index** | Published market price series feeding contract price formulas | Daily/Monthly Price Index (+datasets); Price Objects compute via rule sets | PRICE_*, PRODUCT_PRICE_* |
| **Stream item** | Revenue's tracked quantity unit (a measurable commodity flow) | Quantity module; accruals ACCRUAL→FINAL when actuals late | STIM_* (VO.* screens) |
| **Booking period** | Accounting period a financial doc posts into | Doc lifecycle OPEN→VALID1→VALID2→TRANSFER→BOOKED; close requires all BOOKED | Financial Transaction screens |
| **Accrual (revenue)** | Estimated value booked before actuals arrive, reversed later | RUN ACCRUAL methods; ERP accrual reversals | — |
| **Royalty** | Government/owner share of production value | Royalty Canada/USA engines | Royalty branch |
| **Injection point / dosage** | Where chemicals are injected & how much per produced volume | ChemCalc* CRON schedules compute target vs actual | CHEM_INJ_POINT_STATUS, CHEM_TANK_STATUS |
| **Groupmodel (EC)** | — (EC concept) | Hierarchical object filters driving navigators + visibility; Op/Cp/Geo parents live in the groupmodel layer, NOT as object columns (Pipeline lesson!) | `oa.*` sources in OV views |
| **Business action / job action** | — (EC concept) | Scheduler unit (e.g. ECISAction) + chained job actions with params | TV_ACTION_INSTANCE(+_PARAM), ACTION_JOB_CONFIG |
| **Custody transfer** | The point where ownership/value of product changes hands — metered to fiscal accuracy | Export/sales-point metering is high-accuracy; drives why allocation exists | (HCA allocation network) |
| **Fiscal measurement** | A meter reading used for taxation/royalty (e.g. flare-gas meter if taxed) | Higher-accuracy meters at custody/fiscal points vs poorly-metered/estimated wells | flare metering |
| **Why allocate (rationale)** | Wells are poorly metered (low accuracy / estimated); the total at the export/custody meter is accurate | EC measures the accurate total + allocates it back to wells by theoretical/estimated rates (reconciliation factors pro-rate the gap) | allocation network, RF |
| **Standard vs Normal Conditions** | Reference temp/pressure for reporting gas/liquid volumes | **Standard = 15°C + 1 atm** (e.g. Sm3/d flow rates); **Normal = 0°C + 1 atm**. The basis VCF corrects observed volumes TO | feeds VCF (`vcf-calculation.md`), flow rates |
| **ACL (Access Control List)** | — (EC concept) | Drives the ACCESS screens of EC Configuration; **Object Partition** screen has a **'Refresh ACL'** button to make changes take effect immediately | Object Partition / ACCESS screens |
| **ACQ / DCQ / MDQ** | Gas-contract quantities: Annual / Daily Contract Quantity + Maximum Daily Quantity the buyer must take / seller deliver | Sales contract terms validated against nominations (shortfall/take-or-pay) | EC Sales (contracts, nominations) |
| **TSA / TSO** | Transport Service Agreement (sign to become a pipeline shipper) / Transport Service Operator (confirms nominations, runs the transport schedule); GTA = Gas Transport Agreement = TSA | Place shippers' nominations to the TSO; TSO confirms | NOMINATION_CYCLE, EC Sales |
| **PSA (Production Sharing Agreement)** | Contract between a government and an extraction company splitting production | Royalty/PSA accounting splits | Royalty branch, Revenue RTY |
| **CGR / GOR** | Condensate-to-Gas Ratio / Gas-to-Oil Ratio — liquid vs gas produced at standard conditions | Production ratios feeding allocation/test basis | PWEL_* rates, well test |
| **Diluent** | Light hydrocarbon added to heavy/extra-heavy crude to cut viscosity for transport (recovered later by distillation) | An allocated quantity in the allocation result | PWEL_DAY_ALLOC.ALLOC_DILUENT_VOL |
| **Recovery Factor** | % of oil/gas in place that's economically recoverable (gas ~60-70% water-drive, up to 90% depletion-drive) | Reserves/UOP + forecasting basis | Revenue FC/reserves, IAM |
| **Lifter / Lifting Account** | The company holding ownership of the petroleum product / the ledger tracking how much of each product it has available | Daily forecast + official lifting balances; entitlement accrues with production share | LIFT_ACC_DAY_* |
| **Reconciliation Factor (RF)** | The pro-rating factor closing the gap between summed well/stream estimates and the measured total | Per product/well/stream, daily+monthly; \|RF\| over a threshold raises a validation WARNING | V_ALLOC_* checks; RFw_ProdHC etc. |
| **CO2e / Emission Factor / Emission Intensity** | CO2-equivalent (GHG weighted by GWP); EF = emission per unit activity; intensity = emission per unit production | ZWPC_EMISSION_DISCHARGE 11-step calc: component EF → CO2e EF → CO2e emission → pollutant → intensity | ZWP_EMIS_STRM_DATA, XEM.0001 |
| **PRRT** | Petroleum Resource Rent Tax (Australian profit-based tax on petroleum projects) | C_PRRT calc: Pluto PRRT Feed → Phase Points (Pluto + Scarborough) | ZWP_PRRT_MTH_V0 |
| **RAU** | Rate of Average Uptime / restricted availability (deferment-related) | C_DEF_RAU_CALC (deferment + RAU) | DEFER_* |
| **Component set** | The fixed list of hydrocarbon components a gas analysis/allocation tracks | Pluto single set: C1,C2,C3,iC4,nC4(=C4),iC5,nC5(=C5/C5+) — shared by allocation + emissions | STRM_GAS_COMPONENT, COMPONENT_CONSTANT |
| **Lifting year vs calendar year** | Cargo-lifting accounting year differs from calendar | Calendar = Jan-Dec; **lifting-account year = Apr-Mar** (year-till-date totals differ) | SCTR_ACC_* cumulative |
| **EFK ↔ RD130** | — | EFK "EC Knowledge" pages are thin intros; depth lives in the **RD130 Release Documentation** Confluence space + the Pluto As-Built. Use RD130 for any future product deep-dive. | — |
