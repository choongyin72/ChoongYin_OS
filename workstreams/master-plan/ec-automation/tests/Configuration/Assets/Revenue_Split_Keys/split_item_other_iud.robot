*** Settings ***
Documentation       EC IUD Test - Split Item Other (Configuration > Assets > Revenue_Split_Keys >
...                 Split Item Other, CD.0017). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_SPLIT_ITEM_OTHER).
...                 Layered: this test -> split_item_other_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_SIO, matching
...                 Bank/Berth's convention) rather than a generated unique code - confirmed
...                 absent from OV_SPLIT_ITEM_OTHER before this was wired in (2026-08-23).
...                 Every run must complete TC05 (delete) so the code is free for the next run -
...                 EC never lets a DELETED code be reused, but this fixed code only stays
...                 reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/split_item_other_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    split_item_other


*** Variables ***
${TEST_CODE}        AUTOTEST_SIO
${OBJ_NAME}         AUTOTEST Split Item Other
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/split_item_other_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Split Item Other UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Split Item Other Screen
    Verify Split Item Other Record Does Not Exist
    Logout From EC Application

TC02 Insert Split Item Other Data
    Login To EC Application
    Open Split Item Other Screen
    Insert Split Item Other Record And Save
    Verify Split Item Other Record Exists
    Logout From EC Application

TC03 Update Split Item Other Data
    Login To EC Application
    Open Split Item Other Screen
    Update Split Item Other Record And Save
    Verify Split Item Other Record Updated
    Logout From EC Application

TC04 Find Split Item Other Data
    Login To EC Application
    Open Split Item Other Screen
    Find Split Item Other Record
    Verify Split Item Other Record Found
    Logout From EC Application

TC05 Delete Split Item Other Data
    Login To EC Application
    Open Split Item Other Screen
    Delete Split Item Other Record And Save
    Verify Split Item Other Record Removed
    Logout From EC Application
