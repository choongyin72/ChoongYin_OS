-- ============================================================================
-- ROLLBACK for ECSR-35236 — restores the 8 PHD check rules to pre-fix state:
--   * strips the appended " and ${...} ..." criterion from WHERE_FORMULA
--   * removes ONLY the variables this change added (guarded by REV_TEXT='ECSR-35236')
-- Idempotent + re-runnable. Verified on COPSDEV/plutodev (8/8 restored).
-- ============================================================================
DECLARE
  PROCEDURE unscope(p_name VARCHAR2, p_tail VARCHAR2) IS
    v_cid NUMBER; v_wf VARCHAR2(4000);
  BEGIN
    SELECT check_id, where_formula INTO v_cid, v_wf
      FROM tv_ctrl_check_rules WHERE check_name = p_name;
    IF INSTR(v_wf, TRIM(p_tail)) > 0 THEN
      UPDATE tv_ctrl_check_rules
         SET where_formula = REPLACE(v_wf, p_tail, ''),
             last_updated_by = 'ECKERNEL_EC', last_updated_date = SYSDATE,
             rev_text = 'ECSR-35236-ROLLBACK'
       WHERE check_id = v_cid;
    END IF;
    DELETE FROM tv_ctrl_check_rule_variable
     WHERE check_id = v_cid AND rev_text = 'ECSR-35236'
       AND variable_name IN ('GrsMassMethod','StdDensMethod','DensityMethod',
                              'GcvMethod','ConstMEASURED','ConstCOMP','OnStrmHrs');
  END;
BEGIN
  unscope('PHD_TANK_DIP_GRS_MASS_VAL1',     ' and ${GrsMassMethod} = ${ConstMEASURED}');
  unscope('PHD_TANK_DIP_STD_DENSITY_VAL1',  ' and ${StdDensMethod} = ${ConstMEASURED}');
  unscope('PHD_STRM_ANALYSIS_DENSITY_VAL1', ' and ${DensityMethod} = ${ConstCOMP}');
  unscope('PHD_STRM_ANALYSIS_GCV_VAL1',     ' and ${GcvMethod} = ${ConstCOMP}');
  FOR r IN (SELECT column_value AS nm FROM TABLE(sys.odcivarchar2list(
              'PHD_PWEL_STATUS_NODATA_BHTEMP','PHD_PWEL_STATUS_NODATA_WHTEMP',
              'PHD_PWEL_STATUS_NODATA_BHPRESS','PHD_PWEL_STATUS_NODATA_WHPRESS'))) LOOP
    unscope(r.nm, ' and ${OnStrmHrs} > 0');
  END LOOP;
  COMMIT;
END;
/
