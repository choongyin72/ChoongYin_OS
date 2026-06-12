# ECIS Excel File Upload + EC Scheduler — Deep Dive
**Date:** 2026-06-12 · **Purpose:** real project task — manual Excel upload as a BACKUP
path for PHD data when the automated PHD process is down (target: COPSDEV) + EC Scheduler
implementation. **Sources:** EC 14.2.4/5 tech docs (full pages in `docs/`), COPSDEV live
config (`copsdev_examples.json`), Woodside repo Flyway precedents, local docs KB.

---

## 1. THE BIG PICTURE (Advanced File Import)

```
Excel file ──> [1] Source mappings ──> [2] STAGING area ──> [3] Target mappings ──> [4] EC class data
              (read cells by paths)    (IMP_STAGING)        (ECKey -> Class.Attr)     (insert/update)
              └────── extraction ──────┘                  └────────── loading ──────────┘
```
- Everything is configured **in EC screens** (no code needed unless user exits).
- Execution = **EC Scheduler** running ECIS **Job Actions**; monitoring = Scheduler History.
- File pickup: **drop folder** on the app server, **FTP**, or — the Woodside way — **DB file
  drop** (`FILE_DROP_SERVICE=DB`): the user uploads the Excel via the EC screen; the file is
  stored in `IMP_SOURCE_INTERFACE_FILE`, no server filesystem access needed. Perfect for a
  manual backup flow.

## 2. THE FOUR CONFIG OBJECTS (screens ↔ tables)

| Screen | Table | Holds |
|---|---|---|
| Mapping Configuration (interface) | `IMP_SOURCE_INTERFACE` | Interface code/name, Type (INSERT / INSERT_UPDATE / UPDATE), Transaction Type (ROW vs JOB), Source Type (EXCEL/CSV/TEXT/XML), Overwrite (FULL/INCREMENTAL), EC Data Level (P/V/A), EC Validation Level, Manual-staging flag, 4 user-exit hooks |
| — source mappings | `IMP_SOURCE_MAPPING` | One per extracted value-set: `PATH_ORIGIN` (`Sheet.Cell`, e.g. `Upload_data.C2`), TYPE = KEY_VALUE / **KEY_LIST** (1-D list) / **DATA** (value set), VALUE_TYPE (STRING/DATE/NUMBER), `EC_KEY` links DATA mappings to a target mapping, KEY_1..10 |
| — source paths | `IMP_SOURCE_PATH` | Per mapping: UPPER_LEFT + LOWER_RIGHT commands — `Move(x,y)`, `FindVertical("txt"[,CELL_BEFORE])`, `FindHorizontal(...)`; `FindVertical("")` = read until first blank cell |
| Target Mapping Configuration | `IMP_TARGET_MAPPING` | `EC_KEY` → CLASS + ATTRIBUTE; CLASS_KEY_1..10 link staging keys → class PK columns in order; CONSTANT_STRING/NUMBER/DATE for mandatory attrs absent from the file; FROM/TO_UNIT conversion |
| User Exit Configuration | UE columns on the above | Java or **PLSQL** hooks: pre/post **staging**, pre/post **EC write**; at interface OR mapping level. PLSQL signature = proc(interface_code, code, file_name, ec_key, key_1..10, numeric/date/string_value) |
| Mapping Codes | (EC codes) | seen in repo `EXC_*__MAPPING_CODE.sql` — code lists used by mappings |
| Staging Area (preview) | `IMP_STAGING` | imported rows awaiting (optional manual) promotion; "import data" button when `Manual Staging Import` ticked |
| Import History | — | what was loaded, per interface+file+date |

## 3. EXECUTION — ECIS JOB ACTIONS + SCHEDULER (CO.0130)

Job Action classes (`com.ec.ecdm.is.advancedexcel.*`):
1. `sourcemapping.jobaction.AdvancedExcelJobAction` — file → staging format
2. `staging.jobaction.StagingJobActionTarget` — staging format → `IMP_STAGING`
3. `staging.jobaction.StagingJobActionSource[Chunked]` — staging → loading pipeline (per file; Chunked for big files)
4. `targetmapping.jobaction.TargetMappingJobAction` — write to EC classes

**Flow options:** automated = one schedule chains 1→2→4. Manual-staging = two schedules
(1→2, then 3→4 after a human clicks IMPORT DATA in the Staging screen).
*For a PHD-backup flow, Manual Staging = recommended: the operator uploads, REVIEWS the
staging preview, then promotes.*

**Scheduler anatomy** (from the Woodside SCHED_* migrations — the real thing):
```
TV_SCHEDULE_LIST   (NAME, FUNCTIONAL_AREA_ID='ECIS', ENABLED, START_DATE)
TV_SCHEDULE_DETAILS(USERNAME='sysadmin', LOG_LEVEL, IGNORE_MISFIRE, RETAIN_COUNT)
TV_JOB_SCHEDULE    (SCHEDULE_TYPE='ONCE' | cron-like, PIN_TO='EC-Cluster:ECDS', SCHEDULE_WHEN_CLASS)
QRTZ_JOB_DETAILS   (Quartz job → com.ec.frmw.scheduler.job.BusinessControllerInvokerJob)
TV_ACTION_INSTANCE (links the schedule to BUSINESS_ACTION 'ECISAction', EXEC_ORDER)
ACTION_JOB_CONFIG  (params per Job Action: DROP_FOLDER, COMPLETED_FOLDER, ERROR_FOLDER,
                    FILE_FILTER, FILE_DROP_SERVICE='DB'!, FTP_*, INTERFACE...)
```
- Business Action `ECISAction` + per-action `ACTION_JOB_CONFIG` rows = the import job.
- Tag-style ECIS uses BA on `com.ec.frmw.is.engine.source.action.SourceAction` with
  mandatory params `configurationid` (DT_SOURCE_ID) + `jobid` — not needed for the
  DB-file-drop Excel path.

## 4. THE WOODSIDE PRECEDENTS (COPSDEV live + repo Flyway)

**6 live interfaces on COPSDEV** (full dump: `copsdev_examples.json`):
| Interface | Purpose | UE |
|---|---|---|
| **ZWP_INTERIM_DATA_UPLOAD** | "Interim Data upload" — THE backup-style upload precedent | `ZWP_P_ECIS_UTIL.runPostStaging` (post-staging PLSQL) |
| ZWP_PROD_TARGET | Production targets → `FCST_FCTY1_DAY_STATUS` (+ZWP_* cols) | `ZWP_P_ECIS_UTIL.processFcstScen` |
| ZWP_PROD_WELL_RESULT | Well test results | `ZWP_P_ECIS_UTIL.postStagingWellTestResultInterface` |
| I_IN_RAU_TARGET / I_IN_UPLOAD_GAS_OIL_GREASE / I_IN_TAS | other uploads | — |

**The ZWP pattern** (key insight): Excel rows land in thin ZWP holding classes
(`ZWP_I_UPLOAD_INT_VALUE`: CLASS_NAME, KEY, DATE, OBJECT_CODE, ACCOUNT/COMPANY_CODE,
TIME_SPAN, COLUMN_NAME, VALUE), then the **post-staging PLSQL user exit distributes** the
generic rows into the real EC tables. This keeps ONE generic Excel format able to feed many
target classes — exactly what a PHD-backup sheet wants (CLASS_NAME + OBJECT + DATE +
COLUMN_NAME + VALUE = any data class).

**Excel layout** (ZWP_INTERIM_DATA_UPLOAD, sheet `Upload_data`, headers row 1, data from row 2):
| A | B | C | D | E..H | I |
|---|---|---|---|---|---|
| CLASS_NAME | KEY | DATE | OBJECT_CODE | (acc/company/span/column) | VALUE |
Every column = one source mapping with origin `Upload_data.<Col>2`, paths
`UPPER_LEFT Move(0,0)` + `LOWER_RIGHT FindVertical("")` (read until blank). KEY_LISTs for
the key columns, DATA (with EC_KEY → target mapping) for value columns.

**Delivery pattern:** config ships as **Flyway migrations** in
`extensions/Pluto_Config/.../NNN/050_Interfaces/` — paired scripts:
- `V*__<INTERFACE>.sql` — idempotent PL/SQL inserts into IMP_* (NOT EXISTS guards,
  `ec_imp_source_interface.object_id_by_uk(...)` lookups)
- `V*__SCHED_<NAME>.sql` — schedule + business action + ACTION_JOB_CONFIG params
Packages (`ZWP_P_ECIS_UTIL`) live in `Pluto_Base/.../packages/R__0400/0500_*.sql`;
holding classes as class XMLs in `Pluto_Base/.../classes/`.

## 5. IMPLEMENTATION PROPOSAL (PHD-backup upload — for discussion)

1. **Reuse, not rebuild**: `ZWP_INTERIM_DATA_UPLOAD` may already cover the PHD-backup need
   (generic CLASS_NAME/OBJECT/DATE/COLUMN/VALUE). First question for the 10am discussion:
   does the backup data fit the existing interim format, or do PHD classes (stream/well
   daily statuses, gas component analyses) need a dedicated interface + UE distribution?
2. If dedicated: follow the ZWP pattern — new sheet layout per PHD class family, new
   interface Flyway script + (likely) new `ZWP_P_ECIS_UTIL` procedure, Manual Staging = Y
   for operator review, EC_DATA_LEVEL = P.
3. **Schedule**: SCHED_* Flyway twin; SCHEDULE_TYPE ONCE (run-on-demand after upload) or
   interval polling of the DB drop — existing precedents use ONCE + manual run.
4. Local sandbox first for the working example (awaiting the sample Excel), then COPSDEV
   via Flyway PR — never hand-config on COPSDEV.

## 6. OPEN ITEMS / NEXT STEPS
- [ ] 10am: discuss reuse-vs-new interface; get sample Excel + Scheduler example access
- [ ] Read `ZWP_P_ECIS_UTIL` body (runPostStaging) — the distribution logic
- [ ] ECpedia pass (BPR space) for upload best practices
- [ ] ec-application source: `com.ec.ecdm.is.advancedexcel` module walk-through
- [ ] Local sandbox: recon the 5 screens (Mapping Config, Target Mapping, User Exit,
      Staging Area, Import History) + build the working example end-to-end
- [ ] COPSDEV proposal (Flyway scripts) for sign-off
