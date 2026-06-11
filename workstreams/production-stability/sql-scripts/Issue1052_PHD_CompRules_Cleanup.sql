-- =============================================================================
-- Issue_1052: CLEANUP — remove invalid composition check rules 1142/1143 + their group
-- Author : Choong-Yin Lee  |  Date: 2026-06-11
-- Why    : PHD_STRM_COMP_MOL_PCT_VAL1 (1142) / PHD_STRM_COMP_WT_PCT_VAL1 (1143) on
--          STRM_COMP_ANALYSIS are INVALID / no longer used. They are the ONLY rules in
--          group V_PHD_STREAM_COMP (verified), so the now-empty group is dropped too.
-- Safe   : Re-runnable; matched by CHECK_NAME (id-agnostic); children -> parent -> group.
-- =============================================================================

DECLARE
    PROCEDURE purge_rule (p_name IN VARCHAR2) IS
        v_id NUMBER; v_cnt NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_cnt FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_name;
        IF v_cnt > 0 THEN
            SELECT CHECK_ID INTO v_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_name;
            DELETE FROM TV_CTRL_CHECK_COMBINATION   WHERE CHECK_ID = v_id;   -- group link (child)
            DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P   WHERE CHECK_ID = v_id;   -- func params (child)
            DELETE FROM TV_CTRL_CHECK_RULE_VARIABLE WHERE CHECK_ID = v_id;   -- variables (child)
            DELETE FROM TV_CTRL_CHECK_RULES         WHERE CHECK_ID = v_id;   -- rule (parent)
        END IF;
    END purge_rule;
BEGIN
    purge_rule('PHD_STRM_COMP_MOL_PCT_VAL1');
    purge_rule('PHD_STRM_COMP_WT_PCT_VAL1');
    -- drop the now-empty group (only ever held 1142/1143)
    DELETE FROM TV_CTRL_CHECK_GROUP WHERE CHECK_GROUP = 'V_PHD_STREAM_COMP';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: all three expected EMPTY (0 rows)
-- =============================================================================
SELECT CHECK_ID, CHECK_NAME FROM TV_CTRL_CHECK_RULES
 WHERE CHECK_NAME IN ('PHD_STRM_COMP_MOL_PCT_VAL1','PHD_STRM_COMP_WT_PCT_VAL1');

SELECT CHECK_GROUP, CHECK_ID FROM CTRL_CHECK_COMBINATION WHERE CHECK_GROUP = 'V_PHD_STREAM_COMP';

SELECT CHECK_GROUP FROM TV_CTRL_CHECK_GROUP WHERE CHECK_GROUP = 'V_PHD_STREAM_COMP';
-- Expected: 0 rows each
