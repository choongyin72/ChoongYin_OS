*** Settings ***
Documentation       EC IUD Test - Disposition Type (Configuration > Assets > Hydrocarbon Objects >
...                 Disposition Type). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_DISPOSITION_TYPE). Layered: this test -> disposition_type_page
...                 (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_DISPOSITION_TYPE,
...                 matching Bank's own fixed-code convention) rather than a generated unique code -
...                 confirmed absent from OV_DISPOSITION_TYPE before this was wired in (fresh DB
...                 query, 2026-08-24). Every run must complete TC05 (delete) so the code is free
...                 for the next run - EC never lets a DELETED code be reused, but this fixed code
...                 only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on
...                 ONE browser opened once in Suite Setup - not 5 separate browser launches. This
...                 is a conscious tradeoff: 5 real logins instead of 1 costs real runtime, and
...                 TC03/TC04/TC05 still depend on TC02's inserted record existing (the per-TC
...                 login/logout makes each TC LOOK self-contained, it does not remove that data
...                 dependency) - accepted deliberately for a client-readable process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-24): see disposition_type_page
...                 .resource's Documentation for what changed vs the prior OLD-pattern build.

Resource            ../../../../pageobjects/Configuration/Assets/Hydrocarbon_Objects/disposition_type_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    disposition_type


*** Variables ***
${TEST_CODE}        AUTOTEST_DISPOSITION_TYPE
${OBJ_NAME}         AUTOTEST Disposition Type
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/disposition_type_insert.properties -
# Verify Disposition Type Record Exists (TC02) screen-verifies them against what that file
# actually set, not an independent assumption.
${OBJ_DESC}         AUTOTEST desc
# These values must stay in sync with testdata/disposition_type_update.properties -
# Verify Disposition Type Record Updated (TC03) screen-verifies them against what that file
# actually set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Disposition Type UPDATED
${OBJ_DESC_UPD}     AUTOTEST desc UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Disposition Type Screen
    Verify Disposition Type Record Does Not Exist
    Logout From EC Application

TC02 Insert Disposition Type Data
    Login To EC Application
    Open Disposition Type Screen
    Insert Disposition Type Record And Save
    Verify Disposition Type Record Exists
    Logout From EC Application

TC03 Update Disposition Type Data
    Login To EC Application
    Open Disposition Type Screen
    Update Disposition Type Record And Save
    Verify Disposition Type Record Updated
    Logout From EC Application

TC04 Find Disposition Type Data
    Login To EC Application
    Open Disposition Type Screen
    Find Disposition Type Record
    Verify Disposition Type Record Found
    Logout From EC Application

TC05 Delete Disposition Type Data
    Login To EC Application
    Open Disposition Type Screen
    Delete Disposition Type Record And Save
    Verify Disposition Type Record Removed
    Logout From EC Application
