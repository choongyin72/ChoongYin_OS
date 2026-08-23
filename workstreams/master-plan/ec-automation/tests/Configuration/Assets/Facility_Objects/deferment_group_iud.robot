*** Settings ***
Documentation       EC IUD Test - Deferment Group (Configuration > Assets > Facility_Objects > Deferment Group, CO.0149).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DEFERMENT_GROUP).
...                 Layered: this test -> deferment_group_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_DEFERMENT_GROUP,
...                 matching Bank/State/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_DEFERMENT_GROUP before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/State/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    deferment_group


*** Variables ***
${TEST_CODE}        AUTOTEST_DEFERMENT_GROUP
${OBJ_NAME}         AUTOTEST Deferment Group
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/deferment_group_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Deferment Group UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Deferment Group Screen
    Verify Deferment Group Record Does Not Exist
    Logout From EC Application

TC02 Insert Deferment Group Data
    Login To EC Application
    Open Deferment Group Screen
    Insert Deferment Group Record And Save
    Verify Deferment Group Record Exists
    Logout From EC Application

TC03 Update Deferment Group Data
    Login To EC Application
    Open Deferment Group Screen
    Update Deferment Group Record And Save
    Verify Deferment Group Record Updated
    Logout From EC Application

TC04 Find Deferment Group Data
    Login To EC Application
    Open Deferment Group Screen
    Find Deferment Group Record
    Verify Deferment Group Record Found
    Logout From EC Application

TC05 Delete Deferment Group Data
    Login To EC Application
    Open Deferment Group Screen
    Delete Deferment Group Record And Save
    Verify Deferment Group Record Removed
    Logout From EC Application
