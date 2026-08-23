*** Settings ***
Documentation       EC IUD Test - Carrier (Configuration > Assets > Cargo Objects > Carrier).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CARRIER).
...                 Layered: this test -> carrier_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_CARRIER,
...                 matching Bank/Berth/Port's convention) rather than a generated unique code -
...                 confirmed absent from OV_CARRIER before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth/Port's convention (docs/rf-suite-styles.md).
...                 Carrier's navigator is only an optional date + GO (NOT gated) - confirmed via
...                 the prior SOW recon + proven Playwright driver, re-confirmed before this
...                 Batch 11 conversion.

Resource            ../../../../pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    carrier


*** Variables ***
${TEST_CODE}        AUTOTEST_CARRIER
${OBJ_NAME}         AUTOTEST Carrier
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/carrier_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Carrier UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Carrier Screen
    Verify Carrier Record Does Not Exist
    Logout From EC Application

TC02 Insert Carrier Data
    Login To EC Application
    Open Carrier Screen
    Insert Carrier Record And Save
    Verify Carrier Record Exists
    Logout From EC Application

TC03 Update Carrier Data
    Login To EC Application
    Open Carrier Screen
    Update Carrier Record And Save
    Verify Carrier Record Updated
    Logout From EC Application

TC04 Find Carrier Data
    Login To EC Application
    Open Carrier Screen
    Find Carrier Record
    Verify Carrier Record Found
    Logout From EC Application

TC05 Delete Carrier Data
    Login To EC Application
    Open Carrier Screen
    Delete Carrier Record And Save
    Verify Carrier Record Removed
    Logout From EC Application
