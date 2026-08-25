*** Settings ***
Documentation       EC IUD Test - Data Extract Setup (Configuration > Assets > Data_Mapping_Objects >
...                 Data Extract Setup, SP.0043). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_SUMMARY_SETUP).
...                 Layered: this test -> data_extract_setup_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_DXS, matching
...                 Bank/State/Data Extract Set's convention) rather than a generated unique code -
...                 confirmed absent from OV_SUMMARY_SETUP before this was wired in (2026-08-25).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/State/Data Extract Set's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_setup_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    data_extract_setup


*** Variables ***
${TEST_CODE}        AUTOTEST_DXS
${OBJ_NAME}         AUTOTEST Data Extract Setup
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/data_extract_setup_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Data Extract Setup UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Data Extract Setup Screen
    Verify Data Extract Setup Record Does Not Exist
    Logout From EC Application

TC02 Insert Data Extract Setup Data
    Login To EC Application
    Open Data Extract Setup Screen
    Insert Data Extract Setup Record And Save
    Verify Data Extract Setup Record Exists
    Logout From EC Application

TC03 Update Data Extract Setup Data
    Login To EC Application
    Open Data Extract Setup Screen
    Update Data Extract Setup Record And Save
    Verify Data Extract Setup Record Updated
    Logout From EC Application

TC04 Find Data Extract Setup Data
    Login To EC Application
    Open Data Extract Setup Screen
    Find Data Extract Setup Record
    Verify Data Extract Setup Record Found
    Logout From EC Application

TC05 Delete Data Extract Setup Data
    Login To EC Application
    Open Data Extract Setup Screen
    Delete Data Extract Setup Record And Save
    Verify Data Extract Setup Record Removed
    Logout From EC Application
