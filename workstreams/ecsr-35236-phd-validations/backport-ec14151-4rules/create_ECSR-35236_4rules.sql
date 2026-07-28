-- =====================================================================================================
-- CREATE 4 PHD/Missing-Data check rules (ECSR-35236) + their variables + check-group links.
-- Governed source for rules that were hand-inserted on ec14151 (2026-07-21) outside version control.
--   1147 PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY  (RV_STRM_DAY_STREAM_MEAS_GAS)  -> group V_PHD_STREAM_GAS
--   1148 PHD_STREAM_GAS_MEAS_VAL_GCV          (RV_STRM_DAY_STREAM_MEAS_GAS)  -> group V_PHD_STREAM_GAS
--   1149 MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS (RV_TANK_DAY_DIP_STATUS) -> group V_MD_TANK_DAY_INV_OIL
--   1150 MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS  (RV_TANK_DAY_DIP_STATUS) -> group V_MD_TANK_DAY_INV_OIL
-- Style: TV_ views, target by CHECK_NAME (CHECK_ID is env-local, resolved at runtime), update-insert
--        (UPDATE; IF SQL%ROWCOUNT=0 THEN INSERT), REV_TEXT on every DML, no MERGE, no exception, no COMMIT.
-- STATUS: VERIFIED 2026-07-27 on LOCAL sandbox (localhost:1521/ORCL) via ROLLBACK dry-run - nothing persisted:
--   CREATE -> 4 rules + 12 variables + 4 combination links; re-run -> identical counts (IDEMPOTENT);
--   matching delete_*.sql -> 0/0/0 (re-runnable teardown); rollback -> 0 residual.
--   Resolved: (a) the IUD_CTRL_CHECK_RULES trigger requires CHECK_ID on INSERT (raises ORA-20103 if null) and
--   there is NO sequence -> supply check_id = (SELECT NVL(MAX(check_id),0)+1 FROM ctrl_check_rules); env-portable.
--   (b) TABLE_ID accepts the class NAME ('RV_...') on INSERT (trigger accepted it). (c) the combination FK needs
--   the parent groups V_PHD_STREAM_GAS / V_MD_TANK_DAY_INV_OIL to pre-exist (they do on the target Woodside env;
--   for the local dry-run they were synthesized in-txn then rolled back).
--   NOTE: a true-env rollback dry-run on ec14151/plutodev is a WRITE to Woodside ECaaS -> needs Simon/Mayyin
--   approval before running there (not done from here).
-- =====================================================================================================
DECLARE
  lv_rev VARCHAR2(20) := 'ECSR-35236';
BEGIN

  -- ============================ RULE 1: PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY ============================
  UPDATE tv_ctrl_check_rules
     SET table_id = 'RV_STRM_DAY_STREAM_MEAS_GAS', select_clause = 'Count(*)', severity_level = 'ERROR',
         check_message = 'Stream :STREAM_NAME has negative or missing standard density',
         class_obj_validation_ind = 'N',
         where_formula = '((${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensityMethod} = ${ConstCOMP_ANALYSIS})',
         rev_text = lv_rev
   WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rules
      (check_id, check_name, table_id, select_clause, severity_level, check_message, class_obj_validation_ind, where_formula, rev_text)
    VALUES ((SELECT NVL(MAX(check_id),0)+1 FROM ctrl_check_rules), 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY', 'RV_STRM_DAY_STREAM_MEAS_GAS', 'Count(*)', 'ERROR',
            'Stream :STREAM_NAME has negative or missing standard density', 'N',
            '((${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensityMethod} = ${ConstCOMP_ANALYSIS})', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'MEAS_STD_DENSITY_KGPERSM3', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY') AND variable_name = 'StdDensity';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY'), 'StdDensity', 'ATTRIBUTE', 'MEAS_STD_DENSITY_KGPERSM3', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'STD_DENSITY_METHOD', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY') AND variable_name = 'StdDensityMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY'), 'StdDensityMethod', 'ATTRIBUTE', 'STD_DENSITY_METHOD', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'CONST_STRING', variable_value = 'COMP_ANALYSIS', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY') AND variable_name = 'ConstCOMP_ANALYSIS';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY'), 'ConstCOMP_ANALYSIS', 'CONST_STRING', 'COMP_ANALYSIS', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_combination SET check_group_description = 'Daily Stream Gas Status - PHD Validations', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY') AND check_group = 'V_PHD_STREAM_GAS';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_combination (table_class_name, check_id, check_group, check_group_description, rev_text)
    VALUES ('CTRL_CHECK_COMBINATION', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY'), 'V_PHD_STREAM_GAS', 'Daily Stream Gas Status - PHD Validations', lv_rev);
  END IF;

  -- ============================ RULE 2: PHD_STREAM_GAS_MEAS_VAL_GCV ============================
  UPDATE tv_ctrl_check_rules
     SET table_id = 'RV_STRM_DAY_STREAM_MEAS_GAS', select_clause = 'Count(*)', severity_level = 'ERROR',
         check_message = 'Stream :STREAM_NAME has negative or missing GCV', class_obj_validation_ind = 'N',
         where_formula = '((${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP_ANALYSIS})', rev_text = lv_rev
   WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rules
      (check_id, check_name, table_id, select_clause, severity_level, check_message, class_obj_validation_ind, where_formula, rev_text)
    VALUES ((SELECT NVL(MAX(check_id),0)+1 FROM ctrl_check_rules), 'PHD_STREAM_GAS_MEAS_VAL_GCV', 'RV_STRM_DAY_STREAM_MEAS_GAS', 'Count(*)', 'ERROR',
            'Stream :STREAM_NAME has negative or missing GCV', 'N',
            '((${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP_ANALYSIS})', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'GCV_GJ', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV') AND variable_name = 'Gcv';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV'), 'Gcv', 'ATTRIBUTE', 'GCV_GJ', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'GCV_METHOD', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV') AND variable_name = 'GcvMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV'), 'GcvMethod', 'ATTRIBUTE', 'GCV_METHOD', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'CONST_STRING', variable_value = 'COMP_ANALYSIS', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV') AND variable_name = 'ConstCOMP_ANALYSIS';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV'), 'ConstCOMP_ANALYSIS', 'CONST_STRING', 'COMP_ANALYSIS', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_combination SET check_group_description = 'Daily Stream Gas Status - PHD Validations', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV') AND check_group = 'V_PHD_STREAM_GAS';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_combination (table_class_name, check_id, check_group, check_group_description, rev_text)
    VALUES ('CTRL_CHECK_COMBINATION', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STREAM_GAS_MEAS_VAL_GCV'), 'V_PHD_STREAM_GAS', 'Daily Stream Gas Status - PHD Validations', lv_rev);
  END IF;

  -- ============================ RULE 3: MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS ============================
  UPDATE tv_ctrl_check_rules
     SET table_id = 'RV_TANK_DAY_DIP_STATUS', select_clause = 'Count(*)', severity_level = 'ERROR',
         check_message = 'Tank :OBJECT_CODE has negative or missing gross mass', class_obj_validation_ind = 'N',
         where_formula = '((${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED})', rev_text = lv_rev
   WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rules
      (check_id, check_name, table_id, select_clause, severity_level, check_message, class_obj_validation_ind, where_formula, rev_text)
    VALUES ((SELECT NVL(MAX(check_id),0)+1 FROM ctrl_check_rules), 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS', 'RV_TANK_DAY_DIP_STATUS', 'Count(*)', 'ERROR',
            'Tank :OBJECT_CODE has negative or missing gross mass', 'N',
            '((${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED})', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'ZWP_GRS_MASS_TONNES', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS') AND variable_name = 'GrsMass';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS'), 'GrsMass', 'ATTRIBUTE', 'ZWP_GRS_MASS_TONNES', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'GRS_MASS_METHOD', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS') AND variable_name = 'GrsMassMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS'), 'GrsMassMethod', 'ATTRIBUTE', 'GRS_MASS_METHOD', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'CONST_STRING', variable_value = 'MEASURED', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS') AND variable_name = 'ConstMEASURED';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS'), 'ConstMEASURED', 'CONST_STRING', 'MEASURED', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_combination SET check_group_description = 'Daily Tank Status - Missing Data Validation', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS') AND check_group = 'V_MD_TANK_DAY_INV_OIL';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_combination (table_class_name, check_id, check_group, check_group_description, rev_text)
    VALUES ('CTRL_CHECK_COMBINATION', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS'), 'V_MD_TANK_DAY_INV_OIL', 'Daily Tank Status - Missing Data Validation', lv_rev);
  END IF;

  -- ============================ RULE 4: MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS ============================
  UPDATE tv_ctrl_check_rules
     SET table_id = 'RV_TANK_DAY_DIP_STATUS', select_clause = 'Count(*)', severity_level = 'ERROR',
         check_message = 'Tank :OBJECT_CODE has negative or missing standard density', class_obj_validation_ind = 'N',
         where_formula = '((${StdDens} IS NULL OR ${StdDens} < 0) and ${StdDensMethod} = ${ConstMEASURED})', rev_text = lv_rev
   WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rules
      (check_id, check_name, table_id, select_clause, severity_level, check_message, class_obj_validation_ind, where_formula, rev_text)
    VALUES ((SELECT NVL(MAX(check_id),0)+1 FROM ctrl_check_rules), 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS', 'RV_TANK_DAY_DIP_STATUS', 'Count(*)', 'ERROR',
            'Tank :OBJECT_CODE has negative or missing standard density', 'N',
            '((${StdDens} IS NULL OR ${StdDens} < 0) and ${StdDensMethod} = ${ConstMEASURED})', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'STD_DENS_SG', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS') AND variable_name = 'StdDens';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS'), 'StdDens', 'ATTRIBUTE', 'STD_DENS_SG', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'ATTRIBUTE', variable_value = 'STD_DENS_METHOD', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS') AND variable_name = 'StdDensMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS'), 'StdDensMethod', 'ATTRIBUTE', 'STD_DENS_METHOD', lv_rev);
  END IF;
  UPDATE tv_ctrl_check_rule_variable SET variable_type = 'CONST_STRING', variable_value = 'MEASURED', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS') AND variable_name = 'ConstMEASURED';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS'), 'ConstMEASURED', 'CONST_STRING', 'MEASURED', lv_rev);
  END IF;

  UPDATE tv_ctrl_check_combination SET check_group_description = 'Daily Tank Status - Missing Data Validation', rev_text = lv_rev
   WHERE check_id = (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS') AND check_group = 'V_MD_TANK_DAY_INV_OIL';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_combination (table_class_name, check_id, check_group, check_group_description, rev_text)
    VALUES ('CTRL_CHECK_COMBINATION', (SELECT check_id FROM ctrl_check_rules WHERE check_name = 'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS'), 'V_MD_TANK_DAY_INV_OIL', 'Daily Tank Status - Missing Data Validation', lv_rev);
  END IF;

END;
/
