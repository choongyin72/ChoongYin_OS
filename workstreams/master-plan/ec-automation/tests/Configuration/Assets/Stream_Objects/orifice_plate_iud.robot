*** Settings ***
Documentation       EC IUD Test - Orifice Plate (Configuration > Assets > Stream_Objects > Orifice Plate, CO.0089).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_ORIFICE_PLATE).
...                 Layered: this test -> orifice_plate_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_ORIFICE_PLATE,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_ORIFICE_PLATE before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/orifice_plate_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    orifice_plate


*** Variables ***
${TEST_CODE}        AUTOTEST_ORIFICE_PLATE
${OBJ_NAME}         AUTOTEST Orifice Plate
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/orifice_plate_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Orifice Plate UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Orifice Plate Screen
    Verify Orifice Plate Record Does Not Exist
    Logout From EC Application

TC02 Insert Orifice Plate Data
    Login To EC Application
    Open Orifice Plate Screen
    Insert Orifice Plate Record And Save
    Verify Orifice Plate Record Exists
    Logout From EC Application

TC03 Update Orifice Plate Data
    Login To EC Application
    Open Orifice Plate Screen
    Update Orifice Plate Record And Save
    Verify Orifice Plate Record Updated
    Logout From EC Application

TC04 Find Orifice Plate Data
    Login To EC Application
    Open Orifice Plate Screen
    Find Orifice Plate Record
    Verify Orifice Plate Record Found
    Logout From EC Application

TC05 Delete Orifice Plate Data
    Login To EC Application
    Open Orifice Plate Screen
    Delete Orifice Plate Record And Save
    Verify Orifice Plate Record Removed
    Logout From EC Application
