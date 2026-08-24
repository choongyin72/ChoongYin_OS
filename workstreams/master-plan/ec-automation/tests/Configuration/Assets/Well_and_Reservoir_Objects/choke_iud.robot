*** Settings ***
Documentation       EC IUD Test - Choke (Configuration > Assets > Well and Reservoir Objects,
...                 Choke, CO.0185). Manage-Object (OV, date-effective) screen. DELETE = End Date
...                 = Start Date (true delete in OV_CHOKE). Layered: this test -> choke_page (T3)
...                 -> manage_object (T2) + common (T1).
...                 NEVER touch existing data — the grid has real seed data ("P1 C001").
...                 Uses a FIXED test code (AUTOTEST_CHOKE, matching Bank's own fixed-code
...                 convention) rather than a generated unique code — confirmed absent from
...                 OV_CHOKE before this was wired in (fresh DB query, 2026-08-25). Every run
...                 must complete TC05 (delete) so the code is free for the next run - EC never
...                 lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on
...                 ONE browser opened once in Suite Setup - not 5 separate browser launches.
...                 This is a conscious tradeoff: 5 real logins instead of 1 costs real runtime,
...                 and TC03/TC04/TC05 still depend on TC02's inserted record existing (the
...                 per-TC login/logout makes each TC LOOK self-contained, it does not remove
...                 that data dependency) - accepted deliberately for a client-readable
...                 process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-25): see choke_page.
...                 resource's Documentation for what changed vs the prior OLD-pattern build, and
...                 for the live evidence that overturns docs/bank-pattern-conversion-checklist.
...                 md's stale "Excluded" classification for THIS screen — the LAST unverified
...                 member of the original "Document Date Term, Payment Term, Choke, Choke
...                 Model" mandatory-date-gate group.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/choke_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    choke    well_and_reservoir_objects


*** Variables ***
${TEST_CODE}        AUTOTEST_CHOKE
${OBJ_NAME}         AUTOTEST Choke
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/choke_update.properties -
# Verify Choke Record Updated (TC03) screen-verifies them against what that file actually set,
# not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Choke UPDATED
${OBJ_CMT_UPD}      AUTOTEST cmt UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Choke Screen
    Verify Choke Record Does Not Exist
    Logout From EC Application

TC02 Insert Choke Data
    Login To EC Application
    Open Choke Screen
    Insert Choke Record And Save
    Verify Choke Record Exists
    Logout From EC Application

TC03 Update Choke Data
    Login To EC Application
    Open Choke Screen
    Update Choke Record And Save
    Verify Choke Record Updated
    Logout From EC Application

TC04 Find Choke Data
    Login To EC Application
    Open Choke Screen
    Find Choke Record
    Verify Choke Record Found
    Logout From EC Application

TC05 Delete Choke Data
    Login To EC Application
    Open Choke Screen
    Delete Choke Record And Save
    Verify Choke Record Removed
    Logout From EC Application
