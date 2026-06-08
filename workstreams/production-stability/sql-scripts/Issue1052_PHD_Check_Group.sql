-- =============================================================================
-- Issue_1052: Create Check GROUPS for PHD Tag Validation + link to Check Rules
-- Author : Choong-Yin Lee
-- Date   : 2026-06-08
-- Status : COPS DEV deploy candidate (RECORD_STATUS defaults to 'P' = Provisional)
-- Pattern: UPDATE then INSERT (re-runnable / idempotent). No MERGE.
--          CHECK_ID resolved dynamically by CHECK_NAME (per-DB-instance safe).
-- ECPR   : ECPR-Issue1052  (replace with real ECPR no. before production)
--
-- WHAT THIS DOES
--   The 8 Issue_1052 check rules (PHD_STRM_COMP_*, PHD_STRM_ANALYSIS_*, PHD_TANK_DIP_*)
--   exist in CTRL_CHECK_RULES but have NO group -> nothing runs them. EC resolves a
--   group's rules via the junction table CTRL_CHECK_COMBINATION (CHECK_GROUP <-> CHECK_ID).
--   This script:
--     1. Creates 3 new check groups under parent V_DAILY_PHD_VALIDATION, each linked
--        to its proper EC screen (EC_USER_OBJECT).
--     2. Links each rule to its group via CTRL_CHECK_COMBINATION.
--
--   GROUP                 SCREEN (EC_USER_OBJECT)                                          RULES
--   V_PHD_STREAM_COMP     stream_gas_component_analysis (qualified: STRM_SET/COMP_SET)      MOL_PCT, WT_PCT
--   V_PHD_STREAM_ANALYSIS stream_gas_component_analysis (qualified: STRM_SET/COMP_SET)      DENSITY, GCV
--   V_PHD_TANK_DIP        /com.ec.prod.po.screens/daily_tank_dip_status                    GRS_VOL, GRS_MASS, AVG_TEMP, STD_DENSITY
--   (stream screen needs the STRM_SET/COMP_SET qualifier to resolve in the Check Group screen;
--    the bare template root renders a blank Screen column — fixed 2026-06-08.)
--
-- PREREQUISITE: run Issue1052_PHD_Check_Rules.sql first (creates the 8 rules).
-- =============================================================================

DECLARE

    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052';      -- TODO: real ECPR no.
    c_parent   CONSTANT VARCHAR2(30) := 'V_DAILY_PHD_VALIDATION';

    -- ---------------------------------------------------------------------
    -- Create / refresh a check group under the PHD parent group
    -- ---------------------------------------------------------------------
    PROCEDURE upsert_check_group (
        p_group   IN VARCHAR2,
        p_screen  IN VARCHAR2,
        p_desc    IN VARCHAR2
    ) IS
    BEGIN
        UPDATE TV_CTRL_CHECK_GROUP SET
            PARENT_GROUP   = c_parent,
            EC_USER_OBJECT = p_screen,
            DESCRIPTION    = p_desc,
            REV_TEXT       = c_rev_text
        WHERE CHECK_GROUP = p_group;

        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO TV_CTRL_CHECK_GROUP
                (TABLE_CLASS_NAME, CHECK_GROUP, PARENT_GROUP, EC_USER_OBJECT,
                 DESCRIPTION, REV_TEXT)
            VALUES
                ('CTRL_CHECK_GROUP', p_group, c_parent, p_screen,
                 p_desc, c_rev_text);
        END IF;
    END upsert_check_group;

    -- ---------------------------------------------------------------------
    -- Link a check rule (by name) to a group via CTRL_CHECK_COMBINATION
    -- PK is composite (CHECK_ID, CHECK_GROUP). CHECK_ID resolved at runtime.
    -- ---------------------------------------------------------------------
    PROCEDURE link_rule_to_group (
        p_check_name IN VARCHAR2,
        p_group      IN VARCHAR2
    ) IS
        v_check_id  NUMBER;
    BEGIN
        SELECT CHECK_ID INTO v_check_id
          FROM CTRL_CHECK_RULES
         WHERE CHECK_NAME = p_check_name;

        UPDATE TV_CTRL_CHECK_COMBINATION SET
            REV_TEXT = c_rev_text
        WHERE CHECK_ID    = v_check_id
          AND CHECK_GROUP = p_group;

        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO TV_CTRL_CHECK_COMBINATION
                (TABLE_CLASS_NAME, CHECK_ID, CHECK_GROUP, REV_TEXT)
            VALUES
                ('CTRL_CHECK_COMBINATION', v_check_id, p_group, c_rev_text);
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20001,
                'Check rule not found: ' || p_check_name ||
                ' - run Issue1052_PHD_Check_Rules.sql before this script.');
    END link_rule_to_group;

BEGIN

    -- =========================================================================
    -- STEP 1: create the 3 new check groups (under V_DAILY_PHD_VALIDATION)
    -- =========================================================================
    upsert_check_group(
        p_group  => 'V_PHD_STREAM_COMP',
        p_screen => '/com.ec.prod.po.screens/stream_gas_component_analysis/STRM_SET/PO.0020/COMP_SET/STRM_GAS_COMP?screentemplate=/com.ec.prod.po.screens/stream_gas_component_analysis',
        p_desc   => 'Stream Gas Component Analysis (Composition) - PHD Validations');

    upsert_check_group(
        p_group  => 'V_PHD_STREAM_ANALYSIS',
        p_screen => '/com.ec.prod.po.screens/stream_gas_component_analysis/STRM_SET/PO.0020/COMP_SET/STRM_GAS_COMP?screentemplate=/com.ec.prod.po.screens/stream_gas_component_analysis',
        p_desc   => 'Stream Gas Component Analysis (Analysis) - PHD Validations');

    upsert_check_group(
        p_group  => 'V_PHD_TANK_DIP',
        p_screen => '/com.ec.prod.po.screens/daily_tank_dip_status',
        p_desc   => 'Daily Tank Status - VCF Calc - PHD Validations');

    -- =========================================================================
    -- STEP 2: link each rule to its group (CTRL_CHECK_COMBINATION)
    -- =========================================================================
    -- Group V_PHD_STREAM_COMP  (STRM_COMP_ANALYSIS)
    link_rule_to_group('PHD_STRM_COMP_MOL_PCT_VAL1',     'V_PHD_STREAM_COMP');
    link_rule_to_group('PHD_STRM_COMP_WT_PCT_VAL1',      'V_PHD_STREAM_COMP');

    -- Group V_PHD_STREAM_ANALYSIS  (STRM_ANALYSIS)
    link_rule_to_group('PHD_STRM_ANALYSIS_DENSITY_VAL1', 'V_PHD_STREAM_ANALYSIS');
    link_rule_to_group('PHD_STRM_ANALYSIS_GCV_VAL1',     'V_PHD_STREAM_ANALYSIS');

    -- Group V_PHD_TANK_DIP  (TANK_DAY_DIP_STATUS)
    link_rule_to_group('PHD_TANK_DIP_GRS_VOL_VAL1',      'V_PHD_TANK_DIP');
    link_rule_to_group('PHD_TANK_DIP_GRS_MASS_VAL1',     'V_PHD_TANK_DIP');
    link_rule_to_group('PHD_TANK_DIP_AVG_TEMP_VAL1',     'V_PHD_TANK_DIP');
    link_rule_to_group('PHD_TANK_DIP_STD_DENSITY_VAL1',  'V_PHD_TANK_DIP');

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY 1: the 3 new groups exist under the PHD parent
-- =============================================================================
SELECT CHECK_GROUP, PARENT_GROUP, EC_USER_OBJECT, RECORD_STATUS
  FROM TV_CTRL_CHECK_GROUP
 WHERE CHECK_GROUP IN ('V_PHD_STREAM_COMP','V_PHD_STREAM_ANALYSIS','V_PHD_TANK_DIP')
 ORDER BY CHECK_GROUP;

-- =============================================================================
-- VERIFY 2: each rule is linked to its group (expect 8 rows)
-- =============================================================================
SELECT c.CHECK_GROUP, c.CHECK_ID, r.CHECK_NAME, r.TABLE_ID
  FROM CTRL_CHECK_COMBINATION c
  JOIN CTRL_CHECK_RULES r ON r.CHECK_ID = c.CHECK_ID
 WHERE c.CHECK_GROUP IN ('V_PHD_STREAM_COMP','V_PHD_STREAM_ANALYSIS','V_PHD_TANK_DIP')
 ORDER BY c.CHECK_GROUP, c.CHECK_ID;
-- Expected: 8 rows
--   V_PHD_STREAM_ANALYSIS -> PHD_STRM_ANALYSIS_DENSITY_VAL1 / _GCV_VAL1   (RV_STRM_ANALYSIS)
--   V_PHD_STREAM_COMP     -> PHD_STRM_COMP_MOL_PCT_VAL1 / _WT_PCT_VAL1    (RV_STRM_COMP_ANALYSIS)
--   V_PHD_TANK_DIP        -> PHD_TANK_DIP_GRS_VOL/_GRS_MASS/_AVG_TEMP/_STD_DENSITY (RV_TANK_DAY_DIP_STATUS)
