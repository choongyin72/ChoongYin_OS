*** Settings ***
Documentation       EC IUD Test - Cost Object Mapping (Configuration > Assets > Financial
...                 Objects > Cost Object Mapping). Manage-Object (OV) screen. DELETE = End
...                 Date = Start Date (true delete in OV_FIN_COST_OBJECT).
...                 Layered: this test -> cost_object_mapping_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_CMAP) rather than a generated unique code - confirmed absent from
...                 OV_FIN_COST_OBJECT before this was wired in. Every run must complete TC05
...                 (delete) so the code is free for the next run - EC never lets a DELETED code
...                 be reused, but this fixed code only stays reusable if each run actually
...                 cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches. Converted from the old
...                 hardcoded-field-id pattern to the label-driven, properties-file-driven "Bank
...                 pattern" (Batch 4, 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    cost-object-mapping


*** Variables ***
${TEST_CODE}        AUTOTEST_CMAP
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Cost Object Mapping Screen
    Verify Cost Object Mapping Record Does Not Exist
    Logout From EC Application

TC02 Insert Cost Object Mapping Data
    Login To EC Application
    Open Cost Object Mapping Screen
    Insert Cost Object Mapping Record And Save
    Verify Cost Object Mapping Record Exists
    Logout From EC Application

TC03 Update Cost Object Mapping Data
    Login To EC Application
    Open Cost Object Mapping Screen
    Update Cost Object Mapping Record And Save
    Verify Cost Object Mapping Record Updated
    Logout From EC Application

TC04 Find Cost Object Mapping Data
    Login To EC Application
    Open Cost Object Mapping Screen
    Find Cost Object Mapping Record
    Verify Cost Object Mapping Record Found
    Logout From EC Application

TC05 Delete Cost Object Mapping Data
    Login To EC Application
    Open Cost Object Mapping Screen
    Delete Cost Object Mapping Record And Save
    Verify Cost Object Mapping Record Removed
    Logout From EC Application
