-- =============================================================================
-- Issue_1052: ROLLBACK - Unlink FROZEN-VALUE Check Rules from their Check Groups
-- Purpose : Revert the 4 ACTIVE links created by Issue1052_PHD_Frozen_Check_Group.sql
--           (1150/1151 composition already unlinked + ON HOLD - not handled here.)
-- Author  : Choong-Yin Lee  |  Date: 2026-06-09
-- Safe    : Re-runnable - DELETE on non-existent rows returns 0 rows, no error
--
-- SURGICAL: deletes ONLY the specific (frozen-rule, group) pairs by CHECK_ID.
--   Never DELETE WHERE CHECK_GROUP = ... alone — these groups also hold pre-existing
--   live rules (e.g. 1049, 1026) and the Phase-1 rules; a group-wide delete would
--   unlink those too. Groups themselves are NOT dropped (they are shared/live).
-- =============================================================================

DECLARE
    PROCEDURE unlink_rule (p_check_name IN VARCHAR2, p_group IN VARCHAR2) IS
        v_check_id NUMBER;
        v_count    NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;
        IF v_count > 0 THEN
            SELECT CHECK_ID INTO v_check_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;
            DELETE FROM TV_CTRL_CHECK_COMBINATION
             WHERE CHECK_ID = v_check_id AND CHECK_GROUP = p_group;
        END IF;
    END unlink_rule;

BEGIN
    -- ON HOLD - 1150/1151 already unlinked/dormant (not re-handled here):
    --   unlink_rule('PHD_STRM_COMP_MOL_PCT_FROZEN_V1', 'V_PHD_STREAM_COMP');
    --   unlink_rule('PHD_STRM_COMP_WT_PCT_FROZEN_V1',  'V_PHD_STREAM_COMP');
    unlink_rule('PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1', 'V_PHD_STREAM_ANALYSIS');
    unlink_rule('PHD_STRM_ANALYSIS_GCV_FROZEN_V1',     'V_PHD_STREAM_ANALYSIS');
    unlink_rule('PHD_STREAM_WATER_OILINWAT_FROZEN_V1', 'V_PHD_STREAM_WATER');
    unlink_rule('PHD_PWEL_AVG_GAS_RATE_FROZEN_V1',     'V_PHD_PWEL_STATUS');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- VERIFY: the 4 ACTIVE frozen-rule links removed (expect 0 rows).
SELECT c.CHECK_GROUP, c.CHECK_ID, r.CHECK_NAME
  FROM CTRL_CHECK_COMBINATION c
  JOIN CTRL_CHECK_RULES r ON r.CHECK_ID = c.CHECK_ID
 WHERE r.CHECK_NAME IN (
    'PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1',
    'PHD_STRM_ANALYSIS_GCV_FROZEN_V1',
    'PHD_STREAM_WATER_OILINWAT_FROZEN_V1',
    'PHD_PWEL_AVG_GAS_RATE_FROZEN_V1'
 );
-- Expected: 0 rows
