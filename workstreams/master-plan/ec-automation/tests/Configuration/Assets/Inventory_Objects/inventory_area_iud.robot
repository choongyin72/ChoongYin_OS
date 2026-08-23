*** Settings ***
Documentation       EC IUD Test - Inventory Area (Configuration > Assets > Inventory_Objects > Inventory Area, CD.0115).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_INVENTORY_AREA).
...                 Layered: this test -> inventory_area_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_INVA,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_INVENTORY_AREA before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Inventory_Objects/inventory_area_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    inventory_area


*** Variables ***
${TEST_CODE}        AUTOTEST_INVA
${OBJ_NAME}         AUTOTEST Inventory Area
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/inventory_area_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Inventory Area UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Inventory Area Screen
    Verify Inventory Area Record Does Not Exist
    Logout From EC Application

TC02 Insert Inventory Area Data
    Login To EC Application
    Open Inventory Area Screen
    Insert Inventory Area Record And Save
    Verify Inventory Area Record Exists
    Logout From EC Application

TC03 Update Inventory Area Data
    Login To EC Application
    Open Inventory Area Screen
    Update Inventory Area Record And Save
    Verify Inventory Area Record Updated
    Logout From EC Application

TC04 Find Inventory Area Data
    Login To EC Application
    Open Inventory Area Screen
    Find Inventory Area Record
    Verify Inventory Area Record Found
    Logout From EC Application

TC05 Delete Inventory Area Data
    Login To EC Application
    Open Inventory Area Screen
    Delete Inventory Area Record And Save
    Verify Inventory Area Record Removed
    Logout From EC Application
