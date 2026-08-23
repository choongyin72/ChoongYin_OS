*** Settings ***
Documentation       EC IUD Test - Reservoir Formation (Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation, CO.0135).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_RESV_FORMATION).
...                 Layered: this test -> reservoir_formation_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_RESVF,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_RESV_FORMATION before this was wired in
...                 (2026-08-23, fresh oracledb connection). Every run must complete TC05
...                 (delete) so the code is free for the next run - EC never lets a DELETED
...                 code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    reservoir_formation


*** Variables ***
${TEST_CODE}        AUTOTEST_RESVF
${OBJ_NAME}         AUTOTEST Reservoir Formation
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/reservoir_formation_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Reservoir Formation UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Reservoir Formation Screen
    Verify Reservoir Formation Record Does Not Exist
    Logout From EC Application

TC02 Insert Reservoir Formation Data
    Login To EC Application
    Open Reservoir Formation Screen
    Insert Reservoir Formation Record And Save
    Verify Reservoir Formation Record Exists
    Logout From EC Application

TC03 Update Reservoir Formation Data
    Login To EC Application
    Open Reservoir Formation Screen
    Update Reservoir Formation Record And Save
    Verify Reservoir Formation Record Updated
    Logout From EC Application

TC04 Find Reservoir Formation Data
    Login To EC Application
    Open Reservoir Formation Screen
    Find Reservoir Formation Record
    Verify Reservoir Formation Record Found
    Logout From EC Application

TC05 Delete Reservoir Formation Data
    Login To EC Application
    Open Reservoir Formation Screen
    Delete Reservoir Formation Record And Save
    Verify Reservoir Formation Record Removed
    Logout From EC Application
