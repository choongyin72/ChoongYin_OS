-- =============================================================================
-- Issue_1052: Add Check Rules for PHD Tags without Check Rule Validation
-- Classes: STRM_COMP_ANALYSIS, STRM_ANALYSIS, TANK_DAY_DIP_STATUS
-- Author : Choong-Yin Lee
-- Date   : 2026-06-03
-- Status : LOCAL DRAFT - DO NOT DEPLOY without Grant approval
-- Pattern: UPDATE then INSERT (re-runnable)
--          CHECK_ID dynamically assigned per DB instance
-- ECPR   : TBD - replace 'ECPR-Issue1052' with actual ECPR ticket before deploy
-- Covers : 131 NEITHER PHD tags (no check rule, no class validation)
-- =============================================================================

DECLARE

    c_rev_text CONSTANT VARCHAR2(50) := 'ECPR-Issue1052'; -- TODO: replace with actual ECPR no.

    PROCEDURE upsert_check_rule (
        p_check_name   IN VARCHAR2,
        p_table_id     IN VARCHAR2,
        p_where        IN VARCHAR2,
        p_message      IN VARCHAR2,
        p_severity     IN VARCHAR2,
        p_var_name     IN VARCHAR2,
        p_var_value    IN VARCHAR2
    ) IS
        v_check_id  NUMBER;
    BEGIN
        -- Step 1: Try UPDATE on check rule (match by CHECK_NAME)
        UPDATE TV_CTRL_CHECK_RULES SET
            TABLE_ID                 = p_table_id,
            CLASS_OBJ_VALIDATION_IND = 'N',
            WHERE_FORMULA            = p_where,
            CHECK_MESSAGE            = p_message,
            SEVERITY_LEVEL           = p_severity,
            REV_TEXT                 = c_rev_text
        WHERE CHECK_NAME = p_check_name;

        IF SQL%ROWCOUNT > 0 THEN
            -- Rule existed - get its ID
            SELECT CHECK_ID INTO v_check_id
              FROM CTRL_CHECK_RULES
             WHERE CHECK_NAME = p_check_name;
        ELSE
            -- Rule does not exist - INSERT with next available ID for this DB instance
            SELECT NVL(MAX(CHECK_ID), 0) + 1 INTO v_check_id
              FROM CTRL_CHECK_RULES;

            INSERT INTO TV_CTRL_CHECK_RULES
                (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
                 CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL,
                 REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULES', v_check_id, p_check_name, 'Count(*)', p_table_id,
                 'N', p_where, p_message, p_severity,
                 c_rev_text);
        END IF;

        -- Step 2: Try UPDATE on variable (match by CHECK_ID + VARIABLE_NAME)
        UPDATE TV_CTRL_CHECK_RULE_VARIABLE SET
            VARIABLE_TYPE  = 'ATTRIBUTE',
            VARIABLE_VALUE = p_var_value,
            REV_TEXT       = c_rev_text
        WHERE CHECK_ID    = v_check_id
          AND VARIABLE_NAME = p_var_name;

        IF SQL%ROWCOUNT = 0 THEN
            -- Variable does not exist - INSERT
            INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
                (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE,
                 REV_TEXT)
            VALUES
                ('CTRL_CHECK_RULE_VARIABLE', v_check_id, p_var_name, 'ATTRIBUTE', p_var_value,
                 c_rev_text);
        END IF;

    END upsert_check_rule;

BEGIN

    -- =========================================================================
    -- PART 1: STRM_COMP_ANALYSIS - MOL_PCT (78 tags)
    -- Streams: 1C1401 to E1405A/B, DBNGP Export, HP/MP Fuel Gas GT4001-4004,
    --          1KT1410/1430, Pluto Feed Ref, Train 1 HP N2 Vent
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_STRM_COMP_MOL_PCT_VAL1',
        p_table_id   => 'RV_STRM_COMP_ANALYSIS',
        p_where      => '(${MolPct} IS NULL OR ${MolPct} < 0 OR ${MolPct} > 100)',
        p_message    => 'Stream :STREAM_NAME component :COMPONENT_NO has invalid or missing Mol% for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'MolPct',
        p_var_value  => 'MOL_PCT'
    );

    -- =========================================================================
    -- PART 2: STRM_COMP_ANALYSIS - WT_PCT (24 tags)
    -- Streams: 1C1401 to E1405A/B, Flare Pilot A, Pluto-NWS Interconnector
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_STRM_COMP_WT_PCT_VAL1',
        p_table_id   => 'RV_STRM_COMP_ANALYSIS',
        p_where      => '(${WtPct} IS NULL OR ${WtPct} < 0 OR ${WtPct} > 100)',
        p_message    => 'Stream :STREAM_NAME component :COMPONENT_NO has invalid or missing Wt% for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'WtPct',
        p_var_value  => 'WT_PCT'
    );

    -- =========================================================================
    -- PART 3: STRM_ANALYSIS - DENSITY (6 tags)
    -- Streams: HP Fuel Gas 1KT1410/1430, MP Fuel Gas GT4001-GT4004
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_STRM_ANALYSIS_DENSITY_VAL1',
        p_table_id   => 'RV_STRM_ANALYSIS',
        p_where      => '(${Density} IS NULL OR ${Density} < 0)',
        p_message    => 'Stream :STREAM_NAME has invalid or missing Density value for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'Density',
        p_var_value  => 'DENSITY'
    );

    -- =========================================================================
    -- PART 4: STRM_ANALYSIS - GCV (9 tags)
    -- Streams: HP/MP Fuel Gas GT4001-4004, 1KT1410/1430, Flare Pilots A/B, RTO
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_STRM_ANALYSIS_GCV_VAL1',
        p_table_id   => 'RV_STRM_ANALYSIS',
        p_where      => '(${Gcv} IS NULL OR ${Gcv} < 0)',
        p_message    => 'Stream :STREAM_NAME has invalid or missing GCV value for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'Gcv',
        p_var_value  => 'GCV_MJPERSM3'
    );

    -- =========================================================================
    -- PART 5: TANK_DAY_DIP_STATUS - GRS_VOL (5 tags)
    -- Tanks: LNG T3101/T3102, Condensate T3301/T3302/T3303
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_TANK_DIP_GRS_VOL_VAL1',
        p_table_id   => 'RV_TANK_DAY_DIP_STATUS',
        p_where      => '(${GrsVol} IS NULL OR ${GrsVol} < 0)',
        p_message    => 'Tank :TANK_NAME has invalid or missing Gross Volume for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'GrsVol',
        p_var_value  => 'GRS_VOL_SM3'
    );

    -- =========================================================================
    -- PART 6: TANK_DAY_DIP_STATUS - ZWP_GRS_MASS (2 tags)
    -- Tanks: LNG Tank 3101, LNG Tank 3102
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_TANK_DIP_GRS_MASS_VAL1',
        p_table_id   => 'RV_TANK_DAY_DIP_STATUS',
        p_where      => '(${GrsMass} IS NULL OR ${GrsMass} < 0)',
        p_message    => 'Tank :TANK_NAME has invalid or missing Gross Mass for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'GrsMass',
        p_var_value  => 'ZWP_GRS_MASS_TONNES'
    );

    -- =========================================================================
    -- PART 7: TANK_DAY_DIP_STATUS - AVG_TEMP (5 tags)
    -- Tanks: LNG T3101/T3102, Condensate T3301/T3302/T3303
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_TANK_DIP_AVG_TEMP_VAL1',
        p_table_id   => 'RV_TANK_DAY_DIP_STATUS',
        p_where      => '(${AvgTemp} IS NULL)',
        p_message    => 'Tank :TANK_NAME has missing Average Temperature for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'AvgTemp',
        p_var_value  => 'AVG_TEMP_C'
    );

    -- =========================================================================
    -- PART 8: TANK_DAY_DIP_STATUS - MEAS_STD_DENSITY (2 tags)
    -- Tanks: LNG Tank 3101, LNG Tank 3102
    -- =========================================================================
    upsert_check_rule(
        p_check_name => 'PHD_TANK_DIP_STD_DENSITY_VAL1',
        p_table_id   => 'RV_TANK_DAY_DIP_STATUS',
        p_where      => '(${StdDensity} IS NULL OR ${StdDensity} < 0)',
        p_message    => 'Tank :TANK_NAME has invalid or missing Standard Density for :DAYTIME',
        p_severity   => 'ERROR',
        p_var_name   => 'StdDensity',
        p_var_value  => 'MEAS_STD_DENSITY_KGPERSM3'
    );

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: Confirm all 8 rules exist after running
-- =============================================================================
SELECT CHECK_ID, CHECK_NAME, TABLE_ID, SEVERITY_LEVEL, REV_TEXT
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
 )
 ORDER BY CHECK_ID;

-- =============================================================================
-- NOT included (requires separate ECPR):
--   - Sum check 98-102% for MOL_PCT/WT_PCT (needs custom SQL function)
--   - Frozen value check (needs ZWP_P_VALIDATION function reference)
--   - ZWT_OILINWAT check (ECPR-F)
-- =============================================================================
