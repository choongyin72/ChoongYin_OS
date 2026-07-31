# SOW - Well IUD (Configuration > Assets > Well_and_Reservoir_Objects)

- **Screen:** Well   **BF:** CO.0049   **View:** `OV_WELL`   **Base:** `WELL`   **Class match note:** resolver
  returned ['WELL','FORECAST_WELL']; OV_WELL confirmed the live view by REAL lookup ('P1 W001 OP' present, 506 rows).
- **Type:** OV-GM (grid `manageObject:form:T_data`) with a 5-dd navigator, but **only the standard
  3-level cascade is required**: SPECIFIC P1 values (P1 Production Unit -> P1 Area -> P1 Facility 1)
  + GO lists the wells while the 2nd-row dds (Well & Well Hookup / Well) stay EMPTY - owner
  screenshot ground truth (2026-07-30). The original park ("5th level empty under first-available
  AS1") was a data-scope artifact, not a structural blocker.
- **Insert extras:** Well Type (mandatory dropdown, first-available). NO Op Production Unit field on
  the form - the row lists under the nav scope regardless (same as Facility Class 1).
- **Start Date = 2020-01-01** (P1 wells effective 2010-01-01, DB-checked).
- DELETE = End Date = Start Date. Unique `AUTOTEST_WE_<timestamp>` per run; self-cleaning.

## Known risks
- Nav scope is DATA-dependent (P1 objects) - if the P1 cascade is renamed/removed the suite fails at
  navigator-apply; re-derive a working scope (owner walk-through or DB).
- Hand-built driver/T3/suite (generator does not support specific nav values).
