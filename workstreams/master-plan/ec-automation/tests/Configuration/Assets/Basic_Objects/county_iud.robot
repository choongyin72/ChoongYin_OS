*** Settings ***
Documentation       EC IUD Test - County (Configuration > Assets > Basic Objects > County).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 ov_county). Layered: this test -> county_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_COUNTY, matching the AUTOTEST_ACCOUNT/BANK_CHINA convention) rather
...                 than a generated unique code - confirmed absent from OV_COUNTY before this was
...                 wired in (fresh oracledb query, 2026-08-23: 0 rows for CODE LIKE 'AUTOTEST%').
...                 Every run must complete TC05 (delete) so the code is free for the next run - EC
...                 never lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup (matches bank_iud.robot's convention) - TC03/TC04/TC05 still depend
...                 on TC02's inserted record existing.
...                 Converted 2026-08-23 from the old hardcoded-field-id pattern to the
...                 label-driven, properties-file-driven, T2-consolidated Bank pattern (batch-2
...                 conversion, see tmp/batch2_shared_findings.md).
...                 PURE SCREEN verification (matches bank_iud.robot's owner-requested
...                 2026-08-18 convention: no DB check here) - removed the extra inline
...                 DB-read keywords this suite originally had, to match Bank exactly
...                 (2026-08-24 alignment fix).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/county_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    county


*** Variables ***
${TEST_CODE}        AUTOTEST_COUNTY
${OBJ_NAME}         AUTOTEST County
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These 2 values must stay in sync with testdata/county_insert.properties - TC02 DB-verifies them
# against what that file actually set, not an independent assumption.
${OBJ_DESC}         AUTOTEST desc
# These 2 values must stay in sync with testdata/county_update.properties - TC03 DB-verifies them
# against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST County UPDATED
${OBJ_DESC_UPD}     AUTOTEST desc UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open County Screen
    Verify County Record Does Not Exist
    Logout From EC Application

TC02 Insert County Data
    Login To EC Application
    Open County Screen
    Insert County Record And Save
    Verify County Record Exists
    Logout From EC Application

TC03 Update County Data
    Login To EC Application
    Open County Screen
    Update County Record And Save
    Verify County Record Updated
    Logout From EC Application

TC04 Find County Data
    Login To EC Application
    Open County Screen
    Find County Record
    Verify County Record Found
    Logout From EC Application

TC05 Delete County Data
    Login To EC Application
    Open County Screen
    Delete County Record And Save
    Verify County Record Removed
    Logout From EC Application
