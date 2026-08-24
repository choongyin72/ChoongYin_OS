*** Settings ***
Documentation       EC IUD Test - Report Group (Configuration > Assets > Facility Objects >
...                 Report Group, CO.0158). Manage-Object (OV) screen. DELETE = End Date = Start
...                 Date (true delete in OV_REPORT_GROUP). Layered: this test -> report_group_page
...                 (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_REPORT_GROUP,
...                 matching Bank's/Disposition Type's own fixed-code convention) rather than a
...                 generated unique code — confirmed absent from OV_REPORT_GROUP before this was
...                 wired in (fresh DB query, 2026-08-24). Every run must complete TC05 (delete)
...                 so the code is free for the next run — EC never lets a DELETED code be
...                 reused, but this fixed code only stays reusable if each run actually cleans
...                 up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on
...                 ONE browser opened once in Suite Setup — not 5 separate browser launches. This
...                 is a conscious tradeoff: 5 real logins instead of 1 costs real runtime, and
...                 TC03/TC04/TC05 still depend on TC02's inserted record existing (the per-TC
...                 login/logout makes each TC LOOK self-contained, it does not remove that data
...                 dependency) — accepted deliberately for a client-readable process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-24): see report_group_page
...                 .resource's Documentation for what changed vs the prior PARTIAL-pattern build.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/report_group_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    report_group


*** Variables ***
${TEST_CODE}        AUTOTEST_REPORT_GROUP
${OBJ_NAME}         AUTOTEST Report Group
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/report_group_insert.properties -
# Verify Report Group Record Exists (TC02) screen-verifies them against what that file
# actually set, not an independent assumption.
${OBJ_DESC}         AUTOTEST Report Group description
# These values must stay in sync with testdata/report_group_update.properties -
# Verify Report Group Record Updated (TC03) screen-verifies them against what that file
# actually set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Report Group UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Report Group Screen
    Verify Report Group Record Does Not Exist
    Logout From EC Application

TC02 Insert Report Group Data
    Login To EC Application
    Open Report Group Screen
    Insert Report Group Record And Save
    Verify Report Group Record Exists
    Logout From EC Application

TC03 Update Report Group Data
    Login To EC Application
    Open Report Group Screen
    Update Report Group Record And Save
    Verify Report Group Record Updated
    Logout From EC Application

TC04 Find Report Group Data
    Login To EC Application
    Open Report Group Screen
    Find Report Group Record
    Verify Report Group Record Found
    Logout From EC Application

TC05 Delete Report Group Data
    Login To EC Application
    Open Report Group Screen
    Delete Report Group Record And Save
    Verify Report Group Record Removed
    Logout From EC Application
