-- =============================================================================
-- Issue_1052: Link SUM 98-102% MOLE % Check Rules to their Check Groups  (LINK-ONLY)
-- Author : Choong-Yin Lee  |  Date: 2026-06-10
-- Pattern: UPDATE then INSERT (re-runnable). CHECK_ID resolved dynamically by CHECK_NAME.
-- Companion to Issue1052_PHD_Sum_MolPct_Checks.sql (the 2 MOL% sum rules).
--
-- LINK-ONLY: both target groups already exist (they hold the parent WT% rules 1077/1083),
--   so NO group is created/modified here — the MOL% rule simply joins the same group as its
--   WT% sibling, exactly as decided (mirror parent).
--
--   GROUP                         MOL% RULE
--   V_DLY_SAMPLING_STRM_GAS_COMP  DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1
--   V_DLY_SAMPLING_WELL_GAS_COMP  DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1
--
-- PREREQUISITE: run Issue1052_PHD_Sum_MolPct_Checks.sql first (creates the 2 rules).
-- =============================================================================

DECLARE
    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052-SUM-MOL';

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
                'MOL% sum check rule not found: ' || p_check_name ||
                ' - run Issue1052_PHD_Sum_MolPct_Checks.sql before this script.');
    END link_rule_to_group;

BEGIN
    link_rule_to_group('DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1', 'V_DLY_SAMPLING_STRM_GAS_COMP');
    link_rule_to_group('DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1', 'V_DLY_SAMPLING_WELL_GAS_COMP');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: each MOL% rule linked to its group.  Expected: 2 rows.
-- =============================================================================
SELECT c.CHECK_GROUP, c.CHECK_ID, r.CHECK_NAME, r.TABLE_ID
  FROM CTRL_CHECK_COMBINATION c
  JOIN CTRL_CHECK_RULES r ON r.CHECK_ID = c.CHECK_ID
 WHERE r.CHECK_NAME IN (
    'DAILY_SAMPLING_STRM_GAS_COMPONENT_COMP_MOL_PCT_V1',
    'DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1'
 )
 ORDER BY c.CHECK_GROUP, r.CHECK_NAME;
-- Expected: 2 rows
