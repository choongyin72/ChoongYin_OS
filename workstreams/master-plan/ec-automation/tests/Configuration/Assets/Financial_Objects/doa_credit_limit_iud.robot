*** Settings ***
Documentation       EC IUD Test - DOA Credit Limit (Configuration > Assets > Financial Objects >
...                 DOA Credit Limit). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_DOA_CREDIT_LIMIT). Layered: this test ->
...                 doa_credit_limit_page (T3) -> manage_object (T2) + common (T1). NEVER touch
...                 existing data. Uses a FIXED test code (AUTOTEST_DOA, matching Bank/VAT Code's
...                 convention) rather than a generated unique code - confirmed absent from
...                 OV_DOA_CREDIT_LIMIT before this was wired in (2026-08-23, live DB check: 0
...                 rows LIKE 'AUTOTEST_DOA%'). Every run must complete TC05 (delete) so the code
...                 is free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/VAT Code's convention (docs/rf-suite-styles.md).
...                 PURE SCREEN verification (matches bank_iud.robot's owner-requested
...                 2026-08-18 convention: no DB check here) - removed the extra inline
...                 DB-read keywords this suite originally had, to match Bank exactly
...                 (2026-08-25 alignment fix).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/doa_credit_limit_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    doa-credit-limit


*** Variables ***
${TEST_CODE}        AUTOTEST_DOA
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open DOA Credit Limit Screen
    Verify DOA Credit Limit Record Does Not Exist
    Logout From EC Application

TC02 Insert DOA Credit Limit Data
    Login To EC Application
    Open DOA Credit Limit Screen
    Insert DOA Credit Limit Record And Save
    Verify DOA Credit Limit Record Exists
    Logout From EC Application

TC03 Update DOA Credit Limit Data
    Login To EC Application
    Open DOA Credit Limit Screen
    Update DOA Credit Limit Record And Save
    Verify DOA Credit Limit Record Updated
    Logout From EC Application

TC04 Find DOA Credit Limit Data
    Login To EC Application
    Open DOA Credit Limit Screen
    Find DOA Credit Limit Record
    Verify DOA Credit Limit Record Found
    Logout From EC Application

TC05 Delete DOA Credit Limit Data
    Login To EC Application
    Open DOA Credit Limit Screen
    Delete DOA Credit Limit Record And Save
    Verify DOA Credit Limit Record Removed
    Logout From EC Application
