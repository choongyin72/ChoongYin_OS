*** Settings ***
Documentation       EC IUD Test - Process Train (Configuration > Assets > Facility_Objects >
...                 Process Train, CO.0120). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_PROCESS_TRAIN).
...                 Layered: this test -> process_train_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_PT, matching Bank/Berth's convention) rather than a generated
...                 unique code - confirmed absent from OV_PROCESS_TRAIN before this was wired
...                 in (2026-08-23). Every run must complete TC05 (delete) so the code is free
...                 for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    process_train


*** Variables ***
${TEST_CODE}        AUTOTEST_PT
${OBJ_NAME}         AUTOTEST Process Train
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/process_train_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Process Train UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Process Train Screen
    Verify Process Train Record Does Not Exist
    Logout From EC Application

TC02 Insert Process Train Data
    Login To EC Application
    Open Process Train Screen
    Insert Process Train Record And Save
    Verify Process Train Record Exists
    Logout From EC Application

TC03 Update Process Train Data
    Login To EC Application
    Open Process Train Screen
    Update Process Train Record And Save
    Verify Process Train Record Updated
    Logout From EC Application

TC04 Find Process Train Data
    Login To EC Application
    Open Process Train Screen
    Find Process Train Record
    Verify Process Train Record Found
    Logout From EC Application

TC05 Delete Process Train Data
    Login To EC Application
    Open Process Train Screen
    Delete Process Train Record And Save
    Verify Process Train Record Removed
    Logout From EC Application
