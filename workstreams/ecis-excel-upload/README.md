# ECIS Excel Upload - reusable demo bundle

Self-contained bundle for **EC ECIS Advanced File Import (Excel upload)** on the local sandbox. Start here for
any ECIS Excel-file task: it has the proven scripts, the live evidence, and points to the full runbook.

- **Full how-to + SME lessons:** [`DeepDiveLearnings/ecis-deep-dive/ECIS-UPLOAD-RUNBOOK.md`](../../DeepDiveLearnings/ecis-deep-dive/ECIS-UPLOAD-RUNBOOK.md)
  (4-part step-by-step) + `AUDREY-EXAMPLE-NOTES.md` (gesture recipe) + `ECIS-EXCEL-UPLOAD-DEEP-DIVE.md`.
- **Memory anchor:** `project_ecis_excel_upload_task` (auto-loaded each session) points here.
- **Env:** sandbox `https://ap-f0a7g341jn6d...` (sysadmin/sysadmin); DB `localhost:1521/ORCL` (ECKERNEL_EC/energy).

## What it proves (live, DB-verified)
Excel -> **Upload Files** -> `IMP_SOURCE_INTERFACE_FILE` (DB blob, `FILE_DROP_SERVICE=DB`) -> **EXCEL_IMPORT_1**
(file->`IMP_STAGING`) -> **EXCEL_IMPORT_2** (staging->EC) -> `PWEL_DAY_STATUS.AVG_BH_TEMP`, visible on the
*Daily Prod Well Status 1, by Well* screen (DHT [degC] cell). Wells `AS1_Well_001/002/003`.

## evidence/
- `config_mapping_configuration.png` - the ECIS **config** (Mapping Configuration: CLAUDE_WELL_TEST interface + source/target mappings)
- `pwel_BEFORE.png` / `pwel_AFTER.png` - the well-status screen **before (empty) -> after (filled)**

## sql/ — re-runnable create-config SQL (the delivery artifact)
- **`create_CLAUDE_WELL_TEST_interface.sql`** — recreates the ECIS interface config
  (`IMP_SOURCE_INTERFACE` → `IMP_SOURCE_MAPPING` + `IMP_SOURCE_PATH` per column → `IMP_TARGET_MAPPING`) as one
  PL/SQL block. **Update-insert (idempotent / re-runnable)**, `REV_TEXT='ECPR-XXXX'` on every DML (replace with
  the real ECPR ticket), FK resolved by business key (`ec_functional_area.object_id_by_uk('ECIS')`), no hardcoded
  GUIDs. Mirrors the Pluto `050_Interfaces/V*__ZWP_INTERIM_DATA_UPLOAD.sql` template + **dependency order**
  (parent→child). Proven: delete→run→re-run = 3 mappings / 6 paths / 1 target both times, no dups
  (`scripts/ecis_apply_sql.py`). For COPSDEV: rename to a versioned Flyway file under Pluto_Config/.../050_Interfaces/.
- **`delete_CLAUDE_WELL_TEST_interface.sql`** — TEARDOWN: clears the whole interface config child-first
  (path -> target -> mapping -> interface), scoped to the interface by linkage (handles duplicates/leftovers),
  PRODUCTS UNTOUCHED, idempotent, no COMMIT in file. Proven: CLAUDE -> 0, product mappings unchanged. Run it
  before a clean re-create.
- **`create_ClaudeExcelImport_schedule.sql`** + **`delete_ClaudeExcelImport_schedule.sql`** — the SCHEDULE task
  that *runs* the import (runtime counterpart of the interface config). Modelled on the live **AudreyExcelImport**
  schedule: one schedule, two `ECISAction` instances (exec 10 → `ClaudeJobID` file→staging; exec 20 →
  `ClaudeReadFromStaging` staging→target), `INTERFACE_CODE='CLAUDE_WELL_TEST'`, `FILE_DROP_SERVICE='DB'`,
  `ENABLED='N'` (manual RUN NOW, no cron — like Audrey). Same house style (constants, `IF SQL%ROWCOUNT=0`
  update-insert, `REV_TEXT`, local `upsert_*` procs). Proven: delete→create→re-run = sched + 2 instances +
  13/4 job-config rows both runs, idempotent. **Writes the `jobid` to the `ACTION_INSTANCE_VALUE` base table**
  (sidesteps the `TV_ACTION_INSTANCE_PARAM` join-view `ORA-01779`).
- Recon helper: `scripts/ecis_dump_config.py` (dumps the live rows of the 4 tables).

## scripts/  (run with `py -X utf8 workstreams/ecis-excel-upload/scripts/<name>`)
**Turnkey demo (self-cleaning - empty -> upload -> filled -> reverted):**
- `ecis_pwel_beforeafter.py` - **the demo to run**: config-aware before/after on the EC screen, auto-reverts on teardown.
- `ecis_live_demo.py` - headed end-to-end (upload -> run _1 -> run _2 -> data lands), fresh date.

**Build / rebuild MY interface (CLAUDE_WELL_TEST) via the EC screens:**
- `build_claude_interface.py` -> `build_claude_children.py` (mappings) ; `ecis_build_claude_schedule_db.py` (schedule via DB - see runbook caveat) ; `set_claude_job_params.py`.

**Product path (guaranteed working) + run helpers:**
- `ecis_make_and_upload.py`, `ecis_product_e2e.py`, `ecis_enable_and_run.py <SCHED>`, `ecis_run_both.py`, `ecis_run_stage2.py`, `ecis_disable_schedules.py`, `fix_xlsx_order.py`.

**Recon / diagnostics:**
- `ecis_state_recon.py`, `ecis_sched_recon.py`, `ecis_jobconfig_dump.py`, `recon_param_base.py`, `recon_pwel_screen.py`, `recon_pwel_nav.py`, `recon_as1_scope.py`, `ecis_screens_recon.py`, `ecis_upload2..5.py`, `ecis_run_schedules.py`.

**Self-clean:** `ecis_revert_demo_data.py` - reverts demo AVG_BH_TEMP to NULL.

> Note: scripts write scratch output to `tmp/ecis_recon/` (test xlsx + run screenshots); the committed proof is in `evidence/`.

## 2 SME lessons (full detail in the runbook)
1. **DB-direct schedule build IS achievable** (earlier "walled" finding corrected). The `ORA-01779` only hits
   when the `jobid` is written through the **`TV_ACTION_INSTANCE_PARAM` view** (a join-view). Writing it to the
   **`ACTION_INSTANCE_VALUE` base table** (the AudreyExcelImport / Pluto pattern) works — see
   `sql/create_ClaudeExcelImport_schedule.sql`. The `TV_SCHEDULE` view + `ACTION_INSTANCE` base table also
   insert fine. (Screen / Flyway remain valid too.)
2. **RUN NOW** - decide enable-state from the **DB read** (`tv_schedule_list.enabled`; the UI checkbox isn't
   readable), and it's **async** (run _1, await staging, then _2).

## TODO when next touched (per standing rules)
- Retrofit `build_claude_*` / `ecis_build_claude_schedule_db.py` to be **upsert (re-runnable)** + set
  **`REV_TEXT = ECPR-XXXX`** on every INSERT/UPDATE (see memory `feedback_db_script_rerunnable_revtext`).
- Excel-file touch-ups (user, 2026-06-21).
