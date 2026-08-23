*** Settings ***
Documentation       EC IUD Test - Calendar (Configuration > Assets > Date Objects > Calendar,
...                 CD.0024). Manage-Object (OV, date-effective), CUSTOM-URL variant (no
...                 navigator/GO). DELETE = End Date = Start Date (true delete in OV_CALENDAR).
...                 Layered: this test -> calendar_page (T3) -> manage_object (T2) + common
...                 (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_CALENDAR, matching Bank/Royalty Owner's convention) rather than
...                 a generated unique code - confirmed absent from OV_CALENDAR before this
...                 was wired in (2026-08-23). Every run must complete TC05 (delete) so the
...                 code is free for the next run - EC never lets a DELETED code be reused,
...                 but this fixed code only stays reusable if each run actually cleans up
...                 after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Royalty Owner's convention
...                 (docs/rf-suite-styles.md).
...                 OUT OF SCOPE: the "Member Calendars"/"Calendar Usage" child grid (per
...                 docs/ec_screen_registry.md's existing entry) - this suite only covers the
...                 plain Code/Name/Start Date IUD flow.
...                 Rebuilt 2026-08-23 (Batch 6 Bank-pattern conversion, final batch) from the
...                 older hardcoded-field-id pattern.

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/calendar_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    calendar    date-objects


*** Variables ***
${TEST_CODE}        AUTOTEST_CALENDAR
${OBJ_NAME}         AUTOTEST Calendar
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/calendar_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Calendar UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Calendar Screen
    Verify Calendar Record Does Not Exist
    Logout From EC Application

TC02 Insert Calendar Data
    Login To EC Application
    Open Calendar Screen
    Insert Calendar Record And Save
    Verify Calendar Record Exists
    Logout From EC Application

TC03 Update Calendar Data
    Login To EC Application
    Open Calendar Screen
    Update Calendar Record And Save
    Verify Calendar Record Updated
    Logout From EC Application

TC04 Find Calendar Data
    Login To EC Application
    Open Calendar Screen
    Find Calendar Record
    Verify Calendar Record Found
    Logout From EC Application

TC05 Delete Calendar Data
    Login To EC Application
    Open Calendar Screen
    Delete Calendar Record And Save
    Verify Calendar Record Removed
    Logout From EC Application
