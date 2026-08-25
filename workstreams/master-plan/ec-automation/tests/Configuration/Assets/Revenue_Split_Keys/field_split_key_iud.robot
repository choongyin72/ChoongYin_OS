*** Settings ***
Documentation       EC IUD Test - Field Split Key (Configuration > Assets > Revenue Split Keys >
...                 Field Split Key, BF_CODE CD.0095, class SPLIT_KEY, view OV_SPLIT_KEY).
...                 Manage-Object-shaped OV screen (Date+GO navigator, no mandatory scope) via the
...                 custom controller manage_object_split_key/CLASS_NAME/SPLIT_KEY/SPLIT_TYPE/
...                 FIELD. DELETE = End Date = Start Date (true delete in ov_split_key).
...                 Layered: this test -> field_split_key_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 One of 6 sibling "* Split Key" screens sharing the SAME base view
...                 OV_SPLIT_KEY (Product/Company/Field/Stream Item Category/Other/Stream Item),
...                 distinguished only by SPLIT_TYPE - uses a FIXED, uniquely-scoped test code
...                 (AUTOTEST_SPLITKEY_FIELD, confirmed absent from ov_split_key before this was
...                 wired in) rather than a generic AUTOTEST_SPLIT_KEY, specifically to avoid
...                 cross-screen collision with the 5 sibling builds. Every run must complete
...                 TC05 (delete) so the code stays free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches (same convention as Bank).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/field_split_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    field_split_key


*** Variables ***
${TEST_CODE}        AUTOTEST_SPLITKEY_FIELD
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Field Split Key Screen
    Verify Field Split Key Record Does Not Exist
    Logout From EC Application

TC02 Insert Field Split Key Data
    Login To EC Application
    Open Field Split Key Screen
    Insert Field Split Key Record And Save
    Verify Field Split Key Record Exists
    Logout From EC Application

TC03 Update Field Split Key Data
    Login To EC Application
    Open Field Split Key Screen
    Update Field Split Key Record And Save
    Verify Field Split Key Record Updated
    Logout From EC Application

TC04 Find Field Split Key Data
    Login To EC Application
    Open Field Split Key Screen
    Find Field Split Key Record
    Verify Field Split Key Record Found
    Logout From EC Application

TC05 Delete Field Split Key Data
    Login To EC Application
    Open Field Split Key Screen
    Delete Field Split Key Record And Save
    Verify Field Split Key Record Removed
    Logout From EC Application
