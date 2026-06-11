-- =============================================================================
-- Issue_1052: ROLLBACK - Remove Check GROUPS + rule links for PHD Tag Validation
-- Purpose : Revert everything created by Issue1052_PHD_Check_Group.sql
--           (the 2 groups and their CTRL_CHECK_COMBINATION rule links)
-- Author  : Choong-Yin Lee
-- Date    : 2026-06-08
-- Safe    : Re-runnable - DELETE on non-existent rows returns 0 rows, no error
-- Order   : Combination links deleted FIRST (child), then groups (parent)
-- NOTE    : This does NOT delete the check rules themselves. The rules have their
--           own revert: Issue1052_PHD_Check_Rules_ROLLBACK.sql
-- =============================================================================

DECLARE
    PROCEDURE drop_group (p_group IN VARCHAR2) IS
    BEGIN
        -- Step 1: remove rule links for this group (child)
        DELETE FROM TV_CTRL_CHECK_COMBINATION
         WHERE CHECK_GROUP = p_group;

        -- Step 2: remove the check group itself (parent)
        DELETE FROM TV_CTRL_CHECK_GROUP
         WHERE CHECK_GROUP = p_group;
    END drop_group;

BEGIN

    -- V_PHD_STREAM_COMP removed 2026-06-11 (its only rules 1142/1143 are invalid)
    drop_group('V_PHD_STREAM_ANALYSIS');
    drop_group('V_PHD_TANK_DIP');

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY 1: groups removed (expect 0 rows)
-- =============================================================================
SELECT CHECK_GROUP, PARENT_GROUP
  FROM TV_CTRL_CHECK_GROUP
 WHERE CHECK_GROUP IN ('V_PHD_STREAM_ANALYSIS','V_PHD_TANK_DIP');
-- Expected: 0 rows

-- =============================================================================
-- VERIFY 2: rule links removed (expect 0 rows)
-- =============================================================================
SELECT CHECK_GROUP, CHECK_ID
  FROM CTRL_CHECK_COMBINATION
 WHERE CHECK_GROUP IN ('V_PHD_STREAM_ANALYSIS','V_PHD_TANK_DIP');
-- Expected: 0 rows
