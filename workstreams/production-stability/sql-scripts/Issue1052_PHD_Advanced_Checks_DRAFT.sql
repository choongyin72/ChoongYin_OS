-- =============================================================================
-- Issue_1052: ADVANCED CHECKS (DRAFT — FOR REVIEW, NOT YET DEPLOYED)
-- Author : Choong-Yin Lee  |  Date: 2026-06-09
-- STATUS : *** DRAFT — DO NOT RUN ON COPS DEV until reviewed + Grant confirms scope ***
--          Not deployed, not committed. For review after 9am 2026-06-10.
--
-- WHAT THIS COVERS (the two deferred advanced checks from Issue1052_PHD_Check_Rules.sql):
--   1. Sum 98-102% composition check (MOL_PCT / WT_PCT totals)
--   2. Frozen-value check
--
-- KEY FACT (verified on COPS DEV): the logic ALREADY EXISTS as DB functions — this is
-- check-rule WIRING, not new PL/SQL. Pattern = a FUNCTION-type check-rule variable +
-- func-params + a constant, with WHERE_FORMULA testing the function's return. Templates:
--   - FROZEN  : live rule 1026  PHD_PWEL_STATUS_FROZEN_VALUE_V1  -> ZWP_P_TOOLTIP.getValFrozenValue
--   - SUM     : live rule 1077  DAILY_SAMPLING_..._COMP_WT_PCT_V3 -> ZWP_P_VALIDATION.isComponentSumOutOfTolerance
--
-- OPEN DECISIONS (confirm with Grant before deploy):
--   A. SUM check: which class/grain for the Issue_1052 composition?  Finding-1 ambiguity —
--      DB has STRM_COMP_ANALYSIS.MOL_PCT/WT_PCT (per-component, ANALYSIS_NO 2587 etc.), but the
--      existing sum rule (1077) runs on event-grain RV_STRM_GAS_ANALYSIS + TV_STRM_GAS_COMPONENT.
--      => the SUM section below uses <<PLACEHOLDER>> values; DO NOT RUN until confirmed.
--   B. FROZEN check: which attributes need it? Drafted here for STRM_ANALYSIS DENSITY + GCV
--      (the Issue_1052 stream-analysis attrs). Confirm the list with Grant.
--   C. Which group(s) to link to (drafted: V_PHD_STREAM_ANALYSIS for frozen).
--   D. Severity (drafted ERROR, matching the templates).
-- =============================================================================

DECLARE
    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052-ADV';   -- TODO: real ECPR no.

    -- ---- upsert the rule row (match by CHECK_NAME; dynamic CHECK_ID like the other scripts)
    PROCEDURE upsert_rule (p_name VARCHAR2, p_table_id VARCHAR2, p_where VARCHAR2,
                           p_message VARCHAR2, p_sev VARCHAR2) IS
        v_id NUMBER;
    BEGIN
        UPDATE TV_CTRL_CHECK_RULES
           SET TABLE_ID = p_table_id, CLASS_OBJ_VALIDATION_IND = 'N',
               WHERE_FORMULA = p_where, CHECK_MESSAGE = p_message,
               SEVERITY_LEVEL = p_sev, REV_TEXT = c_rev_text
         WHERE CHECK_NAME = p_name;
        IF SQL%ROWCOUNT = 0 THEN
            SELECT NVL(MAX(CHECK_ID),0)+1 INTO v_id FROM CTRL_CHECK_RULES;
            INSERT INTO TV_CTRL_CHECK_RULES
                (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
                 CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL, REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULES', v_id, p_name, 'Count(*)', p_table_id,
                 'N', p_where, p_message, p_sev, c_rev_text);
        END IF;
    END;

    PROCEDURE upsert_var (p_name VARCHAR2, p_var VARCHAR2, p_type VARCHAR2, p_value VARCHAR2) IS
        v_id NUMBER;
    BEGIN
        SELECT CHECK_ID INTO v_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_name;
        UPDATE TV_CTRL_CHECK_RULE_VARIABLE
           SET VARIABLE_TYPE = p_type, VARIABLE_VALUE = p_value, REV_TEXT = c_rev_text
         WHERE CHECK_ID = v_id AND VARIABLE_NAME = p_var;
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
                (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE, REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULE_VARIABLE', v_id, p_var, p_type, p_value, c_rev_text);
        END IF;
    END;

    -- one function-parameter row (idempotent: delete-by-key then insert)
    PROCEDURE set_param (p_name VARCHAR2, p_var VARCHAR2, p_param VARCHAR2, p_dtype VARCHAR2,
                         p_pos NUMBER, p_ptype VARCHAR2, p_pvalue VARCHAR2) IS
        v_id NUMBER;
    BEGIN
        SELECT CHECK_ID INTO v_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_name;
        DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P
         WHERE CHECK_ID = v_id AND VARIABLE_NAME = p_var AND PARAMETER_NAME = p_param;
        INSERT INTO TV_CTRL_CHECK_RULE_FUNC_P
            (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, PARAMETER_NAME, DATA_TYPE,
             POSITION, PARAMETER_TYPE, PARAMETER_VALUE, REV_TEXT)
        VALUES
            ('CTRL_CHECK_RULE_FUNC_PARAM', v_id, p_var, p_param, p_dtype,
             p_pos, p_ptype, p_pvalue, c_rev_text);
    END;

    PROCEDURE link_group (p_name VARCHAR2, p_group VARCHAR2) IS
        v_id NUMBER;
    BEGIN
        SELECT CHECK_ID INTO v_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_name;
        UPDATE TV_CTRL_CHECK_COMBINATION SET REV_TEXT = c_rev_text
         WHERE CHECK_ID = v_id AND CHECK_GROUP = p_group;
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO TV_CTRL_CHECK_COMBINATION
                (TABLE_CLASS_NAME, CHECK_ID, CHECK_GROUP, REV_TEXT)
            VALUES ('CTRL_CHECK_COMBINATION', v_id, p_group, c_rev_text);
        END IF;
    END;

    -- frozen-value rule helper (clone of live rule 1026)
    PROCEDURE frozen_rule (p_name VARCHAR2, p_table_id VARCHAR2, p_class VARCHAR2,
                           p_value_col VARCHAR2, p_msg VARCHAR2, p_group VARCHAR2) IS
    BEGIN
        upsert_rule(p_name, p_table_id, '(${FunctionFrozenValue}  = ${ConstBOOLEAN})', p_msg, 'ERROR');
        upsert_var(p_name, 'FunctionFrozenValue', 'FUNCTION', 'ZWP_P_TOOLTIP');
        upsert_var(p_name, 'ConstBOOLEAN', 'CONST_STRING', 'FROZEN');
        set_param(p_name, 'FunctionFrozenValue', 'P_CLASS_NAME', 'VARCHAR2', 1, 'ATTRIBUTE',    'DATA_CLASS_NAME');
        set_param(p_name, 'FunctionFrozenValue', 'P_OBJECT_ID',  'VARCHAR2', 2, 'ATTRIBUTE',    'OBJECT_ID');
        set_param(p_name, 'FunctionFrozenValue', 'P_DAYTIME',    'DATE',     3, 'ATTRIBUTE',    'DAYTIME');
        set_param(p_name, 'FunctionFrozenValue', 'P_VALUE',      'NUMBER',   4, 'ATTRIBUTE',    p_value_col);
        set_param(p_name, 'FunctionFrozenValue', 'P_ATTRIBUTE',  'VARCHAR2', 5, 'CONST_STRING', p_value_col);
        link_group(p_name, p_group);
    END;

BEGIN
    -- =========================================================================
    -- PART 1 — FROZEN-VALUE checks  (CONCRETE; clones live rule 1026)
    --   STRM_ANALYSIS Density + GCV (the Issue_1052 stream-analysis attributes)
    --   columns from rules 1144/1145: DENSITY , GCV_MJPERSM3
    -- =========================================================================
    frozen_rule('PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1', 'RV_STRM_ANALYSIS', 'STRM_ANALYSIS',
                'DENSITY',      'Stream :STREAM_NAME Density is frozen (unchanged vs prior days) for :DAYTIME',
                'V_PHD_STREAM_ANALYSIS');
    frozen_rule('PHD_STRM_ANALYSIS_GCV_FROZEN_V1', 'RV_STRM_ANALYSIS', 'STRM_ANALYSIS',
                'GCV_MJPERSM3', 'Stream :STREAM_NAME GCV is frozen (unchanged vs prior days) for :DAYTIME',
                'V_PHD_STREAM_ANALYSIS');

    -- =========================================================================
    -- PART 2 — SUM 98-102% composition check  (TEMPLATE — placeholders, DO NOT RUN as-is)
    --   Clone of live rule 1077 (ZWP_P_VALIDATION.isComponentSumOutOfTolerance).
    --   ⚠️ Grant decision needed (Finding-1): correct class/grain for Issue_1052 composition.
    --   Template wiring (confirm <<PLACEHOLDER>> values):
    --
    --   upsert_rule('PHD_STRM_COMP_MOL_PCT_SUM_V1',
    --               '<<RULE_TABLE_ID: event-grain view, e.g. RV_STRM_GAS_ANALYSIS or RV_STRM_COMP_ANALYSIS>>',
    --               '(${isComponentSumOutOfTolerance} = ${ConstYES})',
    --               'Stream :STREAM_NAME gas composition MOL% does not total ~100% for :DAYTIME', 'ERROR');
    --   upsert_var('PHD_STRM_COMP_MOL_PCT_SUM_V1','isComponentSumOutOfTolerance','FUNCTION','ZWP_P_VALIDATION');
    --   upsert_var('PHD_STRM_COMP_MOL_PCT_SUM_V1','ConstYES','CONST_STRING','YES');
    --   set_param(...,'isComponentSumOutOfTolerance','P_CLASS_NAME','VARCHAR2',1,'CONST_STRING','<<TV_STRM_GAS_COMPONENT or TV_STRM_COMP_ANALYSIS>>');
    --   set_param(...,'isComponentSumOutOfTolerance','P_ANALYSIS_NO','NUMBER',2,'ATTRIBUTE','ANALYSIS_NO');
    --   set_param(...,'isComponentSumOutOfTolerance','P_COLUMN_NAME','VARCHAR2',3,'CONST_STRING','<<COMP_MOL_PCT or MOL_PCT>>');
    --   set_param(...,'isComponentSumOutOfTolerance','P_DAYTIME','DATE',4,'ATTRIBUTE','DAYTIME');
    --   link_group('PHD_STRM_COMP_MOL_PCT_SUM_V1','<<V_PHD_STREAM_COMP>>');
    --   (repeat for WT_PCT)
    --
    --   NOTE: isComponentSumOutOfTolerance returns 'YES' when the per-ANALYSIS_NO sum is outside the
    --   tolerance band (the function encodes ~98-102%; getValSumComp uses a 0.98 factor). Confirm the
    --   exact bounds + that it applies to STRM_COMP_ANALYSIS before enabling.
    --   >>> Part 2 intentionally NOT executed in this draft. <<<

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY (after a reviewed run): the frozen rules exist + are linked
-- =============================================================================
SELECT r.CHECK_ID, r.CHECK_NAME, r.TABLE_ID, r.SEVERITY_LEVEL, c.CHECK_GROUP
  FROM TV_CTRL_CHECK_RULES r
  LEFT JOIN CTRL_CHECK_COMBINATION c ON c.CHECK_ID = r.CHECK_ID
 WHERE r.CHECK_NAME IN ('PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1','PHD_STRM_ANALYSIS_GCV_FROZEN_V1')
 ORDER BY r.CHECK_NAME;
