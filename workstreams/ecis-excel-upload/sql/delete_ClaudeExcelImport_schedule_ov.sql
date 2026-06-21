-- =====================================================================================================
-- TEARDOWN of the ClaudeExcelImport schedule preferring the TV_ object VIEWS (view-class-level delete),
-- falling back to the base table ONLY where the view cannot be deleted through.
-- Alternative to delete_ClaudeExcelImport_schedule.sql (which deletes base tables directly).
--
-- Verified on the sandbox (2026-06-21), child-first. What deletes via a VIEW vs needs a BASE fallback:
--   * Job chains      -> VIEW  TV_ECIS_ACTION_JOB_PARAM            (instead-of-delete; OK)
--   * jobid VALUES    -> BASE  ACTION_INSTANCE_VALUE              (TV_ACTION_INSTANCE_PARAM is a join-view ->
--                                                                  ORA-01752 "cannot delete from a join view")
--   * Action instances-> VIEW  TV_ACTION_INSTANCE                 (instead-of-delete; OK, once VALUES gone)
--   * Schedule        -> VIEW  TV_SCHEDULE                        (instead-of-delete; OK, once INSTANCES gone -
--                                                                  else ORA-02292 FK_ACTION_INSTANCE_1)
--   * QRTZ triggers / run-history -> BASE (no views exist for these); defensive, only present once enabled/run.
--
-- Scoped to ClaudeExcelImport (by name) + its two jobids. Re-runnable (subquery scoping => no-op if absent, no
-- NO_DATA_FOUND). One declare..begin..end; - NO COMMIT in the file (caller / Flyway commits).
-- =====================================================================================================
declare
  v_sched constant varchar2(200) := 'ClaudeExcelImport';
  v_job1  constant varchar2(100) := 'ClaudeJobID';
  v_job2  constant varchar2(100) := 'ClaudeReadFromStaging';
begin

  -- 1) JOB CHAINS  -- VIEW: TV_ECIS_ACTION_JOB_PARAM
  DELETE FROM TV_ECIS_ACTION_JOB_PARAM WHERE job_id IN (v_job1, v_job2);

  -- 2) instance run-history  -- BASE (no view); child of action_instance, remove before instances
  DELETE FROM ACTION_INSTANCE_HISTORY WHERE action_instance_no IN
    (SELECT action_instance_no FROM action_instance
      WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched));

  -- 3) jobid parameter VALUES  -- BASE fallback (TV_ACTION_INSTANCE_PARAM is a non-deletable join-view, ORA-01752)
  DELETE FROM ACTION_INSTANCE_VALUE WHERE action_instance_no IN
    (SELECT action_instance_no FROM action_instance
      WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched));

  -- 4) ACTION INSTANCES  -- VIEW: TV_ACTION_INSTANCE
  DELETE FROM TV_ACTION_INSTANCE
   WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched);

  -- 5) quartz trigger rows  -- BASE (no view); defensive
  DELETE FROM QRTZ_SIMPLE_TRIGGERS WHERE trigger_name = v_sched;  -- ONCE schedule -> simple trigger
  DELETE FROM QRTZ_CRON_TRIGGERS   WHERE trigger_name = v_sched;
  DELETE FROM QRTZ_BLOB_TRIGGERS   WHERE trigger_name = v_sched;
  DELETE FROM QRTZ_FIRED_TRIGGERS  WHERE trigger_name = v_sched;
  DELETE FROM QRTZ_TRIGGERS        WHERE trigger_name = v_sched;
  DELETE FROM QRTZ_JOB_DETAILS     WHERE job_name = v_sched;

  -- 6) schedule run-history  -- BASE (no view); child of schedule, remove before schedule
  DELETE FROM SCHEDULE_HISTORY WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched);

  -- 7) the SCHEDULE  -- VIEW: TV_SCHEDULE
  DELETE FROM TV_SCHEDULE WHERE name = v_sched;

end;
/
