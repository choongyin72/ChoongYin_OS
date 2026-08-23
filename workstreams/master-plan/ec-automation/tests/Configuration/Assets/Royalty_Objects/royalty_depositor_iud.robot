*** Settings ***
Documentation       EC IUD Test - Royalty Depositor (Configuration > Assets > Royalty Objects >
...                 Royalty Depositor). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in ov_royalty_depositor). Layered: this test -> royalty_depositor_page
...                 (T3) -> manage_object (T2) + common (T1). Bank-pattern conversion (Batch 5,
...                 2026-08-23): property-file-driven + label-driven + T2-consolidated, replacing
...                 the older hardcoded-field-id driver. NEVER touch existing data. Uses a FIXED
...                 test code (AUTOTEST_ROYALTY_DEP, matching Bank/Account's own convention)
...                 confirmed absent from ov_royalty_depositor before this was wired in (live
...                 fresh-connection query, 2026-08-23). Every run must complete TC05 (delete) so
...                 the code is free for the next run - EC never lets a DELETED code be reused,
...                 but this fixed code only stays reusable if each run actually cleans up after
...                 itself. EACH test case does its own real Login/Logout on ONE browser opened
...                 once in Suite Setup - matches Bank's convention.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    royalty_depositor


*** Variables ***
${TEST_CODE}        AUTOTEST_ROYALTY_DEP
${OBJ_NAME}         Automation Test Royalty Depositor
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/royalty_depositor_update.properties - TC03 verifies against
# what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}     Automation Test Royalty Depositor UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Royalty Depositor Screen
    Verify Royalty Depositor Record Does Not Exist
    Logout From EC Application

TC02 Insert Royalty Depositor Data
    Login To EC Application
    Open Royalty Depositor Screen
    Insert Royalty Depositor Record And Save
    Verify Royalty Depositor Record Exists
    Royalty Depositor Should Exist In DB    ${TEST_CODE}
    Logout From EC Application

TC03 Update Royalty Depositor Data
    Login To EC Application
    Open Royalty Depositor Screen
    Update Royalty Depositor Record And Save
    Verify Royalty Depositor Record Updated
    Logout From EC Application

TC04 Find Royalty Depositor Data
    Login To EC Application
    Open Royalty Depositor Screen
    Find Royalty Depositor Record
    Verify Royalty Depositor Record Found
    Logout From EC Application

TC05 Delete Royalty Depositor Data
    Login To EC Application
    Open Royalty Depositor Screen
    Delete Royalty Depositor Record And Save
    Verify Royalty Depositor Record Removed
    Logout From EC Application


*** Keywords ***
Royalty Depositor Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_royalty_depositor.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_royalty_depositor    ${code}
