*** Settings ***
Documentation       EC IUD Test - Document Received Term (Configuration > Assets > Date Objects >
...                 Document Received Term, CD.0108). Manage-Object (OV, date-effective) screen.
...                 DELETE = End Date = Start Date (true delete in OV_DOC_RECEIVED_TERM).
...                 Layered: this test -> document_received_term_page (T3) -> manage_object (T2)
...                 + common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_DRT, matching Bank/Berth/Port's convention) rather than a
...                 generated unique code - confirmed absent from OV_DOC_RECEIVED_TERM before
...                 this was wired in (2026-08-24). Every run must complete TC05 (delete) so the
...                 code is free for the next run - EC never lets a DELETED code be reused, but
...                 this fixed code only stays reusable if each run actually cleans up after
...                 itself. EACH test case does its own real Login/Logout on ONE browser opened
...                 once in Suite Setup, matching Bank/Berth/Port's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/document_received_term_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    document-received-term    date-objects


*** Variables ***
${TEST_CODE}        AUTOTEST_DRT
${OBJ_NAME}         AUTOTEST Document Received Term
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/document_received_term_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Document Received Term UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Document Received Term Screen
    Verify Document Received Term Record Does Not Exist
    Logout From EC Application

TC02 Insert Document Received Term Data
    Login To EC Application
    Open Document Received Term Screen
    Insert Document Received Term Record And Save
    Verify Document Received Term Record Exists
    Logout From EC Application

TC03 Update Document Received Term Data
    Login To EC Application
    Open Document Received Term Screen
    Update Document Received Term Record And Save
    Verify Document Received Term Record Updated
    Logout From EC Application

TC04 Find Document Received Term Data
    Login To EC Application
    Open Document Received Term Screen
    Find Document Received Term Record
    Verify Document Received Term Record Found
    Logout From EC Application

TC05 Delete Document Received Term Data
    Login To EC Application
    Open Document Received Term Screen
    Delete Document Received Term Record And Save
    Verify Document Received Term Record Removed
    Logout From EC Application
