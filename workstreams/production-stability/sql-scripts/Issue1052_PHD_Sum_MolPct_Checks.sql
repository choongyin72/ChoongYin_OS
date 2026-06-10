-- =============================================================================
-- Issue_1052: SUM 98-102% Composition Check Rules for MOLE % (COMP_MOL_PCT)
-- Author : Choong-Yin Lee  |  Date: 2026-06-10
-- Template: live rules 1077 (stream) / 1083 (well) — ZWP_P_VALIDATION.isComponentSumOutOfTolerance.
--           Faithful clone (full-row diff); the ONLY functional change is the tested column:
--           P_COLUMN_NAME  COMP_WT_PCT  ->  COMP_MOL_PCT.
-- Purpose : enforce that the sum of mole-% across a gas analysis's components is within the
--           98%-102% tolerance band (ZWP_STRM_SUM_COMP_LOWER/_UPPER; NVL defaults 0.98/1.02).
--           Mirrors the existing weight-% check, which only covers COMP_WT_PCT.
-- Mirror parent: SEVERITY_LEVEL=ERROR, ZWP_SCREEN_VAL='N' (batch only), SELECT_CLAUSE='Count(*)'.
-- IDs    : auto-assigned NVL(MAX(CHECK_ID),0)+1 per DB instance (re-runnable; matched by CHECK_NAME).
-- Linking: group<->rule linkage lives in Issue1052_PHD_Sum_MolPct_Check_Group.sql (run after this).
--          Stream -> V_DLY_SAMPLING_STRM_GAS_COMP ; Well -> V_DLY_SAMPLING_WELL_GAS_COMP
--          (the same groups as parents 1077/1083).
-- Pattern: UPDATE then INSERT (re-runnable). Func-param TABLE_CLASS_NAME = 'CTRL_CHECK_RULE_FUNC_P'.
-- =============================================================================

DECLARE
    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052-SUM-MOL';

    PROCEDURE sum_rule (p_name     IN VARCHAR2,
                        p_table_id IN VARCHAR2,
                        p_class    IN VARCHAR2,
                        p_message  IN VARCHAR2) IS
        v_id NUMBER;

        PROCEDURE set_param (p_param VARCHAR2, p_dtype VARCHAR2, p_pos NUMBER,
                             p_ptype VARCHAR2, p_pvalue VARCHAR2) IS
        BEGIN
            DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P
             WHERE CHECK_ID = v_id AND VARIABLE_NAME = 'isComponentSumOutOfTolerance'
               AND PARAMETER_NAME = p_param;
            INSERT INTO TV_CTRL_CHECK_RULE_FUNC_P
                (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, PARAMETER_NAME, DATA_TYPE,
                 POSITION, PARAMETER_TYPE, PARAMETER_VALUE, REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULE_FUNC_P', v_id, 'isComponentSumOutOfTolerance', p_param, p_dtype,
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
               WHERE_FORMULA = '(${isComponentSumOutOfTolerance} = ${ConstYES})',
               CHECK_MESSAGE = p_message, SEVERITY_LEVEL = 'ERROR',
               ZWP_SCREEN_VAL = 'N', REV_TEXT = c_rev_text
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
                 '(${isComponentSumOutOfTolerance} = ${ConstYES})', p_message, 'ERROR',
                 'N', c_rev_text);
        END IF;

        -- variables (same wiring as 1077/1083)
        set_var('ConstYES',                     'CONST_STRING', 'YES');
        set_var('isComponentSumOutOfTolerance', 'FUNCTION',     'ZWP_P_VALIDATION',
                'ISCOMPONENTSUMOUTOFTOLERANCE');

        -- function parameters (positions 1-4; ONLY P_COLUMN_NAME differs from parent: MOL not WT)
        set_param('P_CLASS_NAME',  'VARCHAR2', 1, 'CONST_STRING', p_class);
        set_param('P_ANALYSIS_NO', 'NUMBER',   2, 'ATTRIBUTE',    'ANALYSIS_NO');
        set_param('P_COLUMN_NAME', 'VARCHAR2', 3, 'CONST_STRING', 'COMP_MOL_PCT');
        set_param('P_DAYTIME',     'DATE',     4, 'ATTRIBUTE',    'DAYTIME');
    END sum_rule;

BEGIN
    -- STREAM (clone of 1077): RV_STRM_GAS_ANALYSIS / TV_STRM_GAS_COMPONENT
    sum_rule('DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1',
             'RV_STRM_GAS_ANALYSIS', 'TV_STRM_GAS_COMPONENT',
             'Stream :STREAM_NAME with sum of mole percentage is outside the defined ranges');

    -- WELL (clone of 1083): RV_WELL_GAS_ANALYSIS / TV_WELL_GAS_COMPONENT
    sum_rule('DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1',
             'RV_WELL_GAS_ANALYSIS', 'TV_WELL_GAS_COMPONENT',
             'Well :WELL_NAME with sum of mole percentage is outside the defined ranges');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: expect 2 rows, SEVERITY_LEVEL=ERROR, ZWP_SCREEN_VAL=N, and the func-param
--         P_COLUMN_NAME = COMP_MOL_PCT for each new rule.
-- =============================================================================
SELECT r.CHECK_ID, r.CHECK_NAME, r.TABLE_ID, r.SEVERITY_LEVEL, r.ZWP_SCREEN_VAL,
       p.PARAMETER_VALUE AS P_COLUMN_NAME
  FROM TV_CTRL_CHECK_RULES r
  LEFT JOIN CTRL_CHECK_RULE_FUNC_PARAM p
         ON p.CHECK_ID = r.CHECK_ID
        AND p.VARIABLE_NAME = 'isComponentSumOutOfTolerance'
        AND p.PARAMETER_NAME = 'P_COLUMN_NAME'
 WHERE r.CHECK_NAME IN (
    'DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1',
    'DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1'
 )
 ORDER BY r.CHECK_NAME;
-- Expected: 2 rows, both P_COLUMN_NAME = COMP_MOL_PCT
