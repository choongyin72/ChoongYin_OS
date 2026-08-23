*** Settings ***
Documentation       EC IUD Test - Data Extract Set (Configuration > Assets > Data_Mapping_Objects >
...                 Data Extract Set, SP.0049). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_SUMMARY_SET).
...                 Layered: this test -> data_extract_set_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_DXT, matching
...                 Bank/Berth's convention) rather than a generated unique code - confirmed
...                 absent from OV_SUMMARY_SET before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_set_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    data_extract_set


*** Variables ***
${TEST_CODE}        AUTOTEST_DXT
${OBJ_NAME}         AUTOTEST Data Extract Set
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/data_extract_set_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Data Extract Set UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Data Extract Set Screen
    Verify Data Extract Set Record Does Not Exist
    Logout From EC Application

TC02 Insert Data Extract Set Data
    Login To EC Application
    Open Data Extract Set Screen
    Insert Data Extract Set Record And Save
    Verify Data Extract Set Record Exists
    Logout From EC Application

TC03 Update Data Extract Set Data
    Login To EC Application
    Open Data Extract Set Screen
    Update Data Extract Set Record And Save
    Verify Data Extract Set Record Updated
    Logout From EC Application

TC04 Find Data Extract Set Data
    Login To EC Application
    Open Data Extract Set Screen
    Find Data Extract Set Record
    Verify Data Extract Set Record Found
    Logout From EC Application

TC05 Delete Data Extract Set Data
    Login To EC Application
    Open Data Extract Set Screen
    Delete Data Extract Set Record And Save
    Verify Data Extract Set Record Removed
    Logout From EC Application
