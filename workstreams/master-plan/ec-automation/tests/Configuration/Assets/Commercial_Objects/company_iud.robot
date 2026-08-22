*** Settings ***
Documentation       EC IUD Test - Company (Configuration > Assets > Commercial Objects >
...                 Company). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_COMPANY). Layered: this test -> company_page (T3) ->
...                 manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_COMPANY,
...                 matching the other rebuilt screens' convention) rather than a generated
...                 unique code - confirmed absent from OV_COMPANY before this was wired in
...                 (2026-08-22). Every run must complete TC05 (delete) so the code is free
...                 for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching the other rebuilt screens' convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/company_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    company


*** Variables ***
${TEST_CODE}        AUTOTEST_COMPANY
${OBJ_NAME}         AUTOTEST Company
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/company_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Company UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Company Screen
    Verify Company Record Does Not Exist
    Logout From EC Application

TC02 Insert Company Data
    Login To EC Application
    Open Company Screen
    Insert Company Record And Save
    Verify Company Record Exists
    Logout From EC Application

TC03 Update Company Data
    Login To EC Application
    Open Company Screen
    Update Company Record And Save
    Verify Company Record Updated
    Logout From EC Application

TC04 Find Company Data
    Login To EC Application
    Open Company Screen
    Find Company Record
    Verify Company Record Found
    Logout From EC Application

TC05 Delete Company Data
    Login To EC Application
    Open Company Screen
    Delete Company Record And Save
    Verify Company Record Removed
    Logout From EC Application
