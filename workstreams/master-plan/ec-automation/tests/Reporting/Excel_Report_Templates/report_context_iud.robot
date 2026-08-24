*** Settings ***
Documentation       EC IUD Test - Report Context (Reporting > Excel Report Templates >
...                 Report Context, RP.0007). Custom-URL OV (no navigator/GO at all - grid
...                 nav:form:T_data renders directly on open). DELETE = End Date = Start Date
...                 (true delete in OV_REPT_CONTEXT).
...                 Layered: this test -> report_context_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_REPORT_CONTEXT,
...                 matching Bank/WBS's convention) rather than a generated unique code -
...                 confirmed absent from OV_REPT_CONTEXT before this was wired in (2026-08-24).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/WBS's convention (docs/rf-suite-styles.md).

Resource            ../../../pageobjects/Reporting/Excel_Report_Templates/report_context_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    report_context


*** Variables ***
${TEST_CODE}        AUTOTEST_REPORT_CONTEXT
${OBJ_NAME}         AUTOTEST REPORT CONTEXT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/report_context_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST REPORT CONTEXT UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Report Context Screen
    Verify Report Context Record Does Not Exist
    Logout From EC Application

TC02 Insert Report Context Data
    Login To EC Application
    Open Report Context Screen
    Insert Report Context Record And Save
    Verify Report Context Record Exists
    Logout From EC Application

TC03 Update Report Context Data
    Login To EC Application
    Open Report Context Screen
    Update Report Context Record And Save
    Verify Report Context Record Updated
    Logout From EC Application

TC04 Find Report Context Data
    Login To EC Application
    Open Report Context Screen
    Find Report Context Record
    Verify Report Context Record Found
    Logout From EC Application

TC05 Delete Report Context Data
    Login To EC Application
    Open Report Context Screen
    Delete Report Context Record And Save
    Verify Report Context Record Removed
    Logout From EC Application
