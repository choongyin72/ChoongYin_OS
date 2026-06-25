-- ECSR-35264 (Issue_1044B) - Burrup LNG Park Daily Production Report (PLUTO): dedicated '_PLU' message config.
-- Idempotent update-insert (REV_TEXT), mirroring precedent ECPR-31089 (R_PLU_NOPTA). REVIEW baseline; once
-- approved it is cloned to the Scarborough set (R_BLP_DAILY_PROD_ALLOC_SCA) so the two reports get SEPARATE
-- ACTOR Maintenance (Ruchi's ask).
--
-- DESIGN (why this runs clean): Oracle cannot UPDATE a CODE that child rows reference (no ON-UPDATE-CASCADE) ->
--   renaming the existing shared objects fails (ORA-02292). So this CREATES new, consistently-named '_PLU'
--   objects (group + contacts + distribution set) and RE-POINTS the R_BLP_DAILY_PROD_ALLOC_PLUTO message-def +
--   distribution connection to them. The OLD shared objects (R_BLP_DAILY_ALLOC / R_BLP_DAILY_PROD_ALLOC /
--   *_R_BLP_DAILY_PROD_ALLOC) are LEFT INTACT (referenced by historical messages -> not deleted here).
--   Optional later cleanup of the now-unused shared objects can follow once history dependence is checked.
-- RE-RUNNABLE (idempotent): every object is UPDATE-first, INSERT only if absent, keyed on its unique CODE
--   (or OBJECT_ID/OBJECT_CODE) -> re-running updates in place, never duplicates; REV_TEXT stamped on every
--   write; NO DELETE. Safe to run any number of times. The DV_MESSAGE_DISTRIBUTION row is single per OBJECT_CODE
--   so the SELECT ... INTO lv_msg_distr_no returns exactly one row on every run.
-- NOTE: final Flyway version/folder + REV_TEXT=<ECPR> set by the team at delivery into Pluto_Config.
DECLARE
  lv_rev_text     VARCHAR2(15) := 'ECSR-35264';
  lv_object_id    VARCHAR2(32);
  lv_msg_distr_no NUMBER;
BEGIN

  --(1) Contact Group Set (new code R_BLP_DAILY_PROD_ALLOC_PLUTO; normalise name to "(Pluto)")
  UPDATE OV_CONTACT_GROUP_SET
     SET NAME='Burrup LNG Park Daily Production Report (Pluto)', OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'), FUNCTIONAL_AREA_CODE='EC', REV_TEXT=lv_rev_text
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN
    INSERT INTO OV_CONTACT_GROUP_SET (CODE,NAME,OBJECT_START_DATE,DAYTIME,FUNCTIONAL_AREA_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_PLUTO','Burrup LNG Park Daily Production Report (Pluto)',
            TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'EC',lv_rev_text);
  END IF;

  --(2) NEW Contact Group 'R_BLP_DAILY_ALLOC_PLUTO' (created, not renamed) -> the set
  UPDATE OV_CONTACT_GROUP
     SET NAME='PHBR-R_BLP_DAIY_PROD_ALLOC_PLUTO', OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'), CONTACT_GROUP_SET_CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO'
   WHERE CODE='R_BLP_DAILY_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN
    INSERT INTO OV_CONTACT_GROUP (CODE,NAME,OBJECT_START_DATE,DAYTIME,CONTACT_GROUP_SET_CODE)
    VALUES ('R_BLP_DAILY_ALLOC_PLUTO','PHBR-R_BLP_DAIY_PROD_ALLOC_PLUTO',
            TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'R_BLP_DAILY_PROD_ALLOC_PLUTO');
  END IF;

  --(3) NEW '_PLUTO' message contacts (created) -> group R_BLP_DAILY_ALLOC_PLUTO. Same addresses as the Pluto set.
  --  FROM (sender)
  UPDATE OV_MESSAGE_CONTACT SET NAME='Default mail sender - R_BLP_DAILY_PROD_ALLOC_PLUTO',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='WBOperator'||chr(64)||'woodside.com.au',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='DMS_R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('DMS_R_BLP_DAILY_PROD_ALLOC_PLUTO','Default mail sender - R_BLP_DAILY_PROD_ALLOC_PLUTO',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'WBOperator'||chr(64)||'woodside.com.au','C_WDE','EC','R_BLP_DAILY_ALLOC_PLUTO',lv_rev_text); END IF;
  --  Internal (CC)
  UPDATE OV_MESSAGE_CONTACT SET NAME='Internal-Burrup LNG Park Daily Production Report (Pluto)',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='prodreporting'||chr(64)||'woodside.com',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='INT_R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('INT_R_BLP_DAILY_PROD_ALLOC_PLUTO','Internal-Burrup LNG Park Daily Production Report (Pluto)',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'prodreporting'||chr(64)||'woodside.com','C_WDE','EC','R_BLP_DAILY_ALLOC_PLUTO',lv_rev_text); END IF;
	   
  --  Internal (TO) - '_PLUTO 1'
  /**
  UPDATE OV_MESSAGE_CONTACT SET NAME='Internal-Burrup LNG Park Daily Production Report (Pluto) 1',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='PASReportPJVInternal'||chr(64)||'woodside.com',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='INT_R_BLP_DAILY_PROD_ALLOC_PLUTO 1';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('INT_R_BLP_DAILY_PROD_ALLOC_PLUTO 1','Internal-Burrup LNG Park Daily Production Report (Pluto) 1',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'PASReportPJVInternal'||chr(64)||'woodside.com','C_WDE','EC','R_BLP_DAILY_ALLOC_PLUTO',lv_rev_text); END IF;
  --  External (TO)
  **/
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report (Pluto)',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='PASReportPJV'||chr(64)||'woodside.com',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO','External-Burrup LNG Park Daily Production Report (Pluto)',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'PASReportPJV'||chr(64)||'woodside.com','C_WDE','EC','R_BLP_DAILY_ALLOC_PLUTO',lv_rev_text); END IF;
  /**	   
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report (Pluto) 1',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='pluto'||chr(64)||'kepha.au',
         COMPANY_CODE='C_KEPA',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO_1';

  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO_1','External-Burrup LNG Park Daily Production Report (Pluto) 1',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'pluto'||chr(64)||'kepha.au','C_KEPA','EC','R_BLP_DAILY_ALLOC_PLUTO',lv_rev_text); END IF;
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report (Pluto) 2',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='PlutoOperationsReport'||chr(64)||'midoceanenergy.com',
         COMPANY_CODE='C_MP',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO_2';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO_2','External-Burrup LNG Park Daily Production Report (Pluto) 2',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'PlutoOperationsReport'||chr(64)||'midoceanenergy.com','C_MP','EC','R_BLP_DAILY_ALLOC_PLUTO',lv_rev_text); END IF;
  **/
  
  --(4) Message Type -> RE-POINT COMPANY_CONTACT_CODE to the new '_PLUTO' sender
  UPDATE OV_MESSAGE_DEFINITION
     SET NAME='R_BLP_DAILY_PROD_ALLOC_PLUTO Message Definition',OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),
         OBJECT_END_DATE=NULL,DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),END_DATE=NULL,
         MESSAGE_SUBJECT='Burrup LNG Park Daily Allocation Statement for Production Date',MESSAGE_HANDLING='AUTO',
         MESSAGE_LOAD_JOB=NULL,MESSAGE_GENERATE_JOB=NULL,MESSAGE_VALIDATE_JOB=NULL,INTERNAL_FORMAT_TYPE='TEXT',
         DIRECTION='OUT',FREQUENCY='EVENT',XML_SCHEMA_URL=NULL,EXTERNAL_FORMAT='TEXT',FUNCTIONAL_AREA_CODE='EC',
         COMPANY_CONTACT_CODE='DMS_R_BLP_DAILY_PROD_ALLOC_PLUTO',REV_TEXT=lv_rev_text
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_DEFINITION
    (CODE,NAME,OBJECT_START_DATE,OBJECT_END_DATE,DAYTIME,END_DATE,MESSAGE_SUBJECT,MESSAGE_HANDLING,MESSAGE_LOAD_JOB,
     MESSAGE_GENERATE_JOB,MESSAGE_VALIDATE_JOB,INTERNAL_FORMAT_TYPE,DIRECTION,FREQUENCY,XML_SCHEMA_URL,EXTERNAL_FORMAT,
     FUNCTIONAL_AREA_CODE,COMPANY_CONTACT_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_PLUTO','R_BLP_DAILY_PROD_ALLOC_PLUTO Message Definition',
       TO_DATE('01/01/2000','DD/MM/YYYY'),NULL,TO_DATE('01/01/2000','DD/MM/YYYY'),NULL,
       'Burrup LNG Park Daily Allocation Statement for Production Date','AUTO',NULL,NULL,NULL,'TEXT','OUT','EVENT',
       NULL,'TEXT','EC','DMS_R_BLP_DAILY_PROD_ALLOC_PLUTO',lv_rev_text); END IF;

  --(5) Message Format (TEXT default)
  UPDATE DV_MESSAGE_FORMAT SET DEFAULT_EXT_FORMAT='Y',REV_TEXT=lv_rev_text
   WHERE OBJECT_CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO' AND FORMAT_CODE='TEXT';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO DV_MESSAGE_FORMAT (OBJECT_CODE,FORMAT_CODE,DEFAULT_EXT_FORMAT,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_PLUTO','TEXT','Y',lv_rev_text); END IF;

  --(6) Freetext Message Template (subject + body, {production_day})
  lv_object_id := ec_message_definition.object_id_by_uk('R_BLP_DAILY_PROD_ALLOC_PLUTO');
  UPDATE DV_MSG_FREE_TEXT_TEMPLATE
     SET SUBJECT='Burrup LNG Park Daily Production Report '||chr(123)||'production_day'||chr(125),
         TEMPLATE=to_clob('Hi,

Please find attached Burrup LNG Park Daily Production Report (Pluto) for Production Date - '||chr(123)||'production_day'||chr(125)||'.

Note this report is designed to meet the requirements of Burrup LNG Park Production Allocation Agreement (PAA) from the PAA Effective Date.

For any queries or issues please contact PlutoJVNotices'||chr(64)||'woodside.com.au.

Disclaimer - You are receiving this email as a designated recipient for the above-listed Report Type. If you no longer wish to receive these emails, please contact the Production '||chr(38)||' Emission Allocation Team - Australian Business.

Regards,
Prod Reporting
Production '||chr(38)||' Emission Allocation Team


'||chr(91)||'This notification is automatically generated by Pluto Hub ECaaS.'||chr(93)),
         REV_TEXT=lv_rev_text
   WHERE OBJECT_ID=lv_object_id;
  IF SQL%ROWCOUNT=0 THEN INSERT INTO DV_MSG_FREE_TEXT_TEMPLATE (OBJECT_ID,SUBJECT,TEMPLATE,REV_TEXT)
    VALUES (lv_object_id,'Burrup LNG Park Daily Production Report '||chr(123)||'production_day'||chr(125),
       to_clob('Hi,

Please find attached Burrup LNG Park Daily Production Report (Pluto) for Production Date - '||chr(123)||'production_day'||chr(125)||'.

Note this report is designed to meet the requirements of Burrup LNG Park Production Allocation Agreement (PAA) from the PAA Effective Date.

For any queries or issues please contact PlutoJVNotices'||chr(64)||'woodside.com.au.

Disclaimer - You are receiving this email as a designated recipient for the above-listed Report Type. If you no longer wish to receive these emails, please contact the Production '||chr(38)||' Emission Allocation Team - Australian Business.

Regards,
Prod Reporting
Production '||chr(38)||' Emission Allocation Team


'||chr(91)||'This notification is automatically generated by Pluto Hub ECaaS.'||chr(93)),lv_rev_text); END IF;

  --(7) NEW Distribution Set 'R_BLP_DAILY_PROD_ALLOC_PLUTO'
  UPDATE TV_DISTRIBUTION_SET SET NAME='Burrup LNG Park Daily Production Report (Pluto)',FUNCTIONAL_AREA_CODE='EC',REV_TEXT=lv_rev_text
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_DISTRIBUTION_SET (CODE,NAME,FUNCTIONAL_AREA_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_PLUTO','Burrup LNG Park Daily Production Report (Pluto)','EC',lv_rev_text); END IF;

  --(8) Recipients on the new '_PLUTO' distribution set (CC=INT, FROM=DMS, TO=EXT, TO='INT_... 1')
  FOR r IN (SELECT 'CC' rt,'INT_R_BLP_DAILY_PROD_ALLOC_PLUTO' cc FROM dual
            UNION ALL SELECT 'FROM','DMS_R_BLP_DAILY_PROD_ALLOC_PLUTO' FROM dual
            UNION ALL SELECT 'TO','EXT_R_BLP_DAILY_PROD_ALLOC_PLUTO' FROM dual
            --UNION ALL SELECT 'TO','INT_R_BLP_DAILY_PROD_ALLOC_PLUTO 1' FROM dual
			) LOOP
    UPDATE TV_DISTRIBUTION_SET_CONTACT SET FORMAT_CODE='TEXT',REV_TEXT=lv_rev_text
     WHERE CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO' AND RECIPIENT_TYPE=r.rt AND COMPANY_CONTACT_CODE=r.cc;
    IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_DISTRIBUTION_SET_CONTACT (CODE,RECIPIENT_TYPE,COMPANY_CONTACT_CODE,FORMAT_CODE,REV_TEXT)
      VALUES ('R_BLP_DAILY_PROD_ALLOC_PLUTO',r.rt,r.cc,'TEXT',lv_rev_text); END IF;
  END LOOP;

  --(9) Message Distribution (object = the message def; existing row updated to TEXT)
  UPDATE DV_MESSAGE_DISTRIBUTION SET FORMAT_CODE='TEXT',REV_TEXT=lv_rev_text WHERE OBJECT_CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO DV_MESSAGE_DISTRIBUTION (OBJECT_CODE,FORMAT_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_PLUTO','TEXT',lv_rev_text); END IF;
  SELECT MESSAGE_DISTRIBUTION_NO INTO lv_msg_distr_no FROM DV_MESSAGE_DISTRIBUTION WHERE OBJECT_CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO';

  --(10) Param: Report Name
  UPDATE TV_MESSAGE_DISTR_PARAM SET PARAMETER_VALUE='Burrup LNG Park Daily Production Report (Pluto)',
         PARAMETER_TYPE='BASIC_TYPE',PARAMETER_SUB_TYPE='STRING',REV_TEXT=lv_rev_text
   WHERE MESSAGE_DISTRIBUTION_NO=lv_msg_distr_no AND PARAMETER_NAME='Report Name';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_MESSAGE_DISTR_PARAM (MESSAGE_DISTRIBUTION_NO,PARAMETER_NAME,PARAMETER_VALUE,PARAMETER_TYPE,PARAMETER_SUB_TYPE,REV_TEXT)
    VALUES (lv_msg_distr_no,'Report Name','Burrup LNG Park Daily Production Report (Pluto)','BASIC_TYPE','STRING',lv_rev_text); END IF;

  --(11) Connection -> RE-POINT to the new '_PLUTO' distribution set
  UPDATE TV_MESSAGE_DISTR_CONN SET DISTR_SET_CODE='R_BLP_DAILY_PROD_ALLOC_PLUTO',DESCRIPTION='Burrup LNG Park Daily Production Report (Pluto)',REV_TEXT=lv_rev_text
   WHERE MESSAGE_DISTRIBUTION_NO=lv_msg_distr_no;
  IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_MESSAGE_DISTR_CONN (MESSAGE_DISTRIBUTION_NO,DISTR_SET_CODE,DESCRIPTION,REV_TEXT)
    VALUES (lv_msg_distr_no,'R_BLP_DAILY_PROD_ALLOC_PLUTO','Burrup LNG Park Daily Production Report (Pluto)',lv_rev_text); END IF;

END;
/
