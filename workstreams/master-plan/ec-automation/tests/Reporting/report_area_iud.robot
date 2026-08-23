*** Settings ***
Documentation       EC IUD Test - Report Area (Reporting > Report Area, RP.0017).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_REPORT_AREA).
...                 Layered: this test -> report_area_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_RPTA, matching
...                 Bank/Berth's convention) rather than a generated unique code - confirmed
...                 absent from OV_REPORT_AREA before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../pageobjects/Reporting/report_area_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    report_area


*** Variables ***
${TEST_CODE}        AUTOTEST_RPTA
${OBJ_NAME}         AUTOTEST Report Area
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/report_area_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Report Area UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Report Area Screen
    Verify Report Area Record Does Not Exist
    Logout From EC Application

TC02 Insert Report Area Data
    Login To EC Application
    Open Report Area Screen
    Insert Report Area Record And Save
    Verify Report Area Record Exists
    Logout From EC Application

TC03 Update Report Area Data
    Login To EC Application
    Open Report Area Screen
    Update Report Area Record And Save
    Verify Report Area Record Updated
    Logout From EC Application

TC04 Find Report Area Data
    Login To EC Application
    Open Report Area Screen
    Find Report Area Record
    Verify Report Area Record Found
    Logout From EC Application

TC05 Delete Report Area Data
    Login To EC Application
    Open Report Area Screen
    Delete Report Area Record And Save
    Verify Report Area Record Removed
    Logout From EC Application
