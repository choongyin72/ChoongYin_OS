# ECIS Excel Upload - Runbook (local sandbox, end-to-end)

**Goal:** upload a simple Excel file into EC via ECIS and see the data appear on an EC screen.
**Environment:** local sandbox `https://ap-f0a7g341jn6d...` (sysadmin/sysadmin); DB `localhost:1521/ORCL`
(ECKERNEL_EC/energy). **Demo data:** wells `AS1_Well_001/002/003`, date `2003-01-05`, a Pressure value per
well -> lands in `PWEL_DAY_STATUS.AVG_BH_PRESS` (visible via `dv_pwel_day_status` and the well day-status screen).

> The four things this runbook shows: **(A)** the file-upload **interface config**, **(B)** the EC **Scheduler
> task config**, **(C)** how to **upload** the Excel, **(D)** how to **see the uploaded data** in a screen.
> ASCII-only. All ids are PrimeFaces clientIds observed live on this sandbox.

---

## Concept in one paragraph
ECIS "Advanced File Import" turns a spreadsheet into EC records in two hops:
**Excel file -> (AdvancedExcel job) -> IMP_STAGING -> (TargetMapping job) -> EC class table.**
You configure ONE **interface** (how to read the sheet + where each value goes) on the *Mapping Configuration*
screen, and ONE **schedule** (an EC Scheduler task whose Business Action `ECISAction` runs the job-action
chain) on the *Schedules* screen. Files are provided via the *Upload Files* screen because the job uses
**FILE_DROP_SERVICE = DB** (no server folder needed - the file is stored as a blob in
`IMP_SOURCE_INTERFACE_FILE`). You trigger it with **RUN NOW** (or it fires on its cron trigger).

---

## Part A - File-upload INTERFACE config  (screen: Mapping Configuration)
Interface built here = **CLAUDE_WELL_TEST** (DB-verified rebuilt 2026-06-20).

**A1. Create the interface row** - Insert > *Source Interface*, fill the blank row:
| Col | Field | Value |
|----|-------|-------|
| C0 | Interface Code | `CLAUDE_WELL_TEST` |
| C1 | Name | `Claude Well Test` |
| C2 | Functional Area | `ECIS Interface Area` |
| C3 | Transaction Type | `First Insert then Update` (INSERT_UPDATE) |
| C4 | Source Type | `Row based transactions` (ROW) |
| C5 | Type | `Excel` |
| C7 | EC Valid Level | `Provisional` |
| C8 | EC Data Level | `Provisional` |
| C9 | Overwrite | `Full` |

Save (toolbar disk icon). **Gotcha:** Save is async - re-read the DB to confirm; the UI's own "saved" signal
can precede the commit (the build script's immediate check showed empty, but the row WAS there a moment later).

**A2. Source mappings** (grid SOURCE MAPPING; one row per column you read). Origin cell `Data.A1`:
| Mapping | Exec | Type | Data type | EC Key | Key 1 | Key 2 |
|---------|------|------|-----------|--------|-------|-------|
| WELL | 10 | KEY_LIST | STRING | - | - | - |
| DATE | 20 | KEY_LIST | DATE | - | - | - |
| PRESSURE | 30 | DATA | NUMBER | `claudePress` | `ROWS:WELL` | `ROWS:DATE` |

**A3. Source mapping commands** (tab "Source Mapping Commands"; how to find each column's cells in the sheet):
- WELL: `UPPER_LEFT Move(0,1)` then `LOWER_RIGHT FindVertical("")`
- DATE: `UPPER_LEFT Move(1,1)` then `LOWER_RIGHT FindVertical("")`
- PRESSURE: `UPPER_LEFT Move(2,1)` then `LOWER_RIGHT FindVertical("")`
  (Move(col,row) from the header cell; FindVertical("") = read down until a blank row.)

**A4. Target mapping** (bottom grid; where the value lands):
- `claudePress` -> class `PWEL_DAY_STATUS`, attribute `AVG_BH_PRESS`, **Class Key 1 = KEY_1** (well code),
  **Class Key 2 = KEY_2** (date). (Class keys are discoverable via `ECDP_ADV_EXCEL_HELPER.getKey(class,n)`.)

**Mapping Configuration UI gotchas:** grid dropdown cells need the `_dd_button` + panel `tr[data-item-label]`
click (typing+Tab does NOT commit); dd labels are DISPLAY text ('First Insert then Update', 'Row based
transactions', 'Move(col, row)', 'FindVertical(text)', 'Key 1'/'Key 2'); the Insert menu item "Source
Interface" exists in BOTH Insert and Delete submenus -> disambiguate with `contains(@onclick,"insert")`.

---

## Part B - EC SCHEDULER task config  (screen: Schedules)
A schedule is an EC Scheduler task. For ECIS it carries a Business Action **`ECISAction`**
(`com.ec.frmw.is.dc.core.businessaction.ECISAction`) whose `jobid` param points at an **ACTION_JOB_CONFIG**
chain. Two layout options (both proven on this sandbox):

- **Product pattern (two schedules):** `EXCEL_IMPORT_1` = file->staging, `EXCEL_IMPORT_2` = staging->EC.
- **My pattern (one schedule):** `CLAUDE_EXCEL_IMPORT` = one job chaining 10 AdvancedExcel -> 20 StagingTarget
  -> 30 TargetMapping. Simpler; works for a manual RUN NOW.

**Exact DB anatomy (dumped live from the proven `EXCEL_IMPORT_1`):**
```
TV_SCHEDULE_LIST        : SCHEDULE_NO 5079, NAME EXCEL_IMPORT_1, ENABLED N, STATUS EXPIRED
TV_ACTION_INSTANCE      : ACTION_INSTANCE_NO 5214, BUSINESS_ACTION_NAME 'ECISAction',
                          BUSINESS_ACTION_NO 8, EXEC_ORDER 10, SCHEDULE_NO 5079, FA 'ECIS', RECORD_STATUS P
TV_ACTION_INSTANCE_PARAM: NAME 'jobid', PARAMETER_VALUE 'EXCEL_IMPORT_1', PARAMETER_TYPE BASIC_TYPE,
                          PARAMETER_SUBTYPE STRING, ACTION_INSTANCE_NO 5214
ACTION_JOB_CONFIG (JOB_ID 'EXCEL_IMPORT_1') : per JOB_ACTION_NO ->
   10 JOB_ACTION_CLASS 'AdvancedExcelJobAction'  params: FILE_DROP_SERVICE=DB, INTERFACE_CODE=EXCEL_IMPORT,
                                                          FILE_FILTER=*, CONFIG_VALIDATION=Y, FTP_* empty
   20 JOB_ACTION_CLASS 'StagingJobActionTarget'
   (EXCEL_IMPORT_2's JOB_ID chain = 10 StagingJobActionSource -> 20 TargetMappingJobAction = staging->EC)
```
So to build **CLAUDE_EXCEL_IMPORT** equivalently (one schedule, full chain) you create: the schedule row;
one `ECISAction` instance (EXEC_ORDER 10) with param `jobid=CLAUDE_JOB`; and an `ACTION_JOB_CONFIG` for
`CLAUDE_JOB` = 10 AdvancedExcelJobAction (INTERFACE_CODE=`CLAUDE_WELL_TEST`, FILE_DROP_SERVICE=DB,
FILE_FILTER=*, CONFIG_VALIDATION=Y) -> 20 StagingJobActionTarget -> 30 TargetMappingJobAction.

**Schedules UI gotchas:** the navigator `Active Status` dd defaults to *Enabled* (new/expired schedules are
hidden) -> set it to **All** + GO, then find your schedule via the **Name filter** (`schedule:form:T:sfilter0`);
the grid is inline so row "names" are INPUT VALUES not cell text; RUN NOW = `runNowButton:form:B`; the Enabled
checkbox is on the DETAILS tab (`tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb`) + toolbar Save; job-action
param rows AUTO-GENERATE when the action row is created (just fill values).

---

## Part C - Upload the Excel  (screen: Upload Files)
**C1. The Excel** - sheet `Data`, header row 1 = `Well | Date | Pressure`, then one row per well:
```
Well          Date         Pressure
AS1_Well_001  2003-01-05   151.5
AS1_Well_002  2003-01-05   152.7
AS1_Well_003  2003-01-05   153.9
```
**Gotcha (cost a whole debug cycle):** openpyxl writes the zip with `docProps` first, so EC/Tika rejects it as
`application/zip`. Fix: rewrite the .xlsx zip so **`[Content_Types].xml` is the FIRST entry**
(`tmp/scripts/fix_xlsx_order.py`, also inlined in `claude_e2e_run.py`).

**C2. Upload** - open *Upload Files*: pick **Functional Area** = `ECIS Interface Area` -> **Interface** =
`Claude Well Test` -> **GO** (mandatory; without GO first you get "Missing values in required fields") ->
choose the file (input `upload_file_btn:form:fa_input`) -> click **Upload File** (button has no id; click by
text, visible only). The file lands in `IMP_SOURCE_INTERFACE_FILE` (FILE_CONTENT blob; UPLOADED_INTO_EC_IND
tracks state).

---

## Part D - Run it + see the data
**D1. Enable + RUN NOW** - Schedules -> Active Status=All + GO -> find `CLAUDE_EXCEL_IMPORT` -> DETAILS tab:
tick **Enabled** + Save (RUN NOW refuses a disabled schedule: "Enable before you run schedule") -> click
**RUN NOW** -> confirm. (One-schedule design runs the whole chain; product two-schedule design = RUN NOW _1
then _2.) Restore by un-ticking Enabled + Save afterwards.

**D2. Verify (DB ground truth):**
```sql
SELECT object_code, avg_bh_press FROM dv_pwel_day_status
 WHERE daytime = DATE '2003-01-05' AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003');
-- expect 151.5 / 152.7 / 153.9   (baseline before run = NULL, confirmed clean 2026-06-20)
```
Intermediate checks: `IMP_SOURCE_INTERFACE_FILE` (file present), `IMP_STAGING` (rows after the AdvancedExcel
job), `TV_ACTION_INSTANCE_HISTORY` (run_status OK per ECISAction).

**D3. See it on a screen:** open the well **Daily Status** screen for those wells on 2003-01-05 -> the Pressure
(AVG_BH_PRESS) cells show the uploaded values. (This is the "data visible in EC" proof the upload worked.)

---

## Current live status (2026-06-20, this session)
- **Part A DONE + DB-verified live:** `CLAUDE_WELL_TEST` interface + all source/target mappings rebuilt via the
  Mapping Configuration UI (scripts `build_claude_interface.py`, `build_claude_children.py`). Baseline
  `dv_pwel_day_status` for the test date confirmed empty (clean).
- **Part B PARTIAL (blocker, not thrashed):** `CLAUDE_EXCEL_IMPORT` schedule SHELL created (TV_SCHEDULE_LIST
  5110, STATUS WAITING) but its `ECISAction` + job-action chain did NOT get added - the Schedules-screen build
  (`build_claude_schedule.py`) timed out on the inline-grid re-find after creating the shell. Per the agreed
  policy I stopped thrashing the screen and characterised the exact wiring from the DB instead (Part B above).
  **Two clean ways to finish it:** (i) do it on the Schedules screen together (live), or (ii) the way it is
  REALLY delivered to COPSDEV anyway - **Flyway SQL** mirroring the EXCEL_IMPORT rows (As-Built 05 pattern) -
  never hand-config production.
- **Parts C/D:** ready; the live RUN NOW carries a known sandbox risk (RUN NOW may not fire without an EC app
  restart; REST fallback `POST /services/ecis/interfaces/<CODE>/files` exists) - best run together so we can
  watch it land.

## Proven fallback for a guaranteed live demo
The product example **`EXCEL_IMPORT` interface + `EXCEL_IMPORT_1/_2` schedules** survived the sandbox refresh
and is wired correctly. Tooling ready: `ecis_make_and_upload.py` (gen+upload), `ecis_enable_and_run.py <SCHED>`
(enable+RUN NOW+verify), `ecis_disable_schedules.py` (restore). If the custom schedule path stalls, we
demonstrate the identical end-to-end on EXCEL_IMPORT (lands `PWEL_DAY_STATUS.AVG_BH_TEMP`).

## Real-project delivery (not this sandbox demo)
For COPSDEV the interface + schedule are delivered as paired Flyway migrations in the Woodside repo
`Pluto_Config/.../050_Interfaces/` (V*__<IFACE>.sql + V*__SCHED_<name>.sql) mirroring As-Built 05
(`ZWP_INTERIM_DATA_UPLOAD` is the closest precedent). Never hand-configure COPSDEV via the screens.

_Built 2026-06-20 on branch feature/ecis-excel-upload-demo. Source of truth for gestures: AUDREY-EXAMPLE-NOTES.md._
