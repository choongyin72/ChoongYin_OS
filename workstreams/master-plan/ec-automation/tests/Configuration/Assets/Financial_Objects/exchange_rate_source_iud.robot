*** Settings ***
Documentation       EC IUD Test - Exchange Rate Source (Configuration > Assets > Financial
...                 Objects > Exchange Rate Source). Manage-Object (OV) screen. DELETE = End
...                 Date = Start Date (true delete in OV_FOREX_SOURCE). Layered: this test ->
...                 exchange_rate_source_page (T3) -> manage_object (T2) + common (T1). NEVER
...                 touch existing data. Uses a FIXED test code
...                 (AUTOTEST_EXCHANGE_RATE_SOURCE, matching Bank/State's convention) rather
...                 than a generated unique code - confirmed absent from OV_FOREX_SOURCE
...                 before this was wired in (2026-08-22). Every run must complete TC05
...                 (delete) so the code is free for the next run - EC never lets a DELETED
...                 code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself. EACH test case does its own real
...                 Login/Logout on ONE browser opened once in Suite Setup, matching
...                 Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/exchange_rate_source_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    exchange_rate_source


*** Variables ***
${TEST_CODE}        AUTOTEST_EXCHANGE_RATE_SOURCE
${OBJ_NAME}         AUTOTEST Exchange Rate Source
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/exchange_rate_source_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Exchange Rate Source UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Exchange Rate Source Screen
    Verify Exchange Rate Source Record Does Not Exist
    Logout From EC Application

TC02 Insert Exchange Rate Source Data
    Login To EC Application
    Open Exchange Rate Source Screen
    Insert Exchange Rate Source Record And Save
    Verify Exchange Rate Source Record Exists
    Logout From EC Application

TC03 Update Exchange Rate Source Data
    Login To EC Application
    Open Exchange Rate Source Screen
    Update Exchange Rate Source Record And Save
    Verify Exchange Rate Source Record Updated
    Logout From EC Application

TC04 Find Exchange Rate Source Data
    Login To EC Application
    Open Exchange Rate Source Screen
    Find Exchange Rate Source Record
    Verify Exchange Rate Source Record Found
    Logout From EC Application

TC05 Delete Exchange Rate Source Data
    Login To EC Application
    Open Exchange Rate Source Screen
    Delete Exchange Rate Source Record And Save
    Verify Exchange Rate Source Record Removed
    Logout From EC Application
