*** Settings ***
Documentation       EC IUD Test - Production Unit (Configuration > Assets > Basic Objects >
...                 Production Unit). Manage-Object (OV) screen. DELETE = End Date = Start
...                 Date (true delete in OV_PRODUCTIONUNIT). Layered: this test ->
...                 production_unit_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_PU, matching
...                 the other rebuilt screens' convention) rather than a generated unique
...                 code - confirmed absent from OV_PRODUCTIONUNIT before this was wired in
...                 (2026-08-22). Every run must complete TC05 (delete) so the code is free
...                 for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching the other rebuilt screens' convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/production_unit_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    production-unit


*** Variables ***
${TEST_CODE}        AUTOTEST_PU
${OBJ_NAME}         AUTOTEST Production Unit
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/production_unit_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Production Unit UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Production Unit Screen
    Verify Production Unit Record Does Not Exist
    Logout From EC Application

TC02 Insert Production Unit Data
    Login To EC Application
    Open Production Unit Screen
    Insert Production Unit Record And Save
    Verify Production Unit Record Exists
    Logout From EC Application

TC03 Update Production Unit Data
    Login To EC Application
    Open Production Unit Screen
    Update Production Unit Record And Save
    Verify Production Unit Record Updated
    Logout From EC Application

TC04 Find Production Unit Data
    Login To EC Application
    Open Production Unit Screen
    Find Production Unit Record
    Verify Production Unit Record Found
    Logout From EC Application

TC05 Delete Production Unit Data
    Login To EC Application
    Open Production Unit Screen
    Delete Production Unit Record And Save
    Verify Production Unit Record Removed
    Logout From EC Application
