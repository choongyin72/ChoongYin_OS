*** Settings ***
Documentation       EC IUD Test - Document Sequence (Configuration > Assets > Revenue
...                 Document Objects > Document Sequence, CD.0109). Custom-URL OV (no
...                 navigator/GO at all - grid nav:form:T_data renders directly on open).
...                 DELETE = End Date = Start Date (true delete in OV_DOC_SEQUENCE).
...                 Layered: this test -> document_sequence_page (T3) -> manage_object (T2)
...                 + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_DOCUMENT_SEQUENCE, matching Bank/Report Context's convention)
...                 rather than a generated unique code - confirmed absent from
...                 OV_DOC_SEQUENCE before this was wired in (2026-08-25). Every run must
...                 complete TC05 (delete) so the code is free for the next run - EC never
...                 lets a DELETED code be reused, but this fixed code only stays reusable
...                 if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened
...                 once in Suite Setup, matching Bank/Report Context's convention
...                 (docs/rf-suite-styles.md).
...                 Bank-pattern conversion (2026-08-25): upgraded from the older
...                 timestamped-code/label-driven/inline-DB-verify shape (4 TCs, no TC04
...                 Find, DB-verify calls embedded directly in this file) to the
...                 properties-file-driven, T2-consolidated, PURE SCREEN verification
...                 pattern - matches Report Context (RP.0007), the precedent for a
...                 custom-URL OV screen built to the full Bank pattern.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Document_Objects/document_sequence_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    document_sequence


*** Variables ***
${TEST_CODE}        AUTOTEST_DOCUMENT_SEQUENCE
${OBJ_NAME}         AUTOTEST DOCUMENT SEQUENCE
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/document_sequence_update.properties - TC03 verifies
# against it.
${OBJ_NAME_UPD}     AUTOTEST DOCUMENT SEQUENCE UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Document Sequence Screen
    Verify Document Sequence Record Does Not Exist
    Logout From EC Application

TC02 Insert Document Sequence Data
    Login To EC Application
    Open Document Sequence Screen
    Insert Document Sequence Record And Save
    Verify Document Sequence Record Exists
    Logout From EC Application

TC03 Update Document Sequence Data
    Login To EC Application
    Open Document Sequence Screen
    Update Document Sequence Record And Save
    Verify Document Sequence Record Updated
    Logout From EC Application

TC04 Find Document Sequence Data
    Login To EC Application
    Open Document Sequence Screen
    Find Document Sequence Record
    Verify Document Sequence Record Found
    Logout From EC Application

TC05 Delete Document Sequence Data
    Login To EC Application
    Open Document Sequence Screen
    Delete Document Sequence Record And Save
    Verify Document Sequence Record Removed
    Logout From EC Application
