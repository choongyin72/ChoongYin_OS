---
name: ecis-excel-upload-builder
description: >
  Build an EC (Energy Components) ECIS Advanced File Import (Excel upload) END-TO-END: interface config +
  source/target mappings + scheduler task + Excel template, then upload → run → DB-verify → evidence doc →
  self-clean. Use when the request is to set up / reproduce / demo an ECIS Excel file upload that lands a
  spreadsheet into an EC class (e.g. "build the ECIS upload for <data> into <class.attr>", "set up a manual
  Excel upload interface + schedule", "reproduce the CLAUDE_WELL_TEST upload"). This is the WHAT, in order;
  pairs with `ec-sql-script-builder` (SQL house style) and `ec-screen-automation` (UI gestures).
---

# ECIS Excel Upload Builder — end-to-end playbook

Proven live + DB-verified (CLAUDE_WELL_TEST / ClaudeExcelImport, 2026-06-21). The reusable bundle and the
full runbook are the exemplars — read them first:
- Bundle: `workstreams/ecis-excel-upload/` (sql/, scripts/, evidence/, README.md)
- Runbook: `DeepDiveLearnings/ecis-deep-dive/ECIS-UPLOAD-RUNBOOK.md`
- Memory: `project_ecis_excel_upload_task`, `feedback_ecis_upload_sequence_and_pace`

## INPUT CONTRACT — only build when the requirement is clear + sufficient
Do NOT start building until you have all of these (ask the user if any is missing — never assume):
1. **Target** EC class + attribute(s) to load (e.g. `PWEL_DAY_STATUS.AVG_BH_PRESS`).
2. **Business keys** that identify a target row (e.g. Well + Date) → become `CLASS_KEY_1/2` and the source
   `KEY_1='ROWS:<col>'`, `KEY_2='ROWS:<col>'`.
3. **Excel layout**: sheet name, column order (key columns + data column(s)), whether there's a header row.
4. **Names**: interface CODE + name, schedule name, functional area (usually `ECIS`).
5. **Verification target**: which EC screen shows the result + a date/scope that has instantiated target rows,
   and the DB view/column for ground truth (e.g. `dv_pwel_day_status.avg_bh_press`).
If the data model, keys, or Excel shape are ambiguous → STOP and ask. A wrong key/attr silently lands 0 rows.

## Guardrails
- **Test on a THROWAWAY code, never churn a shared live config** (repeated delete/recreate makes leftover messes).
- **DB ground truth for every pass claim** — and the REAL end-to-end outcome (does data land?), not row-count proxies.
- **Self-clean**: revert target data to NULL, clear filedrop, disable the schedule — leave the sandbox as found.
- **Never assert an unproven cause; stop + rethink after ~2 fails** (don't grind).
- Client repos under `C:\DEV\GIT\` are READ-ONLY — deliver via Flyway/their PR, never hand-config.

## Steps (in order)
**1. Recon.** Confirm the target class/attribute + keys exist; find the verification screen + a scope with
   instantiated rows + empty baseline. Model on a working interface by DB recon (e.g. `AudreyExcelImport` /
   `EXCEL_IMPORT_1`): dump its source mappings, paths, target mapping, schedule instances + `ACTION_JOB_CONFIG`.

**2. Interface config SQL** (use `ec-sql-script-builder`): `create_<IFACE>.sql` via OV_ views, dependency order —
   `OV_IMP_SOURCE_INTERFACE` (FUNCTIONAL_AREA_CODE='ECIS', SOURCE_TYPE='EXCEL', INTERFACE_TYPE='INSERT_UPDATE')
   → `OV_IMP_SOURCE_MAPPING` (key cols = `KEY_LIST`, data col = `DATA` with `EC_KEY`, `KEY_1/2='ROWS:<col>'`,
   `PATH_ORIGIN='<Sheet>.A1'`) → `OV_IMP_SOURCE_PATH` (per mapping: UPPER_LEFT `Move(col,1)` + LOWER_RIGHT
   `FindVertical("")`; ⚠️ filter on `IMP_SOURCE_MAPPING` (code) not `IMP_SOURCE_MAPPING_CODE` (GUID)) →
   `OV_IMP_TARGET_MAPPING` (CLASS, ATTRIBUTE, EC_KEY, CLASS_KEY_1/2). Plus `delete_<IFACE>.sql` (+ `_ov`)
   teardowns — these classes are INVARIANT → DELETE, not End=Start.

**3. Schedule SQL** (use `ec-sql-script-builder`): `create_<SCHED>.sql` — one `TV_SCHEDULE`, two `ECISAction`
   instances (exec 10 jobid `<X>JobID` file→staging; exec 20 jobid `<X>ReadFromStaging` staging→target), jobid
   written to **base `ACTION_INSTANCE_VALUE`** (NOT the `TV_ACTION_INSTANCE_PARAM` join-view → ORA-01779/01752),
   `ACTION_JOB_CONFIG` chains (10 `AdvancedExcelJobAction` params: `FILE_DROP_SERVICE='DB'`, `INTERFACE_CODE`,
   `FILE_FILTER='*'`, `CONFIG_VALIDATION='Y'`; 20 `StagingJobActionTarget`; then `StagingJobActionSource` +
   `TargetMappingJobAction`). **Set `TV_JOB_SCHEDULE.START_DATE` (Valid From) + `SCHEDULE_TYPE='ONCE'` +
   `SCHEDULE_WHEN_CLASS='SCHEDULE_ONCE'`** (else the Schedule-tab control is blank → EXPIRED). Teardown must delete
   ALL qrtz sub-types (`qrtz_simple_triggers`+cron+blob+fired+triggers+job_details) child-first.

**4. Apply + verify config.** Run create scripts; assert interface counts + schedule (2 instances, job-config
   rows); run `ec-sql-script-builder/sql_idempotency_check.py` (delete→create→re-create = identical, no dup).

**5. Build the Excel.** Sheet **named to match `PATH_ORIGIN`** (e.g. `Data`), columns in the mapped order, real
   key values; **re-pack the .xlsx so `[Content_Types].xml` is the FIRST zip entry** (EC importer expects it;
   openpyxl doesn't do this). A `Sheet1` file against a `Data.A1` interface fails "sheet not found".

**6. Upload → run (the SEQUENCE matters — steps depend on each other):**
   1. **Upload the Excel FIRST** (Upload Files → FA + interface + GO → Select File → Upload File) — into the filedrop.
   2. **Ensure the schedule is ENABLED** (tick Enabled + Save).
   3. **RUN NOW** — only works when ENABLED, never disabled.
   (UI gestures: `ec-screen-automation`. RUN NOW is async; poll the DB.)

**7. Verify end-to-end (DB ground truth):** Upload Files file → `File Status = WRITTEN_TO_EC` (+ Parsed/Written
   dates); Schedule **Monitor tab → run status `OK`**; target table populated (e.g. `dv_pwel_day_status.avg_bh_press`)
   and visible on the screen. 0 rows + "could not find any files in the filedrop area" ⇒ see Gotchas.

**8. Evidence doc.** Per-step screenshots + DB before/after table, one step per page (page breaks). See
   `workstreams/ecis-excel-upload/evidence/`.

**9. Self-clean.** Revert target data to NULL, clear `imp_source_interface_file` + `imp_staging`, disable the schedule.

**10. Deliver.** For client envs, package as Flyway `050_Interfaces/V*__<IFACE>.sql` + `V*__<SCHED>.sql`.

## Gotchas (the hard-won ones — check these)
- ⚠️ **KNOWN OPEN ISSUE — upload→RUN NOW timing.** Clicking RUN NOW seconds after an automated upload reproducibly
  fails ("Could not find any files in the filedrop area / 0 staging rows / folder 'null'"), even with the file
  confirmed committed. The proven success had a longer gap (~minutes) between upload and RUN NOW. Root cause NOT
  yet confirmed (leading hypothesis: a delay before EC makes the file processable). For now: leave a real gap /
  retry RUN NOW after a wait, and verify data actually lands — do NOT trust the run; do NOT claim a cause unproven.
- **Sequence dependency:** upload first → enable → RUN NOW (RUN NOW needs ENABLED). Toggling enable immediately
  before RUN NOW is unreliable.
- **Schedule Type / Valid From must be set** (Schedule-tab control is blank from a bare create → EXPIRED).
- **Excel sheet name must equal the `PATH_ORIGIN` sheet**; `[Content_Types].xml` first in the zip.
- **`FILE_DROP_SERVICE='DB'`** (DB filedrop, no server folder).
- Deleting an already-uploaded file via the UI is **optional** — unrelated to whether the import works.

## Done = an ECIS upload is "built" when
create+delete SQL (interface + schedule, idempotency-proven) + Excel template + a **live, DB-verified end-to-end
run (data lands)** + page-broken evidence doc + self-clean + (for client) Flyway packaging. Reference build:
`workstreams/ecis-excel-upload/` (CLAUDE_WELL_TEST + ClaudeExcelImport).
