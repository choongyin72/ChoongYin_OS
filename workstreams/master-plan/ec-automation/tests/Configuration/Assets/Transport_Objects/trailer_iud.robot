*** Settings ***
Documentation       EC IUD Test - Trailer (Configuration > Assets > Transport_Objects).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_TRAILER).
...                 Layered: this test -> trailer_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_TRAILER,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_TRAILER before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/trailer_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    trailer


*** Variables ***
${TEST_CODE}        AUTOTEST_TRAILER
${OBJ_NAME}         AUTOTEST Trailer
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/trailer_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Trailer UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Trailer Screen
    Verify Trailer Record Does Not Exist
    Logout From EC Application

TC02 Insert Trailer Data
    Login To EC Application
    Open Trailer Screen
    Insert Trailer Record And Save
    Verify Trailer Record Exists
    Logout From EC Application

TC03 Update Trailer Data
    Login To EC Application
    Open Trailer Screen
    Update Trailer Record And Save
    Verify Trailer Record Updated
    Logout From EC Application

TC04 Find Trailer Data
    Login To EC Application
    Open Trailer Screen
    Find Trailer Record
    Verify Trailer Record Found
    Logout From EC Application

TC05 Delete Trailer Data
    Login To EC Application
    Open Trailer Screen
    Delete Trailer Record And Save
    Verify Trailer Record Removed
    Logout From EC Application
