*** Settings ***
Documentation       EC IUD Test - Calendar Collection (Configuration > Assets > Date Objects >
...                 Calendar Collection, CD.0105). Custom-URL OV (date-effective) screen. DELETE
...                 = End Date = Start Date (true delete in OV_CALENDAR_COLLECTION).
...                 Layered: this test -> calendar_collection_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_CALENDAR_COLLECTION, matching Bank/Country/State's convention)
...                 rather than a generated unique code - confirmed absent from
...                 OV_CALENDAR_COLLECTION before this was wired in (2026-08-23). Every run must
...                 complete TC05 (delete) so the code is free for the next run - EC never lets
...                 a DELETED code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself. EACH test case does its own real
...                 Login/Logout on ONE browser opened once in Suite Setup, matching
...                 Bank/Country/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    calendar-collection    date-objects


*** Variables ***
${TEST_CODE}        AUTOTEST_CALENDAR_COLLECTION
${OBJ_NAME}         AUTOTEST Calendar Collection
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/calendar_collection_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Calendar Collection UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Calendar Collection Screen
    Verify Calendar Collection Record Does Not Exist
    Logout From EC Application

TC02 Insert Calendar Collection Data
    Login To EC Application
    Open Calendar Collection Screen
    Insert Calendar Collection Record And Save
    Verify Calendar Collection Record Exists
    Logout From EC Application

TC03 Update Calendar Collection Data
    Login To EC Application
    Open Calendar Collection Screen
    Update Calendar Collection Record And Save
    Verify Calendar Collection Record Updated
    Logout From EC Application

TC04 Find Calendar Collection Data
    Login To EC Application
    Open Calendar Collection Screen
    Find Calendar Collection Record
    Verify Calendar Collection Record Found
    Logout From EC Application

TC05 Delete Calendar Collection Data
    Login To EC Application
    Open Calendar Collection Screen
    Delete Calendar Collection Record And Save
    Verify Calendar Collection Record Removed
    Logout From EC Application
