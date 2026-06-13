# Pattern N3 — Status-process RUN + verify (HA.0001 Daily Data Status Processes) — recon + plan (2026-06-14)
The P→V→A record-status engine: run a **Status Process** over a date(range) + scope, which lifts
`RECORD_STATUS` on day-status data (Provisional → Verified → Approved). Verify with a **DB status-
transition oracle** (the row's RECORD_STATUS moves P→V) + the engine's own `STAT_PROCESS_STATUS.
ROWS_UPDATED` count. This is the third operational-core pattern after N1 (edit-in-place) and N2
(allocation RUN). **Recon DONE; build is a GO (N2-analog). This doc = the ready-to-execute plan.**

## Why N3 = an N2 analog (the big de-risk)
HA.0001 "Daily Data Status Processes" (`com.ec.prod.ha` family) has the **same RUN scaffolding** as
HA.0002 allocation (probe `tmp/scripts/n3_ha0001_probe.py`, shot `tmp/n3_ha0001.png`):
- Navigator: **From Date** `nav:form:G:0:R:1:C:0:da_input` + **To Date** `nav:form:G:1…` + GO
  `button:form:B` ("Go..."). (Same as HA.0002.)
- A **`dateStartJob:form`** block (job start time / Simulate area — HA.0002's Simulate lived here at
  `dateStartJob:form:G:0:R:1:C:2:cb`; check whether status processes expose the same Simulate).
- **`statusProcess:form`** = the process selector + run trigger (analog of HA.0002's calc-job dd +
  `ProdAllocButton:form:B`). The exact process dropdown id + RUN button id still need a live crack
  (post-GO; the forms populate after the navigator GO, like HA.0002).
- **`RunningJobs:form:T_data`** in-flight grid (same executor surface as HA.0002) — and a completed-
  runs/log grid should appear post-run (HA.0002 = `log_list:form:T_data`). The "Process Automation"
  bell text is present = the same BPM red herring (NOT necessarily a blocker — HA.0002 ran synchronously
  via its RUN button despite the same bell).
⇒ **Reuse `resources/allocation_run.resource` as the template** for a new `resources/status_process_run.resource`
(set date range, GO, pick process, optional Simulate, click RUN, poll the log for Exit Status).

## DB model + oracle (DONE)
- Config: **`STATUS_PROCESS`** (key `PROCESS_ID`; `PROCESS_TEXT`, `FROM_RS_LEVEL`→`TO_RS_LEVEL`,
  `PROCESS_INTERVAL` DAY/MTH, `REVERSE_FLAG`, `PROD_FCTY_ID`, `PARENT_PROCESS_ID`). Levels decode via
  `CTRL_RECORD_STATUS_LEVEL`. (`tmp/scripts/n3_process_list.py`)
- Run log / oracle: **`STAT_PROCESS_STATUS`** (`PROCESS_ID`, `RECORD_STATUS_LEVEL`, `DAYTIME`,
  `RUN_DAYTIME`, **`ROWS_UPDATED`**) — a run appends a row here with how many rows it lifted. Run
  history is currently **EMPTY** (no status process has ever run in this sandbox).
- Target data: **`PWEL_DAY_STATUS`** = 69,794 rows, **ALL `RECORD_STATUS='P'`** (STRM_DAY_STREAM =
  59,513, all `P`). Abundant Provisional data to lift; 113 P rows on the N1 scope day 2003-01-01.

### Chosen process for the positive test
- **`P3_VERIFY_FCTY`** — "Verify P3 Facility Process", the one explicit **FROM=P → TO=V**, DAY,
  `REVERSE_FLAG=N`. (Alternatives: `VER_ONS_FCTY` "Verify daily Onshore facility data" blank→V;
  `P1_FwdUpd` blank→V; `P1FctyAlloc_DailyBPM_Ver` blank→V.)
- **Self-clean (revert V→P):** a reverse process exists (`P1_RevUpd` `REVERSE_FLAG=Y`; parent
  `P1_RevUpdPar1` →P). Confirm the reverse path lifts V back to P for the chosen scope so the test
  leaves the data exactly as found (the N1/N2 self-cleaning discipline).

## The N3 oracle (what a pass asserts — DB ground truth)
1. **Status transition:** the scoped (object × day) rows move **`RECORD_STATUS` P → V** in
   `PWEL_DAY_STATUS` after the run (DbVerify: count P before, count V after = the same rows).
2. **Engine self-report:** a new `STAT_PROCESS_STATUS` row for the PROCESS_ID/DAYTIME with
   **`ROWS_UPDATED` = the number of rows lifted** (> 0, matches the count).
3. **Revert (cleanup):** after the reverse process, the rows are **back to P** (self-cleaning).
4. (Negative/■ guard, optional) running on a **locked month** or empty scope lifts 0 rows.

## Remaining live cracks (the build's first step — all post-GO on HA.0001)
1. After setting dates + GO: dump `statusProcess:form` — the **process-select control** (dropdown? a
   grid row to tick?) + the **RUN button id** (analog of `ProdAllocButton:form:B`).
2. Is there a **Simulate** (no-DB-write) toggle for status processes? (If yes, dry-iterate like N2.)
3. The **completed-run/log grid** id + its Exit-Status column (analog of `log_list:form:T_data` col 7).
4. ⚠️ **Executor risk:** status processes may run via the **BPM Job Executor (jbpmengine)** (DOC-08).
   If the RUN dispatches async to that executor, it may **stall like N2 non-simulate** (ACQUIRED). If
   so → N3 run parks with the same PA/executor blocker; the DB oracle is still buildable against any
   row that DOES get lifted. First live run will tell (watch `RunningJobs` vs a synchronous log row).

## Build steps (when executed — mirrors the N1/N2 rhythm)
1. Live-crack the statusProcess form (step above) on a tiny scope (one facility/day), Simulate if avail.
2. `libraries/DbVerify.py`: add `record_status_count(table, daytime, status)` +
   `status_should_lift(table, daytime, from→to)` + read `STAT_PROCESS_STATUS.ROWS_UPDATED`.
3. T2 `resources/status_process_run.resource` (fork of `allocation_run.resource`): date range, GO,
   select process, [Simulate], RUN, poll log Exit Status.
4. T3 `pageobjects/Production/ha0001_daily_status_process_page.resource` (screen + scope: P3_VERIFY_FCTY,
   a scope day with P rows, the reverse process for cleanup).
5. Suite `tests/Production/daily_status_process_run.robot`: TC01 run verify → assert P→V + ROWS_UPDATED;
   TC02 (cleanup) reverse → assert back to P. Dryrun → live (headed) → DB-verify → robocop → commit.
6. Re-test habit (canary + random) since DbVerify changes; registry row + scorecard update.

## Status
Recon complete; **GO for build next session** (high confidence it's an N2-analog). Only real risk =
the BPM-executor stall (#4) — same family as the N2 non-simulate blocker; the first live run resolves
it. Recon scripts: `tmp/scripts/n3_*.py`.
