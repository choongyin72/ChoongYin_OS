*** Settings ***
Documentation       EC IUD Test - Choke Model (Configuration > Assets > Stream Objects > Choke
...                 Model, CO.0217). Manage-Object (OV, date-effective) screen. DELETE = End
...                 Date = Start Date (true delete in OV_CHOKE_MODEL). Layered: this test ->
...                 choke_model_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_CHOKE_MODEL,
...                 matching Bank's own fixed-code convention) rather than a generated unique
...                 code - confirmed absent from OV_CHOKE_MODEL before this was wired in (fresh
...                 DB query, 2026-08-24). Every run must complete TC05 (delete) so the code is
...                 free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on
...                 ONE browser opened once in Suite Setup - not 5 separate browser launches.
...                 This is a conscious tradeoff: 5 real logins instead of 1 costs real runtime,
...                 and TC03/TC04/TC05 still depend on TC02's inserted record existing (the
...                 per-TC login/logout makes each TC LOOK self-contained, it does not remove
...                 that data dependency) - accepted deliberately for a client-readable
...                 process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-24): see
...                 choke_model_page.resource's Documentation for what changed vs the prior
...                 OLD-pattern build, and for the live evidence that overturns
...                 docs/bank-pattern-conversion-checklist.md's stale "Excluded" classification
...                 for THIS screen specifically.

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/choke_model_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    choke_model    stream_objects


*** Variables ***
${TEST_CODE}        AUTOTEST_CHOKE_MODEL
${OBJ_NAME}         AUTOTEST Choke Model
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/choke_model_update.properties -
# Verify Choke Model Record Updated (TC03) screen-verifies them against what that file actually
# set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Choke Model UPDATED
${OBJ_DESC_UPD}     AUTOTEST desc UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Choke Model Screen
    Verify Choke Model Record Does Not Exist
    Logout From EC Application

TC02 Insert Choke Model Data
    Login To EC Application
    Open Choke Model Screen
    Insert Choke Model Record And Save
    Verify Choke Model Record Exists
    Logout From EC Application

TC03 Update Choke Model Data
    Login To EC Application
    Open Choke Model Screen
    Update Choke Model Record And Save
    Verify Choke Model Record Updated
    Logout From EC Application

TC04 Find Choke Model Data
    Login To EC Application
    Open Choke Model Screen
    Find Choke Model Record
    Verify Choke Model Record Found
    Logout From EC Application

TC05 Delete Choke Model Data
    Login To EC Application
    Open Choke Model Screen
    Delete Choke Model Record And Save
    Verify Choke Model Record Removed
    Logout From EC Application
