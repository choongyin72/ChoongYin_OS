*** Settings ***
Documentation       EC IUD Test - Account Mapping (Configuration > Assets > Financial
...                 Objects > Account Mapping). Manage-Object (OV) screen. DELETE = End
...                 Date = Start Date (true delete in OV_FIN_ACCOUNT_MAPPING).
...                 Layered: this test -> account_mapping_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_AM) rather than a generated unique code - confirmed absent from
...                 OV_FIN_ACCOUNT_MAPPING before this was wired in. Every run must complete
...                 TC05 (delete) so the code is free for the next run - EC never lets a
...                 DELETED code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches. Converted from the old
...                 hardcoded-field-id pattern to the label-driven, properties-file-driven "Bank
...                 pattern" (Batch 6, 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    account-mapping


*** Variables ***
${TEST_CODE}        AUTOTEST_AM
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Account Mapping Screen
    Verify Account Mapping Record Does Not Exist
    Logout From EC Application

TC02 Insert Account Mapping Data
    Login To EC Application
    Open Account Mapping Screen
    Insert Account Mapping Record And Save
    Verify Account Mapping Record Exists
    Logout From EC Application

TC03 Update Account Mapping Data
    Login To EC Application
    Open Account Mapping Screen
    Update Account Mapping Record And Save
    Verify Account Mapping Record Updated
    Logout From EC Application

TC04 Find Account Mapping Data
    Login To EC Application
    Open Account Mapping Screen
    Find Account Mapping Record
    Verify Account Mapping Record Found
    Logout From EC Application

TC05 Delete Account Mapping Data
    Login To EC Application
    Open Account Mapping Screen
    Delete Account Mapping Record And Save
    Verify Account Mapping Record Removed
    Logout From EC Application
