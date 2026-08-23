*** Settings ***
Documentation       EC IUD Test - Field Group (Configuration > Assets > Commercial Objects >
...                 Field Group). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_FIELD_GROUP). Layered: this test -> field_group_page (T3)
...                 -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_FIELD_GROUP,
...                 matching Bank/State/Country/Object List's convention) rather than a generated
...                 unique code - confirmed absent from OV_FIELD_GROUP before this was wired in
...                 (2026-08-23). Every run must complete TC05 (delete) so the code is free for
...                 the next run - EC never lets a DELETED code be reused, but this fixed code
...                 only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State/Country/Object List's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/field_group_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    field-group


*** Variables ***
${TEST_CODE}        AUTOTEST_FIELD_GROUP
${OBJ_NAME}         AUTOMATION TEST FIELD GROUP
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/field_group_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOMATION TEST FIELD GROUP UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Field Group Screen
    Verify Field Group Record Does Not Exist
    Logout From EC Application

TC02 Insert Field Group Data
    Login To EC Application
    Open Field Group Screen
    Insert Field Group Record And Save
    Verify Field Group Record Exists
    Logout From EC Application

TC03 Update Field Group Data
    Login To EC Application
    Open Field Group Screen
    Update Field Group Record And Save
    Verify Field Group Record Updated
    Logout From EC Application

TC04 Find Field Group Data
    Login To EC Application
    Open Field Group Screen
    Find Field Group Record
    Verify Field Group Record Found
    Logout From EC Application

TC05 Delete Field Group Data
    Login To EC Application
    Open Field Group Screen
    Delete Field Group Record And Save
    Verify Field Group Record Removed
    Logout From EC Application
