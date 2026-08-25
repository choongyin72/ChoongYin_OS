*** Settings ***
Documentation       EC IUD Test - Input List (Configuration > Assets > Revenue_Lists > Input List,
...                 CD.0035). Manage-Object (OV) screen. DELETE = End Date = Start Date (true
...                 delete in OV_STREAM_ITEM_COLLECTION). Layered: this test -> input_list_page
...                 (T3) -> manage_object (T2) + common (T1). NEVER touch existing data. Uses a
...                 FIXED test code (AUTOTEST_INPUTLIST) rather than a generated unique code -
...                 confirmed absent from OV_STREAM_ITEM_COLLECTION before this was wired in
...                 (2026-08-25, fresh oracledb query). Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Object List's convention (docs/rf-suite-styles.md).
...                 Bank-pattern conversion (2026-08-25): replaces the earlier generated suite,
...                 which called DB-verify keywords (Input List Should Exist In DB / Should Not
...                 Exist In DB / Field Should Equal In View) directly from these test cases -
...                 this suite is PURE SCREEN verification only; DB ground-truth lives inside the
...                 shared T2 keywords (Verify Object Removed) this delegates to.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Lists/input_list_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    input_list


*** Variables ***
${TEST_CODE}        AUTOTEST_INPUTLIST
${OBJ_NAME}         AUTOTEST Input List
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/input_list_insert.properties - TC02 verifies against it.
${LIST_CATEGORY}    INPUT
# Must stay in sync with testdata/input_list_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Input List UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Input List Screen
    Verify Input List Record Does Not Exist
    Logout From EC Application

TC02 Insert Input List Data
    Login To EC Application
    Open Input List Screen
    Insert Input List Record And Save
    Verify Input List Record Exists
    Logout From EC Application

TC03 Update Input List Data
    Login To EC Application
    Open Input List Screen
    Update Input List Record And Save
    Verify Input List Record Updated
    Logout From EC Application

TC04 Find Input List Data
    Login To EC Application
    Open Input List Screen
    Find Input List Record
    Verify Input List Record Found
    Logout From EC Application

TC05 Delete Input List Data
    Login To EC Application
    Open Input List Screen
    Delete Input List Record And Save
    Verify Input List Record Removed
    Logout From EC Application
