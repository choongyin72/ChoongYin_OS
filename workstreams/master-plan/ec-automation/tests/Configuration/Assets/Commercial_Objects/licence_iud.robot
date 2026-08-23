*** Settings ***
Documentation       EC IUD Test - Licence (Configuration > Assets > Commercial Objects > Licence).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_LICENCE).
...                 Layered: this test -> licence_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_LICENCE,
...                 matching Bank/State/Country's convention) rather than a generated
...                 unique code - confirmed absent from OV_LICENCE before this was wired in
...                 (2026-08-23). Every run must complete TC05 (delete) so the code is free
...                 for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State/Country's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/licence_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    licence


*** Variables ***
${TEST_CODE}        AUTOTEST_LICENCE
${OBJ_NAME}         AUTOTEST Licence
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/licence_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Licence UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Licence Screen
    Verify Licence Record Does Not Exist
    Logout From EC Application

TC02 Insert Licence Data
    Login To EC Application
    Open Licence Screen
    Insert Licence Record And Save
    Verify Licence Record Exists
    Logout From EC Application

TC03 Update Licence Data
    Login To EC Application
    Open Licence Screen
    Update Licence Record And Save
    Verify Licence Record Updated
    Logout From EC Application

TC04 Find Licence Data
    Login To EC Application
    Open Licence Screen
    Find Licence Record
    Verify Licence Record Found
    Logout From EC Application

TC05 Delete Licence Data
    Login To EC Application
    Open Licence Screen
    Delete Licence Record And Save
    Verify Licence Record Removed
    Logout From EC Application
