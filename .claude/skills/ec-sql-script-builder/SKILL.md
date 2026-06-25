---
name: ec-sql-script-builder
description: >
  Produce high-quality, re-runnable EC (Energy Components) config/scheduler SQL scripts in the proven house
  style. Use whenever generating or refactoring SQL that writes EC configuration (interfaces, mappings,
  schedules, business actions, object views OV_*/TV_*, ECIS, IUD config) or any DB script that must be
  idempotent + auditable. Covers the format, the create+delete pairing, the verify-before-assume gotchas,
  and the mandatory verification + pace discipline learned from the ECIS Excel-upload build.
---

# EC SQL Script Builder — house style + standards

Goal: every EC SQL script we produce is **clean, readable, re-runnable (idempotent), auditable, and
delivery-ready** (Flyway). Follow this exactly; deviate only with a stated reason.

Reference exemplars (read before writing): `workstreams/ecis-excel-upload/sql/` —
`create_CLAUDE_WELL_TEST_interface.sql`, `create_ClaudeExcelImport_schedule.sql`, and their `delete_*` +
`delete_*_ov.sql` teardowns. Client pattern: Woodside Pluto `Pluto_Config/.../050_Interfaces/V*.sql`.
Related memory: `feedback_db_script_rerunnable_revtext`, `feedback_ecis_upload_sequence_and_pace`.

**Companion files in this skill:**
- `sql_idempotency_check.py` — the re-runnability harness (delete→create→re-create→assert counts); see §5.
- `references/sql-precommit-checklist.md` — 10-tick scan before committing.
- `references/ec-config-tables-glossary.md` — EC config tables/views, VERSIONED vs INVARIANT, delete method, gotchas.

## 1. Format rules (non-negotiable)
1. **Write through the `OV_*` / `TV_*` object views**, not base `IMP_*`/base tables, when a view exists — its
   INSTEAD-OF trigger handles object_id / rec_id / date-effective housekeeping. (Base tables only where no
   usable view, or where a view is a non-deletable join-view — see §4.)
2. **FK by business CODE, never hardcoded GUIDs.** Resolve parents by code subquery
   (`(SELECT object_id FROM OV_x WHERE code = v_code)`) or `EcDp_Objects.GetObjIDFromCode('FUNCTIONAL_AREA','ECIS')`.
3. **Hoist repeated literals into `DECLARE` constants** — `v_code`, `v_rev` (the ECPR ticket), date constants
   (`v_sd`), class-name constants. Never repeat a literal inline.
4. **Update-insert (idempotent), this exact pattern — NO `MERGE`, NO `SELECT … NOT EXISTS`:**
   ```sql
   UPDATE OV_x SET <cols>, REV_TEXT = v_rev WHERE <business key>;
   IF SQL%ROWCOUNT = 0 THEN
     INSERT INTO OV_x (<cols>, REV_TEXT) VALUES (<vals>, v_rev);
   END IF;
   ```
5. **Flat blocks, one per row — NOT local procedures.** Repetition is fine and matches the EC norm; procedures
   hurt readability/auditability (we tried, reverted).
6. **`REV_TEXT = 'ECPR-XXXX'` on every INSERT and UPDATE** (the governing change ticket; `ECPR-DEMO` only for
   throwaway experiments, flagged as such). Ties each row to its change request.
7. **NO `BEGIN/EXCEPTION` block, NO `COMMIT` in the file.** One `declare … begin <statements> end; /`. The
   caller / Flyway commits.
8. **Dependency order:** CREATE = parent → child (e.g. INTERFACE → SOURCE_MAPPING → SOURCE_PATH → TARGET_MAPPING).
   DELETE = child → parent.

## 2. Header comment standard
Every script opens with a banner: what it builds/removes, the object/table, the style note, and a **STATUS**
line (`VERIFIED <date>` with how, or `RUNTIME-VERIFY PENDING` with why). Note any non-obvious gotcha inline.

## 3. Always ship the create + a matching teardown
- `create_<NAME>.sql` (update-insert) **and** `delete_<NAME>.sql` (teardown). Optionally `delete_<NAME>_ov.sql`
  (view-level delete) when the views support it.
- Teardowns: **child-first, scoped by business key/linkage, re-runnable (no-op if absent), no COMMIT.** Delete
  by linkage (not object_code) so leftovers/duplicates are caught regardless of how their codes were set.
- Products/other configs **must stay untouched** — scope strictly to the object you own.

## 4. Verify-before-assume gotchas (these bit us — check every time)
- **OV_ column: CODE vs OBJECT_ID.** Before filtering, confirm which column holds the *business code* vs the
  *object_id (GUID)*. On `OV_IMP_SOURCE_PATH`, `IMP_SOURCE_MAPPING` = the code ('WELL'); `IMP_SOURCE_MAPPING_CODE`
  = the GUID. Filtering the wrong one silently matches 0 rows → spurious INSERT → `ORA-00001`. Don't assume
  `*_CODE` is the code.
- **Delete method depends on `class_cnfg.TIME_SCOPE_CODE`:** `VERSIONED` (date-effective, e.g. Bank) ⇒ delete by
  **End Date = Start Date**; `INVARIANT` (e.g. ECIS interface classes) ⇒ End=Start does NOT remove it (the OV
  view ignores END_DATE) → use a real **`DELETE`** (via the OV view's INSTEAD-OF-DELETE trigger, or base tables).
  Check the time scope first.
- **Some view columns are DERIVED, not settable.** e.g. on `TV_JOB_SCHEDULE`, `START_DATE`/`SCHEDULE_TYPE` persist
  via a view UPDATE, but `NEXT_FIRE_TIME`/`STATUS` are computed by the app (a raw UPDATE won't stick; `WAITING`
  needs a QRTZ trigger the app creates on save). Know what SQL can and cannot set; don't fake derived state.
- **Schedules: teardown must remove ALL qrtz child rows** — `qrtz_simple_triggers` (ONCE), `qrtz_cron_triggers`,
  `qrtz_blob_triggers`, `qrtz_fired_triggers`, `qrtz_triggers`, `qrtz_job_details` — child-first, or you hit
  `FK_QRTZ_SIMPLE_TRIGGERS_1` / similar.
- **Non-deletable join-views:** `DELETE FROM` a TV_ join-view → `ORA-01752`/`ORA-01779`. Fall back to the base
  table for that level only (document why), keep the rest view-level.

## 5. Verification — mandatory before calling a script "done"
1. **Idempotency proof:** run `delete → create → create-again` and assert the object counts are **identical both
   create runs**, no duplicates, no error. (Tiny py harness pattern: run each .sql block, count, assert.)
2. **Prove the REAL outcome, not a proxy.** Row counts (3/6/1) are necessary but NOT sufficient — verify the
   config actually *works end-to-end* (the import lands, the schedule runs, the data appears). "Idempotent +
   right counts" can still be functionally broken.
3. **Test on a THROWAWAY code/object, never churn the shared live config.** Repeated delete/recreate of the
   live object creates leftover-data messes and false signals.
4. **Cite the proof** in the commit/PR (live N/N pass + the exact assertion).

## 6. Pace discipline (the meta-lesson)
Refactor is where speed turns dangerous: a fresh build that *looks* done can be subtly broken.
- **Never state a root cause you haven't demonstrated.** Don't put unproven theories in the user's hands as fact.
- **Stop + rethink after ~2 failures** of the same thing — investigate, don't grind/re-run blindly.
- One controlled change at a time; verify the actual result before the next change.

## 7. Skeleton
```sql
-- =====================================================================================================
-- <CREATE|TEARDOWN> <object> <CODE>.  <one-line purpose>
-- Style: OV_ views, FK by code, update-insert (UPDATE; IF SQL%ROWCOUNT=0 THEN INSERT), REV_TEXT, no MERGE,
--        no exception, no COMMIT.  STATUS: <VERIFIED yyyy-mm-dd how | RUNTIME-VERIFY PENDING why>
-- =====================================================================================================
declare
  v_code constant varchar2(30) := '<CODE>';
  v_rev  constant varchar2(30) := 'ECPR-XXXX';
  v_sd   constant date         := to_date('2000-01-01','YYYY-MM-DD');
begin
  UPDATE OV_x SET <cols>, rev_text = v_rev WHERE code = v_code;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO OV_x (code, <cols>, rev_text) VALUES (v_code, <vals>, v_rev);
  END IF;
  -- … child objects, parent→child …
end;
/
```

## 8. Delivery
For client envs (e.g. COPSDEV), rename to a versioned Flyway file under the client repo
`<Config>/.../db/migration/<ver>/050_Interfaces/V*__<NAME>.sql` — never hand-config the env. Client repos
under `C:\DEV\GIT\` are READ-ONLY (deliver via their PR process).
