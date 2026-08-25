*** Settings ***
Documentation       EC IUD Test - Calculation Context (Configuration > Assets > Calculation_Objects >
...                 Calculation Context, CO.1059). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_CALC_CONTEXT).
...                 Layered: this test -> calculation_context_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_CALCCTX, matching
...                 Bank's convention) rather than a per-run generated code - confirmed absent from
...                 OV_CALC_CONTEXT before this was wired in (live DB check, 2026-08-23). Every run
...                 must complete TC05 (delete) so the code is free for the next run - EC never lets
...                 a DELETED code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches (matches Bank's convention).
...                 PURE SCREEN verification (matches bank_iud.robot's owner-requested
...                 2026-08-18 convention: no DB check here) - removed the extra inline
...                 DB-read keywords this suite originally had, to match Bank exactly
...                 (2026-08-25 alignment fix).

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/calculation_context_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    calculation_context


*** Variables ***
${TEST_CODE}        AUTOTEST_CALCCTX
${OBJ_NAME}         Automation Test Calculation Context
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These 2 values must stay in sync with testdata/calculation_context_insert.properties - TC02
# verifies them on screen against what that file actually set, not an independent assumption.
${OBJ_DESC}         Automation test calc context description
${OBJ_COMMENTS}     Automation test calc context comments
# These 3 values must stay in sync with testdata/calculation_context_update.properties - TC03
# verifies them on screen against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}      Automation Test Calculation Context UPDATED
${OBJ_DESC_UPD}      Automation test calc context description UPDATED
${OBJ_COMMENTS_UPD}  Automation test calc context comments UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Calculation Context Screen
    Verify Calculation Context Record Does Not Exist
    Logout From EC Application

TC02 Insert Calculation Context Data
    Login To EC Application
    Open Calculation Context Screen
    Insert Calculation Context Record And Save
    Verify Calculation Context Record Exists
    Logout From EC Application

TC03 Update Calculation Context Data
    Login To EC Application
    Open Calculation Context Screen
    Update Calculation Context Record And Save
    Verify Calculation Context Record Updated
    Logout From EC Application

TC04 Find Calculation Context Data
    Login To EC Application
    Open Calculation Context Screen
    Find Calculation Context Record
    Verify Calculation Context Record Found
    Logout From EC Application

TC05 Delete Calculation Context Data
    Login To EC Application
    Open Calculation Context Screen
    Delete Calculation Context Record And Save
    Verify Calculation Context Record Removed
    Logout From EC Application
