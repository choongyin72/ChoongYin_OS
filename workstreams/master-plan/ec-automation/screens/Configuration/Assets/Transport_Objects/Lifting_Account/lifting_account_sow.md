# SOW - Lifting Account IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Lifting Account   **BF:** CO.2004   **View:** `OV_LIFTING_ACCOUNT`   **Base:** `LIFTING_ACCOUNT`
- **Type:** OV-GM **4-LEVEL nav variant** (grid `manageObject:form:T_data`): standard PU -> Area ->
  Facility Class 1 cascade (nav row 1, C:1..3) **plus a mandatory Storage dropdown on a second
  navigator row** (`nav:form:G:0:R:3:C:0:dd`, recon-verified id).
- **Navigator uses SPECIFIC owner-provided values, NOT first-available:** the Storage level is EMPTY
  under the first-available AS1 path (verified fill-timeout in the original scan - why this screen was
  parked). Working scope: **P1 Production Unit -> P1 Area -> P1 Facility 1 -> P1_CRUDE_STOR**.
- **Insert extras:** Company Name (first-available; 146 companies effective at 2020-01-01, DB-checked)
  + **Storage Name = the nav Storage** (parent-matching rule - the row never lists otherwise).
- **Start Date = 2020-01-01**: P1_CRUDE_STOR effective 2010-01-01 (DB-checked).
- DELETE = End Date = Start Date (true delete from the OV view). Unique `AUTOTEST_LA_<timestamp>`
  per run; never touch existing rows; self-cleaning.

## Known risks
- The nav scope is DATA-dependent (P1 objects): if the sandbox's P1_CRUDE_STOR storage or the P1
  cascade is removed/renamed, the suite fails at navigator-apply - re-derive a working scope the same
  way (owner walk-through or DB query of storages under a facility).
- Hand-built driver/T3/suite (generator does not support a second nav row / specific nav values).
