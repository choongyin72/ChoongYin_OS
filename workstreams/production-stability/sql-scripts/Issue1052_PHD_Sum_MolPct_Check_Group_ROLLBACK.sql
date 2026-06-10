-- =============================================================================
-- Issue_1052: ROLLBACK — Unlink SUM 98-102% MOLE % Check Rules from their Groups
-- Purpose : Surgically remove ONLY the two MOL% rule<->group links added by
--           Issue1052_PHD_Sum_MolPct_Check_Group.sql. The groups themselves and the
--           parent WT% links (1077/1083) are left untouched.
-- Author  : Choong-Yin Lee  |  Date: 2026-06-10
-- Safe    : Re-runnable. Matched by CHECK_NAME + CHECK_GROUP (never by hard-coded id).
-- =============================================================================

DECLARE
    PROCEDURE unlink_rule_from_group (p_check_name IN VARCHAR2, p_group IN VARCHAR2) IS
        v_check_id NUMBER;
        v_count    NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;
        IF v_count > 0 THEN
            SELECT CHECK_ID INTO v_check_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;
            DELETE FROM TV_CTRL_CHECK_COMBINATION
             WHERE CHECK_ID = v_check_id AND CHECK_GROUP = p_group;
        END IF;
    END unlink_rule_from_group;

BEGIN
    unlink_rule_from_group('DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1', 'V_DLY_SAMPLING_STRM_GAS_COMP');
    unlink_rule_from_group('DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1', 'V_DLY_SAMPLING_WELL_GAS_COMP');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: confirm the 2 MOL% links removed.  Expected: 0 rows.
-- =============================================================================
SELECT c.CHECK_GROUP, c.CHECK_ID, r.CHECK_NAME
  FROM CTRL_CHECK_COMBINATION c
  JOIN CTRL_CHECK_RULES r ON r.CHECK_ID = c.CHECK_ID
 WHERE r.CHECK_NAME IN (
    'DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1',
    'DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1'
 );
-- Expected: 0 rows
