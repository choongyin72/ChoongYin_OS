*** Settings ***
Documentation       EC IUD Test - Bank Account (Configuration > Assets > Financial Objects >
...                 Bank Account). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_BANK_ACCOUNT). Layered: this test -> bank_account_page
...                 (T3) -> manage_object (T2) + common (T1).
...                 Rebuilt 2026-08-23 (Batch 11) from the OLDER hardcoded-field-id/generated-
...                 timestamp-code/single-Suite-Setup-login pattern to Bank/Berth's label-driven,
...                 properties-file-driven, T2-consolidated, per-TC-login pattern (see
...                 `tmp/batch11_shared_findings.md`). Uses a FIXED test code (AUTOTEST_BACC,
...                 confirmed absent from OV_BANK_ACCOUNT via a fresh oracledb query before this
...                 build) rather than a generated unique code - every run must complete TC05
...                 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matching Bank's/Berth's process-flow report convention.

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/bank_account_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    bank-account


*** Variables ***
${TEST_CODE}        AUTOTEST_BACC
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Bank Account Screen
    Verify Bank Account Record Does Not Exist
    Logout From EC Application

TC02 Insert Bank Account Data
    Login To EC Application
    Open Bank Account Screen
    Insert Bank Account Record And Save
    Verify Bank Account Record Exists
    Logout From EC Application

TC03 Update Bank Account Data
    Login To EC Application
    Open Bank Account Screen
    Update Bank Account Record And Save
    Verify Bank Account Record Updated
    Logout From EC Application

TC04 Find Bank Account Data
    Login To EC Application
    Open Bank Account Screen
    Find Bank Account Record
    Verify Bank Account Record Found
    Logout From EC Application

TC05 Delete Bank Account Data
    Login To EC Application
    Open Bank Account Screen
    Delete Bank Account Record And Save
    Verify Bank Account Record Removed
    Logout From EC Application
