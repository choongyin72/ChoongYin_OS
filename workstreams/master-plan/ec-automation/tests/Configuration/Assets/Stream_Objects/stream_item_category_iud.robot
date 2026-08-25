*** Settings ***
Documentation       EC IUD Test - Stream Item Category (Configuration > Assets > Stream_Objects >
...                 Stream Item Category, CD.0016). Manage-Object (OV) screen. DELETE = End Date =
...                 Start Date (true delete in OV_STREAM_ITEM_CATEGORY).
...                 Layered: this test -> stream_item_category_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_SIC, confirmed absent from OV_STREAM_ITEM_CATEGORY before this was
...                 wired in) rather than a generated unique code, matching Bank's convention.
...                 Every run must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches, matching Bank/Berth's
...                 convention (owner-requested 2026-08-18/22).
...                 Rebuilt (Batch 10) from the older 4-TC no-filter/no-properties pattern to
...                 the full 5-TC properties-file-driven, grid-filter-wired pattern.
...                 PURE SCREEN verification (matches bank_iud.robot's owner-requested
...                 2026-08-18 convention: no DB check here) - removed the extra inline
...                 DB-read keywords this suite originally had, to match Bank exactly
...                 (2026-08-25 alignment fix).

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/stream_item_category_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    stream_item_category


*** Variables ***
${TEST_CODE}        AUTOTEST_SIC
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/stream_item_category_insert.properties - TC02 verifies on
# screen against what that file actually set, not an independent assumption.
${OBJ_NAME}         AUTOTEST Stream Item Category
# Must stay in sync with testdata/stream_item_category_update.properties - TC03 verifies on
# screen against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}     AUTOTEST Stream Item Category UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Stream Item Category Screen
    Verify Stream Item Category Record Does Not Exist
    Logout From EC Application

TC02 Insert Stream Item Category Data
    Login To EC Application
    Open Stream Item Category Screen
    Insert Stream Item Category Record And Save
    Verify Stream Item Category Record Exists
    Logout From EC Application

TC03 Update Stream Item Category Data
    Login To EC Application
    Open Stream Item Category Screen
    Update Stream Item Category Record And Save
    Verify Stream Item Category Record Updated
    Logout From EC Application

TC04 Find Stream Item Category Data
    Login To EC Application
    Open Stream Item Category Screen
    Find Stream Item Category Record
    Verify Stream Item Category Record Found
    Logout From EC Application

TC05 Delete Stream Item Category Data
    Login To EC Application
    Open Stream Item Category Screen
    Delete Stream Item Category Record And Save
    Verify Stream Item Category Record Removed
    Logout From EC Application
