*** Settings ***
Documentation       EC IUD Test - Business Unit (Configuration > Assets > Basic Objects >
...                 Business Unit). Manage-Object (OV) screen. DELETE = End Date = Start
...                 Date (true delete in OV_BUSINESS_UNIT). Layered: this test ->
...                 business_unit_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_BU, matching
...                 the other rebuilt screens' convention) rather than a generated unique
...                 code - confirmed absent from OV_BUSINESS_UNIT before this was wired in
...                 (2026-08-22). Every run must complete TC05 (delete) so the code is free
...                 for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching the other rebuilt screens' convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/business_unit_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    business-unit


*** Variables ***
${TEST_CODE}        AUTOTEST_BU
${OBJ_NAME}         AUTOTEST Business Unit
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/business_unit_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Business Unit UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Business Unit Screen
    Verify Business Unit Record Does Not Exist
    Logout From EC Application

TC02 Insert Business Unit Data
    Login To EC Application
    Open Business Unit Screen
    Insert Business Unit Record And Save
    Verify Business Unit Record Exists
    Logout From EC Application

TC03 Update Business Unit Data
    Login To EC Application
    Open Business Unit Screen
    Update Business Unit Record And Save
    Verify Business Unit Record Updated
    Logout From EC Application

TC04 Find Business Unit Data
    Login To EC Application
    Open Business Unit Screen
    Find Business Unit Record
    Verify Business Unit Record Found
    Logout From EC Application

TC05 Delete Business Unit Data
    Login To EC Application
    Open Business Unit Screen
    Delete Business Unit Record And Save
    Verify Business Unit Record Removed
    Logout From EC Application
