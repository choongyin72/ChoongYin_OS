*** Settings ***
Documentation       EC IUD Test - Storage Flow (Configuration > Assets > Tank_and_Storage_Objects > Storage Flow, CO.2091).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STORAGE_FLOW).
...                 Layered: this test -> storage_flow_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_STFLOW,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_STORAGE_FLOW before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_flow_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    storage_flow


*** Variables ***
${TEST_CODE}        AUTOTEST_STFLOW
${OBJ_NAME}         AUTOTEST Storage Flow
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/storage_flow_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Storage Flow UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Storage Flow Screen
    Verify Storage Flow Record Does Not Exist
    Logout From EC Application

TC02 Insert Storage Flow Data
    Login To EC Application
    Open Storage Flow Screen
    Insert Storage Flow Record And Save
    Verify Storage Flow Record Exists
    Logout From EC Application

TC03 Update Storage Flow Data
    Login To EC Application
    Open Storage Flow Screen
    Update Storage Flow Record And Save
    Verify Storage Flow Record Updated
    Logout From EC Application

TC04 Find Storage Flow Data
    Login To EC Application
    Open Storage Flow Screen
    Find Storage Flow Record
    Verify Storage Flow Record Found
    Logout From EC Application

TC05 Delete Storage Flow Data
    Login To EC Application
    Open Storage Flow Screen
    Delete Storage Flow Record And Save
    Verify Storage Flow Record Removed
    Logout From EC Application
