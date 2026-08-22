*** Settings ***
Documentation       EC IUD Test - Account (Configuration > Assets > Financial Objects > Account).
...                 Custom-URL OV screen (confirmed live 2026-08-22: grid nav:form:T_data, NO GO
...                 button, reload via toolbar Refresh). DELETE = End Date = Start Date (true
...                 delete in OV_FIN_ACCOUNT). Layered: this test -> account_page (T3) ->
...                 manage_object (T2) + common (T1). NEVER touch existing data. Uses a FIXED
...                 test code (AUTOTEST_ACCOUNT, matching Bank/State's convention) rather than a
...                 generated unique code - confirmed absent from OV_FIN_ACCOUNT before this was
...                 wired in (2026-08-22). Every run must complete TC05 (delete) so the code is
...                 free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/account_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    account


*** Variables ***
${TEST_CODE}        AUTOTEST_ACCOUNT
${OBJ_NAME}         AUTOTEST Account
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/account_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Account UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Account Screen
    Verify Account Record Does Not Exist
    Logout From EC Application

TC02 Insert Account Data
    Login To EC Application
    Open Account Screen
    Insert Account Record And Save
    Verify Account Record Exists
    Logout From EC Application

TC03 Update Account Data
    Login To EC Application
    Open Account Screen
    Update Account Record And Save
    Verify Account Record Updated
    Logout From EC Application

TC04 Find Account Data
    Login To EC Application
    Open Account Screen
    Find Account Record
    Verify Account Record Found
    Logout From EC Application

TC05 Delete Account Data
    Login To EC Application
    Open Account Screen
    Delete Account Record And Save
    Verify Account Record Removed
    Logout From EC Application
