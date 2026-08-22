*** Settings ***
Documentation       EC IUD Test - VAT Code (Configuration > Assets > Financial Objects > VAT Code).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 OV_VAT_CODE). Layered: this test -> vat_code_page (T3) -> manage_object (T2)
...                 + common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_VAT, matching Bank/Account's convention) rather than a generated
...                 unique code - confirmed absent from OV_VAT_CODE before this was wired in
...                 (2026-08-23). Every run must complete TC05 (delete) so the code is free for
...                 the next run - EC never lets a DELETED code be reused, but this fixed code
...                 only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Account's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/vat_code_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    vat-code


*** Variables ***
${TEST_CODE}        AUTOTEST_VAT
${OBJ_NAME}         AUTOTEST VAT Code
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/vat_code_update.properties - TC03/TC04 verify against it.
${OBJ_NAME_UPD}     AUTOTEST VAT Code UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open VAT Code Screen
    Verify VAT Code Record Does Not Exist
    Logout From EC Application

TC02 Insert VAT Code Data
    Login To EC Application
    Open VAT Code Screen
    Insert VAT Code Record And Save
    Verify VAT Code Record Exists
    Logout From EC Application

TC03 Update VAT Code Data
    Login To EC Application
    Open VAT Code Screen
    Update VAT Code Record And Save
    Verify VAT Code Record Updated
    Logout From EC Application

TC04 Find VAT Code Data
    Login To EC Application
    Open VAT Code Screen
    Find VAT Code Record
    Verify VAT Code Record Found
    Logout From EC Application

TC05 Delete VAT Code Data
    Login To EC Application
    Open VAT Code Screen
    Delete VAT Code Record And Save
    Verify VAT Code Record Removed
    Logout From EC Application
