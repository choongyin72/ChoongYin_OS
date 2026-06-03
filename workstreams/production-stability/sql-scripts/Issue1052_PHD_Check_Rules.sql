-- =============================================================================
-- Issue_1052: Add Check Rules for PHD Tags without Check Rule Validation
-- Classes: STRM_COMP_ANALYSIS, STRM_ANALYSIS, TANK_DAY_DIP_STATUS
-- Author : Choong-Yin Lee
-- Date   : 2026-06-03
-- Status : LOCAL DRAFT - DO NOT DEPLOY without Grant approval
-- Note   : CHECK_IDs start at 1142 (max existing = 1141)
-- Covers : 131 NEITHER PHD tags (no check rule, no class validation)
-- =============================================================================


-- =============================================================================
-- PART 1: STRM_COMP_ANALYSIS - MOL_PCT (78 tags)
-- Rule: MOL_PCT must not be NULL, < 0, or > 100
-- Affected streams: 1C1401 to E1405A/B, DBNGP Pipeline Export, HP/MP Fuel Gas
--                  GT4001-4004, 1KT1410/1430, Pluto Feed Ref, Train 1 HP N2 Vent
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1142, 'PHD_STRM_COMP_MOL_PCT_VAL1', 'Count(*)',
     'RV_STRM_COMP_ANALYSIS', 'N',
     '(${MolPct} IS NULL OR ${MolPct} < 0 OR ${MolPct} > 100)',
     'Stream :STREAM_NAME component :COMPONENT_NO has invalid or missing Mol% value for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1142, 'MolPct', 'ATTRIBUTE', 'MOL_PCT');


-- =============================================================================
-- PART 2: STRM_COMP_ANALYSIS - WT_PCT (24 tags)
-- Rule: WT_PCT must not be NULL, < 0, or > 100
-- Affected streams: 1C1401 to E1405A/B, Flare Pilot A, Pluto-NWS Interconnector
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1143, 'PHD_STRM_COMP_WT_PCT_VAL1', 'Count(*)',
     'RV_STRM_COMP_ANALYSIS', 'N',
     '(${WtPct} IS NULL OR ${WtPct} < 0 OR ${WtPct} > 100)',
     'Stream :STREAM_NAME component :COMPONENT_NO has invalid or missing Wt% value for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1143, 'WtPct', 'ATTRIBUTE', 'WT_PCT');


-- =============================================================================
-- PART 3: STRM_ANALYSIS - DENSITY (6 tags)
-- Rule: DENSITY must not be NULL or <= 0
-- Affected streams: HP Fuel Gas to 1KT1410/1430, MP Fuel Gas to GT4001-GT4004
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1144, 'PHD_STRM_ANALYSIS_DENSITY_VAL1', 'Count(*)',
     'RV_STRM_ANALYSIS', 'N',
     '(${Density} IS NULL OR ${Density} <= 0)',
     'Stream :STREAM_NAME has invalid or missing Density value for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1144, 'Density', 'ATTRIBUTE', 'DENSITY');


-- =============================================================================
-- PART 4: STRM_ANALYSIS - GCV (9 tags)
-- Rule: GCV must not be NULL or <= 0
-- Affected streams: HP/MP Fuel Gas to GT4001-4004, 1KT1410/1430, Flare Pilots
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1145, 'PHD_STRM_ANALYSIS_GCV_VAL1', 'Count(*)',
     'RV_STRM_ANALYSIS', 'N',
     '(${Gcv} IS NULL OR ${Gcv} <= 0)',
     'Stream :STREAM_NAME has invalid or missing GCV value for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1145, 'Gcv', 'ATTRIBUTE', 'GCV_MJPERSM3');


-- =============================================================================
-- PART 5: TANK_DAY_DIP_STATUS - GRS_VOL (5 tags)
-- Rule: GRS_VOL must not be NULL or < 0
-- Affected tanks: LNG T3101/T3102, Condensate T3301/T3302/T3303
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1146, 'PHD_TANK_DIP_GRS_VOL_VAL1', 'Count(*)',
     'RV_TANK_DAY_DIP_STATUS', 'N',
     '(${GrsVol} IS NULL OR ${GrsVol} < 0)',
     'Tank :TANK_NAME has invalid or missing Gross Volume for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1146, 'GrsVol', 'ATTRIBUTE', 'GRS_VOL_SM3');


-- =============================================================================
-- PART 6: TANK_DAY_DIP_STATUS - ZWP_GRS_MASS (2 tags)
-- Rule: ZWP_GRS_MASS must not be NULL or < 0
-- Affected tanks: LNG Tank 3101, LNG Tank 3102
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1147, 'PHD_TANK_DIP_GRS_MASS_VAL1', 'Count(*)',
     'RV_TANK_DAY_DIP_STATUS', 'N',
     '(${GrsMass} IS NULL OR ${GrsMass} < 0)',
     'Tank :TANK_NAME has invalid or missing Gross Mass for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1147, 'GrsMass', 'ATTRIBUTE', 'ZWP_GRS_MASS_TONNES');


-- =============================================================================
-- PART 7: TANK_DAY_DIP_STATUS - AVG_TEMP (5 tags)
-- Rule: AVG_TEMP must not be NULL
-- Affected tanks: LNG T3101/T3102, Condensate T3301/T3302/T3303
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1148, 'PHD_TANK_DIP_AVG_TEMP_VAL1', 'Count(*)',
     'RV_TANK_DAY_DIP_STATUS', 'N',
     '(${AvgTemp} IS NULL)',
     'Tank :TANK_NAME has missing Average Temperature for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1148, 'AvgTemp', 'ATTRIBUTE', 'AVG_TEMP_C');


-- =============================================================================
-- PART 8: TANK_DAY_DIP_STATUS - MEAS_STD_DENSITY (2 tags)
-- Rule: MEAS_STD_DENSITY must not be NULL or <= 0
-- Affected tanks: LNG Tank 3101, LNG Tank 3102
-- =============================================================================

INSERT INTO TV_CTRL_CHECK_RULES
    (TABLE_CLASS_NAME, CHECK_ID, CHECK_NAME, SELECT_CLAUSE, TABLE_ID,
     CLASS_OBJ_VALIDATION_IND, WHERE_FORMULA, CHECK_MESSAGE, SEVERITY_LEVEL)
VALUES
    ('CTRL_CHECK_RULES', 1149, 'PHD_TANK_DIP_STD_DENSITY_VAL1', 'Count(*)',
     'RV_TANK_DAY_DIP_STATUS', 'N',
     '(${StdDensity} IS NULL OR ${StdDensity} <= 0)',
     'Tank :TANK_NAME has invalid or missing Standard Density for :DAYTIME',
     'ERROR');

INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE
    (TABLE_CLASS_NAME, CHECK_ID, VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE)
VALUES
    ('CTRL_CHECK_RULE_VARIABLE', 1149, 'StdDensity', 'ATTRIBUTE', 'MEAS_STD_DENSITY_KGPERSM3');


-- =============================================================================
-- SUMMARY
-- Total new rules: 8 (CHECK_ID 1142 to 1149)
-- Total PHD tags covered: 131
--
-- NOT included (requires separate ECPR):
--   - Sum check 98-102% for MOL_PCT + WT_PCT (needs custom SQL function)
--   - Frozen value check (needs ZWP_P_VALIDATION function reference)
--   - ZWT_OILINWAT check (separate ECPR-F)
-- =============================================================================
