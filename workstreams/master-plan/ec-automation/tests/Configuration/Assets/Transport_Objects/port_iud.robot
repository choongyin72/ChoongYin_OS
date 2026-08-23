*** Settings ***
Documentation       EC IUD Test - Port (Configuration > Assets > Transport Objects > Port, CO.2003).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PORT).
...                 Layered: this test -> port_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_PORT,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_PORT before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).
...                 Port's grid is PAGINATED (2 pages) - the shared T2 row-locate/filter
...                 keywords already walk all pages (confirmed live 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/port_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    port


*** Variables ***
${TEST_CODE}        AUTOTEST_PORT
${OBJ_NAME}         AUTOTEST Port
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/port_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Port UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Port Screen
    Verify Port Record Does Not Exist
    Logout From EC Application

TC02 Insert Port Data
    Login To EC Application
    Open Port Screen
    Insert Port Record And Save
    Verify Port Record Exists
    Logout From EC Application

TC03 Update Port Data
    Login To EC Application
    Open Port Screen
    Update Port Record And Save
    Verify Port Record Updated
    Logout From EC Application

TC04 Find Port Data
    Login To EC Application
    Open Port Screen
    Find Port Record
    Verify Port Record Found
    Logout From EC Application

TC05 Delete Port Data
    Login To EC Application
    Open Port Screen
    Delete Port Record And Save
    Verify Port Record Removed
    Logout From EC Application
