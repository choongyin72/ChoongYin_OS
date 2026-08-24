*** Settings ***
Documentation       EC IUD Test - Stream - All (EC Production > Stream - All, CD.0007).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STREAM).
...                 Layered: this test -> stream_all_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_STREAM,
...                 matching Bank/Berth's convention) rather than a generated unique code -
...                 confirmed absent from OV_STREAM before this was wired in (2026-08-24).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).
...                 Genuinely new build 2026-08-24 - no prior automation existed for class
...                 STREAM/view OV_STREAM anywhere in the repo (docs/ov-reuse-targets.md's
...                 "covered" claim for this screen was stale/wrong, corrected in this PR).

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/stream_all_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    stream_all


*** Variables ***
${TEST_CODE}        AUTOTEST_STREAM
${OBJ_NAME}         AUTOTEST Stream
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/stream_all_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Stream UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Stream All Screen
    Verify Stream All Record Does Not Exist
    Logout From EC Application

TC02 Insert Stream All Data
    Login To EC Application
    Open Stream All Screen
    Insert Stream All Record And Save
    Verify Stream All Record Exists
    Logout From EC Application

TC03 Update Stream All Data
    Login To EC Application
    Open Stream All Screen
    Update Stream All Record And Save
    Verify Stream All Record Updated
    Logout From EC Application

TC04 Find Stream All Data
    Login To EC Application
    Open Stream All Screen
    Find Stream All Record
    Verify Stream All Record Found
    Logout From EC Application

TC05 Delete Stream All Data
    Login To EC Application
    Open Stream All Screen
    Delete Stream All Record And Save
    Verify Stream All Record Removed
    Logout From EC Application
