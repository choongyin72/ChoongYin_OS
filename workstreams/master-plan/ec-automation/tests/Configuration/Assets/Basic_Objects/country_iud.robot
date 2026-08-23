*** Settings ***
Documentation       EC IUD Test - Country (Configuration > Assets > Basic Objects > Country).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_COUNTRY).
...                 Layered: this test -> country_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_COUNTRY,
...                 matching Bank/State/Object List's convention) rather than a generated
...                 unique code - confirmed absent from OV_COUNTRY before this was wired in
...                 (2026-08-23). Every run must complete TC05 (delete) so the code is free
...                 for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State/Object List's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/country_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    country


*** Variables ***
${TEST_CODE}        AUTOTEST_COUNTRY
${OBJ_NAME}         AUTOTEST Country
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/country_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Country UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Country Screen
    Verify Country Record Does Not Exist
    Logout From EC Application

TC02 Insert Country Data
    Login To EC Application
    Open Country Screen
    Insert Country Record And Save
    Verify Country Record Exists
    Logout From EC Application

TC03 Update Country Data
    Login To EC Application
    Open Country Screen
    Update Country Record And Save
    Verify Country Record Updated
    Logout From EC Application

TC04 Find Country Data
    Login To EC Application
    Open Country Screen
    Find Country Record
    Verify Country Record Found
    Logout From EC Application

TC05 Delete Country Data
    Login To EC Application
    Open Country Screen
    Delete Country Record And Save
    Verify Country Record Removed
    Logout From EC Application
