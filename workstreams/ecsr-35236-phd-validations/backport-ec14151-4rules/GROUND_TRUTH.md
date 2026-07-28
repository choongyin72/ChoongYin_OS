# ECSR-35236 back-port: 4 ec14151 check rules -> idempotent upsert script (ground truth)

_Extracted READ-ONLY from ec14151 (`db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151`, ECKERNEL_EC),
2026-07-27. These 4 rules were hand-inserted directly on ec14151 on 2026-07-21 14:23 (REV_TEXT=ECSR-35236),
NOT in any repo. Task: author a governed idempotent update-insert script (+ teardown) so they have a source._

## Target-by-CHECK_NAME (CHECK_ID 1147-1150 are env-local; resolve at runtime). House style = the sibling
`../sql/V1.1.8.0030.0001__ECSR-35236__PHD_check_rule_method_scope.sql` (UPDATE; IF SQL%ROWCOUNT=0 INSERT; REV_TEXT).

## tv_ctrl_check_rules (4 NEW rules) — cols: CHECK_NAME, TABLE_ID, SELECT_CLAUSE='Count(*)', SEVERITY_LEVEL='ERROR', CHECK_MESSAGE, CLASS_OBJ_VALIDATION_IND='N', WHERE_FORMULA
| CHECK_NAME | TABLE_ID | WHERE_FORMULA | CHECK_MESSAGE |
|---|---|---|---|
| PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY | RV_STRM_DAY_STREAM_MEAS_GAS | `((${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensityMethod} = ${ConstCOMP_ANALYSIS})` | Stream :STREAM_NAME has negative or missing standard density |
| PHD_STREAM_GAS_MEAS_VAL_GCV | RV_STRM_DAY_STREAM_MEAS_GAS | `((${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP_ANALYSIS})` | Stream :STREAM_NAME has negative or missing GCV |
| MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS | RV_TANK_DAY_DIP_STATUS | `((${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED})` | Tank :OBJECT_CODE has negative or missing gross mass |
| MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS | RV_TANK_DAY_DIP_STATUS | `((${StdDens} IS NULL OR ${StdDens} < 0) and ${StdDensMethod} = ${ConstMEASURED})` | Tank :OBJECT_CODE has negative or missing standard density |

## tv_ctrl_check_rule_variable (12 rows; 3 per rule) — cols: TABLE_CLASS_NAME='CTRL_CHECK_RULE_VARIABLE', CHECK_ID(runtime), VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE
| Rule | VARIABLE_NAME | VARIABLE_TYPE | VARIABLE_VALUE |
|---|---|---|---|
| STD_DENSITY (1147) | StdDensity | ATTRIBUTE | MEAS_STD_DENSITY_KGPERSM3 |
| STD_DENSITY (1147) | StdDensityMethod | ATTRIBUTE | STD_DENSITY_METHOD |
| STD_DENSITY (1147) | ConstCOMP_ANALYSIS | CONST_STRING | COMP_ANALYSIS |
| GCV (1148) | Gcv | ATTRIBUTE | GCV_GJ |
| GCV (1148) | GcvMethod | ATTRIBUTE | GCV_METHOD |
| GCV (1148) | ConstCOMP_ANALYSIS | CONST_STRING | COMP_ANALYSIS |
| GRS_MASS (1149) | GrsMass | ATTRIBUTE | ZWP_GRS_MASS_TONNES |
| GRS_MASS (1149) | GrsMassMethod | ATTRIBUTE | GRS_MASS_METHOD |
| GRS_MASS (1149) | ConstMEASURED | CONST_STRING | MEASURED |
| STD_DENS (1150) | StdDens | ATTRIBUTE | STD_DENS_SG |
| STD_DENS (1150) | StdDensMethod | ATTRIBUTE | STD_DENS_METHOD |
| STD_DENS (1150) | ConstMEASURED | CONST_STRING | MEASURED |

## tv_ctrl_check_rule_subq_var: 0 rows (none). tv_ctrl_check_rule_func_p: 0 rows (none). -> script omits both.

## tv_ctrl_check_combination (4 rows) — cols: TABLE_CLASS_NAME='CTRL_CHECK_COMBINATION', CHECK_ID(runtime), CHECK_GROUP, CHECK_GROUP_DESCRIPTION
| Rule | CHECK_GROUP | CHECK_GROUP_DESCRIPTION |
|---|---|---|
| 1147, 1148 | V_PHD_STREAM_GAS | Daily Stream Gas Status - PHD Validations |
| 1149, 1150 | V_MD_TANK_DAY_INV_OIL | Daily Tank Status - Missing Data Validation |

## tv_ctrl_check_group: combination refs groups by NAME (V_PHD_STREAM_GAS, V_MD_TANK_DAY_INV_OIL) - these are
pre-existing standard groups (NOT created by the 21-Jul batch; their combination rows only LINK the new rules
into them). **TODO tomorrow (read-only):** confirm both groups already exist in tv_ctrl_check_group on the
target env; if yes, the script only upserts the 4 rules + 12 vars + 4 combination links (do NOT create groups).

## Build plan (tomorrow)
1. `create_ECSR-35236_4rules.sql`: per rule -> upsert tv_ctrl_check_rules (by CHECK_NAME) -> upsert its 3
   tv_ctrl_check_rule_variable (by CHECK_ID resolved + VARIABLE_NAME) -> upsert tv_ctrl_check_combination
   (by CHECK_ID + CHECK_GROUP). Flat blocks, REV_TEXT='ECSR-35236', no MERGE/exception/COMMIT.
2. `delete_ECSR-35236_4rules.sql`: child-first (combination -> variables -> rule), scoped by CHECK_NAME.
3. Verify idempotency (delete->create->create, counts identical) on a SAFE target (local sandbox if the RV_
   classes exist there, else request approved read/write). DO NOT run on Woodside without Simon/Mayyin approval.
4. Decide with owner: is the intent to REPRODUCE these (governed source) or to RECONCILE/REMOVE them as
   out-of-process duplicates of our PHD_STRM_ANALYSIS_*/PHD_TANK_DIP_* rules? (They are functional duplicates.)
