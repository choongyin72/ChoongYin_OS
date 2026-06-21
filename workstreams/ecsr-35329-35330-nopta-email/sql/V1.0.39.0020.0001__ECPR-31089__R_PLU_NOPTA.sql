--ECPR-31089  (ECSR-35329) Enable Email send for Pluto Upstream NOPTA Report (R_PLU_NOPTA)
-- Mirrors the implemented precedent ECPR-31028 (R_SCA_DAILY_PARTNER). Idempotent update-insert, REV_TEXT.
-- Decisions (user 2026-06-21): (1) Format = TEXT to match other implemented messages (was REPORT/XML);
-- (2) message-type Subject cleaned to 'Pluto Upstream NOPTA Report for Production Date' (was "'SUSPECTED
-- DUPLICATE' - ..."); (3) message-def COMPANY_CONTACT_CODE unchanged (DMS_WDS_Reporting); (4) recipients
-- unchanged (FROM DMS_R_PLU_NOPTA plutohubpas@woodside.com, TO INT_R_PLU_NOPTA prodreporting@woodside.com).
-- NOTE: Flyway version/timestamp in the filename is a placeholder for our system; the team sets the final
-- 1.0.x.0020.<ts> name + folder at delivery into Pluto_Config/020_Configuration.
DECLARE
  lv_object_id    VARCHAR2(32);
  lv_rev_text     VARCHAR2(10) := 'ECPR-31089';
  lv_msg_distr_no NUMBER;
BEGIN

  --Maintain Contact Group Set
  UPDATE OV_CONTACT_GROUP_SET
     SET NAME                 = 'Pluto Upstream NOPTA Report',
         OBJECT_START_DATE    = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         DAYTIME              = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         FUNCTIONAL_AREA_CODE = 'EC',
         REV_TEXT             = lv_rev_text
   WHERE CODE = 'R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO OV_CONTACT_GROUP_SET
      (CODE,
       NAME,
       OBJECT_START_DATE,
       DAYTIME,
       FUNCTIONAL_AREA_CODE,
       REV_TEXT)
    VALUES
      ('R_PLU_NOPTA',
       'Pluto Upstream NOPTA Report',
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       'EC',
       lv_rev_text);
  END IF;

  --Actor Maintenance: Contact Group
  UPDATE OV_CONTACT_GROUP
     SET NAME                   = 'PHBR-R_PLU_NOPTA',
         OBJECT_START_DATE      = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         DAYTIME                = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         CONTACT_GROUP_SET_CODE = 'R_PLU_NOPTA'
   WHERE CODE = 'R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO OV_CONTACT_GROUP
      (CODE, NAME, OBJECT_START_DATE, DAYTIME, CONTACT_GROUP_SET_CODE)
    VALUES
      ('R_PLU_NOPTA',
       'PHBR-R_PLU_NOPTA',
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       'R_PLU_NOPTA');
  END IF;

  --Actor Maintenance: sender (FROM)  [decision 4: address unchanged = plutohubpas@woodside.com]
  UPDATE OV_MESSAGE_CONTACT
     SET NAME                 = 'Default mail sender - R_PLU_NOPTA',
         OBJECT_START_DATE    = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         DAYTIME              = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         DELIVERY_METHOD      = 'SMTP',
         DELIVERY_ADDRESS     = 'plutohubpas' || chr(64) || 'woodside.com',
         COUNTRY_CODE         = 'AUS',
         COMPANY_CODE         = 'C_WDE',
         FUNCTIONAL_AREA_CODE = 'EC',
         CONTACT_GROUP_CODE   = 'R_PLU_NOPTA',
         REV_TEXT             = lv_rev_text
   WHERE CODE = 'DMS_R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO OV_MESSAGE_CONTACT
      (CODE,
       NAME,
       OBJECT_START_DATE,
       DAYTIME,
       DELIVERY_METHOD,
       DELIVERY_ADDRESS,
       COUNTRY_CODE,
       COMPANY_CODE,
       FUNCTIONAL_AREA_CODE,
       CONTACT_GROUP_CODE,
       REV_TEXT)
    VALUES
      ('DMS_R_PLU_NOPTA',
       'Default mail sender - R_PLU_NOPTA',
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       'SMTP',
       'plutohubpas' || chr(64) || 'woodside.com',
       'AUS',
       'C_WDE',
       'EC',
       'R_PLU_NOPTA',
       lv_rev_text);
  END IF;

  --Actor Maintenance: recipient (TO)  [decision 4: address unchanged = prodreporting@woodside.com]
  UPDATE OV_MESSAGE_CONTACT
     SET NAME                 = 'Internal-Pluto Upstream NOPTA Report',
         OBJECT_START_DATE    = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         DAYTIME              = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         DELIVERY_METHOD      = 'SMTP',
         DELIVERY_ADDRESS     = 'prodreporting' || chr(64) || 'woodside.com',
         COUNTRY_CODE         = 'AUS',
         COMPANY_CODE         = 'C_WDE',
         FUNCTIONAL_AREA_CODE = 'EC',
         CONTACT_GROUP_CODE   = 'R_PLU_NOPTA',
         REV_TEXT             = lv_rev_text
   WHERE CODE = 'INT_R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO OV_MESSAGE_CONTACT
      (CODE,
       NAME,
       OBJECT_START_DATE,
       DAYTIME,
       DELIVERY_METHOD,
       DELIVERY_ADDRESS,
       COUNTRY_CODE,
       COMPANY_CODE,
       FUNCTIONAL_AREA_CODE,
       CONTACT_GROUP_CODE,
       REV_TEXT)
    VALUES
      ('INT_R_PLU_NOPTA',
       'Internal-Pluto Upstream NOPTA Report',
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       'SMTP',
       'prodreporting' || chr(64) || 'woodside.com',
       'AUS',
       'C_WDE',
       'EC',
       'R_PLU_NOPTA',
       lv_rev_text);
  END IF;

  --Maintain Message Type  [decision 1: INTERNAL_FORMAT_TYPE/EXTERNAL_FORMAT = TEXT ; decision 2: clean subject ;
  --                        decision 3: COMPANY_CONTACT_CODE unchanged = DMS_WDS_Reporting]
  UPDATE OV_MESSAGE_DEFINITION
     SET NAME                 = 'R_PLU_NOPTA Message Definition',
         OBJECT_START_DATE    = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         OBJECT_END_DATE      = NULL,
         DAYTIME              = TO_DATE('01/01/2000', 'DD/MM/YYYY'),
         END_DATE             = NULL,
         MESSAGE_SUBJECT      = 'Pluto Upstream NOPTA Report for Production Date',
         MESSAGE_HANDLING     = 'AUTO',
         MESSAGE_LOAD_JOB     = NULL,
         MESSAGE_GENERATE_JOB = NULL,
         MESSAGE_VALIDATE_JOB = NULL,
         INTERNAL_FORMAT_TYPE = 'TEXT',
         DIRECTION            = 'OUT',
         FREQUENCY            = 'EVENT',
         XML_SCHEMA_URL       = NULL,
         EXTERNAL_FORMAT      = 'TEXT',
         FUNCTIONAL_AREA_CODE = 'EC',
         COMPANY_CONTACT_CODE = 'DMS_WDS_Reporting',
         REV_TEXT             = lv_rev_text
   WHERE CODE = 'R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO OV_MESSAGE_DEFINITION
      (CODE,
       NAME,
       OBJECT_START_DATE,
       OBJECT_END_DATE,
       DAYTIME,
       END_DATE,
       MESSAGE_SUBJECT,
       MESSAGE_HANDLING,
       MESSAGE_LOAD_JOB,
       MESSAGE_GENERATE_JOB,
       MESSAGE_VALIDATE_JOB,
       INTERNAL_FORMAT_TYPE,
       DIRECTION,
       FREQUENCY,
       XML_SCHEMA_URL,
       EXTERNAL_FORMAT,
       FUNCTIONAL_AREA_CODE,
       COMPANY_CONTACT_CODE,
       REV_TEXT)
    VALUES
      ('R_PLU_NOPTA',
       'R_PLU_NOPTA Message Definition',
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       NULL,
       TO_DATE('01/01/2000', 'DD/MM/YYYY'),
       NULL,
       'Pluto Upstream NOPTA Report for Production Date',
       'AUTO',
       NULL,
       NULL,
       NULL,
       'TEXT',
       'OUT',
       'EVENT',
       NULL,
       'TEXT',
       'EC',
       'DMS_WDS_Reporting',
       lv_rev_text);
  END IF;

  --Message Format  [decision 1: TEXT] 
  -- Convert existing R_PLU_NOPTA from REPORT/XML to TEXT. FORMAT_CODE is keyed/FK'd
  -- (FK_MESSAGE_DISTRIBUTION_3) so it cannot be UPDATEd in place -> drop the format-dependent chain
  -- child-first, then the sections below rebuild it as TEXT. (No-op on a fresh install.)
  DELETE FROM TV_MESSAGE_DISTR_CONN  WHERE MESSAGE_DISTRIBUTION_NO IN (SELECT MESSAGE_DISTRIBUTION_NO FROM DV_MESSAGE_DISTRIBUTION WHERE OBJECT_CODE = 'R_PLU_NOPTA');
  DELETE FROM TV_MESSAGE_DISTR_PARAM WHERE MESSAGE_DISTRIBUTION_NO IN (SELECT MESSAGE_DISTRIBUTION_NO FROM DV_MESSAGE_DISTRIBUTION WHERE OBJECT_CODE = 'R_PLU_NOPTA');
  DELETE FROM DV_MESSAGE_DISTRIBUTION    WHERE OBJECT_CODE = 'R_PLU_NOPTA';
  DELETE FROM TV_DISTRIBUTION_SET_CONTACT WHERE CODE = 'R_PLU_NOPTA';
  -- NOTE: do NOT delete DV_MESSAGE_FORMAT - the existing XML format row is referenced by historical
  -- outgoing messages (FK_MESSAGE_OUT_4). Keep XML for history; make TEXT the default format instead.

  -- demote the existing (XML) format from default
  UPDATE DV_MESSAGE_FORMAT
     SET DEFAULT_EXT_FORMAT = 'N', REV_TEXT = lv_rev_text
   WHERE OBJECT_CODE = 'R_PLU_NOPTA' AND FORMAT_CODE <> 'TEXT';

  -- add/ensure the TEXT format as the default
  UPDATE DV_MESSAGE_FORMAT
     SET DEFAULT_EXT_FORMAT = 'Y',
         REV_TEXT           = lv_rev_text
   WHERE OBJECT_CODE = 'R_PLU_NOPTA' AND FORMAT_CODE = 'TEXT';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO DV_MESSAGE_FORMAT
      (OBJECT_CODE, FORMAT_CODE, DEFAULT_EXT_FORMAT, REV_TEXT)
    VALUES
      ('R_PLU_NOPTA', 'TEXT', 'Y', lv_rev_text);
  END IF;

  --Freetext Message Template (body) -- required for TEXT format
  lv_object_id := ec_message_definition.object_id_by_uk('R_PLU_NOPTA');
  UPDATE DV_MSG_FREE_TEXT_TEMPLATE
     SET SUBJECT  = 'Pluto Upstream NOPTA Report for Production Date - ' ||
                    chr(123) || 'production_day' || chr(125),
         TEMPLATE = to_clob('Hi,

Please find attached Pluto Upstream NOPTA Report for Production Date - ' ||
                             chr(123) || 'production_day' || chr(125) || '.

For any queries or issues please contact PlutoJVNotices' ||
                             chr(64) ||
                             'woodside.com.au.

Disclaimer - You are receiving this email as a designated recipient for the above-listed Report Type. If you no longer wish to receive these emails, please contact the Production ' ||
                             chr(38) || ' Emission Allocation Team - Australian Business.

Regards,
Prod Reporting
Production ' || chr(38) || ' Emission Allocation Team

' || chr(91) ||
                             'This notification is automatically generated by Pluto Hub ECaaS.' ||
                             chr(93)),
         REV_TEXT = lv_rev_text
   WHERE OBJECT_ID = lv_object_id;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO DV_MSG_FREE_TEXT_TEMPLATE
      (OBJECT_ID, SUBJECT, TEMPLATE, REV_TEXT)
    VALUES
      (lv_object_id,
       'Pluto Upstream NOPTA Report for Production Date - ' || chr(123) ||
       'production_day' || chr(125),
       to_clob('Hi,

Please find attached Pluto Upstream NOPTA Report for Production Date - ' ||
                chr(123) || 'production_day' || chr(125) || '.

For any queries or issues please contact PlutoJVNotices' ||
                chr(64) ||
                'woodside.com.au.

Disclaimer - You are receiving this email as a designated recipient for the above-listed Report Type. If you no longer wish to receive these emails, please contact the Production ' ||
                chr(38) || ' Emission Allocation Team - Australian Business.

Regards,
Prod Reporting
Production ' || chr(38) || ' Emission Allocation Team

' || chr(91) ||
                'This notification is automatically generated by Pluto Hub ECaaS.' ||
                chr(93)),
       lv_rev_text);
  END IF;

  --Distribution List
  UPDATE TV_DISTRIBUTION_SET
     SET NAME                 = 'Pluto Upstream NOPTA Report',
         FUNCTIONAL_AREA_CODE = 'EC',
         REV_TEXT             = lv_rev_text
   WHERE CODE = 'R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO TV_DISTRIBUTION_SET
      (CODE, NAME, FUNCTIONAL_AREA_CODE, REV_TEXT)
    VALUES
      ('R_PLU_NOPTA', 'Pluto Upstream NOPTA Report', 'EC', lv_rev_text);
  END IF;

  --Recipients: FROM  [decision 1: FORMAT_CODE = TEXT]
  UPDATE TV_DISTRIBUTION_SET_CONTACT
     SET FORMAT_CODE    = 'TEXT',
         RECIPIENT_TYPE = 'FROM',
         REV_TEXT       = lv_rev_text
   WHERE CODE = 'R_PLU_NOPTA'
     AND COMPANY_CONTACT_CODE = 'DMS_R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO TV_DISTRIBUTION_SET_CONTACT
      (CODE, RECIPIENT_TYPE, COMPANY_CONTACT_CODE, FORMAT_CODE, REV_TEXT)
    VALUES
      ('R_PLU_NOPTA', 'FROM', 'DMS_R_PLU_NOPTA', 'TEXT', lv_rev_text);
  END IF;

  --Recipients: TO
  UPDATE TV_DISTRIBUTION_SET_CONTACT
     SET FORMAT_CODE    = 'TEXT',
         RECIPIENT_TYPE = 'TO',
         REV_TEXT       = lv_rev_text
   WHERE CODE = 'R_PLU_NOPTA'
     AND COMPANY_CONTACT_CODE = 'INT_R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO TV_DISTRIBUTION_SET_CONTACT
      (CODE, RECIPIENT_TYPE, COMPANY_CONTACT_CODE, FORMAT_CODE, REV_TEXT)
    VALUES
      ('R_PLU_NOPTA', 'TO', 'INT_R_PLU_NOPTA', 'TEXT', lv_rev_text);
  END IF;

  --Message Distribution  [decision 1: FORMAT_CODE = TEXT]
  UPDATE DV_MESSAGE_DISTRIBUTION
     SET FORMAT_CODE = 'TEXT', REV_TEXT = lv_rev_text
   WHERE OBJECT_CODE = 'R_PLU_NOPTA';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO DV_MESSAGE_DISTRIBUTION
      (OBJECT_CODE, FORMAT_CODE, REV_TEXT)
    VALUES
      ('R_PLU_NOPTA', 'TEXT', lv_rev_text);
  END IF;

  SELECT MESSAGE_DISTRIBUTION_NO
    INTO lv_msg_distr_no
    FROM DV_MESSAGE_DISTRIBUTION
   WHERE OBJECT_CODE = 'R_PLU_NOPTA';

  --Message Distribution param: Report Name
  UPDATE TV_MESSAGE_DISTR_PARAM
     SET PARAMETER_VALUE    = 'Pluto Upstream NOPTA Report',
         PARAMETER_TYPE     = 'BASIC_TYPE',
         PARAMETER_SUB_TYPE = 'STRING',
         REV_TEXT           = lv_rev_text
   WHERE MESSAGE_DISTRIBUTION_NO = lv_msg_distr_no
     AND PARAMETER_NAME = 'Report Name';
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO TV_MESSAGE_DISTR_PARAM
      (MESSAGE_DISTRIBUTION_NO,
       PARAMETER_NAME,
       PARAMETER_VALUE,
       PARAMETER_TYPE,
       PARAMETER_SUB_TYPE,
       REV_TEXT)
    VALUES
      (lv_msg_distr_no,
       'Report Name',
       'Pluto Upstream NOPTA Report',
       'BASIC_TYPE',
       'STRING',
       lv_rev_text);
  END IF;

  --Message Distribution connection -> distribution set
  UPDATE TV_MESSAGE_DISTR_CONN
     SET DISTR_SET_CODE = 'R_PLU_NOPTA',
         DESCRIPTION    = 'Pluto Upstream NOPTA Report',
         REV_TEXT       = lv_rev_text
   WHERE MESSAGE_DISTRIBUTION_NO = lv_msg_distr_no;
  IF SQL%ROWCOUNT = 0 THEN
    INSERT INTO TV_MESSAGE_DISTR_CONN
      (MESSAGE_DISTRIBUTION_NO, DISTR_SET_CODE, DESCRIPTION, REV_TEXT)
    VALUES
      (lv_msg_distr_no,
       'R_PLU_NOPTA',
       'Pluto Upstream NOPTA Report',
       lv_rev_text);
  END IF;

END;
/