-- =============================================================================
-- Issue_1052: FROZEN-VALUE Check Rules for PHD Tags  (DRAFT — DO NOT DEPLOY)
-- Author : Choong-Yin Lee  |  Date: 2026-06-09
-- Template: live rule 1042 (ZWP_P_TOOLTIP.getValFrozenValue, WARNING). Wiring, not new PL/SQL.
-- Scope  : 6 rules, stream + well objects only. Tanks excluded (function handles stream/well only).
-- Open   : STRM_COMP grain; ZWT_OILINWAT needs FROM_UNIT=mg/L; AVG_GAS_RATE UOM assumed SM3.
-- ScreenVal: ZWP_SCREEN_VAL (Woodside project attr) gates on-screen tooltip display. 'N' for all
--          stream rules (batch only, matches stream-family convention); 'Y' for PWEL (matches the
--          8 live PWEL frozen rules). Comp/analysis kept 'N' until grain confirmed by Grant.
-- Linking: group<->rule linkage lives in Issue1052_PHD_Frozen_Check_Group.sql (run it after this).
-- =============================================================================

DECLARE
    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052-FROZEN';

    PROCEDURE frozen_rule (p_name       IN VARCHAR2,
                           p_table_id   IN VARCHAR2,
                           p_value_col  IN VARCHAR2,
                           p_message    IN VARCHAR2,
                           p_screen_val IN VARCHAR2 DEFAULT 'N') IS
        v_id NUMBER;

        PROCEDURE set_param (p_param VARCHAR2, p_dtype VARCHAR2, p_pos NUMBER,
                             p_ptype VARCHAR2, p_pvalue VARCHAR2) IS
        BEGIN
            DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P
             WHERE CHECK_ID = v_id AND VARIABLE_NAME = 'FunctionFrozenValue'
               AND PARAMETER_NAME = p_param;
            INSERT INTO TV_CTRL_CHECK_RULE_FUNC_P
                (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, PARAMETER_NAME, DATA_TYPE,
                 POSITION, PARAMETER_TYPE, PARAMETER_VALUE, REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULE_FUNC_P', v_id, 'FunctionFrozenValue', p_param, p_dtype,
                 p_pos, p_ptype, p_pvalue, c_rev_text);
        END;

        PROCEDURE set_var (p_var VARCHAR2, p_type VARCHAR2, p_value VARCHAR2,
                           p_func_name VARCHAR2 DEFAULT NULL) IS
        BEGIN
            UPDATE TV_CTRL_CHECK_RULE_VARIABLE
               SET VARIABLE_TYPE = p_type, VARIABLE_VALUE = p_value,
                   FUNCTION_NAME = p_func_name, REV_TEXT = c_rev_text
             WHERE CHECK_ID = v_id AND VARIABLE_NAME = p_var;
            IF SQL%ROWCOUNT = 0 THEN
                INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
                    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE,
                     FUNCTION_NAME, REV_TEXT)
                VALUES
                    ('CTRL_CHECK_RULE_VARIABLE', v_id, p_var, p_type, p_value,
                     p_func_name, c_rev_text);
            END IF;
        END;
    BEGIN
        UPDATE TV_CTRL_CHECK_RULES
           SET TABLE_ID = p_table_id, CLASS_OBJ_VALIDATION_IND = 'N',
               WHERE_FORMULA = '(${FunctionFrozenValue}  = ${ConstBOOLEAN})',
               CHECK_MESSAGE = p_message, SEVERITY_LEVEL = 'WARNING',
               ZWP_SCREEN_VAL = p_screen_val, REV_TEXT = c_rev_text
         WHERE CHECK_NAME = p_name;
        IF SQL%ROWCOUNT > 0 THEN
            SELECT CHECK_ID INTO v_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_name;
        ELSE
            SELECT NVL(MAX(CHECK_ID),0)+1 INTO v_id FROM CTRL_CHECK_RULES;
            INSERT INTO TV_CTRL_CHECK_RULES
                (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
                 CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL,
                 ZWP_SCREEN_VAL, REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULES', v_id, p_name, 'Count(*)', p_table_id, 'N',
                 '(${FunctionFrozenValue}  = ${ConstBOOLEAN})', p_message, 'WARNING',
                 p_screen_val, c_rev_text);
        END IF;

        set_var('FunctionFrozenValue', 'FUNCTION',     'ZWP_P_TOOLTIP', 'getValFrozenValue');
        set_var('ConstBOOLEAN',        'CONST_STRING', 'FROZEN');

        set_param('P_CLASS_NAME', 'VARCHAR2', 1, 'ATTRIBUTE',    'DATA_CLASS_NAME');
        set_param('P_OBJECT_ID',  'VARCHAR2', 2, 'ATTRIBUTE',    'OBJECT_ID');
        set_param('P_DAYTIME',    'DATE',     3, 'ATTRIBUTE',    'DAYTIME');
        set_param('P_VALUE',      'NUMBER',   4, 'ATTRIBUTE',    p_value_col);
        set_param('P_ATTRIBUTE',  'VARCHAR2', 5, 'CONST_STRING', p_value_col);
    END frozen_rule;

BEGIN
    -- stream-family rules: ZWP_SCREEN_VAL='N' (batch only)
    frozen_rule('PHD_STRM_COMP_MOL_PCT_FROZEN_V1', 'RV_STRM_COMP_ANALYSIS', 'MOL_PCT',
        'Stream :STREAM_NAME component :COMPONENT_NO has Mol% same as previous day', 'N');
    frozen_rule('PHD_STRM_COMP_WT_PCT_FROZEN_V1', 'RV_STRM_COMP_ANALYSIS', 'WT_PCT',
        'Stream :STREAM_NAME component :COMPONENT_NO has Wt% same as previous day', 'N');
    frozen_rule('PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1', 'RV_STRM_ANALYSIS', 'DENSITY',
        'Stream :STREAM_NAME has Density same as previous day', 'N');
    frozen_rule('PHD_STRM_ANALYSIS_GCV_FROZEN_V1', 'RV_STRM_ANALYSIS', 'GCV_MJPERSM3',
        'Stream :STREAM_NAME has GCV same as previous day', 'N');
    frozen_rule('PHD_STREAM_WATER_OILINWAT_FROZEN_V1', 'RV_STRM_DAY_STREAM_MEAS_WAT',
        'ZWT_OILINWAT_MGPERLITER',
        'Stream :STREAM_NAME has Oil-in-Water same as previous day', 'N');
    -- PWEL rule: ZWP_SCREEN_VAL='Y' (matches the 8 live PWEL frozen rules - on-screen tooltip)
    frozen_rule('PHD_PWEL_AVG_GAS_RATE_FROZEN_V1', 'RV_PWEL_DAY_STATUS', 'AVG_GAS_RATE_SM3',
        'Well :WELL_NAME has Avg Gas Rate same as previous day', 'Y');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- VERIFY: expect 6 rows, all WARNING; ZWP_SCREEN_VAL = N x5 (stream), Y x1 (PWEL).
SELECT r.CHECK_ID, r.CHECK_NAME, r.TABLE_ID, r.SEVERITY_LEVEL, r.ZWP_SCREEN_VAL
  FROM TV_CTRL_CHECK_RULES r
 WHERE r.CHECK_NAME IN (
    'PHD_STRM_COMP_MOL_PCT_FROZEN_V1',
    'PHD_STRM_COMP_WT_PCT_FROZEN_V1',
    'PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1',
    'PHD_STRM_ANALYSIS_GCV_FROZEN_V1',
    'PHD_STREAM_WATER_OILINWAT_FROZEN_V1',
    'PHD_PWEL_AVG_GAS_RATE_FROZEN_V1'
 )
 ORDER BY r.CHECK_NAME;
