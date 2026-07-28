-- =====================================================================================================
-- TEARDOWN the 4 ECSR-35236 back-port check rules (reverse of create_ECSR-35236_4rules.sql).
-- Child-first: combination links -> rule variables -> the rules. Target by CHECK_NAME. Re-runnable
-- (no-op if already absent). No exception, no COMMIT. Removes ONLY these 4 rules; touches nothing else.
--   PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY, PHD_STREAM_GAS_MEAS_VAL_GCV,
--   MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS, MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS
-- NOTE: leaves the parent groups (V_PHD_STREAM_GAS / V_MD_TANK_DAY_INV_OIL) intact - they are standard
--       pre-existing groups, not created by this back-port.
-- STATUS: VERIFIED 2026-07-27 on local sandbox (rollback dry-run: create -> delete -> 0 residual).
-- =====================================================================================================
DECLARE
  lv_rev VARCHAR2(20) := 'ECSR-35236';
BEGIN
  -- child 1: group combination links (delete by rule linkage, both groups)
  DELETE FROM tv_ctrl_check_combination
   WHERE check_id IN (SELECT check_id FROM ctrl_check_rules
                       WHERE check_name IN ('PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV',
                                            'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS'));

  -- child 2: rule variables
  DELETE FROM tv_ctrl_check_rule_variable
   WHERE check_id IN (SELECT check_id FROM ctrl_check_rules
                       WHERE check_name IN ('PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV',
                                            'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS'));

  -- parent: the rules themselves
  DELETE FROM tv_ctrl_check_rules
   WHERE check_name IN ('PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV',
                        'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS');
END;
/
