*** Settings ***
Documentation       EC IUD Test - State (Configuration > Assets > Basic Objects > State).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STATE).
...                 Layered: this test -> state_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_STATE,
...                 matching Bank/Object List's convention) rather than a generated unique
...                 code - confirmed absent from OV_STATE before this was wired in
...                 (2026-08-22). Every run must complete TC05 (delete) so the code is free
...                 for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Object List's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/state_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    state


*** Variables ***
${TEST_CODE}        AUTOTEST_STATE
${OBJ_NAME}         AUTOTEST State
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/state_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST State UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open State Screen
    Verify State Record Does Not Exist
    Logout From EC Application

TC02 Insert State Data
    Login To EC Application
    Open State Screen
    Insert State Record And Save
    Verify State Record Exists
    Logout From EC Application

TC03 Update State Data
    Login To EC Application
    Open State Screen
    Update State Record And Save
    Verify State Record Updated
    Logout From EC Application

TC04 Find State Data
    Login To EC Application
    Open State Screen
    Find State Record
    Verify State Record Found
    Logout From EC Application

TC05 Delete State Data
    Login To EC Application
    Open State Screen
    Delete State Record And Save
    Verify State Record Removed
    Logout From EC Application
