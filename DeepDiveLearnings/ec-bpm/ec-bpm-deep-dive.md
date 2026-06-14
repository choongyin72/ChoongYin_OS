# EC BPM (ECBPM / jBPM) — deep dive from the SDK working examples (2026-06-14)
Source: `C:\DEV\EC\SDK\energycomponents-sdk-14.2.4\examples\bpm\*` (working sample processes +
authoring/deployment docs) + EC source `C:\DEV\GIT\ec-application`. Prompted by tracing the
"Daily Offshore Process" `name is null` failure to its root (a never-deployed BPM process) — the user
redirected me to learn the BPM mechanism from the *working* processes instead. Addresses the held
"BPM/Process-Automation deep dive" item.

## What ECBPM is
EC's process-orchestration layer, built on **jBPM** (KIE) running in the **ec-bpm** container (a
separate WildFly from ec-app). BPMN2 processes orchestrate EC work — calculations, reports, status
lifts, user tasks, SQL, events — above the single-action level. EC↔BPM talk over REST
(`EC_URL_BPM=…/jbpm-console`; BPM calls back to `EC_URL_APP/com.ec.frmw.jbpm/endpoint`; secured by
`BPM_CLIENT_SECRET`, dev default `CHANGE_ME`).

## The model (process → template → instance), and how it's wired to EC
1. **Process** — a BPMN2 diagram authored in Eclipse (BPMN2 Modeler + jBPM runtime ext), identified by
   a unique **Process Id** (e.g. `advanced_calc_sample`). Lives in `src/main/resources`.
2. **Deployment** — `mvn install` (KIE maven plugin validates + builds a project zip) → deployed to a
   running EC via the **`ecbpm-maven-plugin`** (`ecbpm:deploy` / `:upgrade`) OR the **Project Management**
   screen (manual upload). Deploy needs a client with the **`JBPM.ADMIN`** role. The deployment is
   identified by a **maven GAV** `groupId:artifactId:version` → this becomes the **`JBPM_DEPLOYMENT_ID`**
   on the business action (e.g. `com.ec.bpm:prod-bpm-building-blocks:1.0`).
3. **Process Template** — created in EC for a deployed process, exposing its **template parameters**
   (typed: Basic String/Date/Boolean, EC Object Type e.g. Allocation Network / Calculation, EC Code Type
   e.g. CALC_LOG_LEVEL).
4. **Process Instance** — a running execution of a template (Process Overview / Process Instances /
   To-do List screens; jBPM runtime in `JBPM_PROCESSINSTANCEINFO`, async work in `JBPM_REQUESTINFO`).
5. **Business action linkage** — `BUSINESS_ACTION` row carries `JBPM_PROCESS_NAME` +
   `JBPM_DEPLOYMENT_ID` + `JBPM_PROCESS_VERSION` + `ACTION_CLASS_NAME` (the jBPM-invoker class, e.g.
   `com.ec.bpm.ext.ec.web.energyx.process_temp…`). A schedule's `ACTION_INSTANCE` → `BUSINESS_ACTION`
   is what the EC scheduler fires.

## ⭐ Why "Daily Offshore Process" fails (root cause, now fully explained)
That `BUSINESS_ACTION` has **`JBPM_DEPLOYMENT_ID='dummy'`**, null version, null `ACTION_CLASS_NAME` —
i.e. the process was **never actually deployed** (no real GAV pushed via the plugin / Project Mgmt
screen, so no process template/class was created — exactly the "samples are not deployed by default,
and no process templates are created for them" note in the SDK). A real deployed process (e.g.
`ECProd_AnalysisDataProcessing` → `com.ec.bpm:prod-bpm-building-blocks:1.0`) has a real GAV + class.
So firing its schedule reads a null class → `getValidatedClass(null)` → `name is null`. **Fix = deploy
the process (real GAV) or remove the placeholder schedule/action.** It's a config/deploy gap, not infra.

## Process building blocks (from the 20+ working samples) — the EC-relevant patterns
- **EC Process Action** (Service Task) — invokes an EC business action from a process, with WARNING/
  ERROR boundary catching events (the EC return-status contract surfaces as BPMN events).
- **CalculationAction** — run an EC calculation (params: start/end date, Allocation Network, Calculation
  id, CALC_LOG_LEVEL) — this is the **N2 allocation RUN wrapped in a process** (`advanced_calc_sample`,
  `multiple_report_sample`). BPM adds rerun-on-data-change, approval-wait, end-of-day timers.
- **GenerateReportAction** + `SendReportHandler` — generate + distribute Jasper reports
  (`advanced_send_report_sample`); needs report definition + messaging distribution configured.
- **User Task** — human-in-the-loop (To-do List screen); the standard "check & fix data" path on a
  calc/report ERROR. (Process Notifications are deprecated → use User Task / Send Email instead.)
- **SQL execution** — SELECT/UPDATE, stored **procedure**, and **function** execution against the EC DB
  from a process (`sql_execution_sample` etc.).
- **EC Datamodel** (`ExecuteEcDataModelAction`) — query an EC class (classname + attributes +
  query params) → list or DatamodelInterface, mapped to a process variable.
- **Events** — signal/message throw+catch, **event-based gateways** (branch on which event arrives
  first), boundary events to **cancel/interrupt** tasks/subprocesses, non-interrupting events for
  parallel paths, event sub-processes. `inbound_and_outbound_event_sample`: run calc → publish
  `ecbpm_ec_allocation_completed` → wait for `AllocationApproved` vs `AllocationDataUpdated` (rerun).
- **Sub-processes / Call Activity** — compose processes (e.g. calc process calls the send-report
  process); multi-instance inline subprocess (for-each-contract).
- **Process Instance viewer tags** — lock/unlock + Process Monitor screen visualization.

## How this connects to my automation track
- **BPM is the orchestration layer above the N1/N2 patterns I built.** The N2 allocation RUN
  (HA.0002 `RUN CALCULATIONS`) is the synchronous, screen-driven equivalent of a BPM `CalculationAction`
  service task. The **N3 status processes** (P→V→A) and allocation can be driven either synchronously
  (screen) or as scheduled/BPM jobs (ec-worker + ec-bpm). The "work-by-exception" Allocation BPM in the
  As-Built is this: calc → checks → status lift → report → approve, with user-task exception handling.
- **Testing implication:** a meaningful BPM test asserts the process **reaches the expected end node /
  produces the expected EC effect** (calc run result, report row, RECORD_STATUS lift) + handles the
  ERROR/WARNING branch — verified at the DB (calc log, `*_DAY_ALLOC`, `RECORD_STATUS`) like N1/N2, not
  just "process started". The jBPM runtime tables (`JBPM_PROCESSINSTANCEINFO`, `JBPM_REQUESTINFO`) +
  Process Overview are the BPM-side oracle.
- **Prereqs to actually run BPM here:** ec-bpm up + **ec-worker** up (the RUNNING-scheduler background
  node) + the process **deployed** (real GAV) + a process template with params. The sandbox currently
  lacks the running ec-worker (see `pattern_n3_status_process_design.md`), so BPM execution is parked;
  the status-process path (DailyDataStatusProcess, valid class) is the simplest first target once the
  worker runs.

## Status / next
Deep-dive complete for the BPM model + deployment + building blocks (this note). "Daily Offshore
Process" root cause fully explained (un-deployed placeholder). Execution still needs ec-worker running.
Next BPM-related learning when unblocked: deploy one SDK sample (e.g. `sql_function_execution_sample`)
via the Project Management screen → create a template → run an instance → observe `JBPM_PROCESSINSTANCEINFO`
+ Process Overview (a clean, low-risk way to prove the BPM execution path end-to-end).

## EC Scheduler internals (EFK Phase-4 "Enable a Schedule Job", read 2026-06-14) — confirms root cause
The on-demand ops page gives the full SQL recipe to create+enable a scheduled job, which nails the
scheduler/business-action wiring (and re-confirms the "Daily Offshore Process" break):
1. **`TV_BUSINESS_ACTION`** — `NAME`, **`ACTION_CLASS_NAME`** (e.g.
   `com.ec.eccommon.genericmodel.model.ejb.GenericRunSqlAction`), `BA_TYPE='SCHEDULER'`. ⭐ A scheduled
   business action MUST have a non-null `ACTION_CLASS_NAME` — precisely what "Daily Offshore Process"
   lacks (null) → the break is unambiguous.
2. **`TV_ACTION_PARAMETER`** — the action's params (type/sub-type/mandatory).
3. **`TV_SCHEDULE`** — the schedule; `ENABLED`, `FUNCTIONAL_AREA_ID`, and **`PIN_TO`** =
   `substr(instance_name,0,instr(instance_name,'.')-1)` from `QRTZ_SCHEDULER_STATE` → pins the job to a
   **specific scheduler node**. (Relevant to the ec-app-vs-ec-worker node question: jobs run on the
   pinned/RUNNING scheduler node.)
4. **`TV_SCHEDULE_DETAILS`** — notify role/level, run-as user, log level, retain count.
5. **`TV_ACTION_INSTANCE`** — links business action ↔ schedule (`EXEC_ORDER`, `ISOLATED_TX_IND`).
6. **`ACTION_INSTANCE_VALUE`** — sets the action's param values for this schedule.
7. **`QRTZ_JOB_DETAILS`** — `JOB_CLASS_NAME='com.ec.frmw.scheduler.job.StatefulBusinessControllerInvokerJob'`
   (the very invoker in the failing stack trace) + durable/stateful flags.
8–10. **`QRTZ_TRIGGERS` / `QRTZ_CRON_TRIGGERS`** — the cron schedule (e.g. `0 0/5 * ? * * *`, TZ
   `Australia/Perth`), `TRIGGER_STATE='WAITING'`.
11. **Enable** — `UPDATE TV_SCHEDULE SET ENABLED='Y'`.

So the EC scheduler = Quartz triggers → `StatefulBusinessControllerInvokerJob` → `UserEventHandler`
→ business action (class from `ACTION_CLASS_NAME`). This is the same path whether the action is plain
Java (e.g. status processes via `DailyDataStatusProcess`/`GenericRunSqlAction`) or jBPM-backed (class =
the jBPM invoker + `JBPM_DEPLOYMENT_ID`). (Phase-4 "Stopping a stuck EC Service" = a Windows-service/
WildFly kill-the-java-process note — not relevant to this docker-swarm deployment.)
