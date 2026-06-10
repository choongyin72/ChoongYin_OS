-- =============================================================================
-- Issue_1052: Link FROZEN-VALUE Check Rules to their Check Groups  (DRAFT)
-- Author : Choong-Yin Lee  |  Date: 2026-06-09
-- Pattern: UPDATE then INSERT (re-runnable). CHECK_ID resolved dynamically by CHECK_NAME.
-- Companion to Issue1052_PHD_Frozen_Checks.sql (the 6 frozen rules).
--
-- LINK-ONLY: all 4 target groups already exist, so NO group is created/modified here.
--   V_PHD_STREAM_COMP / V_PHD_STREAM_ANALYSIS  -> created by Issue1052_PHD_Check_Group.sql
--   V_PHD_STREAM_WATER / V_PHD_PWEL_STATUS     -> pre-existing LIVE EC groups (do not touch)
--
--   GROUP                  FROZEN RULE(S)  [4 ACTIVE links]
--   V_PHD_STREAM_ANALYSIS  PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1, PHD_STRM_ANALYSIS_GCV_FROZEN_V1
--   V_PHD_STREAM_WATER     PHD_STREAM_WATER_OILINWAT_FROZEN_V1
--   V_PHD_PWEL_STATUS      PHD_PWEL_AVG_GAS_RATE_FROZEN_V1
--   ON HOLD (NOT linked): V_PHD_STREAM_COMP <- MOL_PCT/WT_PCT composition frozen (1150/1151)
--
-- PREREQUISITE: run Issue1052_PHD_Frozen_Checks.sql first (creates the 4 active rules).
-- =============================================================================

DECLARE
    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052-FROZEN';

    PROCEDURE link_rule_to_group (p_check_name IN VARCHAR2, p_group IN VARCHAR2) IS
        v_check_id NUMBER;
    BEGIN
        SELECT CHECK_ID INTO v_check_id FROM CTRL_CHECK_RULES WHERE CHECK_NAME = p_check_name;

        UPDATE TV_CTRL_CHECK_COMBINATION SET REV_TEXT = c_rev_text
         WHERE CHECK_ID = v_check_id AND CHECK_GROUP = p_group;
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO TV_CTRL_CHECK_COMBINATION
                (TABLE_CLASS_NAME, CHECK_ID, CHECK_GROUP, REV_TEXT)
            VALUES
                ('CTRL_CHECK_COMBINATION', v_check_id, p_group, c_rev_text);
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20001,
                'Frozen check rule not found: ' || p_check_name ||
                ' - run Issue1052_PHD_Frozen_Checks.sql before this script.');
    END link_rule_to_group;

BEGIN
    -- ON HOLD - composition frozen 1150/1151 (dormant). Do NOT link until component-aware fn:
    --   link_rule_to_group('PHD_STRM_COMP_MOL_PCT_FROZEN_V1', 'V_PHD_STREAM_COMP');
    --   link_rule_to_group('PHD_STRM_COMP_WT_PCT_FROZEN_V1',  'V_PHD_STREAM_COMP');
    link_rule_to_group('PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1', 'V_PHD_STREAM_ANALYSIS');
    link_rule_to_group('PHD_STRM_ANALYSIS_GCV_FROZEN_V1',     'V_PHD_STREAM_ANALYSIS');
    link_rule_to_group('PHD_STREAM_WATER_OILINWAT_FROZEN_V1', 'V_PHD_STREAM_WATER');
    link_rule_to_group('PHD_PWEL_AVG_GAS_RATE_FROZEN_V1',     'V_PHD_PWEL_STATUS');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- VERIFY: each ACTIVE frozen rule linked to its group (expect 4 rows; 1150/1151 ON HOLD, unlinked).
SELECT c.CHECK_GROUP, c.CHECK_ID, r.CHECK_NAME, r.TABLE_ID
  FROM CTRL_CHECK_COMBINATION c
  JOIN CTRL_CHECK_RULES r ON r.CHECK_ID = c.CHECK_ID
 WHERE r.CHECK_NAME IN (
    'PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1',
    'PHD_STRM_ANALYSIS_GCV_FROZEN_V1',
    'PHD_STREAM_WATER_OILINWAT_FROZEN_V1',
    'PHD_PWEL_AVG_GAS_RATE_FROZEN_V1'
 )
 ORDER BY c.CHECK_GROUP, r.CHECK_NAME;
-- Expected: 4 rows
