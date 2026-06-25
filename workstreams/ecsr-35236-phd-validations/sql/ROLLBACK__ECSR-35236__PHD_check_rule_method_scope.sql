--ECSR-35236  (Issue_1052) ROLLBACK - restore the 8 PHD check rules to pre-fix state
-- Resets each WHERE_FORMULA to the original value-only check, and removes ONLY the variables this change
-- added (guarded by REV_TEXT = 'ECSR-35236'). Idempotent + re-runnable.
-- Verified on COPSDEV/plutodev (8/8 restored). Flyway wraps the txn (no COMMIT/EXCEPTION here).
DECLARE
  lv_rev_text VARCHAR2(20) := 'ECSR-35236-ROLLBACK';
BEGIN

  UPDATE tv_ctrl_check_rules SET where_formula = '(${GrsMass} IS NULL OR ${GrsMass} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_TANK_DIP_GRS_MASS_VAL1';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${StdDensity} IS NULL OR ${StdDensity} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_TANK_DIP_STD_DENSITY_VAL1';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${Density} IS NULL OR ${Density} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_STRM_ANALYSIS_DENSITY_VAL1';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${Gcv} IS NULL OR ${Gcv} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_STRM_ANALYSIS_GCV_VAL1';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_PWEL_STATUS_NODATA_BHTEMP';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_PWEL_STATUS_NODATA_WHTEMP';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_PWEL_STATUS_NODATA_BHPRESS';
  UPDATE tv_ctrl_check_rules SET where_formula = '(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0)',
         rev_text = lv_rev_text WHERE check_name = 'PHD_PWEL_STATUS_NODATA_WHPRESS';

  -- remove ONLY the variables this change added (guarded by REV_TEXT = 'ECSR-35236')
  DELETE FROM tv_ctrl_check_rule_variable
   WHERE rev_text = 'ECSR-35236'
     AND variable_name IN ('GrsMassMethod','StdDensMethod','DensityMethod','GcvMethod',
                           'ConstMEASURED','ConstCOMP','OnStrmHrs')
     AND check_id IN (SELECT check_id FROM ctrl_check_rules WHERE check_name IN (
          'PHD_TANK_DIP_GRS_MASS_VAL1','PHD_TANK_DIP_STD_DENSITY_VAL1',
          'PHD_STRM_ANALYSIS_DENSITY_VAL1','PHD_STRM_ANALYSIS_GCV_VAL1',
          'PHD_PWEL_STATUS_NODATA_BHTEMP','PHD_PWEL_STATUS_NODATA_WHTEMP',
          'PHD_PWEL_STATUS_NODATA_BHPRESS','PHD_PWEL_STATUS_NODATA_WHPRESS'));

END;
/
