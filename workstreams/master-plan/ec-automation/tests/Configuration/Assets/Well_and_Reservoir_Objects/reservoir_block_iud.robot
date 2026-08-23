*** Settings ***
Documentation       EC IUD Test - Reservoir Block (Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block, CO.0133).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_RESV_BLOCK).
...                 Layered: this test -> reservoir_block_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_RESVB,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_RESV_BLOCK before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    reservoir_block


*** Variables ***
${TEST_CODE}        AUTOTEST_RESVB
${OBJ_NAME}         AUTOTEST Reservoir Block
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/reservoir_block_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Reservoir Block UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Reservoir Block Screen
    Verify Reservoir Block Record Does Not Exist
    Logout From EC Application

TC02 Insert Reservoir Block Data
    Login To EC Application
    Open Reservoir Block Screen
    Insert Reservoir Block Record And Save
    Verify Reservoir Block Record Exists
    Logout From EC Application

TC03 Update Reservoir Block Data
    Login To EC Application
    Open Reservoir Block Screen
    Update Reservoir Block Record And Save
    Verify Reservoir Block Record Updated
    Logout From EC Application

TC04 Find Reservoir Block Data
    Login To EC Application
    Open Reservoir Block Screen
    Find Reservoir Block Record
    Verify Reservoir Block Record Found
    Logout From EC Application

TC05 Delete Reservoir Block Data
    Login To EC Application
    Open Reservoir Block Screen
    Delete Reservoir Block Record And Save
    Verify Reservoir Block Record Removed
    Logout From EC Application
