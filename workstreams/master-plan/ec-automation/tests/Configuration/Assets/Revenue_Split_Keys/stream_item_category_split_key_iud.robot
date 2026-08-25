*** Settings ***
Documentation       EC IUD Test - Stream Item Category Split Key (Configuration > Assets >
...                 Revenue Split Keys > Stream Item Category Split Key, CD.0042). Custom-URL
...                 OV (no navigator/GO at all - grid nav:form:T_data renders directly on
...                 open). DELETE = End Date = Start Date (true delete in OV_SPLIT_KEY).
...                 Layered: this test -> stream_item_category_split_key_page (T3) ->
...                 manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_SPLITKEY_STREAMCAT) rather than a generated unique code -
...                 confirmed absent from OV_SPLIT_KEY before this was wired in (2026-08-25).
...                 Every run must complete TC05 (delete) so the code is free for the next
...                 run - EC never lets a DELETED code be reused, but this fixed code only
...                 stays reusable if each run actually cleans up after itself.
...                 IMPORTANT - OV_SPLIT_KEY is a SHARED base view written to by 6 sibling
...                 "Split Key" screens (Product/Company/Field/Stream Item Category/Other/
...                 Stream Item), distinguished only by SPLIT_TYPE (server-set from the menu
...                 entry opened). This suite's own test code is deliberately scoped
...                 (AUTOTEST_SPLITKEY_STREAMCAT, not a generic AUTOTEST_SPLIT_KEY) to avoid
...                 colliding with the other 5 screens' own fixed test codes.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/Report Context's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/stream_item_category_split_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    stream_item_category_split_key


*** Variables ***
${TEST_CODE}        AUTOTEST_SPLITKEY_STREAMCAT
${OBJ_NAME}         AUTOTEST Stream Item Category Split Key
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/stream_item_category_split_key_update.properties - TC03
# verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Stream Item Category Split Key UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Stream Item Category Split Key Screen
    Verify Stream Item Category Split Key Record Does Not Exist
    Logout From EC Application

TC02 Insert Stream Item Category Split Key Data
    Login To EC Application
    Open Stream Item Category Split Key Screen
    Insert Stream Item Category Split Key Record And Save
    Verify Stream Item Category Split Key Record Exists
    Logout From EC Application

TC03 Update Stream Item Category Split Key Data
    Login To EC Application
    Open Stream Item Category Split Key Screen
    Update Stream Item Category Split Key Record And Save
    Verify Stream Item Category Split Key Record Updated
    Logout From EC Application

TC04 Find Stream Item Category Split Key Data
    Login To EC Application
    Open Stream Item Category Split Key Screen
    Find Stream Item Category Split Key Record
    Verify Stream Item Category Split Key Record Found
    Logout From EC Application

TC05 Delete Stream Item Category Split Key Data
    Login To EC Application
    Open Stream Item Category Split Key Screen
    Delete Stream Item Category Split Key Record And Save
    Verify Stream Item Category Split Key Record Removed
    Logout From EC Application
