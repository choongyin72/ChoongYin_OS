-- =============================================================================
-- ECSR-35236 (Issue_1052): ROLLBACK - restore the 8 PHD check rules to pre-fix state
-- Author : Choong-Yin Lee  |  Date: 2026-06-25
-- Purpose: reset each WHERE_FORMULA to the original value-only check, and remove ONLY
--          the variables this change added (guarded by REV_TEXT = 'ECSR-35236').
-- Safe   : idempotent + re-runnable. Verified on COPSDEV/plutodev (8/8 restored).
-- =============================================================================
DECLARE
    PROCEDURE restore (p_name VARCHAR2, p_formula VARCHAR2) IS
    BEGIN
        UPDATE tv_ctrl_check_rules
           SET where_formula = p_formula, rev_text = 'ECSR-35236-ROLLBACK'
         WHERE check_name = p_name;
    END restore;
BEGIN
    restore('PHD_TANK_DIP_GRS_MASS_VAL1',     '(${GrsMass} IS NULL OR ${GrsMass} < 0)');
    restore('PHD_TANK_DIP_STD_DENSITY_VAL1',  '(${StdDensity} IS NULL OR ${StdDensity} < 0)');
    restore('PHD_STRM_ANALYSIS_DENSITY_VAL1', '(${Density} IS NULL OR ${Density} < 0)');
    restore('PHD_STRM_ANALYSIS_GCV_VAL1',     '(${Gcv} IS NULL OR ${Gcv} < 0)');
    restore('PHD_PWEL_STATUS_NODATA_BHTEMP',  '(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0)');
    restore('PHD_PWEL_STATUS_NODATA_WHTEMP',  '(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0)');
    restore('PHD_PWEL_STATUS_NODATA_BHPRESS', '(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0)');
    restore('PHD_PWEL_STATUS_NODATA_WHPRESS', '(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0)');

    -- remove ONLY the variables this change added (guarded by REV_TEXT)
    DELETE FROM tv_ctrl_check_rule_variable
     WHERE rev_text = 'ECSR-35236'
       AND variable_name IN ('GrsMassMethod','StdDensMethod','DensityMethod','GcvMethod',
                             'ConstMEASURED','ConstCOMP','OnStrmHrs')
       AND check_id IN (SELECT check_id FROM ctrl_check_rules WHERE check_name IN (
            'PHD_TANK_DIP_GRS_MASS_VAL1','PHD_TANK_DIP_STD_DENSITY_VAL1',
            'PHD_STRM_ANALYSIS_DENSITY_VAL1','PHD_STRM_ANALYSIS_GCV_VAL1',
            'PHD_PWEL_STATUS_NODATA_BHTEMP','PHD_PWEL_STATUS_NODATA_WHTEMP',
            'PHD_PWEL_STATUS_NODATA_BHPRESS','PHD_PWEL_STATUS_NODATA_WHPRESS'));

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: expect all 8 WHERE_FORMULA back to the original value-only check
--         (none contains 'Method' or 'OnStrmHrs'); added variables removed.
-- =============================================================================
SELECT CHECK_NAME, WHERE_FORMULA
  FROM TV_CTRL_CHECK_RULES
 WHERE CHECK_NAME IN (
    'PHD_TANK_DIP_GRS_MASS_VAL1','PHD_TANK_DIP_STD_DENSITY_VAL1',
    'PHD_STRM_ANALYSIS_DENSITY_VAL1','PHD_STRM_ANALYSIS_GCV_VAL1',
    'PHD_PWEL_STATUS_NODATA_BHTEMP','PHD_PWEL_STATUS_NODATA_WHTEMP',
    'PHD_PWEL_STATUS_NODATA_BHPRESS','PHD_PWEL_STATUS_NODATA_WHPRESS')
 ORDER BY CHECK_NAME;
