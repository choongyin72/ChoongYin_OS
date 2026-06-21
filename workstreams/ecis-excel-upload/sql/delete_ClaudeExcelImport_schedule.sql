-- =====================================================================================================
-- TEARDOWN: clear/remove the ECIS Excel-upload SCHEDULE task ClaudeExcelImport.
-- Counterpart to create_ClaudeExcelImport_schedule.sql.
--
-- * Deletes CHILD-FIRST: ACTION_JOB_CONFIG (the two jobids) -> ACTION_INSTANCE_VALUE -> ACTION_INSTANCE_HISTORY
--   -> ACTION_INSTANCE -> QRTZ triggers/job -> SCHEDULE_HISTORY -> TV_SCHEDULE.
-- * Scoped to the ClaudeExcelImport schedule (by schedule_no) + its two jobids; nothing else is touched.
-- * One declare..begin..end; block, NO COMMIT in the file (caller / Flyway commits). Re-runnable (no-op if absent).
-- =====================================================================================================
declare
  v_sched constant varchar2(200) := 'ClaudeExcelImport';
  v_job1  constant varchar2(100) := 'ClaudeJobID';
  v_job2  constant varchar2(100) := 'ClaudeReadFromStaging';
begin

  -- 1) job-action chains (by jobid)
  DELETE FROM action_job_config WHERE job_id IN (v_job1, v_job2);

  -- 2) instance parameter values + run history + instances (children of the schedule)
  DELETE FROM action_instance_value WHERE action_instance_no IN
    (SELECT action_instance_no FROM action_instance
      WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched));
  DELETE FROM action_instance_history WHERE action_instance_no IN
    (SELECT action_instance_no FROM action_instance
      WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched));
  DELETE FROM action_instance WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched);

  -- 3) quartz trigger rows + schedule run history (defensive: a manual schedule has none until enabled/run)
  DELETE FROM qrtz_cron_triggers  WHERE trigger_name = v_sched;
  DELETE FROM qrtz_fired_triggers WHERE trigger_name = v_sched;
  DELETE FROM qrtz_triggers       WHERE trigger_name = v_sched;
  DELETE FROM qrtz_job_details    WHERE job_name = v_sched;
  DELETE FROM schedule_history WHERE schedule_no IN (SELECT schedule_no FROM tv_schedule WHERE name = v_sched);

  -- 4) the schedule itself
  DELETE FROM tv_schedule WHERE name = v_sched;

end;
/
