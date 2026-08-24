*** Settings ***
Documentation       EC IUD Test - Document Date Term (Configuration > Assets > Date Objects >
...                 Document Date Term, CD.0107). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_DOC_DATE_TERM). Layered: this test ->
...                 document_date_term_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_DOCUMENT_DATE_TERM,
...                 matching Bank's own fixed-code convention) rather than a generated unique code -
...                 confirmed absent from OV_DOC_DATE_TERM before this was wired in (fresh DB
...                 query, 2026-08-24). Every run must complete TC05 (delete) so the code is free
...                 for the next run - EC never lets a DELETED code be reused, but this fixed code
...                 only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on
...                 ONE browser opened once in Suite Setup - not 5 separate browser launches. This
...                 is a conscious tradeoff: 5 real logins instead of 1 costs real runtime, and
...                 TC03/TC04/TC05 still depend on TC02's inserted record existing (the per-TC
...                 login/logout makes each TC LOOK self-contained, it does not remove that data
...                 dependency) - accepted deliberately for a client-readable process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-24): see
...                 document_date_term_page.resource's Documentation for what changed vs the prior
...                 OLD-pattern build.

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/document_date_term_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    document_date_term    date-objects


*** Variables ***
${TEST_CODE}        AUTOTEST_DOCUMENT_DATE_TERM
${OBJ_NAME}         AUTOTEST Document Date Term
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/document_date_term_update.properties -
# Verify Document Date Term Record Updated (TC03) screen-verifies them against what that file
# actually set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Document Date Term UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Document Date Term Screen
    Verify Document Date Term Record Does Not Exist
    Logout From EC Application

TC02 Insert Document Date Term Data
    Login To EC Application
    Open Document Date Term Screen
    Insert Document Date Term Record And Save
    Verify Document Date Term Record Exists
    Logout From EC Application

TC03 Update Document Date Term Data
    Login To EC Application
    Open Document Date Term Screen
    Update Document Date Term Record And Save
    Verify Document Date Term Record Updated
    Logout From EC Application

TC04 Find Document Date Term Data
    Login To EC Application
    Open Document Date Term Screen
    Find Document Date Term Record
    Verify Document Date Term Record Found
    Logout From EC Application

TC05 Delete Document Date Term Data
    Login To EC Application
    Open Document Date Term Screen
    Delete Document Date Term Record And Save
    Verify Document Date Term Record Removed
    Logout From EC Application
