-- ECSR-35263 — Fix: email subject/body production-date != attached report date
-- ROOT CAUSE: ZWP_P_MAIL_UTIL.getReportDate(p_message_code) resolves the date by template TYPE
--   (latest report of that type, ORDER BY created_date DESC). The scheduled business action
--   ZWP_UPD_MHM_SUBJECT_AND_BODY (-> updateMsgOutFromMsgTemplate / updateMHMFromMsgTemplate) then
--   stamps that ONE date onto {production_day} in the SUBJECT/BODY of EVERY READY message of that type,
--   while each attachment keeps its own correct date  => subject date != attachment date when 2+ dates
--   of the same report are processed together.
-- FIX (Option A): give each message a link to its OWN report instance, and resolve the date per message.
--   1) MESSAGE_ATTACHMENT gets a REPORT_NO column (addAttachmentToMessage already receives p_report_no).
--   2) new getReportDate(p_message_no) overload resolves report_date via the message's own attachment.
--   3) the two refresh procedures resolve per-message, falling back to the old by-type logic when a
--      pre-existing message has no REPORT_NO (backward compatible).
-- DELIVERY: changes 2-4 are edits to the repeatable package files
--   (R__0400_ZWP_P_MAIL_UTIL_head.sql + R__0500_ZWP_P_MAIL_UTIL_body.sql); change 1 is a versioned migration.
-- TEST: repro on plutodev (R_PLU_DAILY_PARTNER, 2 dates) -> distinct subjects matching attachments.
-- ============================================================================================

-- ---- (1) SCHEMA — versioned migration (idempotent) -----------------------------------------
DECLARE
  n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM all_tab_columns
   WHERE owner='ECKERNEL_EC' AND table_name='MESSAGE_ATTACHMENT' AND column_name='REPORT_NO';
  IF n = 0 THEN
    EXECUTE IMMEDIATE 'ALTER TABLE MESSAGE_ATTACHMENT ADD (REPORT_NO NUMBER)';
  END IF;
END;
/

-- ---- (2) HEAD (R__0400_ZWP_P_MAIL_UTIL_head.sql) — add the overload declaration -------------
-- Add next to the existing getReportDate declaration:
--     FUNCTION getReportDate(p_message_no NUMBER) RETURN VARCHAR2;

-- ---- (3) BODY (R__0500_ZWP_P_MAIL_UTIL_body.sql) — addAttachmentToMessage: store report_no ---
-- In the report-attachment INSERT (currently ~line 214), add REPORT_NO = p_report_no:
--   BEFORE:
--     INSERT INTO message_attachment (message_no, attachment_no, attachment, file_name)
--     VALUES (p_message_no, ecdp_system_key.assignNextNumber('MESSAGE_ATTACHMENT'), lb_content_unzipped, lv_file_name);
--   AFTER:
--     INSERT INTO message_attachment (message_no, attachment_no, attachment, file_name, report_no)
--     VALUES (p_message_no, ecdp_system_key.assignNextNumber('MESSAGE_ATTACHMENT'), lb_content_unzipped, lv_file_name, p_report_no);
--   (the file_attachment INSERT ~line 228 stays as-is — no report there.)

-- ---- (4) BODY — new per-message overload (place beside the existing getReportDate) ----------
--   FUNCTION getReportDate(p_message_no NUMBER) RETURN VARCHAR2
--   IS
--       lv_return_value VARCHAR2(12);
--   BEGIN
--       SELECT to_char(report_date, 'DD Mon YYYY') INTO lv_return_value
--         FROM ( SELECT rg.report_date
--                  FROM message_attachment ma
--                  JOIN tv_report_generated rg ON rg.report_no = ma.report_no
--                 WHERE ma.message_no = p_message_no
--                   AND ma.report_no IS NOT NULL
--                 ORDER BY rg.created_date DESC )
--        WHERE ROWNUM = 1;
--       RETURN lv_return_value;
--   EXCEPTION WHEN NO_DATA_FOUND THEN
--       RETURN NULL;   -- caller falls back to the by-type resolution
--   END getReportDate;

-- ---- (5) BODY — resolve per-message in BOTH refresh procedures (backward-compatible) --------
-- updateMsgOutFromMsgTemplate (~line 429):
--   BEFORE:  lv_report_date := getReportDate(lv_msg_type);
--   AFTER:   lv_report_date := NVL(getReportDate(rec.MESSAGE_NO), getReportDate(lv_msg_type));
-- updateMHMFromMsgTemplate (~lines 384-385): same NVL(getReportDate(<message_no>), getReportDate(MSG_TYPE))
--   pattern, using that loop's message id.
