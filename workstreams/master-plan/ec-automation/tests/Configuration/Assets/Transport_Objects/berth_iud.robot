*** Settings ***
Documentation       EC IUD Test - Berth (Configuration > Assets > Transport Objects > Berth, CO.2012).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BERTH).
...                 Layered: this test -> berth_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_BERTH,
...                 matching Bank/State's convention) rather than a generated unique code -
...                 confirmed absent from OV_BERTH before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/berth_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    berth


*** Variables ***
${TEST_CODE}        AUTOTEST_BERTH
${OBJ_NAME}         AUTOTEST Berth
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/berth_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Berth UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Berth Screen
    Verify Berth Record Does Not Exist
    Logout From EC Application

TC02 Insert Berth Data
    Login To EC Application
    Open Berth Screen
    Insert Berth Record And Save
    Verify Berth Record Exists
    Logout From EC Application

TC03 Update Berth Data
    Login To EC Application
    Open Berth Screen
    Update Berth Record And Save
    Verify Berth Record Updated
    Logout From EC Application

TC04 Find Berth Data
    Login To EC Application
    Open Berth Screen
    Find Berth Record
    Verify Berth Record Found
    Logout From EC Application

TC05 Delete Berth Data
    Login To EC Application
    Open Berth Screen
    Delete Berth Record And Save
    Verify Berth Record Removed
    Logout From EC Application
