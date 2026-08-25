*** Settings ***
Documentation       EC IUD Test - Stream Item Split Key (Configuration > Assets >
...                 Revenue_Split_Keys > Stream Item Split Key, BF_CODE CD.0156). Class
...                 SPLIT_KEY, SPLIT_TYPE=STREAM_ITEM_SPLIT, view OV_SPLIT_KEY. Manage-Object
...                 (OV) screen. DELETE = End Date = Start Date (true delete in OV_SPLIT_KEY).
...                 One of 6 sibling "* Split Key" screens (Product/Company/Field/Stream Item
...                 Category/Other/Stream Item) that ALL share the SAME base view OV_SPLIT_KEY,
...                 differentiated only by SPLIT_TYPE. Uses a distinctly-scoped fixed test code
...                 (AUTOTEST_SPLITKEY_STREAMITEM, NOT the generic AUTOTEST_SPLIT_KEY) so this
...                 screen's IUD run can never collide with a sibling Split Key screen's own
...                 rows in the same shared view - confirmed free in OV_SPLIT_KEY before this
...                 was wired in (2026-08-25).
...                 Layered: this test -> stream_item_split_key_page (T3) -> manage_object (T2)
...                 + common (T1).
...                 NEVER touch existing data. Every run must complete TC05 (delete) so the code
...                 is free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Berth/Split Item Other's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/stream_item_split_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    stream_item_split_key


*** Variables ***
${TEST_CODE}        AUTOTEST_SPLITKEY_STREAMITEM
${OBJ_NAME}         AUTOTEST Stream Item Split Key
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/stream_item_split_key_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Stream Item Split Key UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Stream Item Split Key Screen
    Verify Stream Item Split Key Record Does Not Exist
    Logout From EC Application

TC02 Insert Stream Item Split Key Data
    Login To EC Application
    Open Stream Item Split Key Screen
    Insert Stream Item Split Key Record And Save
    Verify Stream Item Split Key Record Exists
    Logout From EC Application

TC03 Update Stream Item Split Key Data
    Login To EC Application
    Open Stream Item Split Key Screen
    Update Stream Item Split Key Record And Save
    Verify Stream Item Split Key Record Updated
    Logout From EC Application

TC04 Find Stream Item Split Key Data
    Login To EC Application
    Open Stream Item Split Key Screen
    Find Stream Item Split Key Record
    Verify Stream Item Split Key Record Found
    Logout From EC Application

TC05 Delete Stream Item Split Key Data
    Login To EC Application
    Open Stream Item Split Key Screen
    Delete Stream Item Split Key Record And Save
    Verify Stream Item Split Key Record Removed
    Logout From EC Application
