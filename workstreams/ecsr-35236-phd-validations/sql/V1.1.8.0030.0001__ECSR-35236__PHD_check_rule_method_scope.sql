-- ============================================================================
-- ECSR-35236  Issue_1052 — scope PHD check rules by method / on-stream-hours
-- Adds Melanie Murray's criteria to 8 PHD check rules' WHERE_FORMULA so they
-- only fire when the value is one that *should* be present (method = MEASURED /
-- COMP_ANALYSIS) or the well is on stream (ON_STREAM_HRS > 0) — stops the
-- false-positive PHD validations on the tags added since 1 Dec 2025.
--
-- Pattern mirrors existing rule PHD_STREAM_LIQUID_MEAS_VAL2 (1052): a method
-- ATTRIBUTE variable + a CONST_STRING variable, combined as ${Method} = ${Const}.
-- Targets by CHECK_NAME (CHECK_ID is env-local, NOT portable across COPSDEV/ECAASTEST).
-- Idempotent + re-runnable. REV_TEXT = ECSR-35236 on every write. No DELETE.
-- Verified: full apply+rollback write-test on COPSDEV/plutodev (8/8 clean).
-- ============================================================================
DECLARE
  PROCEDURE add_var(p_name VARCHAR2, p_vn VARCHAR2, p_vt VARCHAR2, p_vv VARCHAR2) IS
    v_cid NUMBER; n NUMBER;
  BEGIN
    SELECT check_id INTO v_cid FROM tv_ctrl_check_rules WHERE check_name = p_name;
    SELECT COUNT(*) INTO n FROM tv_ctrl_check_rule_variable
      WHERE check_id = v_cid AND variable_name = p_vn;
    IF n = 0 THEN
      INSERT INTO tv_ctrl_check_rule_variable
        (table_class_name, check_id, variable_name, variable_type, variable_value,
         record_status, created_by, created_date, last_updated_by, last_updated_date,
         rev_no, rev_text, rec_id)
      VALUES ('CTRL_CHECK_RULE_VARIABLE', v_cid, p_vn, p_vt, p_vv,
         'P', 'ECKERNEL_EC', SYSDATE, 'ECKERNEL_EC', SYSDATE,
         1, 'ECSR-35236', RAWTOHEX(SYS_GUID()));
    END IF;
  END;

  PROCEDURE scope_rule(p_name VARCHAR2, p_tail VARCHAR2) IS
    v_cid NUMBER; v_wf VARCHAR2(4000);
  BEGIN
    SELECT check_id, where_formula INTO v_cid, v_wf
      FROM tv_ctrl_check_rules WHERE check_name = p_name;
    IF INSTR(v_wf, TRIM(p_tail)) = 0 THEN     -- only append once (re-runnable)
      UPDATE tv_ctrl_check_rules
         SET where_formula = v_wf || p_tail,
             last_updated_by = 'ECKERNEL_EC', last_updated_date = SYSDATE,
             rev_text = 'ECSR-35236'
       WHERE check_id = v_cid;
    END IF;
  END;
BEGIN
  -- 1) Tank gross mass — only validate when GRS_MASS_METHOD = MEASURED
  add_var('PHD_TANK_DIP_GRS_MASS_VAL1', 'GrsMassMethod', 'ATTRIBUTE', 'GRS_MASS_METHOD');
  add_var('PHD_TANK_DIP_GRS_MASS_VAL1', 'ConstMEASURED', 'CONST_STRING', 'MEASURED');
  scope_rule('PHD_TANK_DIP_GRS_MASS_VAL1', ' and ${GrsMassMethod} = ${ConstMEASURED}');

  -- 2) Tank standard density — only when STD_DENS_METHOD = MEASURED
  add_var('PHD_TANK_DIP_STD_DENSITY_VAL1', 'StdDensMethod', 'ATTRIBUTE', 'STD_DENS_METHOD');
  add_var('PHD_TANK_DIP_STD_DENSITY_VAL1', 'ConstMEASURED', 'CONST_STRING', 'MEASURED');
  scope_rule('PHD_TANK_DIP_STD_DENSITY_VAL1', ' and ${StdDensMethod} = ${ConstMEASURED}');

  -- 3) Stream density — only when STD_DENSITY_METHOD = COMP_ANALYSIS
  add_var('PHD_STRM_ANALYSIS_DENSITY_VAL1', 'DensityMethod', 'ATTRIBUTE', 'STD_DENSITY_METHOD');
  add_var('PHD_STRM_ANALYSIS_DENSITY_VAL1', 'ConstCOMP', 'CONST_STRING', 'COMP_ANALYSIS');
  scope_rule('PHD_STRM_ANALYSIS_DENSITY_VAL1', ' and ${DensityMethod} = ${ConstCOMP}');

  -- 4) Stream GCV — only when GCV_METHOD = COMP_ANALYSIS
  add_var('PHD_STRM_ANALYSIS_GCV_VAL1', 'GcvMethod', 'ATTRIBUTE', 'GCV_METHOD');
  add_var('PHD_STRM_ANALYSIS_GCV_VAL1', 'ConstCOMP', 'CONST_STRING', 'COMP_ANALYSIS');
  scope_rule('PHD_STRM_ANALYSIS_GCV_VAL1', ' and ${GcvMethod} = ${ConstCOMP}');

  -- 5-8) PWEL no-data BH/WH temp/press — only validate when ON_STREAM_HRS > 0
  FOR r IN (SELECT column_value AS nm FROM TABLE(sys.odcivarchar2list(
              'PHD_PWEL_STATUS_NODATA_BHTEMP','PHD_PWEL_STATUS_NODATA_WHTEMP',
              'PHD_PWEL_STATUS_NODATA_BHPRESS','PHD_PWEL_STATUS_NODATA_WHPRESS'))) LOOP
    add_var(r.nm, 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS');
    scope_rule(r.nm, ' and ${OnStrmHrs} > 0');
  END LOOP;

  COMMIT;
END;
/
