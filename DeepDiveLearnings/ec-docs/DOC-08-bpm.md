# DOC-08 — BPM (Business Process Management / workflows)
**Source:** EC 14.2.4 `frmw/bpm` (24 pages) · **Read:** 2026-06-06 (pages 1–11 deep; 12–24 how-tos by title)

> The workflow engine behind the **Allocation BPMs** (DOC-04) and the "work-by-exception" model. BPMN processes run on a tailored **jBPM** engine.

## Architecture
Two systems:
- **Energy Components** — Process Template, Process Action, Process Notification, Viewer Tag, scheduler, presentation; main UI/API entry for end-users; participates in execution via **business action invocation**.
- **BPM Console** — the tailored **jBPM** engine (Process, Process API, Task) on a **separate server group**.
- **Job Executor** runs processes as the **`jbpmengine`** user → must hold roles for the data the processes touch (eDAC) + the Record Status Processes they run.
- Built-in schedules: `BpmSchedulerEnv` (log level), `BpmEventInboundWatcher` (EC dataset tracing), `BpmProcessInstanceCleanUp` (auto delete instances — irreversible).

## Project Management (EC 12+, replaced KIE Workbench)
BPM admins (role **`JBPM.ADMIN`**) create **Projects** (Maven structure: Name, **Group ID** `com.org.project`, **Artifact ID**, **Version** — multiple versions deployable), upload source, deploy/undeploy. A project = the container + smallest deploy unit for process files. *(This is the `prod-bpm-building-blocks` deploy from DOC-04.)* Screen: Process Automation → Project Management.

## Process Template & Execution
**Process Template** = EC alias of a deployed jBPM process — the **only way EC starts a process instance**. Also auto-registered as a **business action** → appears in the Schedules dropdown (schedulable periodically). Fields: Deployment Id, Process Id, Functional Area (access restriction). **Parameters** (dynamic, entered at run) + **Static Parameters** (fixed on the template). Screen: Process Automation → Process Template.

## Process Instance Management
**Process Overview** screen — navigator (From/To date, Date Param variable, Functional Area, Process Template) → Go. Configurable instance-table columns. **Process instance diagram** shows live node states via **Viewer Tags**: Active=green, Pending=yellow, plus completed/error colours (customizable in Viewer Tag screen). Zoom/pan.

## Process Action Invocations
**Process Actions** = actions EC performs on demand from the engine. Each has one+ **action handlers** (a business action or generic handler), executed in order, **chained output→input**; `Handler Parameter Overwrite` for mapping (Default/static/from-output). Purpose: reuse business actions, transform in/out, wrap with pre/post, expose Process Operations (UI) + Process Attributes (shown in Process Overview). Screen: Process Automation → Process Action.

## User Tasks & Task Management
BPMN **User Task** → assigned to actors/groups → appears in the **To-do List** screen (the "Available Tasks" toolbar icon from DOC-01). Task subject = `ec.extension.task.subject` (else Comment); description ≤2000 chars. Assignment: **Actors** (EC login ids, e.g. `sysadmin`) / **Groups** (EC roles, e.g. `SYST.ADM`), set at design time. Supports **ad-hoc tasks** (no process). *(This is the "user only interacts on exception" mechanism from the allocation BPMs.)*

## Process events (in/outbound) — ties to DOC-07
Notify running process instances about data changes via **signal/message event nodes**:
- **Process Inbound Events** (current; EC Inbound Events deprecated): `DatasetUpdated` (`ecbpm_dataset_updated__<var>`), `DatasetDeleted` (`ecbpm_dataset_deleted__<var>`), `EcGenericEvent` (`ecbpm_ec_<name>`, broadcast to all active instances). Use case: calc data updated → notify dependent instances to terminate & rerun; data approved → notify the instance.
- **Process Outbound Events** + **API** (programmatic process control). **TaskStatus** events published to the event engine (DOC-07).
- **Standard Processes** shipped with EC.

## How-tos (pages 12–24, by title)
Configure process-instance list columns (default + per-template) · display button on Process Action node · show query-XML data / External Data view · Variables tab · show calc log & report as data · Process Overview Legacy · Process Monitor Cache · custom viewer tags · production-day offset for sub-daily processes · customize texts/colours · monthly-process execution status. → on demand.

---

## Cross-links
- BPM is the engine for **DOC-04 Allocation BPMs** (daily/monthly, work-by-exception) and Analytics/Analysis BPMs.
- `jbpmengine` user (DOC-03 Oracle users / IAM); Process Templates schedulable (DOC-03 scheduler); `TaskStatus`/`JobCompleted` events (DOC-07).
- Process inbound events (`DatasetUpdated`) ↔ `DomainObjectChanged` (DOC-07) — both react to data changes; my IUD would feed these.
- Next: **DOC-09 EC Extensions / Dev**.
