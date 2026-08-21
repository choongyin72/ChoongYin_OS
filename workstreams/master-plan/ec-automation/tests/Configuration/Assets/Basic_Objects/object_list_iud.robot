*** Settings ***
Documentation       EC IUD Test - Object List (Configuration > Assets > Basic Objects > Object List).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 OV_OBJECT_LIST). Layered: this test -> object_list_page (T3) -> manage_object
...                 (T2) + common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_OBJLIST) rather than a generated unique code - confirmed absent from
...                 OV_OBJECT_LIST before this was wired in (2026-08-21). Every run must complete
...                 TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/object_list_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    object-list


*** Variables ***
${TEST_CODE}        AUTOTEST_OBJLIST
${OBJ_NAME}         AUTOTEST Object List
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/object_list_insert.properties - TC02 DB-verifies against it.
${LIST_CLASS}       BANK
# Must stay in sync with testdata/object_list_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Object List UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Object List Screen
    Verify Object List Record Does Not Exist
    Logout From EC Application

TC02 Insert Object List Data
    Login To EC Application
    Open Object List Screen
    Insert Object List Record And Save
    Verify Object List Record Exists
    Logout From EC Application

TC03 Update Object List Data
    Login To EC Application
    Open Object List Screen
    Update Object List Record And Save
    Verify Object List Record Updated
    Logout From EC Application

TC04 Find Object List Data
    Login To EC Application
    Open Object List Screen
    Find Object List Record
    Verify Object List Record Found
    Logout From EC Application

TC05 Delete Object List Data
    Login To EC Application
    Open Object List Screen
    Delete Object List Record And Save
    Verify Object List Record Removed
    Logout From EC Application
