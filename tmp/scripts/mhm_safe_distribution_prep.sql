-- ============================================================================
-- N-notify SAFE distribution prep  —  REVIEW REQUIRED, DO NOT AUTO-RUN
-- ----------------------------------------------------------------------------
-- Purpose: create a guaranteed-non-deliverable distribution so the N-notify live
--          send (send_freetext_notification.robot) can run with ZERO real-email risk.
--
-- Approach (per clone-by-full-row-diff rule): clone the EXISTING, already-effective
--   FRMW free-text TO contact (FRMW_MHM_RECEIVER_1) + its version row, changing ONLY
--   OBJECT_CODE and DELIVERY_ADDRESS (-> autotest@example.invalid). Then create a new
--   AUTOTEST_FREETEXT_INVALID distribution pointing at that one contact. Cloning a row
--   that already works maximises the chance the new contact behaves identically
--   (effective date, approval, view-generator visibility in the screen dropdown).
--
-- ⚠️ CAVEATS before running (why this is gated, not auto-run):
--   1. EC dropdowns only list objects EFFECTIVE at the form Start Date and APPROVED;
--      a hand-inserted object may need an approval/view-generator refresh to appear.
--   2. The EC-correct route is the Distribution List UI screen (MHM.0001) — prefer it
--      if available. This SQL is the fast path for a sandbox, to be run UNDER SUPERVISION.
--   3. Run inside a transaction; verify; only then COMMIT. Rollback block at the bottom.
--   4. example.invalid is RFC-2606 reserved → can never resolve/deliver anywhere.
-- ============================================================================

-- New ids (EC uses 32-char hex GUIDs for OBJECT_ID / REC_ID)
DEFINE new_contact_oid = 0
-- (use the PL/SQL block below; SQL*Plus DEFINE cannot call SYS_GUID — kept for reference)

DECLARE
  v_src_oid   COMPANY_CONTACT.OBJECT_ID%TYPE;
  v_new_oid   VARCHAR2(32) := RAWTOHEX(SYS_GUID());
  v_new_cc_rec VARCHAR2(32) := RAWTOHEX(SYS_GUID());
  v_new_ver_rec VARCHAR2(32) := RAWTOHEX(SYS_GUID());
  v_new_dsc_rec VARCHAR2(32) := RAWTOHEX(SYS_GUID());
BEGIN
  -- source = the working FRMW free-text TO receiver
  SELECT cc.OBJECT_ID INTO v_src_oid
  FROM COMPANY_CONTACT cc WHERE cc.OBJECT_CODE = 'FRMW_MHM_RECEIVER_1';

  -- 1) clone COMPANY_CONTACT (change OBJECT_ID, OBJECT_CODE, REC_ID only)
  INSERT INTO COMPANY_CONTACT (OBJECT_ID, OBJECT_CODE, CLASS_NAME, COMPANY_ID, START_DATE,
         END_DATE, CONTACT_GROUP_ID, RECORD_STATUS, CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
  SELECT v_new_oid, 'AUTOTEST_INVALID_RCV', CLASS_NAME, COMPANY_ID, START_DATE, END_DATE,
         CONTACT_GROUP_ID, RECORD_STATUS, 'AUTOTEST', SYSDATE, REV_NO, v_new_cc_rec
  FROM COMPANY_CONTACT WHERE OBJECT_ID = v_src_oid;

  -- 2) clone COMPANY_CONTACT_VERSION (change OBJECT_ID, NAME, DELIVERY_ADDRESS, REC_ID only)
  INSERT INTO COMPANY_CONTACT_VERSION (OBJECT_ID, DAYTIME, END_DATE, NAME, DELIVERY_METHOD,
         DELIVERY_ADDRESS, FUNCTIONAL_AREA_ID, RECORD_STATUS, CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
  SELECT v_new_oid, DAYTIME, END_DATE, 'AUTOTEST invalid receiver', DELIVERY_METHOD,
         'autotest@example.invalid', FUNCTIONAL_AREA_ID, RECORD_STATUS, 'AUTOTEST', SYSDATE, REV_NO, v_new_ver_rec
  FROM COMPANY_CONTACT_VERSION WHERE OBJECT_ID = v_src_oid;

  -- 3) new distribution set
  INSERT INTO DISTRIBUTION_SET (DISTRIBUTION_SET_CODE, NAME, FUNCTIONAL_AREA_ID, RECORD_STATUS,
         CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
  SELECT 'AUTOTEST_FREETEXT_INVALID', 'AUTOTEST Freetext (non-deliverable)', FUNCTIONAL_AREA_ID,
         RECORD_STATUS, 'AUTOTEST', SYSDATE, 0, RAWTOHEX(SYS_GUID())
  FROM DISTRIBUTION_SET WHERE DISTRIBUTION_SET_CODE = 'FRMW_DISTR_SET_FREE_TEXT';

  -- 4) link the .invalid contact to the new distribution as TO (FORMAT TEXT, like FRMW)
  INSERT INTO DISTRIBUTION_SET_CONTACT (DISTRIBUTION_SET_CODE, COMPANY_CONTACT_ID, RECIPIENT_TYPE,
         FORMAT_CODE, RECORD_STATUS, CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
  VALUES ('AUTOTEST_FREETEXT_INVALID', v_new_oid, 'TO', 'TEXT', 'P', 'AUTOTEST', SYSDATE, 0, v_new_dsc_rec);

  DBMS_OUTPUT.PUT_LINE('Created contact OBJECT_ID=' || v_new_oid || ' + distribution AUTOTEST_FREETEXT_INVALID');
  -- VERIFY first, then COMMIT manually:
  -- COMMIT;
END;
/

-- ---- VERIFY (run before COMMIT) -------------------------------------------------
-- SELECT dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, ccv.DELIVERY_ADDRESS
-- FROM DISTRIBUTION_SET_CONTACT dsc
-- JOIN COMPANY_CONTACT cc ON cc.OBJECT_ID = dsc.COMPANY_CONTACT_ID
-- JOIN COMPANY_CONTACT_VERSION ccv ON ccv.OBJECT_ID = cc.OBJECT_ID
-- WHERE dsc.DISTRIBUTION_SET_CODE = 'AUTOTEST_FREETEXT_INVALID';
-- expect: TO | autotest@example.invalid

-- ---- ROLLBACK / CLEANUP (reverses everything above) -----------------------------
-- DELETE FROM DISTRIBUTION_SET_CONTACT WHERE DISTRIBUTION_SET_CODE='AUTOTEST_FREETEXT_INVALID';
-- DELETE FROM DISTRIBUTION_SET        WHERE DISTRIBUTION_SET_CODE='AUTOTEST_FREETEXT_INVALID';
-- DELETE FROM COMPANY_CONTACT_VERSION WHERE OBJECT_ID IN (SELECT OBJECT_ID FROM COMPANY_CONTACT WHERE OBJECT_CODE='AUTOTEST_INVALID_RCV');
-- DELETE FROM COMPANY_CONTACT         WHERE OBJECT_CODE='AUTOTEST_INVALID_RCV';
-- COMMIT;
