# EC ec-worker + the EC scheduler — what it is, how it's used (2026-06-14)
Deep dive from the EC tech docs (`/doc/.../frmw/containers/ec-ec-app.html`, authenticated) + the SDK
compose + EC source. Prompted by N3 status-process runs sitting WAITING and never executing.

## What `ec-worker` IS
- **Not a separate product** — it's the **same container image as ec-app** (`registry.energycomponents.com/ec-ec-app`),
  run as a **dedicated background/worker node**. (Confirmed: in `docker stack services EC01`, `ec-worker`
  uses image `ec-ec-app`.)
- The ONLY thing that makes it a "worker" is **config**: its EC **scheduler** is started in
  **`EC_SCHEDULER_STARTUPSTATE=SERVER_STATE_RUNNING`**, so it actively fires/executes scheduled jobs.
  In a split deployment the front-end `ec-app` nodes run **`SERVER_STATE_STANDBY`** (serve the UI, do
  NOT fire jobs). This separates UI serving from heavy background processing (stability + scaling).

## Key settings (ec-ec-app container doc)
- **`EC_SCHEDULER_STARTUPSTATE`** — values: `SERVER_STATE_RUNNING` (fires jobs) / `SERVER_STATE_STANDBY`
  (scheduler registered/checks in but fires nothing) / `SERVER_STATE_SHUTDOWN`. **Default = RUNNING.**
- **`EC_SCHEDULER_THREADCOUNT`** — concurrent job-execution threads.
- **`ECWORKER_CLIENT_SECRET`** — OAuth client secret for **EC background jobs** (incl. Jasper report
  generation); EC↔worker auth. Dev default `CHANGE_ME` (fine for sandbox).

## How a job flows (the execution path)
scheduled job / HA.0001 status-process "Run Process" → queued (shows in `RunningJobs:form:T_data` as
**WAITING**; Quartz trigger row) → the **RUNNING-scheduler node** (ec-worker) acquires it → Quartz
`StatefulBusinessControllerInvokerJob` → `UserEventHandler` → the business action (class from
`BUSINESS_ACTION.ACTION_CLASS_NAME`) → DB effect (e.g. RECORD_STATUS P→V) → result logged
(`STAT_PROCESS_STATUS.ROWS_UPDATED`, the on-screen log grid). If no node has a RUNNING scheduler, the
job stays WAITING forever.

## How it's enabled in the SDK deployment
- Overlay **`12-docker-compose.ec-worker.yml`**: `ec-worker` replicas 1 (base gives it
  `EC_SCHEDULER_STARTUPSTATE=SERVER_STATE_RUNNING`) + sets `ec-app` scheduler to `SERVER_STATE_STANDBY`.
  Without overlay 12, `ec-worker` = 0 replicas and `ec-app` runs the scheduler itself.

## ⚠️ Current anomaly (N3 still blocked even with ec-worker 1/1)
After redeploy `ec-worker` is **1/1**, BUT status-process jobs still don't execute, and the DB shows:
**only ONE Quartz scheduler instance registered (`…ECDS`) and `QRTZ_FIRED_TRIGGERS = 0`** (even the
built-in `DataPurging` trigger sits WAITING). If a node's scheduler were truly RUNNING it would be
firing triggers. ⇒ **No EC node currently has an actively-firing scheduler** — ec-app is STANDBY (by
overlay 12) and ec-worker's scheduler does not appear to be RUNNING/firing despite the container being
up. Decisive check = **ec-worker's startup log**: look for the EC scheduler line
(`ECScheduler … SERVER_STATE_RUNNING` vs STANDBY, or an error). Likely causes to check: the
`EC_SCHEDULER_STARTUPSTATE=RUNNING` env didn't apply to ec-worker after the overlay merge, or the
worker's scheduler failed to start. (Not a per-process defect: nothing fires regardless of which
process is picked.)

## ✅ BREAKTHROUGH (2026-06-14): worker DOES execute now — status process fails on EMPTY DATA
The ec-worker log (after a transient startup crash — `UnknownHostException: ec-messaging` then it
recovered) shows the **ECScheduler IS firing jobs**: `DailyDataStatusProcess` runs on `ECDS_Worker-N`.
So the earlier "no node firing" was a transient (worker mid-restart), NOT a permanent block. The
`ECWORKER_CLIENT_SECRET=CHANGE_ME` auth works fine (service-account-ecworker authenticates OK).

**The status process now EXECUTES but FAILS** — `ACTION_INSTANCE_HISTORY.MESSAGE_DETAIL` (RUN_STATUS=
FAIL, runs #1–3):
`ORA-06569: Collection bound by bind_array contains no elements  at ECKERNEL_EC.PCK_STATUS line 703 /
175`. = `PCK_STATUS` bound an EMPTY collection to DBMS_SQL → **the process found no provisional rows to
lift for the chosen scope/date** (P1 facility @ 2003-01-01). `STAT_PROCESS_STATUS=0`, PWEL still all P.

⇒ **Not infra, not the run mechanism — it's a no-matching-data condition.** Fix = run a status process
on a (facility, date) that actually has provisional rows matching the process's target set. (Arguably
also an EC robustness bug: PCK_STATUS should handle an empty set instead of ORA-06569.) Failure detail
read via `tmp/scripts/n3_fail2.py`. NEXT: find a status-process scope+date with real P data, then the
run should lift P→V and write STAT_PROCESS_STATUS.ROWS_UPDATED.

## ✅✅ N3 PROVEN end-to-end (2026-06-14) — status process lifts P→V
With ec-worker running, fired **"P1 Forward Status Update" @ DATE 2024-02-06** (a date where the P1
facility HAS provisional data) → **SUCCESS**: `STAT_PROCESS_STATUS` row = `P1_FwdUpd / level V /
ROWS_UPDATED=15`. The 15 lifted rows = PWEL_DAY_STATUS(1) + IWEL_DAY_STATUS(1) + **OBJECT_DAY_WEATHER(13)**
all P→V. So the P→V→A record-status engine works; the earlier failures were (a) ec-worker not running,
then (b) ORA-06569 = empty data on 2003-01-01. **The fix was the DATA SCOPE (a date with P rows), not
the mechanism.**
- **Self-clean:** the EC reverse process ("P1 Reverse Status Update" / P1_RevUpd) ran but updated **0
  rows** — it does NOT undo the forward lift. So the suite must self-clean via **DB-restore V→P** (like
  the N1 IWEL/EQPM suites). Cleaned this test run: restored all 15 (PWEL+IWEL+OBJECT_DAY_WEATHER) → 0
  residual V on 2024-02-06 (broad scan of 6382 RECORD_STATUS+DAYTIME tables = clean).
- ec-worker note: it had a transient startup crash (`UnknownHostException: ec-messaging`) then recovered
  — after a redeploy give it a minute before testing.

### N3 build recipe (ready)
Screen HA.0001 "Daily Data Status Processes" (non-iframed). Nav: From/To date G:0/G:1 = **2024-02-06**,
process in **G:2 dd** = "P1 Forward Status Update", GO `button:form:B`, then **RunProcessButton:form:B**.
Oracle: poll `STAT_PROCESS_STATUS` for a new row (PROCESS_ID=P1_FwdUpd, ROWS_UPDATED>0) + assert
RECORD_STATUS P→V on the lifted rows. Self-clean teardown: DB-restore V→P on 2024-02-06 (reuse a
DbVerify reset, broadened to RECORD_STATUS). Scripts: `tmp/scripts/n3_try_process.py` (process+date
args), `n3_verify_lift.py`, `n3_cleanup_lift.py` + `n3_cleanup_weather.py`.
