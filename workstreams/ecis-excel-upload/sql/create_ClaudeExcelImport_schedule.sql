-- =====================================================================================================
-- ECIS Excel-upload SCHEDULE task: ClaudeExcelImport  (runtime counterpart of create_CLAUDE_WELL_TEST_interface.sql)
--
-- Modelled on the live AudreyExcelImport schedule: ONE schedule holding TWO ECISAction instances -
--   exec 10 -> jobid ClaudeJobID          : AdvancedExcelJobAction (file -> IMP_STAGING) + StagingJobActionTarget
--   exec 20 -> jobid ClaudeReadFromStaging : StagingJobActionSource (IMP_STAGING -> target) + TargetMappingJobAction
-- both job chains carry INTERFACE_CODE = 'CLAUDE_WELL_TEST', FILE_DROP_SERVICE = 'DB'.
--
-- Style (same as create_CLAUDE_WELL_TEST_interface.sql + the Pluto 050_Interfaces SCHEDULE files):
--   * DECLARE constants (schedule / interface / jobids / REV_TEXT) + class-name constants - no inline repeats.
--   * Flat update-insert per row: UPDATE ...; IF SQL%ROWCOUNT = 0 THEN INSERT ...; END IF;  (idempotent) - NO MERGE.
--   * REV_TEXT = 'ECPR-DEMO' on every INSERT/UPDATE for audit (sandbox demo objects; use the real ECPR for client work).
--   * One declare..begin..end; - NO procedures, NO exception block, NO COMMIT in the file (caller / Flyway commits).
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
  v_rev   constant varchar2(30)  := 'ECPR-DEMO';   -- sandbox demo objects: no client ECPR (R22)
  c_adv   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.sourcemapping.jobaction.AdvancedExcelJobAction';
  c_sgt   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.staging.jobaction.StagingJobActionTarget';
  c_sgs   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.staging.jobaction.StagingJobActionSource';
  c_tgt   constant varchar2(150) := 'com.ec.ecdm.is.advancedexcel.targetmapping.jobaction.TargetMappingJobAction';
  v_fa    varchar2(32);
  v_ba    number;   -- ECISAction business_action_no
  v_jp    number;   -- ECISAction 'jobid' action_parameter_no
  v_sno   number;   -- schedule_no
  v_ai    number;   -- current action_instance_no
  v_cfg   number;   -- running ACTION_JOB_CONFIG.job_config_no
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
    VALUES (v_sched, 'N', v_fa, 'Claude Excel Import', 'EC-Cluster:ECDS', to_date('2000-01-01','YYYY-MM-DD'), v_rev);
  END IF;
  SELECT schedule_no INTO v_sno FROM tv_schedule WHERE name = v_sched;

  -- 2) SCHEDULE DETAILS (auto-created by the TV_SCHEDULE insert trigger) ---------------------------
  UPDATE TV_SCHEDULE_DETAILS SET username = 'sysadmin', log_level = 'INFO', ignore_misfire = 'Y',
         retain_count = 10, rev_text = v_rev
   WHERE name = v_sched;

  -- 2b) JOB SCHEDULE (Schedule tab) - set Valid From + Schedule Type so the control is not left blank.
  --     (START_DATE + SCHEDULE_TYPE persist via this view; STATUS/NEXT_FIRE_TIME are derived from the
  --      QRTZ trigger which is created when the schedule is saved/armed in the app.)
  UPDATE TV_JOB_SCHEDULE SET start_date = to_date('2000-01-01','YYYY-MM-DD'),
         schedule_type = 'ONCE', schedule_when_class = 'SCHEDULE_ONCE'
   WHERE name = v_sched;

  -- 3) ECISAction INSTANCE exec 10 -> jobid ClaudeJobID --------------------------------------------
  UPDATE action_instance SET description = v_sched, isolated_tx_ind = 'N', rev_text = v_rev
   WHERE schedule_no = v_sno AND business_action_no = v_ba AND exec_order = 10;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO action_instance (business_action_no, description, exec_order, schedule_no, isolated_tx_ind, rev_text)
    VALUES (v_ba, v_sched, 10, v_sno, 'N', v_rev);
  END IF;
  SELECT action_instance_no INTO v_ai FROM action_instance WHERE schedule_no = v_sno AND business_action_no = v_ba AND exec_order = 10;
  UPDATE action_instance_value SET parameter_value = v_job1, rev_text = v_rev
   WHERE action_instance_no = v_ai AND action_parameter_no = v_jp;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO action_instance_value (action_instance_no, action_parameter_no, parameter_value, rev_text)
    VALUES (v_ai, v_jp, v_job1, v_rev);
  END IF;

  -- 4) ECISAction INSTANCE exec 20 -> jobid ClaudeReadFromStaging ----------------------------------
  UPDATE action_instance SET description = v_sched, isolated_tx_ind = 'N', rev_text = v_rev
   WHERE schedule_no = v_sno AND business_action_no = v_ba AND exec_order = 20;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO action_instance (business_action_no, description, exec_order, schedule_no, isolated_tx_ind, rev_text)
    VALUES (v_ba, v_sched, 20, v_sno, 'N', v_rev);
  END IF;
  SELECT action_instance_no INTO v_ai FROM action_instance WHERE schedule_no = v_sno AND business_action_no = v_ba AND exec_order = 20;
  UPDATE action_instance_value SET parameter_value = v_job2, rev_text = v_rev
   WHERE action_instance_no = v_ai AND action_parameter_no = v_jp;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO action_instance_value (action_instance_no, action_parameter_no, parameter_value, rev_text)
    VALUES (v_ai, v_jp, v_job2, v_rev);
  END IF;

  -- 5) JOB CHAIN for ClaudeJobID : file -> IMP_STAGING ---------------------------------------------
  SELECT NVL(MAX(job_config_no), 0) INTO v_cfg FROM action_job_config;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'COMPLETED_FOLDER';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'COMPLETED_FOLDER', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = 'Y', transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'CONFIG_VALIDATION';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'CONFIG_VALIDATION', 'Y', 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'DROP_FOLDER';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'DROP_FOLDER', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'ERROR_FOLDER';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'ERROR_FOLDER', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = 'DB', transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FILE_DROP_SERVICE';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FILE_DROP_SERVICE', 'DB', 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = '*', transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FILE_FILTER';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FILE_FILTER', '*', 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FTP_PASSWORD';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FTP_PASSWORD', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FTP_PORT';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FTP_PORT', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = 'N', transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FTP_REMOVE_FILE';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FTP_REMOVE_FILE', 'N', 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FTP_SERVER_NAME';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FTP_SERVER_NAME', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'FTP_USER_NAME';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'FTP_USER_NAME', NULL, 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_adv, param_value = v_iface, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 10 AND param_name = 'INTERFACE_CODE';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 10, c_adv, 'INTERFACE_CODE', v_iface, 'N', v_rev);
  END IF;

  -- ClaudeJobID action 20: StagingJobActionTarget (no parameters)
  UPDATE action_job_config SET job_action_class = c_sgt, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job1 AND job_action_no = 20 AND param_name IS NULL;
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job1, 20, c_sgt, NULL, NULL, 'N', v_rev);
  END IF;

  -- 6) JOB CHAIN for ClaudeReadFromStaging : IMP_STAGING -> target class ---------------------------
  UPDATE action_job_config SET job_action_class = c_sgs, param_value = 'Y', transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job2 AND job_action_no = 10 AND param_name = 'CONFIG_VALIDATION';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job2, 10, c_sgs, 'CONFIG_VALIDATION', 'Y', 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_sgs, param_value = '*', transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job2 AND job_action_no = 10 AND param_name = 'FILE_NAME';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job2, 10, c_sgs, 'FILE_NAME', '*', 'N', v_rev);
  END IF;

  UPDATE action_job_config SET job_action_class = c_sgs, param_value = v_iface, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job2 AND job_action_no = 10 AND param_name = 'INTERFACE_CODE';
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job2, 10, c_sgs, 'INTERFACE_CODE', v_iface, 'N', v_rev);
  END IF;

  -- ClaudeReadFromStaging action 20: TargetMappingJobAction (no parameters)
  UPDATE action_job_config SET job_action_class = c_tgt, param_value = NULL, transport_component_ind = 'N', rev_text = v_rev
   WHERE job_id = v_job2 AND job_action_no = 20 AND param_name IS NULL;
  IF SQL%ROWCOUNT = 0 THEN
    v_cfg := v_cfg + 1;
    INSERT INTO action_job_config (job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, rev_text)
    VALUES (v_cfg, v_job2, 20, c_tgt, NULL, NULL, 'N', v_rev);
  END IF;

end;
/
