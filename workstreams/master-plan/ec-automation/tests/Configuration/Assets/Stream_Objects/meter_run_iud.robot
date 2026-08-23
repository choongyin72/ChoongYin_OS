*** Settings ***
Documentation       EC IUD Test - Meter Run (Configuration > Assets > Stream Objects > Meter Run, CO.0091).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_METER_RUN).
...                 Layered: this test -> meter_run_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_METER_RUN,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_METER_RUN before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/meter_run_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    meter_run


*** Variables ***
${TEST_CODE}        AUTOTEST_METER_RUN
${OBJ_NAME}         AUTOTEST Meter Run
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/meter_run_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Meter Run UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Meter Run Screen
    Verify Meter Run Record Does Not Exist
    Logout From EC Application

TC02 Insert Meter Run Data
    Login To EC Application
    Open Meter Run Screen
    Insert Meter Run Record And Save
    Verify Meter Run Record Exists
    Logout From EC Application

TC03 Update Meter Run Data
    Login To EC Application
    Open Meter Run Screen
    Update Meter Run Record And Save
    Verify Meter Run Record Updated
    Logout From EC Application

TC04 Find Meter Run Data
    Login To EC Application
    Open Meter Run Screen
    Find Meter Run Record
    Verify Meter Run Record Found
    Logout From EC Application

TC05 Delete Meter Run Data
    Login To EC Application
    Open Meter Run Screen
    Delete Meter Run Record And Save
    Verify Meter Run Record Removed
    Logout From EC Application
