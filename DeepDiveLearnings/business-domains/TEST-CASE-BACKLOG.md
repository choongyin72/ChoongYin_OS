# Business Test-Case Backlog (phase-2 candidates — FOR CHOONG-YIN'S REVIEW)
Consolidated from the 5 domain dives (2026-06-13), then SHARPENED with concrete oracles from
the Pluto As-Built (14 Business Processes, 06 Calculations, 09 Validations). Each has a
DB-verifiable oracle. Nothing gets built until reviewed/prioritized by Choong-Yin.

## As-Built-grounded anchors (use these exact names when building)
- **Process names** (As-Built 14): Pluto Scarborough Daily Production Allocation; Pre-Month-End;
  Monthly Onshore (Burrup LNG Park); Monthly Pluto/Scarborough Offshore; Mismeasurement;
  Misallocation; Monthly Lock. Calc libs: ZWP_ALLOC_ONSHORE_DAY/MTH, ZWP_DAILY_MASS_BALANCE,
  C_SCA_ALLOC_OFFSHORE_DAY/MTH, ZWP_COMMERCIAL_MTH, ZWPC_EMISSION_DISCHARGE(_OFFSHORE/_SCA), C_PRRT.
- **Run/verify screens**: Daily Allocation HA.0002 / Monthly Allocation HA.0003; Daily/Monthly
  Data Status Processes HA.0001/HA.0004; Validation Overview Pluto Scarborough CO.0204.
- **Write/oracle tables** (As-Built 06): PWEL_DAY_ALLOC, STRM_MTH_ALLOC(.NET_MASS/NET_VOL/ENERGY),
  STRM_MTH_COMP_ALLOC.ALLOC_NET_MASS, SCTR_ACC_DAY_STATUS(.MASS_QTY/VOL_QTY/ENERGY +_CPY), XEM/
  ZWP_EMIS_STRM_DATA.EMIS_VALUE. Edge: lifting-year Apr-Mar vs calendar Jan-Dec.
- **Validation rule IDs** (As-Built 09): missing-data 1058-1074; sampling sum 98-102% 1156/1157
  (+1076/1077 WT%); frozen/stddev/%-diff per object; V_DAILY_DATA_APPROVED gates monthly BPM.

Nothing gets built until reviewed/prioritized by Choong-Yin (+ As-Built scope check).

## Tier 1 — core loop, high Pluto relevance, lowest dependency
| # | Test | Oracle | Pre-req |
|---|---|---|---|
| P1 | **Daily-cycle smoke**: InitiateDay → enter one well-day → DailyProductionAllocation → dashboard | new SYSTEM_DAYS day + PWEL_DAY_STATUS rows; PWEL_DAY_ALLOC row for the well | scheduler healthy (currently STALLED on sandbox!) |
| P2 | **Status lifecycle P→V→A + month lock**: insert P data → verify → approve → lock → write rejected | RECORD_STATUS transitions; locked-month write error | status processes configured |
| S1 | **Nomination → delivery chain** (daily gas): nominate → confirm → delivery reflects qty; renominate → revision | NOMPNT_DAY_NOMINATION + delivery rows | seed contract/nompnt |
| E1 | **ECIS backup-path E2E** (= the real task's acceptance test): upload Excel when "PHD down" → staging review → promote → data identical to PHD path | PWEL/staging/target rows | CLAUDE_WELL_TEST pattern (proven) |
| V1 | **Issue_1052 regression pack as business flow**: lab analysis entry → sum/frozen/missing-data checks fire → analyst triage | CTRL_CHECK_LOG counts vs oracle for rules 1156/1157 (MOL% sum), 1058-1074 (missing PHD), frozen/stddev | exists, recast as business suite |
| V2 | **Missing-data validation** (the layer I flagged): blank a mandatory PHD attr (e.g. PWEL_DAY_STATUS.ON_STREAM_HRS, rule 1062) → run CO.0204 → assert ERROR row | CTRL_CHECK_LOG has the rule-1062 violation; clearing it removes the row | As-Built 09 IDs known |
| A1 | **Full allocation chain** (grounds P1 with real names): seed well/stream day data → ZWP_DAILY_MASS_BALANCE → ZWP_ALLOC_ONSHORE_DAY via HA.0002 → assert | PWEL_DAY_ALLOC + STRM_MTH_ALLOC + reconciliation factor within threshold (V_ALLOC_* WARNING absent) | scheduler/app up |

## Tier 2 — domain depth
| # | Test | Oracle |
|---|---|---|
| P3 | Deferment loss math (Down event: rate×downtime; precedence rules) | DEFERMENT_EVENT loss + day alloc impact |
| P4 | Well test → allocation basis change | PWEL_RESULT feeds next alloc differently |
| T1 | Cargo status ladder T→R→C→A drives record status V/A + edit locks | CARGO_TRANSPORT.RECORD_STATUS auto-transitions |
| T2 | Entitlement accrual = share % × production | LIFT_ACC_DAY_FORECAST delta |
| S2 | Price math: index value → price calculation → contract price list | price = rule formula (recompute independently) |
| S3 | Contract account calc (e.g. Take-or-Pay accumulation) | CNTRACC quantity |
| R1 | Document lifecycle OPEN→…→BOOKED + edit-lock after TRANSFER | doc status + booking period |
| R2 | Closing gate: unBOOKED doc blocks booking-period close | close rejected |
| R3 | Accrual flip: RUN ACCRUAL → values = method; actuals → FINAL | STIM values |
| C1 | Chemical inventory balance: level(N) = level(N-1) − injected + refills | CHEM_TANK_STATUS arithmetic |

## Tier 3 — config/UI governance
| # | Test | Oracle |
|---|---|---|
| G1 | CSDV zones (green/orange/red) on a stream item | save allowed/warned/blocked |
| G2 | Sales→Revenue replication gate (interface_to_revenue flag) | IFAC_SALES_QTY rows appear only when flagged |
| G3 | Cargo→Revenue precondition ('Available in Revenue' + Incoterm) | replication present/absent |

## Open scope questions (need As-Built / Choong-Yin)
- Which flows are IN Pluto As-Built scope? (AsBuilt14 BusinessProcesses will answer most.)
- Safe-to-run list for schedulers/calcs on local sandbox (P1 needs InitiateDay).
- Month-lock state on sandbox; deferment & royalty scope; LNG cargo vs pipeline-gas focus.
