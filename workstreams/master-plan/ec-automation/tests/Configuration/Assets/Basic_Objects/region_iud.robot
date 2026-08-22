*** Settings ***
Documentation       EC IUD Test - Region (Configuration > Assets > Basic Objects > Region).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_REGION).
...                 Layered: this test -> region_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_REGION,
...                 matching Bank/Object List/State's convention) rather than a generated unique
...                 code - confirmed absent from OV_REGION before this was wired in (2026-08-22).
...                 Every run must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Object List/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/region_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    region


*** Variables ***
${TEST_CODE}        AUTOTEST_REGION
${OBJ_NAME}         AUTOTEST Region
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/region_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Region UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Region Screen
    Verify Region Record Does Not Exist
    Logout From EC Application

TC02 Insert Region Data
    Login To EC Application
    Open Region Screen
    Insert Region Record And Save
    Verify Region Record Exists
    Logout From EC Application

TC03 Update Region Data
    Login To EC Application
    Open Region Screen
    Update Region Record And Save
    Verify Region Record Updated
    Logout From EC Application

TC04 Find Region Data
    Login To EC Application
    Open Region Screen
    Find Region Record
    Verify Region Record Found
    Logout From EC Application

TC05 Delete Region Data
    Login To EC Application
    Open Region Screen
    Delete Region Record And Save
    Verify Region Record Removed
    Logout From EC Application
