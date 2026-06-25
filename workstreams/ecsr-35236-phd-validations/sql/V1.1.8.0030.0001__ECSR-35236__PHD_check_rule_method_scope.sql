-- =============================================================================
-- ECSR-35236 (Issue_1052): scope 8 PHD check rules by method / on-stream-hours
-- Author : Choong-Yin Lee  |  Date: 2026-06-25
-- Purpose: add Melanie Murray's criteria to each rule's WHERE_FORMULA so they only
--          fire when the value should be present (method = MEASURED / COMP_ANALYSIS)
--          or the well is on stream (ON_STREAM_HRS > 0) - stops the false-positive
--          PHD validations on the tags added since 1 Dec 2025.
-- Pattern: mirrors live rule PHD_STREAM_LIQUID_MEAS_VAL2 - a method ATTRIBUTE var +
--          a CONST_STRING var, combined as ${Method} = ${Const}.
-- Target by CHECK_NAME (CHECK_ID is env-local). Idempotent + re-runnable. No DELETE.
-- Verified on COPSDEV/plutodev (apply 8/8, re-run idempotent, rollback 8/8 restored).
-- =============================================================================
DECLARE
    c_rev_text CONSTANT VARCHAR2(50) := 'ECSR-35236';

    -- upsert a check-rule variable (audit cols default via the TV layer)
    PROCEDURE set_var (p_name VARCHAR2, p_var VARCHAR2, p_type VARCHAR2, p_value VARCHAR2) IS
        v_id NUMBER;
    BEGIN
        SELECT check_id INTO v_id FROM ctrl_check_rules WHERE check_name = p_name;
        UPDATE tv_ctrl_check_rule_variable
           SET variable_type = p_type, variable_value = p_value, rev_text = c_rev_text
         WHERE check_id = v_id AND variable_name = p_var;
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO tv_ctrl_check_rule_variable
                (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
            VALUES ('CTRL_CHECK_RULE_VARIABLE', v_id, p_var, p_type, p_value, c_rev_text);
        END IF;
    END;

    -- set the rule's full WHERE_FORMULA (idempotent: re-run sets the same value)
    PROCEDURE scope_rule (p_name VARCHAR2, p_formula VARCHAR2) IS
    BEGIN
        UPDATE tv_ctrl_check_rules
           SET where_formula = p_formula, rev_text = c_rev_text
         WHERE check_name = p_name;
    END;
BEGIN
    -- 1) Tank gross mass : only when GRS_MASS_METHOD = MEASURED
    set_var('PHD_TANK_DIP_GRS_MASS_VAL1', 'GrsMassMethod', 'ATTRIBUTE',    'GRS_MASS_METHOD');
    set_var('PHD_TANK_DIP_GRS_MASS_VAL1', 'ConstMEASURED', 'CONST_STRING', 'MEASURED');
    scope_rule('PHD_TANK_DIP_GRS_MASS_VAL1',
        '(${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED}');

    -- 2) Tank standard density : only when STD_DENS_METHOD = MEASURED
    set_var('PHD_TANK_DIP_STD_DENSITY_VAL1', 'StdDensMethod', 'ATTRIBUTE',    'STD_DENS_METHOD');
    set_var('PHD_TANK_DIP_STD_DENSITY_VAL1', 'ConstMEASURED', 'CONST_STRING', 'MEASURED');
    scope_rule('PHD_TANK_DIP_STD_DENSITY_VAL1',
        '(${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensMethod} = ${ConstMEASURED}');

    -- 3) Stream density : only when STD_DENSITY_METHOD = COMP_ANALYSIS
    set_var('PHD_STRM_ANALYSIS_DENSITY_VAL1', 'DensityMethod', 'ATTRIBUTE',    'STD_DENSITY_METHOD');
    set_var('PHD_STRM_ANALYSIS_DENSITY_VAL1', 'ConstCOMP',     'CONST_STRING', 'COMP_ANALYSIS');
    scope_rule('PHD_STRM_ANALYSIS_DENSITY_VAL1',
        '(${Density} IS NULL OR ${Density} < 0) and ${DensityMethod} = ${ConstCOMP}');

    -- 4) Stream GCV : only when GCV_METHOD = COMP_ANALYSIS
    set_var('PHD_STRM_ANALYSIS_GCV_VAL1', 'GcvMethod', 'ATTRIBUTE',    'GCV_METHOD');
    set_var('PHD_STRM_ANALYSIS_GCV_VAL1', 'ConstCOMP', 'CONST_STRING', 'COMP_ANALYSIS');
    scope_rule('PHD_STRM_ANALYSIS_GCV_VAL1',
        '(${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP}');

    -- 5) PWEL bottom-hole temperature : only when ON_STREAM_HRS > 0
    set_var('PHD_PWEL_STATUS_NODATA_BHTEMP', 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS');
    scope_rule('PHD_PWEL_STATUS_NODATA_BHTEMP',
        '(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0) and ${OnStrmHrs} > 0');

    -- 6) PWEL well-head temperature
    set_var('PHD_PWEL_STATUS_NODATA_WHTEMP', 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS');
    scope_rule('PHD_PWEL_STATUS_NODATA_WHTEMP',
        '(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0) and ${OnStrmHrs} > 0');

    -- 7) PWEL bottom-hole pressure
    set_var('PHD_PWEL_STATUS_NODATA_BHPRESS', 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS');
    scope_rule('PHD_PWEL_STATUS_NODATA_BHPRESS',
        '(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0) and ${OnStrmHrs} > 0');

    -- 8) PWEL well-head pressure
    set_var('PHD_PWEL_STATUS_NODATA_WHPRESS', 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS');
    scope_rule('PHD_PWEL_STATUS_NODATA_WHPRESS',
        '(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0) and ${OnStrmHrs} > 0');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- VERIFY: expect all 8 WHERE_FORMULA to carry the method / on-stream criterion.
SELECT CHECK_NAME, WHERE_FORMULA
  FROM TV_CTRL_CHECK_RULES
 WHERE CHECK_NAME IN (
    'PHD_TANK_DIP_GRS_MASS_VAL1','PHD_TANK_DIP_STD_DENSITY_VAL1',
    'PHD_STRM_ANALYSIS_DENSITY_VAL1','PHD_STRM_ANALYSIS_GCV_VAL1',
    'PHD_PWEL_STATUS_NODATA_BHTEMP','PHD_PWEL_STATUS_NODATA_WHTEMP',
    'PHD_PWEL_STATUS_NODATA_BHPRESS','PHD_PWEL_STATUS_NODATA_WHPRESS')
 ORDER BY CHECK_NAME;
