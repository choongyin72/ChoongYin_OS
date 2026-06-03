-- =============================================================================
-- Issue_1052: ROLLBACK — Delete Check Rules for PHD Tag Validation
-- Purpose : Remove check rules created by Issue1052_PHD_Check_Rules.sql
--           Use for testing/cleanup in COPS DEV environment
-- Author  : Choong-Yin Lee
-- Date    : 2026-06-03
-- Safe    : Re-runnable — DELETE on non-existent rows returns 0 rows, no error
-- Order   : Variables deleted FIRST (child), then Rules (parent) — avoids FK error
-- =============================================================================

DECLARE
    PROCEDURE delete_check_rule (p_check_name IN VARCHAR2) IS
        v_check_id  NUMBER;
        v_count     NUMBER;
    BEGIN
        -- Check if rule exists
        SELECT COUNT(*) INTO v_count
          FROM CTRL_CHECK_RULES
         WHERE CHECK_NAME = p_check_name;

        IF v_count > 0 THEN
            SELECT CHECK_ID INTO v_check_id
              FROM CTRL_CHECK_RULES
             WHERE CHECK_NAME = p_check_name;

            -- Step 1: Delete variables first (child)
            DELETE FROM TV_CTRL_CHECK_RULE_VARIABLE
             WHERE CHECK_ID = v_check_id;

            -- Step 2: Delete function parameters if any
            DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P
             WHERE CHECK_ID = v_check_id;

            -- Step 3: Delete the check rule (parent)
            DELETE FROM TV_CTRL_CHECK_RULES
             WHERE CHECK_ID = v_check_id;
        END IF;

    END delete_check_rule;

BEGIN

    delete_check_rule('PHD_STRM_COMP_MOL_PCT_VAL1');
    delete_check_rule('PHD_STRM_COMP_WT_PCT_VAL1');
    delete_check_rule('PHD_STRM_ANALYSIS_DENSITY_VAL1');
    delete_check_rule('PHD_STRM_ANALYSIS_GCV_VAL1');
    delete_check_rule('PHD_TANK_DIP_GRS_VOL_VAL1');
    delete_check_rule('PHD_TANK_DIP_GRS_MASS_VAL1');
    delete_check_rule('PHD_TANK_DIP_AVG_TEMP_VAL1');
    delete_check_rule('PHD_TANK_DIP_STD_DENSITY_VAL1');

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: Confirm all 8 rules have been removed
-- Expected result: 0 rows returned
-- =============================================================================
SELECT CHECK_ID, CHECK_NAME, TABLE_ID
  FROM TV_CTRL_CHECK_RULES
 WHERE CHECK_NAME IN (
    'PHD_STRM_COMP_MOL_PCT_VAL1',
    'PHD_STRM_COMP_WT_PCT_VAL1',
    'PHD_STRM_ANALYSIS_DENSITY_VAL1',
    'PHD_STRM_ANALYSIS_GCV_VAL1',
    'PHD_TANK_DIP_GRS_VOL_VAL1',
    'PHD_TANK_DIP_GRS_MASS_VAL1',
    'PHD_TANK_DIP_AVG_TEMP_VAL1',
    'PHD_TANK_DIP_STD_DENSITY_VAL1'
 );
-- Expected: 0 rows
