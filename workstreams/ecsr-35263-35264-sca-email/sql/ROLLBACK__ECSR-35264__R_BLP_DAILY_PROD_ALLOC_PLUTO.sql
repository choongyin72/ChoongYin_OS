-- ROLLBACK for the ECSR-35264 R_BLP_DAILY_PROD_ALLOC_PLUTO forward script.
-- Restores the COPSDEV/plutodev baseline captured 2026-06-23 (verified original values).
-- Idempotent + safe to re-run. As verified, the failed forward run committed NOTHING
-- (0 rows REV_TEXT='ECSR-35264'); this is the safety net to guarantee the original state.
-- The deployer/Flyway controls COMMIT (no COMMIT here, matching the forward-script convention).
DECLARE
BEGIN
  -- 1) remove any NEW '*_PLU'-coded objects a partial run could have inserted (none currently)
  DELETE FROM OV_MESSAGE_CONTACT WHERE CODE IN
    ('DMS_R_BLP_DAILY_PROD_ALLOC_PLU','INT_R_BLP_DAILY_PROD_ALLOC_PLU','INT_R_BLP_DAILY_PROD_ALLOC_PLU 1',
     'EXT_R_BLP_DAILY_PROD_ALLOC_PLU','EXT_R_BLP_DAILY_PROD_ALLOC_PLU_1','EXT_R_BLP_DAILY_PROD_ALLOC_PLU_2');
  DELETE FROM OV_CONTACT_GROUP WHERE CODE='R_BLP_DAILY_ALLOC_PLU';

  -- 2) restore ORIGINAL names + links on the existing (original-code) objects
  UPDATE OV_CONTACT_GROUP_SET
     SET NAME='Burrup LNG Park Daily Production Report'
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_PLU';

  UPDATE OV_CONTACT_GROUP
     SET NAME='PHBR-R_BLP_DAIY_PROD_ALLOC_PLU', CONTACT_GROUP_SET_CODE='R_BLP_DAILY_PROD_ALLOC_PLU'
   WHERE CODE='R_BLP_DAILY_ALLOC';

  UPDATE OV_MESSAGE_CONTACT SET NAME='Default mail sender - R_BLP_DAILY_PROD_ALLOC',
         CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC' WHERE CODE='DMS_R_BLP_DAILY_PROD_ALLOC';
  UPDATE OV_MESSAGE_CONTACT SET NAME='Internal-Burrup LNG Park Daily Production Report',
         CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC' WHERE CODE='INT_R_BLP_DAILY_PROD_ALLOC';
  UPDATE OV_MESSAGE_CONTACT SET NAME='Internal-Burrup LNG Park Daily Production Report 1',
         CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC' WHERE CODE='INT_R_BLP_DAILY_PROD_ALLOC 1';
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report',
         CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC' WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC';
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report 1',
         CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC' WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC_1';
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report 2',
         CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC' WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC_2';

  UPDATE OV_MESSAGE_DEFINITION
     SET COMPANY_CONTACT_CODE='DMS_R_BLP_DAILY_PROD_ALLOC',
         MESSAGE_SUBJECT='Burrup LNG Park Daily Allocation Statement for Production Date'
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO';

  -- distribution recipients reference the ORIGINAL contact codes -> restore if they were repointed
  UPDATE TV_DISTRIBUTION_SET_CONTACT SET COMPANY_CONTACT_CODE='INT_R_BLP_DAILY_PROD_ALLOC'
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC' AND RECIPIENT_TYPE='CC';
  -- (FROM=DMS_..., TO=EXT_..., TO='INT_... 1' codes are unchanged from baseline)
END;
/
