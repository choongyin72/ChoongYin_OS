--ECSR-35236  (Issue_1052) Scope 8 PHD check rules by method / on-stream-hours
-- Melanie Murray (2026-06-23): add a criterion to each rule's WHERE_FORMULA so it only fires when the
-- value should be present (method = MEASURED / COMP_ANALYSIS) or the well is on stream (ON_STREAM_HRS > 0),
-- stopping the false-positive PHD validations on the tags added since 1 Dec 2025.
-- Mirrors live rule PHD_STREAM_LIQUID_MEAS_VAL2: a method ATTRIBUTE variable + a CONST_STRING variable,
-- combined as ${Method} = ${Const} (PWEL rules use a literal ON_STREAM_HRS > 0).
-- Idempotent update-insert; target by CHECK_NAME (CHECK_ID is env-local); REV_TEXT = ECSR-35236 on every DML.
-- Verified on COPSDEV/plutodev (apply 8/8, re-run idempotent, rollback 8/8 restored).
-- NOTE: the Flyway version/timestamp in the filename is a placeholder for our system; the team sets the
-- final 1.0.x.0020.<ts> name + folder at delivery into Pluto_Config/020_Configuration.
DECLARE
  lv_rev_text VARCHAR2(10) := 'ECSR-35236';
  lv_check_id NUMBER;
BEGIN

  --1) Tank gross mass: validate only when GRS_MASS_METHOD = MEASURED
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_TANK_DIP_GRS_MASS_VAL1';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'GRS_MASS_METHOD', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'GrsMassMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'GrsMassMethod', 'ATTRIBUTE', 'GRS_MASS_METHOD', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'CONST_STRING', variable_value = 'MEASURED', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'ConstMEASURED';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'ConstMEASURED', 'CONST_STRING', 'MEASURED', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED}',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --2) Tank standard density: validate only when STD_DENS_METHOD = MEASURED
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_TANK_DIP_STD_DENSITY_VAL1';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'STD_DENS_METHOD', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'StdDensMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'StdDensMethod', 'ATTRIBUTE', 'STD_DENS_METHOD', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'CONST_STRING', variable_value = 'MEASURED', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'ConstMEASURED';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'ConstMEASURED', 'CONST_STRING', 'MEASURED', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensMethod} = ${ConstMEASURED}',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --3) Stream density: validate only when STD_DENSITY_METHOD = COMP_ANALYSIS
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STRM_ANALYSIS_DENSITY_VAL1';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'STD_DENSITY_METHOD', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'DensityMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'DensityMethod', 'ATTRIBUTE', 'STD_DENSITY_METHOD', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'CONST_STRING', variable_value = 'COMP_ANALYSIS', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'ConstCOMP';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'ConstCOMP', 'CONST_STRING', 'COMP_ANALYSIS', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${Density} IS NULL OR ${Density} < 0) and ${DensityMethod} = ${ConstCOMP}',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --4) Stream GCV: validate only when GCV_METHOD = COMP_ANALYSIS
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_STRM_ANALYSIS_GCV_VAL1';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'GCV_METHOD', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'GcvMethod';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'GcvMethod', 'ATTRIBUTE', 'GCV_METHOD', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'CONST_STRING', variable_value = 'COMP_ANALYSIS', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'ConstCOMP';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'ConstCOMP', 'CONST_STRING', 'COMP_ANALYSIS', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP}',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --5) PWEL bottom-hole temperature: validate only when ON_STREAM_HRS > 0
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_PWEL_STATUS_NODATA_BHTEMP';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'ON_STREAM_HRS_HRS', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'OnStrmHrs';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0) and ${OnStrmHrs} > 0',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --6) PWEL well-head temperature: validate only when ON_STREAM_HRS > 0
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_PWEL_STATUS_NODATA_WHTEMP';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'ON_STREAM_HRS_HRS', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'OnStrmHrs';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0) and ${OnStrmHrs} > 0',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --7) PWEL bottom-hole pressure: validate only when ON_STREAM_HRS > 0
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_PWEL_STATUS_NODATA_BHPRESS';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'ON_STREAM_HRS_HRS', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'OnStrmHrs';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0) and ${OnStrmHrs} > 0',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

  --8) PWEL well-head pressure: validate only when ON_STREAM_HRS > 0
  SELECT check_id INTO lv_check_id FROM ctrl_check_rules WHERE check_name = 'PHD_PWEL_STATUS_NODATA_WHPRESS';
  UPDATE tv_ctrl_check_rule_variable
     SET variable_type = 'ATTRIBUTE', variable_value = 'ON_STREAM_HRS_HRS', rev_text = lv_rev_text
   WHERE check_id = lv_check_id AND variable_name = 'OnStrmHrs';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO tv_ctrl_check_rule_variable
      (table_class_name, check_id, variable_name, variable_type, variable_value, rev_text)
    VALUES ('CTRL_CHECK_RULE_VARIABLE', lv_check_id, 'OnStrmHrs', 'ATTRIBUTE', 'ON_STREAM_HRS_HRS', lv_rev_text);
  END IF;
  UPDATE tv_ctrl_check_rules
     SET where_formula = '(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0) and ${OnStrmHrs} > 0',
         rev_text = lv_rev_text
   WHERE check_id = lv_check_id;

END;
/
