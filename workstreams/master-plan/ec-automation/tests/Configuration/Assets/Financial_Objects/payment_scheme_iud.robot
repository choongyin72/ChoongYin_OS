*** Settings ***
Documentation       EC IUD Test - Payment Scheme (Configuration > Assets > Financial Objects >
...                 Payment Scheme). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_PAYMENT_SCHEME). Layered: this test ->
...                 payment_scheme_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_PAYMENT_SCHEME,
...                 matching Bank/State's convention) rather than a generated unique code -
...                 confirmed absent from OV_PAYMENT_SCHEME before this was wired in
...                 (2026-08-22). Every run must complete TC05 (delete) so the code is free for
...                 the next run - EC never lets a DELETED code be reused, but this fixed code
...                 only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/payment_scheme_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    payment-scheme


*** Variables ***
${TEST_CODE}        AUTOTEST_PAYMENT_SCHEME
${OBJ_NAME}         AUTOTEST Payment Scheme
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/payment_scheme_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Payment Scheme UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Payment Scheme Screen
    Verify Payment Scheme Record Does Not Exist
    Logout From EC Application

TC02 Insert Payment Scheme Data
    Login To EC Application
    Open Payment Scheme Screen
    Insert Payment Scheme Record And Save
    Verify Payment Scheme Record Exists
    Logout From EC Application

TC03 Update Payment Scheme Data
    Login To EC Application
    Open Payment Scheme Screen
    Update Payment Scheme Record And Save
    Verify Payment Scheme Record Updated
    Logout From EC Application

TC04 Find Payment Scheme Data
    Login To EC Application
    Open Payment Scheme Screen
    Find Payment Scheme Record
    Verify Payment Scheme Record Found
    Logout From EC Application

TC05 Delete Payment Scheme Data
    Login To EC Application
    Open Payment Scheme Screen
    Delete Payment Scheme Record And Save
    Verify Payment Scheme Record Removed
    Logout From EC Application
