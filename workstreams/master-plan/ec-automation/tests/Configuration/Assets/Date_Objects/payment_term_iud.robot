*** Settings ***
Documentation       EC IUD Test - Payment Term (Configuration > Assets > Date Objects > Payment
...                 Term, CD.0023). Manage-Object (OV, date-effective) screen. DELETE = End Date =
...                 Start Date (true delete in OV_PAYMENT_TERM). Layered: this test ->
...                 payment_term_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_PAYMENT_TERM,
...                 matching Bank's own fixed-code convention) rather than a generated unique code -
...                 confirmed absent from OV_PAYMENT_TERM before this was wired in (fresh DB query,
...                 2026-08-24). Every run must complete TC05 (delete) so the code is free for the
...                 next run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout (matches Bank's convention) on
...                 ONE browser opened once in Suite Setup - not 5 separate browser launches. This
...                 is a conscious tradeoff: 5 real logins instead of 1 costs real runtime, and
...                 TC03/TC04/TC05 still depend on TC02's inserted record existing (the per-TC
...                 login/logout makes each TC LOOK self-contained, it does not remove that data
...                 dependency) - accepted deliberately for a client-readable process-flow report.
...                 Converted to the full Bank-pattern shape (2026-08-24): see payment_term_page
...                 .resource's Documentation for what changed vs the prior OLD-pattern build.

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/payment_term_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    payment_term    date-objects


*** Variables ***
${TEST_CODE}        AUTOTEST_PAYMENT_TERM
${OBJ_NAME}         AUTOTEST Payment Term
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/payment_term_update.properties -
# Verify Payment Term Record Updated (TC03) screen-verifies them against what that file actually
# set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Payment Term UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Payment Term Screen
    Verify Payment Term Record Does Not Exist
    Logout From EC Application

TC02 Insert Payment Term Data
    Login To EC Application
    Open Payment Term Screen
    Insert Payment Term Record And Save
    Verify Payment Term Record Exists
    Logout From EC Application

TC03 Update Payment Term Data
    Login To EC Application
    Open Payment Term Screen
    Update Payment Term Record And Save
    Verify Payment Term Record Updated
    Logout From EC Application

TC04 Find Payment Term Data
    Login To EC Application
    Open Payment Term Screen
    Find Payment Term Record
    Verify Payment Term Record Found
    Logout From EC Application

TC05 Delete Payment Term Data
    Login To EC Application
    Open Payment Term Screen
    Delete Payment Term Record And Save
    Verify Payment Term Record Removed
    Logout From EC Application
