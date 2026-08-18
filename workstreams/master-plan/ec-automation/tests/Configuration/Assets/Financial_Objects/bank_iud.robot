*** Settings ***
Documentation       EC IUD Test - Bank (Configuration > Assets > Financial Objects > Bank).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_bank).
...                 Layered: this test -> bank_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (BANK_CHINA, owner-requested
...                 2026-08-17) rather than a generated unique code - confirmed absent from ov_bank
...                 before this was wired in. Every run must complete TC05 (delete) so the code is
...                 free for the next run - EC never lets a DELETED code be reused, but this fixed
...                 code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (owner-requested 2026-08-18) on
...                 ONE browser opened once in Suite Setup - not 5 separate browser launches. This
...                 is a conscious tradeoff: 5 real logins instead of 1 costs real runtime, and
...                 TC03/TC04/TC05 still depend on TC02's inserted record existing (the per-TC
...                 login/logout makes each TC LOOK self-contained, it does not remove that data
...                 dependency) - accepted deliberately for a client-readable process-flow report.

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/bank_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    bank


*** Variables ***
${TEST_CODE}        BANK_CHINA
${OBJ_NAME}        Bank of China (Hong Kong) Ltd.
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These 3 values must stay in sync with testdata/bank_insert.properties - TC02 DB-verifies
# them against what that file actually set, not an independent assumption.
${OBJ_DESC}         Bank of China
${OBJ_ADDR1}        Bank of China Tower Branch
${OBJ_SWIFT}        BKCHHKHH
# These 2 values must stay in sync with testdata/bank_update.properties - TC03 DB-verifies
# them against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}      Bank of China (Hong Kong) Ltd. UPDATED
${OBJ_DESC_UPD}      Bank of China UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Bank Screen
    Verify Bank Record Does Not Exist
    Logout From EC Application

TC02 Insert Bank Data
    Login To EC Application
    Open Bank Screen
    Insert Bank Record And Save
    Verify Bank Record Exists
    Logout From EC Application

TC03 Update Bank Data
    Login To EC Application
    Open Bank Screen
    Update Bank Record And Save
    Verify Bank Record Updated
    Logout From EC Application

TC04 Find Bank Data
    Login To EC Application
    Open Bank Screen
    Find Bank Record
    Verify Bank Record Found
    Logout From EC Application

TC05 Delete Bank Data
    Login To EC Application
    Open Bank Screen
    Delete Bank Record And Save
    Verify Bank Record Removed
    Logout From EC Application
