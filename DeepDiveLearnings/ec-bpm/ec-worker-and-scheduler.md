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
