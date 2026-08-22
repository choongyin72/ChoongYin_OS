*** Settings ***
Documentation       EC IUD Test - WBS (Configuration > Assets > Financial Objects > WBS).
...                 Custom-URL OV (no navigator/GO — reload via toolbar Refresh). DELETE =
...                 End Date = Start Date (true delete in OV_FIN_WBS).
...                 Layered: this test -> wbs_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_WBS,
...                 matching Bank/State's convention) rather than a generated unique code -
...                 confirmed absent from OV_FIN_WBS before this was wired in (2026-08-22).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/wbs_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    wbs


*** Variables ***
${TEST_CODE}        AUTOTEST_WBS
${OBJ_NAME}         AUTOTEST WBS
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/wbs_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST WBS UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open WBS Screen
    Verify WBS Record Does Not Exist
    Logout From EC Application

TC02 Insert WBS Data
    Login To EC Application
    Open WBS Screen
    Insert WBS Record And Save
    Verify WBS Record Exists
    Logout From EC Application

TC03 Update WBS Data
    Login To EC Application
    Open WBS Screen
    Update WBS Record And Save
    Verify WBS Record Updated
    Logout From EC Application

TC04 Find WBS Data
    Login To EC Application
    Open WBS Screen
    Find WBS Record
    Verify WBS Record Found
    Logout From EC Application

TC05 Delete WBS Data
    Login To EC Application
    Open WBS Screen
    Delete WBS Record And Save
    Verify WBS Record Removed
    Logout From EC Application
