-- =====================================================================================================
-- ECIS Excel-upload SCHEDULE task: ClaudeExcelImport  (runtime counterpart of create_CLAUDE_WELL_TEST_interface.sql)
--
-- Modelled on the live AudreyExcelImport schedule: ONE schedule holding TWO ECISAction instances -
--   exec 10 -> jobid ClaudeJobID          : AdvancedExcelJobAction (file -> IMP_STAGING) + StagingJobActionTarget
--   exec 20 -> jobid ClaudeReadFromStaging : StagingJobActionSource (IMP_STAGING -> target) + TargetMappingJobAction
-- both job chains carry INTERFACE_CODE = 'CLAUDE_WELL_TEST', FILE_DROP_SERVICE = 'DB'.
--
-- Style (per the Pluto 050_Interfaces SCHEDULE files + house rules):
--   * DECLARE constants (schedule/interface/jobids/REV_TEXT) + class-name constants - reuse, no inline repeats.
--   * Update-insert: UPDATE ...; IF SQL%ROWCOUNT = 0 THEN INSERT ...; END IF;  (idempotent / re-runnable) - NO MERGE.
--   * REV_TEXT = 'ECPR-XXXX' on every INSERT/UPDATE for audit (replace with the real ECPR ticket).
--   * Local procedures upsert_instance / upsert_cfg = the reused update-insert logic.
--   * One declare..begin..end; - NO exception block, NO COMMIT in the file (caller / Flyway commits).
--
-- The jobid parameter is written to the ACTION_INSTANCE_VALUE *base table* (the AudreyExcelImport / Pluto
-- pattern) - NOT through the TV_ACTION_INSTANCE_PARAM view, which is a join-view that raises ORA-01779.
-- ENABLED = 'N', no cron trigger: run manually (RUN NOW), exactly like AudreyExcelImport.
-- =====================================================================================================
declare
  v_sched constant varchar2(200) := 'ClaudeExcelImport';
  v_iface constant varchar2(30)  := 'CLAUDE_WELL_TEST';
  v_job1  constant varchar2(100) := 'ClaudeJobID';            -- file  -> staging
  v_job2  constant varchar2(100) := 'ClaudeReadFromStaging';  -- staging -> target
  v_rev   constant varchar2(30)  := 'ECPR-XXXX';
  c_adv   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.sourcemapping.jobaction.AdvancedExcelJobAction';
  c_sgt   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.staging.jobaction.StagingJobActionTarget';
  c_sgs   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.staging.jobaction.StagingJobActionSource';
  c_tgt   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.targetmapping.jobaction.TargetMappingJobAction';
  v_fa    varchar2(32);
  v_ba    number;   -- ECISAction business_action_no
  v_jp    number;   -- ECISAction 'jobid' action_parameter_no
  v_sno   number;   -- schedule_no
  v_cfg   number;   -- running ACTION_JOB_CONFIG.job_config_no

  -- reuse: one ECISAction instance (exec_order) + its jobid parameter value
  procedure upsert_instance(p_exec number, p_jobid varchar2) is
    l_ai number;
  begin
    UPDATE action_instance SET description = v_sched, isolated_tx_ind = 'N', rev_text = v_rev
     WHERE schedule_no = v_sno AND business_action_no = v_ba AND exec_order = p_exec;
    IF SQL%ROWCOUNT = 0 THEN
      INSERT INTO action_instance (business_action_no, description, exec_order, schedule_no, isolated_tx_ind, rev_text)
      VALUES (v_ba, v_sched, p_exec, v_sno, 'N', v_rev);
    END IF;
    SELECT action_instance_no INTO l_ai
      FROM action_instance WHERE schedule_no = v_sno AND business_action_no = v_ba AND exec_order = p_exec;

    UPDATE action_instance_value SET parameter_value = p_jobid, rev_text = v_rev
     WHERE action_instance_no = l_ai AND action_parameter_no = v_jp;
    IF SQL%ROWCOUNT = 0 THEN
      INSERT INTO action_instance_value (action_instance_no, action_parameter_no, parameter_value, rev_text)
      VALUES (l_ai, v_jp, p_jobid, v_rev);
    END IF;
  end;

  -- reuse: one ACTION_JOB_CONFIG row (job-action step or its parameter); param name/value may be NULL
  procedure upsert_cfg(p_job varchar2, p_no number, p_class varchar2, p_name varchar2, p_val varchar2) is
  begin
    UPDATE action_job_config
       SET job_action_class = p_class, param_value = p_val, transport_component_ind = 'N', rev_text = v_rev
     WHERE job_id = p_job AND job_action_no = p_no
       AND (param_name = p_name OR (param_name IS NULL AND p_name IS NULL));
    IF SQL%ROWCOUNT = 0 THEN
      v_cfg := v_cfg + 1;
      INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class,
             param_name, param_value, transport_component_ind, rev_text)
      VALUES (v_cfg, p_job, p_no, p_class, p_name, p_val, 'N', v_rev);
    END IF;
  end;

begin
  v_fa := EcDp_Objects.GetObjIDFromCode('FUNCTIONAL_AREA', 'ECIS');
  SELECT business_action_no INTO v_ba FROM business_action WHERE name = 'ECISAction';
  SELECT action_parameter_no INTO v_jp FROM action_parameter WHERE business_action_no = v_ba AND name = 'jobid';

  -- 1) SCHEDULE ------------------------------------------------------------------------------------
  UPDATE TV_SCHEDULE SET enabled = 'N', functional_area_id = v_fa, description = 'Claude Excel Import',
         pin_to = 'EC-Cluster:ECDS', rev_text = v_rev
   WHERE name = v_sched;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO TV_SCHEDULE (name, enabled, functional_area_id, description, pin_to, start_date, rev_text)
    VALUES (v_sched, 'N', v_fa, 'Claude Excel Import', 'EC-Cluster:ECDS', ecdp_timestamp.getcurrentsysdate, v_rev);
  END IF;
  SELECT schedule_no INTO v_sno FROM tv_schedule WHERE name = v_sched;

  -- 2) SCHEDULE DETAILS (auto-created by the TV_SCHEDULE insert trigger) ---------------------------
  UPDATE TV_SCHEDULE_DETAILS SET username = 'sysadmin', log_level = 'INFO', ignore_misfire = 'Y',
         retain_count = 10, rev_text = v_rev
   WHERE name = v_sched;

  -- 3) TWO ECISAction INSTANCES (+ jobid each) -----------------------------------------------------
  upsert_instance(10, v_job1);
  upsert_instance(20, v_job2);

  -- 4) JOB CHAINS (ACTION_JOB_CONFIG) --------------------------------------------------------------
  SELECT NVL(MAX(job_config_no), 0) INTO v_cfg FROM action_job_config;

  -- 4a) ClaudeJobID : file -> IMP_STAGING
  upsert_cfg(v_job1, 10, c_adv, 'COMPLETED_FOLDER', NULL);
  upsert_cfg(v_job1, 10, c_adv, 'CONFIG_VALIDATION', 'Y');
  upsert_cfg(v_job1, 10, c_adv, 'DROP_FOLDER',       NULL);
  upsert_cfg(v_job1, 10, c_adv, 'ERROR_FOLDER',      NULL);
  upsert_cfg(v_job1, 10, c_adv, 'FILE_DROP_SERVICE', 'DB');
  upsert_cfg(v_job1, 10, c_adv, 'FILE_FILTER',       '*');
  upsert_cfg(v_job1, 10, c_adv, 'FTP_PASSWORD',      NULL);
  upsert_cfg(v_job1, 10, c_adv, 'FTP_PORT',          NULL);
  upsert_cfg(v_job1, 10, c_adv, 'FTP_REMOVE_FILE',   'N');
  upsert_cfg(v_job1, 10, c_adv, 'FTP_SERVER_NAME',   NULL);
  upsert_cfg(v_job1, 10, c_adv, 'FTP_USER_NAME',     NULL);
  upsert_cfg(v_job1, 10, c_adv, 'INTERFACE_CODE',    v_iface);
  upsert_cfg(v_job1, 20, c_sgt, NULL,                NULL);

  -- 4b) ClaudeReadFromStaging : IMP_STAGING -> target class
  upsert_cfg(v_job2, 10, c_sgs, 'CONFIG_VALIDATION', 'Y');
  upsert_cfg(v_job2, 10, c_sgs, 'FILE_NAME',         '*');
  upsert_cfg(v_job2, 10, c_sgs, 'INTERFACE_CODE',    v_iface);
  upsert_cfg(v_job2, 20, c_tgt, NULL,                NULL);

end;
/
