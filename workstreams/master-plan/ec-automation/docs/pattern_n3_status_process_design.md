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

## Live-crack progress (2026-06-14) — nav fully mapped; grid needs the G:2 scope dd
Probed HA.0001 post-GO (`tmp/scripts/n3_ha0001_postgo.py`, `n3_ha0001_deepdump.py`):
- **Navigator = 3 fields:** From Date `nav:form:G:0:R:1:C:0:da_input` + To Date `nav:form:G:1…` +
  **`nav:form:G:2` = a DROPDOWN (hasDd) — a scope/process selector that is MANDATORY**. GO = `button:form:B`.
- **Root cause of the empty grid:** I ran GO with only the two dates set → `statusProcess:form` grid
  stayed empty (no rows, no process names in DOM, no RUN button surfaced). Exactly the N1/N2 rule — the
  grid only renders after the navigator dd (G:2) is picked + GO. So the run path is intact; my probe
  just hadn't set G:2.
- `statusProcess:form` is a **frozen-column datatable** (`fcNum`/`freezePanel`/`hideMenu` = column
  freeze + show/hide menu); its data rows will be `statusProcess:form:T:{r}:…` once populated (NOT a
  `:T_data` suffix — that's why the `:T_data` scan found nothing).
- "Process automation not available" = the toolbar bell only (`screenToolbar:form:taskNotification`) —
  same red herring as HA.0002; NOT a blocker by itself.

### Refined next step (resume here)
1. Open HA.0001 → set From/To date → **open `nav:form:G:2:R:1:C:0:dd_button`, dump its options**
   (likely the facility/asset or data-category scope; pick one that has P rows on the date, e.g. an
   AS2/onshore facility for 2003-01-01) → **GO**.
2. Dump the now-populated `statusProcess:form` grid: the process rows (find `P3_VERIFY_FCTY` / a P→V
   process), how you SELECT a process (row checkbox/click), and the **RUN button** (analog of
   `ProdAllocButton:form:B`) + whether a **Simulate** toggle + a completed-run/log grid appear.
3. Then build per "Build steps" above. Watch first RUN: synchronous log row (buildable) vs `RunningJobs`
   ACQUIRED stall (BPM executor → parks like N2 non-simulate).

## ⛔ LIVE RUN BLOCKER (2026-06-14) — status processes need the BPM/Process-Automation executor
Cracked the full run path and fired a real run; hit a hard infrastructure blocker.
- **Run path (PROVEN):** set From/To date (G:0/G:1) → pick the **process in `nav:form:G:2` dd** (the
  G:2 options ARE the process names, e.g. "Verify P3 Facility Process", "P1 Forward Status Update") →
  GO `button:form:B` → **`RunProcessButton:form:B`** ("Run Process"). Result grid =
  **`statusProcess:form:T_data`** (cols: Run Date · Run By · From · To · Process Name · New Status ·
  **# Rows Updated**). In-flight = `RunningJobs:form:T_data`. No Simulate option for status processes.
- **The blocker:** ran "P1 Forward Status Update" @ 2003-01-01 → the job went to **RunningJobs =
  WAITING and stayed there 24s+, never completing** to the log grid. **DB ground truth: nothing
  changed** — `STAT_PROCESS_STATUS` still EMPTY, `PWEL_DAY_STATUS` still 69,794 all `P`. The job
  dispatches to **BPM** (`BPM_EC_GCOMMAND*` queue) and the **BPM/Process-Automation executor is not
  running in this sandbox** → the job never executes. This is the SAME infra blocker as the **N2
  non-simulate** path (ACQUIRED/WAITING stall). The "Process automation not available" bell is telling
  the truth for the async executor (unlike HA.0002, status processes have NO synchronous Simulate
  bypass, so EVERY run is blocked).
- **Clean:** no data mutated (run never executed); the WAITING job is inert (would only run if BPM is
  enabled — it would then lift the 2003-01-01 P1-facility scope P→V, reversible via "P1 Reverse Status
  Update").

### Decision needed (why N3 can't be finished here without input)
The meaningful N3 test (assert a live `RECORD_STATUS` P→V + `# Rows Updated` + reverse self-clean)
REQUIRES a completed run, which requires the **BPM/Process-Automation executor enabled** in the
sandbox. Options: (a) enable Process Automation / the job executor (env/SME action — also unblocks N2
non-simulate); (b) build the honest partial N3 now (drive screen + submit run + assert it queues +
read-only DB oracle), completion-pending-PA — weaker than N1/N2 since no live P→V can be asserted;
(c) park N3 until PA is available and move to another unblocked item. Recon/run scripts:
`tmp/scripts/n3_ha0001_crack.py`, `n3_live_forward.py`, `n3_after_run_dbcheck.py`.

## Retry after ec-bpm restart (2026-06-14) — still NOT executing; precise diagnosis
User restarted EC app to include ec-bpm; re-fired "P1 Forward Status Update" @2003-01-01 and watched
~3.5 min. Job still goes **RunningJobs = WAITING** and never executes. DB ground truth (read-only):
- `STAT_PROCESS_STATUS` = 0 rows · `PWEL_DAY_STATUS` = all P (no lift) · no change over 3.5 min.
- **Quartz scheduler IS healthy** (`QRTZ_SCHEDULER_STATE` last checkin 5s ago, 7.5s interval) — but its
  only trigger is **`DataPurging`** (WAITING). So status processes do NOT run via Quartz.
- BPM engine = **jBPM** (JBPM_* tables). **`JBPM_PROCESSINSTANCEINFO = 0`** and **`JBPM_REQUESTINFO =
  0`** throughout — i.e. **no jBPM process instance / async request is ever created** for the queued
  job. The EC→jBPM hand-off (or the jBPM async ExecutorService that drains the queue) is not processing.
⇒ Including ec-bpm wasn't sufficient: the **jBPM async job executor isn't picking up the status-process
job**. Needs (one of): the jBPM ExecutorService actually started/enabled; the `jbpmengine` user holding
the required eDAC roles for the data + the status processes (DOC-08); or an EC "Process Automation"
service/toggle beyond deploying ec-bpm. Environment clean (nothing executed; 2 inert WAITING jobs that
would lift the 2003-01-01 P1 scope P→V if the executor ever drains — reversible).

## Root cause (2026-06-14, from server log the user shared) — ec-bpm business-action class is null
The EC scheduler/executor IS running (worker `ECDS_Worker-2` fires `BusinessControllerInvokerJob` for
"Daily Offshore Process"). The job then **fails**:
`BusinessActionAdvancedConfig.createAndInitBusinessAction` → `ResourceServiceEC.getValidatedClass` →
**`java.lang.IllegalArgumentException: name is null`**. I.e. when the framework instantiates the
process's **Business Action**, the action's **implementation class NAME resolves to null** → every
status/scheduled process throws and never updates data (explains RunningJobs=WAITING→fail, DB
unchanged). DB scan of *_ACTION/*_EVENT CLASS columns shows the stored class names are populated
(ECIS/event actions fine) → so this is a **runtime class-resolution / ec-bpm wiring gap**, not a blank
DB value: the ec-bpm extension's action handler class isn't registered/resolvable after the restart.
**This is an EC app/ec-bpm setup fix (user/SME), outside automation.** N3 (and N2 non-simulate) stay
blocked until the business action instantiates. Partial-N3 (submit + read-only oracle) buildable now.

## ✅ ROOT-CAUSE FIX FOUND (2026-06-14) — deployment is missing the ec-worker background service
Deep-dived the SDK deployment `C:\DEV\EC\SDK\energycomponents-sdk-14.2.4\examples\deployments\
010-default-deployment`. The run script `run_EC_14_2_4.bat` deploys:
`-c 01-base -c 02-ssl-internal -c 06-testdb -c 07-config -c 09-debug` (NO overlay 12).
- `ec-bpm` IS running (09-debug sets ec-bpm replicas=1) — so "include ec-bpm" worked.
- BUT **`ec-worker` = replicas 0** in BOTH `07-config` and `09-debug`, and the run command does **NOT**
  include **`12-docker-compose.ec-worker.yml`**. So there is **no EC background service** running.
- EC topology (from `01-base`): `ec-worker` uses the same image as `ec-app` but with
  **`EC_SCHEDULER_STARTUPSTATE=SERVER_STATE_RUNNING`** — it is THE node meant to execute scheduled /
  business / status processes. `12-docker-compose.ec-worker.yml` brings `ec-worker` up (replicas 1)
  AND sets `ec-app` scheduler to **SERVER_STATE_STANDBY**. README §"Setup EC frontend service and
  background service" documents exactly this: add `-c 12-docker-compose.ec-worker.yml`.
- Without overlay 12: no worker, and ec-app's scheduler (not standby) fires the jobs on the frontend
  node → the business action fails to instantiate ("name is null") and status-process jobs sit WAITING.

**THE FIX** — add overlay 12 (after 07/09 so its replica/standby overrides win) to the deploy command:
```
docker stack deploy --with-registry-auth ^
 -c 01-docker-compose.base.yml -c 02-docker-compose.ssl-internal.yml -c 06-docker-compose.testdb.yml ^
 -c 07-docker-compose.config.yml -c 09-docker-compose.debug.yml -c 12-docker-compose.ec-worker.yml EC01
```
Then ec-worker runs the scheduler (RUNNING) + executes status/business processes; ec-app goes STANDBY.
After redeploy, retry the N3 forward run — it should complete (RECORD_STATUS P→V + # Rows Updated) and
the build can finish live. (Secondary: the `BPM_CLIENT_SECRET`/`ECWORKER_CLIENT_SECRET=CHANGE_ME` in
07-config should be real secrets if BPM auth then errors.)
