# Business Test-Case Backlog (phase-2 candidates — FOR CHOONG-YIN'S REVIEW)
Consolidated from the 5 domain dives (2026-06-13). Each has a DB-verifiable oracle.
Nothing gets built until reviewed/prioritized by Choong-Yin (+ As-Built scope check).

## Tier 1 — core loop, high Pluto relevance, lowest dependency
| # | Test | Oracle | Pre-req |
|---|---|---|---|
| P1 | **Daily-cycle smoke**: InitiateDay → enter one well-day → DailyProductionAllocation → dashboard | new SYSTEM_DAYS day + PWEL_DAY_STATUS rows; PWEL_DAY_ALLOC row for the well | scheduler healthy (currently STALLED on sandbox!) |
| P2 | **Status lifecycle P→V→A + month lock**: insert P data → verify → approve → lock → write rejected | RECORD_STATUS transitions; locked-month write error | status processes configured |
| S1 | **Nomination → delivery chain** (daily gas): nominate → confirm → delivery reflects qty; renominate → revision | NOMPNT_DAY_NOMINATION + delivery rows | seed contract/nompnt |
| E1 | **ECIS backup-path E2E** (= the real task's acceptance test): upload Excel when "PHD down" → staging review → promote → data identical to PHD path | PWEL/staging/target rows | CLAUDE_WELL_TEST pattern (proven) |
| V1 | **Issue_1052 regression pack as business flow**: lab analysis entry → sum/frozen checks fire → analyst triage | CTRL_CHECK_LOG counts vs independent oracle | exists, recast as business suite |

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
