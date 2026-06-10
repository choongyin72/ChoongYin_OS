-- =============================================================================
-- Issue_1052: ROLLBACK — Delete SUM 98-102% MOLE % Check Rules (COMP_MOL_PCT)
-- Purpose : Remove the 2 MOL% sum rules created by Issue1052_PHD_Sum_MolPct_Checks.sql.
-- Author  : Choong-Yin Lee  |  Date: 2026-06-10
-- Safe    : Re-runnable — DELETE on non-existent rows returns 0 rows, no error.
--           Matched by CHECK_NAME (IDs were auto-assigned, so never hard-code them).
-- Order   : children first (func-params, variables, group links) then rule (parent).
-- NOTE    : Does NOT touch parents 1077/1083 (the WT% rules) — different CHECK_NAMEs.
-- =============================================================================

DECLARE
    PROCEDURE delete_sum_rule (p_check_name IN VARCHAR2) IS
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
            -- Step 3: group links (child)
            DELETE FROM TV_CTRL_CHECK_COMBINATION    WHERE CHECK_ID = v_check_id;
            -- Step 4: the check rule (parent)
            DELETE FROM TV_CTRL_CHECK_RULES          WHERE CHECK_ID = v_check_id;
        END IF;
    END delete_sum_rule;

BEGIN
    delete_sum_rule('DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1');
    delete_sum_rule('DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: confirm the 2 MOL% sum rules removed.  Expected: 0 rows.
-- =============================================================================
SELECT CHECK_ID, CHECK_NAME, TABLE_ID
  FROM TV_CTRL_CHECK_RULES
 WHERE CHECK_NAME IN (
    'DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1',
    'DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1'
 );
-- Expected: 0 rows
