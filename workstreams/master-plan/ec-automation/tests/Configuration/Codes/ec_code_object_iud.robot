*** Settings ***
Documentation       EC IUD Test - EC Code Object (Configuration > Codes > EC Code Object, CD.0135).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 OV_EC_CODE_OBJECT). Layered: this test -> ec_code_object_page (T3) ->
...                 manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_EC_CODE_OBJECT,
...                 matching Bank's own fixed-code convention) rather than a generated unique code -
...                 confirmed absent from OV_EC_CODE_OBJECT before this was wired in (fresh DB query,
...                 2026-08-24). Every run must complete TC05 (delete) so the code is free for the
...                 next run - EC never lets a DELETED code be reused, but this fixed code only stays
...                 reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on ONE
...                 browser opened once in Suite Setup - not 5 separate browser launches. This is a
...                 conscious tradeoff: 5 real logins instead of 1 costs real runtime, and TC03/TC04/
...                 TC05 still depend on TC02's inserted record existing (the per-TC login/logout
...                 makes each TC LOOK self-contained, it does not remove that data dependency) -
...                 accepted deliberately for a client-readable process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-24): see ec_code_object_page
...                 .resource's Documentation for what changed vs the prior PARTIAL label-driven build
...                 (4 TCs / no Find / inline DB-verify calls in this test file).

Resource            ../../../pageobjects/Configuration/Codes/ec_code_object_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    ec_code_object


*** Variables ***
${TEST_CODE}        AUTOTEST_EC_CODE_OBJECT
${OBJ_NAME}         AUTOTEST EC Code Object
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/ec_code_object_update.properties - Verify EC Code
# Object Record Updated (TC03) screen-verifies them against what that file actually set, not an
# independent assumption.
${OBJ_NAME_UPD}     AUTOTEST EC Code Object UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open EC Code Object Screen
    Verify EC Code Object Record Does Not Exist
    Logout From EC Application

TC02 Insert EC Code Object Data
    Login To EC Application
    Open EC Code Object Screen
    Insert EC Code Object Record And Save
    Verify EC Code Object Record Exists
    Logout From EC Application

TC03 Update EC Code Object Data
    Login To EC Application
    Open EC Code Object Screen
    Update EC Code Object Record And Save
    Verify EC Code Object Record Updated
    Logout From EC Application

TC04 Find EC Code Object Data
    Login To EC Application
    Open EC Code Object Screen
    Find EC Code Object Record
    Verify EC Code Object Record Found
    Logout From EC Application

TC05 Delete EC Code Object Data
    Login To EC Application
    Open EC Code Object Screen
    Delete EC Code Object Record And Save
    Verify EC Code Object Record Removed
    Logout From EC Application
