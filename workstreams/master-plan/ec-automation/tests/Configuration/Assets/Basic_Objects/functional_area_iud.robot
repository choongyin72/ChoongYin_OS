*** Settings ***
Documentation       EC IUD Test - Functional Area (Configuration > Assets > Basic Objects >
...                 Functional Area). Manage-Object (OV) screen. DELETE = End Date = Start
...                 Date (true delete in OV_FUNCTIONAL_AREA). Layered: this test ->
...                 functional_area_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_FA, matching
...                 Bank/Object List/State/Region's convention) rather than a generated
...                 unique code - confirmed absent from OV_FUNCTIONAL_AREA before this was
...                 wired in (2026-08-22). Every run must complete TC05 (delete) so the code
...                 is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Object List/State/Region's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/functional_area_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    functional-area


*** Variables ***
${TEST_CODE}        AUTOTEST_FA
${OBJ_NAME}         AUTOTEST Functional Area
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/functional_area_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Functional Area UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Functional Area Screen
    Verify Functional Area Record Does Not Exist
    Logout From EC Application

TC02 Insert Functional Area Data
    Login To EC Application
    Open Functional Area Screen
    Insert Functional Area Record And Save
    Verify Functional Area Record Exists
    Logout From EC Application

TC03 Update Functional Area Data
    Login To EC Application
    Open Functional Area Screen
    Update Functional Area Record And Save
    Verify Functional Area Record Updated
    Logout From EC Application

TC04 Find Functional Area Data
    Login To EC Application
    Open Functional Area Screen
    Find Functional Area Record
    Verify Functional Area Record Found
    Logout From EC Application

TC05 Delete Functional Area Data
    Login To EC Application
    Open Functional Area Screen
    Delete Functional Area Record And Save
    Verify Functional Area Record Removed
    Logout From EC Application
