-- =============================================================================
-- Issue_1052: ROLLBACK — Delete FROZEN-VALUE Check Rules
-- Purpose : Remove the 9 frozen rules created by Issue1052_PHD_Frozen_Checks.sql
-- Author  : Choong-Yin Lee  |  Date: 2026-06-09
-- Safe    : Re-runnable — DELETE on non-existent rows returns 0 rows, no error
-- Order   : children first (func-params, variables, group links) then rule (parent)
-- =============================================================================

DECLARE
    PROCEDURE delete_frozen_rule (p_check_name IN VARCHAR2) IS
        v_check_id NUMBER;
        v_count    NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;
        IF v_count > 0 THEN
            SELECT CHECK_ID INTO v_check_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;

            -- Step 1: function parameters (child)
            DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P    WHERE CHECK_ID = v_check_id;
            -- Step 2: variables (child)
            DELETE FROM TV_CTRL_CHECK_RULE_VARIABLE  WHERE CHECK_ID = v_check_id;
            -- Step 3: group links (child) — frozen rules add CTRL_CHECK_COMBINATION rows
            DELETE FROM TV_CTRL_CHECK_COMBINATION    WHERE CHECK_ID = v_check_id;
            -- Step 4: the check rule (parent)
            DELETE FROM TV_CTRL_CHECK_RULES          WHERE CHECK_ID = v_check_id;
        END IF;
    END delete_frozen_rule;

BEGIN
    delete_frozen_rule('PHD_STRM_COMP_MOL_PCT_FROZEN_V1');
    delete_frozen_rule('PHD_STRM_COMP_WT_PCT_FROZEN_V1');
    delete_frozen_rule('PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1');
    delete_frozen_rule('PHD_STRM_ANALYSIS_GCV_FROZEN_V1');
    delete_frozen_rule('PHD_STREAM_WATER_OILINWAT_FROZEN_V1');
    delete_frozen_rule('PHD_PWEL_AVG_GAS_RATE_FROZEN_V1');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: confirm all 6 frozen rules removed.  Expected: 0 rows.
-- =============================================================================
SELECT CHECK_ID, CHECK_NAME, TABLE_ID
  FROM TV_CTRL_CHECK_RULES
 WHERE CHECK_NAME IN (
    'PHD_STRM_COMP_MOL_PCT_FROZEN_V1',
    'PHD_STRM_COMP_WT_PCT_FROZEN_V1',
    'PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1',
    'PHD_STRM_ANALYSIS_GCV_FROZEN_V1',
    'PHD_STREAM_WATER_OILINWAT_FROZEN_V1',
    'PHD_PWEL_AVG_GAS_RATE_FROZEN_V1'
 );
-- Expected: 0 rows
