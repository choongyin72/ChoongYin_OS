*** Settings ***
Documentation       EC IUD Test - Product Group (Configuration > Assets > Royalty Objects >
...                 Product Group). Manage-Object (OV) screen. DELETE = End Date = Start
...                 Date (true delete in OV_PRODUCT_GROUP). Layered: this test ->
...                 product_group_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_PRODUCT_GROUP, matching Bank/State's convention) rather than a
...                 generated unique code - confirmed absent from OV_PRODUCT_GROUP before
...                 this was wired in (2026-08-23). Every run must complete TC05 (delete) so
...                 the code is free for the next run - EC never lets a DELETED code be
...                 reused, but this fixed code only stays reusable if each run actually
...                 cleans up after itself. EACH test case does its own real Login/Logout on
...                 ONE browser opened once in Suite Setup, matching Bank/State's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    product_group


*** Variables ***
${TEST_CODE}        AUTOTEST_PRODUCT_GROUP
${OBJ_NAME}         AUTOTEST Product Group
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/product_group_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Product Group UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Product Group Screen
    Verify Product Group Record Does Not Exist
    Logout From EC Application

TC02 Insert Product Group Data
    Login To EC Application
    Open Product Group Screen
    Insert Product Group Record And Save
    Verify Product Group Record Exists
    Logout From EC Application

TC03 Update Product Group Data
    Login To EC Application
    Open Product Group Screen
    Update Product Group Record And Save
    Verify Product Group Record Updated
    Logout From EC Application

TC04 Find Product Group Data
    Login To EC Application
    Open Product Group Screen
    Find Product Group Record
    Verify Product Group Record Found
    Logout From EC Application

TC05 Delete Product Group Data
    Login To EC Application
    Open Product Group Screen
    Delete Product Group Record And Save
    Verify Product Group Record Removed
    Logout From EC Application
