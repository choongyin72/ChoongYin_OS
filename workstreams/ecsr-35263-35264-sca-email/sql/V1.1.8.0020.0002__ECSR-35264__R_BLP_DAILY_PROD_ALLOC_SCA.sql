-- ECSR-35264 (Issue_1044B) - Burrup LNG Park Daily Production Report (SCARBOROUGH): dedicated '_SCA' message config.
-- Cloned from V1.1.8.0020.0001__ECSR-35264__R_BLP_DAILY_PROD_ALLOC_PLUTO.sql (PLUTO->SCA, Pluto->Scarborough).
-- Gives Scarborough its OWN ACTOR Maintenance (Ruchi's ask), separate from Pluto.
--
-- DESIGN: CREATES new '_SCA' objects (group + contacts + distribution set) and RE-POINTS the
--   R_BLP_DAILY_PROD_ALLOC_SCA message-def's COMPANY_CONTACT_CODE + distribution connection to them.
--   OLD shared objects are LEFT INTACT (never deleted).
-- RE-RUNNABLE (idempotent): UPDATE-first, INSERT only if absent, keyed on unique CODE/OBJECT_ID; REV_TEXT
--   stamped; NO DELETE. All '_SCA' codes are <=32 chars (fit OV_*.CODE VARCHAR2(32)).
-- NOTE: final Flyway version/folder + REV_TEXT=<ECPR> set by the team at delivery into Pluto_Config.
DECLARE
  lv_rev_text     VARCHAR2(15) := 'ECSR-35264';
  lv_object_id    VARCHAR2(32);
  lv_msg_distr_no NUMBER;
BEGIN

  --(1) Contact Group Set
  UPDATE OV_CONTACT_GROUP_SET
     SET NAME='Burrup LNG Park Daily Production Report (Scarborough)', OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'), FUNCTIONAL_AREA_CODE='EC', REV_TEXT=lv_rev_text
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN
    INSERT INTO OV_CONTACT_GROUP_SET (CODE,NAME,OBJECT_START_DATE,DAYTIME,FUNCTIONAL_AREA_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_SCA','Burrup LNG Park Daily Production Report (Scarborough)',
            TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'EC',lv_rev_text);
  END IF;

  --(2) NEW Contact Group 'R_BLP_DAILY_ALLOC_SCA' -> the set
  UPDATE OV_CONTACT_GROUP
     SET NAME='PHBR-R_BLP_DAIY_PROD_ALLOC_SCA', OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'), CONTACT_GROUP_SET_CODE='R_BLP_DAILY_PROD_ALLOC_SCA'
   WHERE CODE='R_BLP_DAILY_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN
    INSERT INTO OV_CONTACT_GROUP (CODE,NAME,OBJECT_START_DATE,DAYTIME,CONTACT_GROUP_SET_CODE)
    VALUES ('R_BLP_DAILY_ALLOC_SCA','PHBR-R_BLP_DAIY_PROD_ALLOC_SCA',
            TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'R_BLP_DAILY_PROD_ALLOC_SCA');
  END IF;

  --(3) NEW '_SCA' message contacts -> group R_BLP_DAILY_ALLOC_SCA
  --  FROM (sender)
  UPDATE OV_MESSAGE_CONTACT SET NAME='Default mail sender - R_BLP_DAILY_PROD_ALLOC_SCA',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='WBOperator'||chr(64)||'woodside.com.au',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_SCA',REV_TEXT=lv_rev_text
   WHERE CODE='DMS_R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('DMS_R_BLP_DAILY_PROD_ALLOC_SCA','Default mail sender - R_BLP_DAILY_PROD_ALLOC_SCA',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'WBOperator'||chr(64)||'woodside.com.au','C_WDE','EC','R_BLP_DAILY_ALLOC_SCA',lv_rev_text); END IF;
  --  Internal (CC)
  UPDATE OV_MESSAGE_CONTACT SET NAME='Internal-Burrup LNG Park Daily Production Report (Scarborough)',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='prodreporting'||chr(64)||'woodside.com',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_SCA',REV_TEXT=lv_rev_text
   WHERE CODE='INT_R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('INT_R_BLP_DAILY_PROD_ALLOC_SCA','Internal-Burrup LNG Park Daily Production Report (Scarborough)',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'prodreporting'||chr(64)||'woodside.com','C_WDE','EC','R_BLP_DAILY_ALLOC_SCA',lv_rev_text); END IF;
  --  External (TO)
  UPDATE OV_MESSAGE_CONTACT SET NAME='External-Burrup LNG Park Daily Production Report (Scarborough)',
         OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),
         DELIVERY_METHOD='SMTP',DELIVERY_ADDRESS='PASReportPJV'||chr(64)||'woodside.com',
         COMPANY_CODE='C_WDE',FUNCTIONAL_AREA_CODE='EC',CONTACT_GROUP_CODE='R_BLP_DAILY_ALLOC_SCA',REV_TEXT=lv_rev_text
   WHERE CODE='EXT_R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_CONTACT
    (CODE,NAME,OBJECT_START_DATE,DAYTIME,DELIVERY_METHOD,DELIVERY_ADDRESS,COMPANY_CODE,FUNCTIONAL_AREA_CODE,CONTACT_GROUP_CODE,REV_TEXT)
    VALUES ('EXT_R_BLP_DAILY_PROD_ALLOC_SCA','External-Burrup LNG Park Daily Production Report (Scarborough)',
       TO_DATE('01/01/2000','DD/MM/YYYY'),TO_DATE('01/01/2000','DD/MM/YYYY'),'SMTP',
       'PASReportPJV'||chr(64)||'woodside.com','C_WDE','EC','R_BLP_DAILY_ALLOC_SCA',lv_rev_text); END IF;
  -- (the kepha / midocean / PASReportPJVInternal extras are omitted - mirror the Pluto baseline; add via ACTOR Maintenance if needed)

  --(4) Message Type -> RE-POINT COMPANY_CONTACT_CODE to the new '_SCA' sender
  UPDATE OV_MESSAGE_DEFINITION
     SET NAME='R_BLP_DAILY_PROD_ALLOC_SCA Message Definition',OBJECT_START_DATE=TO_DATE('01/01/2000','DD/MM/YYYY'),
         OBJECT_END_DATE=NULL,DAYTIME=TO_DATE('01/01/2000','DD/MM/YYYY'),END_DATE=NULL,
         MESSAGE_SUBJECT='Burrup LNG Park Daily Allocation Statement for Production Date',MESSAGE_HANDLING='AUTO',
         MESSAGE_LOAD_JOB=NULL,MESSAGE_GENERATE_JOB=NULL,MESSAGE_VALIDATE_JOB=NULL,INTERNAL_FORMAT_TYPE='TEXT',
         DIRECTION='OUT',FREQUENCY='EVENT',XML_SCHEMA_URL=NULL,EXTERNAL_FORMAT='TEXT',FUNCTIONAL_AREA_CODE='EC',
         COMPANY_CONTACT_CODE='DMS_R_BLP_DAILY_PROD_ALLOC_SCA',REV_TEXT=lv_rev_text
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO OV_MESSAGE_DEFINITION
    (CODE,NAME,OBJECT_START_DATE,OBJECT_END_DATE,DAYTIME,END_DATE,MESSAGE_SUBJECT,MESSAGE_HANDLING,MESSAGE_LOAD_JOB,
     MESSAGE_GENERATE_JOB,MESSAGE_VALIDATE_JOB,INTERNAL_FORMAT_TYPE,DIRECTION,FREQUENCY,XML_SCHEMA_URL,EXTERNAL_FORMAT,
     FUNCTIONAL_AREA_CODE,COMPANY_CONTACT_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_SCA','R_BLP_DAILY_PROD_ALLOC_SCA Message Definition',
       TO_DATE('01/01/2000','DD/MM/YYYY'),NULL,TO_DATE('01/01/2000','DD/MM/YYYY'),NULL,
       'Burrup LNG Park Daily Allocation Statement for Production Date','AUTO',NULL,NULL,NULL,'TEXT','OUT','EVENT',
       NULL,'TEXT','EC','DMS_R_BLP_DAILY_PROD_ALLOC_SCA',lv_rev_text); END IF;

  --(5) Message Format (TEXT default)
  UPDATE DV_MESSAGE_FORMAT SET DEFAULT_EXT_FORMAT='Y',REV_TEXT=lv_rev_text
   WHERE OBJECT_CODE='R_BLP_DAILY_PROD_ALLOC_SCA' AND FORMAT_CODE='TEXT';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO DV_MESSAGE_FORMAT (OBJECT_CODE,FORMAT_CODE,DEFAULT_EXT_FORMAT,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_SCA','TEXT','Y',lv_rev_text); END IF;

  --(6) Freetext Message Template (subject + body, {production_day})
  lv_object_id := ec_message_definition.object_id_by_uk('R_BLP_DAILY_PROD_ALLOC_SCA');
  UPDATE DV_MSG_FREE_TEXT_TEMPLATE
     SET SUBJECT='Burrup LNG Park Daily Production Report (Scarborough) '||chr(123)||'production_day'||chr(125),
         TEMPLATE=to_clob('Hi,

Please find attached Burrup LNG Park Daily Production Report (Scarborough) for Production Date - '||chr(123)||'production_day'||chr(125)||'.

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
    VALUES (lv_object_id,'Burrup LNG Park Daily Production Report (Scarborough) '||chr(123)||'production_day'||chr(125),
       to_clob('Hi,

Please find attached Burrup LNG Park Daily Production Report (Scarborough) for Production Date - '||chr(123)||'production_day'||chr(125)||'.

Note this report is designed to meet the requirements of Burrup LNG Park Production Allocation Agreement (PAA) from the PAA Effective Date.

For any queries or issues please contact PlutoJVNotices'||chr(64)||'woodside.com.au.

Disclaimer - You are receiving this email as a designated recipient for the above-listed Report Type. If you no longer wish to receive these emails, please contact the Production '||chr(38)||' Emission Allocation Team - Australian Business.

Regards,
Prod Reporting
Production '||chr(38)||' Emission Allocation Team


'||chr(91)||'This notification is automatically generated by Pluto Hub ECaaS.'||chr(93)),lv_rev_text); END IF;

  --(7) NEW Distribution Set 'R_BLP_DAILY_PROD_ALLOC_SCA'
  UPDATE TV_DISTRIBUTION_SET SET NAME='Burrup LNG Park Daily Production Report (Scarborough)',FUNCTIONAL_AREA_CODE='EC',REV_TEXT=lv_rev_text
   WHERE CODE='R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_DISTRIBUTION_SET (CODE,NAME,FUNCTIONAL_AREA_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_SCA','Burrup LNG Park Daily Production Report (Scarborough)','EC',lv_rev_text); END IF;

  --(8) Recipients on the new '_SCA' distribution set (CC=INT, FROM=DMS, TO=EXT)
  FOR r IN (SELECT 'CC' rt,'INT_R_BLP_DAILY_PROD_ALLOC_SCA' cc FROM dual
            UNION ALL SELECT 'FROM','DMS_R_BLP_DAILY_PROD_ALLOC_SCA' FROM dual
            UNION ALL SELECT 'TO','EXT_R_BLP_DAILY_PROD_ALLOC_SCA' FROM dual) LOOP
    UPDATE TV_DISTRIBUTION_SET_CONTACT SET FORMAT_CODE='TEXT',REV_TEXT=lv_rev_text
     WHERE CODE='R_BLP_DAILY_PROD_ALLOC_SCA' AND RECIPIENT_TYPE=r.rt AND COMPANY_CONTACT_CODE=r.cc;
    IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_DISTRIBUTION_SET_CONTACT (CODE,RECIPIENT_TYPE,COMPANY_CONTACT_CODE,FORMAT_CODE,REV_TEXT)
      VALUES ('R_BLP_DAILY_PROD_ALLOC_SCA',r.rt,r.cc,'TEXT',lv_rev_text); END IF;
  END LOOP;

  --(9) Message Distribution (object = the message def)
  UPDATE DV_MESSAGE_DISTRIBUTION SET FORMAT_CODE='TEXT',REV_TEXT=lv_rev_text WHERE OBJECT_CODE='R_BLP_DAILY_PROD_ALLOC_SCA';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO DV_MESSAGE_DISTRIBUTION (OBJECT_CODE,FORMAT_CODE,REV_TEXT)
    VALUES ('R_BLP_DAILY_PROD_ALLOC_SCA','TEXT',lv_rev_text); END IF;
  SELECT MESSAGE_DISTRIBUTION_NO INTO lv_msg_distr_no FROM DV_MESSAGE_DISTRIBUTION WHERE OBJECT_CODE='R_BLP_DAILY_PROD_ALLOC_SCA';

  --(10) Param: Report Name
  UPDATE TV_MESSAGE_DISTR_PARAM SET PARAMETER_VALUE='Burrup LNG Park Daily Production Report (Scarborough)',
         PARAMETER_TYPE='BASIC_TYPE',PARAMETER_SUB_TYPE='STRING',REV_TEXT=lv_rev_text
   WHERE MESSAGE_DISTRIBUTION_NO=lv_msg_distr_no AND PARAMETER_NAME='Report Name';
  IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_MESSAGE_DISTR_PARAM (MESSAGE_DISTRIBUTION_NO,PARAMETER_NAME,PARAMETER_VALUE,PARAMETER_TYPE,PARAMETER_SUB_TYPE,REV_TEXT)
    VALUES (lv_msg_distr_no,'Report Name','Burrup LNG Park Daily Production Report (Scarborough)','BASIC_TYPE','STRING',lv_rev_text); END IF;

  --(11) Connection -> RE-POINT to the new '_SCA' distribution set
  UPDATE TV_MESSAGE_DISTR_CONN SET DISTR_SET_CODE='R_BLP_DAILY_PROD_ALLOC_SCA',DESCRIPTION='Burrup LNG Park Daily Production Report (Scarborough)',REV_TEXT=lv_rev_text
   WHERE MESSAGE_DISTRIBUTION_NO=lv_msg_distr_no;
  IF SQL%ROWCOUNT=0 THEN INSERT INTO TV_MESSAGE_DISTR_CONN (MESSAGE_DISTRIBUTION_NO,DISTR_SET_CODE,DESCRIPTION,REV_TEXT)
    VALUES (lv_msg_distr_no,'R_BLP_DAILY_PROD_ALLOC_SCA','Burrup LNG Park Daily Production Report (Scarborough)',lv_rev_text); END IF;

END;
/
