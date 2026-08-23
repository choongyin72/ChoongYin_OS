*** Settings ***
Documentation       EC IUD Test - Royalty Owner (Configuration > Assets > Royalty Objects >
...                 Royalty Owner). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_ROYALTY_OWNER).
...                 Layered: this test -> royalty_owner_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_ROYALTY_OWNER, matching Bank/State/Object List's convention)
...                 rather than a generated unique code - confirmed absent from
...                 OV_ROYALTY_OWNER before this was wired in (2026-08-23). Every run must
...                 complete TC05 (delete) so the code is free for the next run - EC never
...                 lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/State/Object List's convention
...                 (docs/rf-suite-styles.md).
...                 Rebuilt 2026-08-23 (Batch 5 Bank-pattern conversion) from the older
...                 hardcoded-field-id/generated-code pattern.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    royalty_owner


*** Variables ***
${TEST_CODE}        AUTOTEST_ROYALTY_OWNER
${OBJ_NAME}         AUTOTEST Royalty Owner
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/royalty_owner_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Royalty Owner UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Royalty Owner Screen
    Verify Royalty Owner Record Does Not Exist
    Logout From EC Application

TC02 Insert Royalty Owner Data
    Login To EC Application
    Open Royalty Owner Screen
    Insert Royalty Owner Record And Save
    Verify Royalty Owner Record Exists
    Logout From EC Application

TC03 Update Royalty Owner Data
    Login To EC Application
    Open Royalty Owner Screen
    Update Royalty Owner Record And Save
    Verify Royalty Owner Record Updated
    Logout From EC Application

TC04 Find Royalty Owner Data
    Login To EC Application
    Open Royalty Owner Screen
    Find Royalty Owner Record
    Verify Royalty Owner Record Found
    Logout From EC Application

TC05 Delete Royalty Owner Data
    Login To EC Application
    Open Royalty Owner Screen
    Delete Royalty Owner Record And Save
    Verify Royalty Owner Record Removed
    Logout From EC Application
