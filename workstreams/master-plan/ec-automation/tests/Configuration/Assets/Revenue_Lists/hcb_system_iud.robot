*** Settings ***
Documentation       EC IUD Test - HCB System (Configuration > Assets > Revenue Lists > HCB System, CD.0097).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BALANCE).
...                 Layered: this test -> hcb_system_page (T3) -> manage_object (T2) + common (T1).
...                 Bank-pattern conversion (2026-08-25): replaces the older driver that used a
...                 generated timestamp code and called the raw DbVerify keywords (Field Should Equal In
...                 View / *Should Exist In DB) directly here - a deviation from Bank's owner-requested
...                 2026-08-18 PURE-SCREEN-verification convention (same deviation class fixed on
...                 Calculation Context/Document Template/Royalty Depositor/Stream Item Category, GitHub
...                 Issue #504). NEVER touch existing data. Uses a FIXED test code (AUTOTEST_HCB,
...                 matching Bank/Royalty Depositor's own convention) confirmed absent from OV_BALANCE
...                 before this was wired in (live fresh-connection query, 2026-08-25). Every run must
...                 complete TC05 (delete) so the code is free for the next run - EC never lets a
...                 DELETED code be reused, but this fixed code only stays reusable if each run actually
...                 cleans up after itself. EACH test case does its own real Login/Logout on ONE browser
...                 opened once in Suite Setup - matches Bank's convention.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Lists/hcb_system_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    hcb_system


*** Variables ***
${TEST_CODE}        AUTOTEST_HCB
${OBJ_NAME}         Automation Test HCB System
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/hcb_system_update.properties - TC03 verifies against what that
# file actually set, not an independent assumption.
${OBJ_NAME_UPD}     Automation Test HCB System UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open HCB System Screen
    Verify HCB System Record Does Not Exist
    Logout From EC Application

TC02 Insert HCB System Data
    Login To EC Application
    Open HCB System Screen
    Insert HCB System Record And Save
    Verify HCB System Record Exists
    Logout From EC Application

TC03 Update HCB System Data
    Login To EC Application
    Open HCB System Screen
    Update HCB System Record And Save
    Verify HCB System Record Updated
    Logout From EC Application

TC04 Find HCB System Data
    Login To EC Application
    Open HCB System Screen
    Find HCB System Record
    Verify HCB System Record Found
    Logout From EC Application

TC05 Delete HCB System Data
    Login To EC Application
    Open HCB System Screen
    Delete HCB System Record And Save
    Verify HCB System Record Removed
    Logout From EC Application
