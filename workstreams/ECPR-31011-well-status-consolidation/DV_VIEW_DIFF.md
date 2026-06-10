# DV_PWEL_DAY_STATUS vs DV_PWEL_DAY_STATUS_2 — full attribute diff
Generated read-only from plutodev on 2026-06-10 (script: dv_view_diff.py).

Totals: DV_1 = 107 cols | DV_2 = 60 cols | shared = 48 |
only DV_1 = 59 | only DV_2 = 12 |
shared-but-different-expression = 3

## 1. ONLY in DV_PWEL_DAY_STATUS_2 (must be added to class 1) — 12

| # | Column | Type | Source | Expression |
|---|--------|------|--------|------------|
| 1 | AVG_FLOW_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_FLOW_RATE` |
| 2 | AVG_MPM_GAS_MASS_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_MPM_GAS_MASS_RATE` |
| 3 | AVG_MPM_GAS_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_MPM_GAS_RATE` |
| 4 | DRIVE_CURRENT | NUMBER | BASE | `PWEL_DAY_STATUS.DRIVE_CURRENT` |
| 5 | DRIVE_FREQUENCY | NUMBER | BASE | `PWEL_DAY_STATUS.DRIVE_FREQUENCY` |
| 6 | PUMP_DISCHARGE_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.PUMP_DISCHARGE_PRESS` |
| 7 | PUMP_PRESSURE | NUMBER | BASE | `PWEL_DAY_STATUS.PUMP_PRESSURE` |
| 8 | ZWP_ALLOC_GAS_ENERGY | NUMBER | BASE | `pwelDayAlloc.alloc_gas_energy` |
| 9 | ZWP_MEAS_EV_RATIO | NUMBER | FUNCTION | `CASE WHEN nvl(pwelDayAlloc.alloc_gas_vol,0)>0 THEN (pwelDayAlloc.alloc_gas_energy/pwelDayA…` |
| 10 | ZWP_MEAS_GAS_ENERGY | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GAS_ENERGY` |
| 11 | ZWP_MEAS_MV_RATIO | NUMBER | FUNCTION | `CASE WHEN nvl(pwelDayAlloc.alloc_gas_vol,0)>0 THEN (pwelDayAlloc.alloc_gas_mass/pwelDayAll…` |
| 12 | ZWP_THEOR_GAS_ENERGY | NUMBER | FUNCTION | `EcBp_Well_Theoretical.getGasEnergyDay(pwel_day_status.object_id, pwel_day_status.daytime)` |

## 2. ONLY in DV_PWEL_DAY_STATUS — 59

| # | Column | Type | Source | Expression |
|---|--------|------|--------|------------|
| 1 | AC_FREQUENCY | NUMBER | BASE | `PWEL_DAY_STATUS.AC_FREQUENCY` |
| 2 | ALLOC_COND_FACTOR | NUMBER | OTHER | `pwelDayAlloc.cond_vol_factor` |
| 3 | ALLOC_COND_MASS | NUMBER | OTHER | `pwelDayAlloc.alloc_cond_mass` |
| 4 | ALLOC_COND_VOL | NUMBER | OTHER | `pwelDayAlloc.alloc_cond_vol` |
| 5 | ALLOC_GAS_ENERGY | NUMBER | BASE | `pwelDayAlloc.alloc_gas_energy` |
| 6 | ALLOC_GAS_FACTOR | NUMBER | OTHER | `pwelDayAlloc.gas_vol_factor` |
| 7 | ALLOC_GL_VOL | NUMBER | OTHER | `pwelDayAlloc.alloc_gl_vol` |
| 8 | ALLOC_OIL_FACTOR | NUMBER | OTHER | `pwelDayAlloc.net_oil_vol_factor` |
| 9 | ALLOC_OIL_VOL | NUMBER | OTHER | `pwelDayAlloc.alloc_net_oil_vol` |
| 10 | ALLOC_WATER_FACTOR | NUMBER | OTHER | `pwelDayAlloc.water_vol_factor` |
| 11 | ALLOC_WATER_VOL | NUMBER | OTHER | `pwelDayAlloc.alloc_water_vol` |
| 12 | ANNULUS_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.ANNULUS_PRESS` |
| 13 | ANNULUS_PRESS_2 | NUMBER | BASE | `PWEL_DAY_STATUS.ANNULUS_PRESS_2` |
| 14 | AVG_BH_PRESS_2 | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_BH_PRESS_2` |
| 15 | AVG_BH_TEMP_2 | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_BH_TEMP_2` |
| 16 | AVG_COND_MASS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_COND_MASS` |
| 17 | AVG_DH_PUMP_POWER | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_DH_PUMP_POWER` |
| 18 | AVG_DH_PUMP_SPEED | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_DH_PUMP_SPEED` |
| 19 | AVG_FLOW_MASS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_FLOW_MASS` |
| 20 | AVG_GAS_ENERGY | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GAS_ENERGY` |
| 21 | AVG_GAS_GCV | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GAS_GCV` |
| 22 | AVG_GL_CHOKE_SIZE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GL_CHOKE` |
| 23 | AVG_GL_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GL_RATE` |
| 24 | AVG_LIQ_VOL | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_LIQUID_RATE_M3` |
| 25 | AVG_MPM_DIFF_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_MPM_DIFF_PRESS` |
| 26 | AVG_OIL_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_OIL_RATE` |
| 27 | AVG_WATER_MASS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WATER_MASS` |
| 28 | AVG_WATER_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WATER_RATE` |
| 29 | AVG_WH_DSC_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WH_DSC_PRESS` |
| 30 | AVG_WH_DSC_TEMP | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WH_DSC_TEMP` |
| 31 | AVG_WH_USC_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WH_USC_PRESS` |
| 32 | BS_W | NUMBER | BASE | `PWEL_DAY_STATUS.BS_W` |
| 33 | CALC_ON_STREAM_HRS | NUMBER | FUNCTION | `EcDp_Well.getPwelOnStreamHrs(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 34 | FLOWLINE | VARCHAR2(4000) | FUNCTION | `EcDp_Flowline_Sub_Well_Conn.FlowlinesForWellProdDay(pwel_day_status.object_id,pwel_day_sta…` |
| 35 | INTAKE_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.INTAKE_PRESS` |
| 36 | INTAKE_TEMP | NUMBER | BASE | `PWEL_DAY_STATUS.INTAKE_TEMP` |
| 37 | MPM_GOR | NUMBER | FUNCTION | `DECODE( pwel_day_status.AVG_MPM_OIL_RATE , 0, to_number(null), pwel_day_status.AVG_MPM_GAS…` |
| 38 | MPM_HC_MASS_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.MPM_HC_MASS_RATE` |
| 39 | MPM_TOT_MASS_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.MPM_TOT_MASS_RATE` |
| 40 | OUTLET_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.OUTLET_PRESS` |
| 41 | OUTLET_TEMP | NUMBER | BASE | `PWEL_DAY_STATUS.OUTLET_TEMP` |
| 42 | PHASE_CURRENT | NUMBER | BASE | `PWEL_DAY_STATUS.PHASE_CURRENT` |
| 43 | PHASE_VOLTAGE | NUMBER | BASE | `PWEL_DAY_STATUS.PHASE_VOLTAGE` |
| 44 | SORT_ORDER | NUMBER | OTHER | `oa.sort_order` |
| 45 | THEOR_GAS_ENERGY | NUMBER | FUNCTION | `EcBp_Well_Theoretical.getGasEnergyDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 46 | THEOR_OIL_VOL | NUMBER | FUNCTION | `EcBp_Well_Theoretical.getOilStdRateDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 47 | ZWP_ACTR_REF | VARCHAR2(2000) | EXT (ZWP_T) | `zwpTPwelDayStatus1.ZWP_ACTR_REF` |
| 48 | ZWP_ALLOC_HC_GAS_MASS | NUMBER | FUNCTION | `ec_zwp_pwel_day_alloc.zwp_alloc_hc_gas_mass(ec_pwel_day_alloc.rec_id(pwel_day_status.objec…` |
| 49 | ZWP_ALLOC_HC_GAS_VOL | NUMBER | FUNCTION | `ec_zwp_pwel_day_alloc.zwp_alloc_hc_gas_vol(ec_pwel_day_alloc.rec_id(pwel_day_status.object…` |
| 50 | ZWP_FLOWLINE_HR_A | NUMBER | FUNCTION | `zwp_prod_well_theoretical.getFlowlineConHrs(pwel_day_status.object_id,pwel_day_status.dayt…` |
| 51 | ZWP_FLOWLINE_HR_B | NUMBER | FUNCTION | `zwp_prod_well_theoretical.getFlowlineConHrs(pwel_day_status.object_id,pwel_day_status.dayt…` |
| 52 | ZWP_THEOR_COND_VOL | NUMBER | FUNCTION | `zwp_prod_well_theoretical.getCondStdRateDay(pwel_day_status.object_id, pwel_day_status.day…` |
| 53 | ZWP_THEOR_GAS_VOL | NUMBER | FUNCTION | `zwp_prod_well_theoretical.getGasStdRateDay(pwel_day_status.object_id, pwel_day_status.dayt…` |
| 54 | ZWP_THEOR_TOTAL_MASS | NUMBER | FUNCTION | `EcBp_Well_Theoretical.findGasMassDay(pwel_day_status.object_id, pwel_day_status.daytime)+E…` |
| 55 | ZWP_THEOR_TOTAL_VOL | NUMBER | FUNCTION | `zwp_prod_well_theoretical.getGasStdRateDay(pwel_day_status.object_id, pwel_day_status.dayt…` |
| 56 | ZWP_THEOR_WAT_VOL | NUMBER | FUNCTION | `EcBp_Well_Theoretical.findWaterMassDay(pwel_day_status.object_id, pwel_day_status.daytime)…` |
| 57 | ZWT_CALC_GCV | NUMBER | FUNCTION | `EcBp_Well_Theoretical.findGCV(PWEL_DAY_STATUS.object_id, PWEL_DAY_STATUS.daytime)` |
| 58 | ZWT_GOR | NUMBER | OTHER | `zwtPwelDayStatus3.ZWT_GOR` |
| 59 | ZWT_RESGAS_VOL | NUMBER | OTHER | `zwtPwelDayAlloc2.ZWT_RESGAS_VOL` |

## 3. SHARED but DIFFERENT source expression — 3

| # | Column | Type | Source | Expression |
|---|--------|------|--------|------------|
| 1 | CHOKE_UOM | VARCHAR2(4000) | FUNCTION | `ec_prosty_codes.code_text(OA.CHOKE_UOM,'CHOKE_UOM')`  ⚠ DV_2 differs: `ec_prosty_codes.code_text(ec_well_version.CHOKE_UOM(pwel_day_status.ob` |
| 2 | CLASS_NAME | CHAR(15) | OTHER | `-- Generated by ecdp_viewlayer 'PWEL_DAY_STATUS'`  ⚠ DV_2 differs: `-- Generated by ecdp_viewlayer 'PWEL_DAY_STATUS_2'` |
| 3 | WELL_STATUS | VARCHAR2(4000) | FUNCTION | `ec_prosty_codes.code_text(EcDp_Well.getWellStatus(pwel_day_status.object_id,pwel_day_statu…`  ⚠ DV_2 differs: `ec_prosty_codes.code_text(ec_well_period_status.well_status(pwel_day_s` |

## 4. SHARED, identical — 45

| # | Column | Type | Source | Expression |
|---|--------|------|--------|------------|
| 1 | ALLOC_GAS_MASS | NUMBER | OTHER | `pwelDayAlloc.alloc_gas_mass` |
| 2 | ALLOC_GAS_VOL | NUMBER | OTHER | `pwelDayAlloc.alloc_gas_vol` |
| 3 | APPROVAL_BY | VARCHAR2(256) | BASE | `PWEL_DAY_STATUS.APPROVAL_BY` |
| 4 | APPROVAL_DATE | DATE | BASE | `PWEL_DAY_STATUS.APPROVAL_DATE` |
| 5 | APPROVAL_STATE | VARCHAR2(1) | BASE | `PWEL_DAY_STATUS.APPROVAL_STATE` |
| 6 | AVG_BH_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_BH_PRESS` |
| 7 | AVG_BH_TEMP | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_BH_TEMP` |
| 8 | AVG_CHOKE_SIZE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_CHOKE_SIZE` |
| 9 | AVG_GAS_MASS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GAS_MASS` |
| 10 | AVG_GAS_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GAS_RATE` |
| 11 | AVG_GL_MF_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GL_MF_PRESS` |
| 12 | AVG_GL_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_GL_PRESS` |
| 13 | AVG_WH_PRESS | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WH_PRESS` |
| 14 | AVG_WH_TEMP | NUMBER | BASE | `PWEL_DAY_STATUS.AVG_WH_TEMP` |
| 15 | CHOKE_MM | NUMBER | FUNCTION | `EcBp_Well_Choke.convertToMilliMeter(pwel_day_status.object_id, pwel_day_status.daytime, pw…` |
| 16 | CHOKE_PROD | VARCHAR2(4000) | FUNCTION | `ec_choke_version.name(ec_well_version.choke_id(pwel_day_status.object_id, pwel_day_status.…` |
| 17 | CHOKE_PROD_DATE | DATE | OTHER | `oa.choke_date` |
| 18 | COMMENTS | VARCHAR2(2000) | BASE | `PWEL_DAY_STATUS.COMMENTS` |
| 19 | CREATED_BY | VARCHAR2(256) | BASE | `PWEL_DAY_STATUS.CREATED_BY` |
| 20 | CREATED_DATE | DATE | BASE | `PWEL_DAY_STATUS.CREATED_DATE` |
| 21 | DATA_CLASS_NAME | VARCHAR2(100) | BASE | `PWEL_DAY_STATUS.DATA_CLASS_NAME` |
| 22 | DAYTIME | DATE | BASE | `PWEL_DAY_STATUS.DAYTIME` |
| 23 | ICON | VARCHAR2(4000) | FUNCTION | `EcBp_Data_Validation.getFaIcon()` |
| 24 | LAST_UPDATED_BY | VARCHAR2(256) | BASE | `PWEL_DAY_STATUS.LAST_UPDATED_BY` |
| 25 | LAST_UPDATED_DATE | DATE | BASE | `PWEL_DAY_STATUS.LAST_UPDATED_DATE` |
| 26 | MODE_ID | VARCHAR2(32) | BASE | `PWEL_DAY_STATUS.MODE_ID` |
| 27 | OBJECT_CODE | VARCHAR2(32) | OTHER | `o.OBJECT_CODE` |
| 28 | OBJECT_ID | VARCHAR2(32) | BASE | `PWEL_DAY_STATUS.OBJECT_ID` |
| 29 | ON_STREAM_HRS | NUMBER | FUNCTION | `EcDp_Well.getPwelOnStreamHrs(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 30 | OVERRIDE_THEOR_COND | NUMBER | BASE | `PWEL_DAY_STATUS.OVERRIDE_THEOR_COND` |
| 31 | OVERRIDE_THEOR_GAS | NUMBER | BASE | `PWEL_DAY_STATUS.OVERRIDE_THEOR_GAS` |
| 32 | OVERRIDE_THEOR_OIL | NUMBER | BASE | `PWEL_DAY_STATUS.OVERRIDE_THEOR_OIL` |
| 33 | OVERRIDE_THEOR_WAT | NUMBER | BASE | `PWEL_DAY_STATUS.OVERRIDE_THEOR_WAT` |
| 34 | RECORD_STATUS | VARCHAR2(1) | BASE | `PWEL_DAY_STATUS.RECORD_STATUS` |
| 35 | REC_ID | VARCHAR2(32) | BASE | `PWEL_DAY_STATUS.REC_ID` |
| 36 | REV_EVENT | NUMBER | OTHER | `etdc.EVENT_NO` |
| 37 | REV_NO | NUMBER | BASE | `PWEL_DAY_STATUS.REV_NO` |
| 38 | REV_TEXT | VARCHAR2(2000) | BASE | `PWEL_DAY_STATUS.REV_TEXT` |
| 39 | SCALE_INJ_RATE | NUMBER | BASE | `PWEL_DAY_STATUS.SCALE_INJ_RATE` |
| 40 | THEOR_COND_MASS | NUMBER | FUNCTION | `EcBp_Well_Theoretical.findCondMassDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 41 | THEOR_COND_VOL | NUMBER | FUNCTION | `EcBp_Well_Theoretical.getCondStdRateDay(pwel_day_status.object_id, pwel_day_status.daytime…` |
| 42 | THEOR_GAS_MASS | NUMBER | FUNCTION | `EcBp_Well_Theoretical.findGasMassDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 43 | THEOR_GAS_VOL | NUMBER | FUNCTION | `EcBp_Well_Theoretical.getGasStdRateDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 44 | THEOR_WATER_MASS | NUMBER | FUNCTION | `EcBp_Well_Theoretical.findWaterMassDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
| 45 | THEOR_WATER_VOL | NUMBER | FUNCTION | `EcBp_Well_Theoretical.getWatStdRateDay(pwel_day_status.object_id, pwel_day_status.daytime)` |
