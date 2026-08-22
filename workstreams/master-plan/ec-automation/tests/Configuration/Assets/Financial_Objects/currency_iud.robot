*** Settings ***
Documentation       EC IUD Test - Currency (Configuration > Assets > Financial Objects > Currency).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 OV_CURRENCY). Layered: this test -> currency_page (T3) -> manage_object (T2)
...                 + common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_CURRENCY, matching Bank/Cost Centre's convention) rather than a
...                 generated unique code - confirmed absent from OV_CURRENCY before this was
...                 wired in (2026-08-23). Every run must complete TC05 (delete) so the code is
...                 free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Cost Centre's convention.

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/currency_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    currency


*** Variables ***
${TEST_CODE}        AUTOTEST_CURRENCY
${OBJ_NAME}         AUTOTEST Currency
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/currency_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Currency UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Currency Screen
    Verify Currency Record Does Not Exist
    Logout From EC Application

TC02 Insert Currency Data
    Login To EC Application
    Open Currency Screen
    Insert Currency Record And Save
    Verify Currency Record Exists
    Logout From EC Application

TC03 Update Currency Data
    Login To EC Application
    Open Currency Screen
    Update Currency Record And Save
    Verify Currency Record Updated
    Logout From EC Application

TC04 Find Currency Data
    Login To EC Application
    Open Currency Screen
    Find Currency Record
    Verify Currency Record Found
    Logout From EC Application

TC05 Delete Currency Data
    Login To EC Application
    Open Currency Screen
    Delete Currency Record And Save
    Verify Currency Record Removed
    Logout From EC Application
