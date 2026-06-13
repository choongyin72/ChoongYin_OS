# EC Transport — domain dive 2 (2026-06-13, local sandbox)

Sources: menu walk (`tmp/biz_domains/ec_transport_branch.txt`, 251 nodes) · DB counts ·
DOC-06 KB. Theory depth lives in DOC-06; this doc = sandbox tie-in + flow + test seeds.

## 1. Menu shape (what the business does)
- **Cargo Planning** (the bulk): Lifting Program, Nomination Entry/Details/Split, Schedule
  Lifting Overview/Chart (±RBS), Daily Entitlement family, Storage/Tank charts, Berth Slot
  Calendar, Cargo Information, Lifting/Document Instruction, Master Plan…
- **Terminal Operation**: BL/MR Info, Unload Info, Port Log, demurrage (Create-button
  pattern!), irregularities.
- **Lifting Account**: account balances/entitlement tracking.
- Gas Dispatching + Oil Delivery + Forecast sections complete the branch.

## 2. Sandbox data (which flows are learnable here)
| Family | Evidence | Meaning |
|---|---|---|
| CARGO_TRANSPORT 649 (+FCST 669) | ✅ | real cargo lifecycle data |
| VOY_CARGO_ACT 1.6k (+FCST 1.6k) | ✅ | new (13.2) physical load/unload activities |
| LIFT_ACC_DAY_FORECAST 13k, _OFFICIAL 758 | ✅ | lifting-account entitlement engine ran |
| NOMPNT_DAY_NOMINATION 4.2k | ✅ | gas nominations (links to our Dispatching screens!) |
| CNTR_SUB_DAY_STATUS **491k**, CNTR_PERIOD_STATUS 79k | ✅✅ | contract sub-day statuses — biggest table family seen yet; contracts are the spine |
| BERTH 11, CARRIER 74 (+368 port clearances) | ✅ | master data for scheduling |

## 3. The core business flow
```
CONTRACT (shared Transport/Sales/Revenue concept: parties, attributes, accounts)
  └─ entitlements accrue daily → LIFT_ACC_DAY_FORECAST/_OFFICIAL (lifting account)
Nomination Entry (CP.0001) creates cargo as Tentative
  └─ cargo status workflow T → R (Lifting Instruction) → C (BL/MR Info) → A
     (own status machine ON TOP of record status; C forces RECORD_STATUS=V, A forces A)
Physical execution: VOY_CARGO_ACT load/unload, Port Log, irregularities, demurrage
Monthly: account balance calc, replication to EC Revenue (LOAD/EXP_UNLOAD/UNLOAD
  quantities per Product Measurement Setup) → invoicing
```
Key insight vs Production: cargo has a **second status dimension** (T/R/C/A) that *drives*
record status — test design must assert both.

## 4. Ties to our work
- Nomination Point / Transport System / Delivery objects (Dispatching slice 1) = the master
  data under NOMPNT_DAY_NOMINATION.
- The Assets scan's Transport Objects section (58 screens, 32 OTHER) maps to this flow's
  config: lifting accounts, measurement setups, document templates → now explainable.
- Contract Objects (Assets) = the shared Contract concept → prerequisite for the deferred
  Assistance screens AND for Sales/Revenue dives.

## 5. Candidate business test cases
1. **Cargo status ladder**: Nomination Entry (T) → Lifting Instruction (R) → BL/MR (C) →
   assert CARGO_TRANSPORT.RECORD_STATUS auto-V → Approve (A) → assert downstream tables A
   + edit-lock. (Status matrix is pure assertable logic.)
2. **Entitlement accrual**: known contract share % → day production → assert
   LIFT_ACC_DAY_FORECAST delta matches share math.
3. **Berth conflict**: two nominations on same berth slot → assert GanttChartConflictDetector
   surfaces the clash (CP.0072).
4. **Revenue replication precondition**: cargo on contract NOT 'Available in Revenue' →
   assert no replication; flip flag → assert LOAD qty lands in Revenue.

## 6. Open questions for Choong-Yin
- Pluto scope: full cargo administration (LNG liftings — likely YES for Pluto LNG) vs
  pipeline-gas only? Which RBS variants are in As-Built scope?
- Are the *_BKP storage tables a migration artifact we should ignore?
