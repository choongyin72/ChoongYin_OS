*** Settings ***
Documentation       EC IUD Test - Calculation Group Context (Configuration > Assets > Calculation_Objects >
...                 Calculation Group Context, CO.0245). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_CALC_GRP_CONTEXT).
...                 Layered: this test -> calculation_group_context_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_CGC_BANK, batch 7, 2026-08-23) rather than a generated unique code -
...                 confirmed absent from OV_CALC_GRP_CONTEXT before this was wired in. Every run
...                 must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout (matching Bank's convention) on ONE
...                 browser opened once in Suite Setup - not 5 separate browser launches.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/calculation_group_context_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    calculation_group_context


*** Variables ***
${TEST_CODE}        AUTOTEST_CGC_BANK
${OBJ_NAME}         AUTOTEST Calculation Group Context Bank
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/calculation_group_context_update.properties - TC03 verifies
# against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Calculation Group Context Bank UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Calculation Group Context Screen
    Verify Calculation Group Context Record Does Not Exist
    Logout From EC Application

TC02 Insert Calculation Group Context Data
    Login To EC Application
    Open Calculation Group Context Screen
    Insert Calculation Group Context Record And Save
    Verify Calculation Group Context Record Exists
    Logout From EC Application

TC03 Update Calculation Group Context Data
    Login To EC Application
    Open Calculation Group Context Screen
    Update Calculation Group Context Record And Save
    Verify Calculation Group Context Record Updated
    Logout From EC Application

TC04 Find Calculation Group Context Data
    Login To EC Application
    Open Calculation Group Context Screen
    Find Calculation Group Context Record
    Verify Calculation Group Context Record Found
    Logout From EC Application

TC05 Delete Calculation Group Context Data
    Login To EC Application
    Open Calculation Group Context Screen
    Delete Calculation Group Context Record And Save
    Verify Calculation Group Context Record Removed
    Logout From EC Application
