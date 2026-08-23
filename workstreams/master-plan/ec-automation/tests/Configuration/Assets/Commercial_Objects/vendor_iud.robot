*** Settings ***
Documentation       EC IUD Test - Vendor (Configuration > Assets > Commercial Objects > Vendor).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_vendor).
...                 Layered: this test -> vendor_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_VEND) rather than a
...                 generated unique code - confirmed absent from OV_VENDOR before this was wired in.
...                 Every run must complete TC05 (delete) so the code is free for the next run - EC
...                 never lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in Suite
...                 Setup - not 5 separate browser launches. Converted from the old hardcoded-field-id
...                 pattern to the label-driven, properties-file-driven "Bank pattern" (Batch 4,
...                 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    vendor


*** Variables ***
${TEST_CODE}        AUTOTEST_VEND
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Vendor Screen
    Verify Vendor Record Does Not Exist
    Logout From EC Application

TC02 Insert Vendor Data
    Login To EC Application
    Open Vendor Screen
    Insert Vendor Record And Save
    Verify Vendor Record Exists
    Logout From EC Application

TC03 Update Vendor Data
    Login To EC Application
    Open Vendor Screen
    Update Vendor Record And Save
    Verify Vendor Record Updated
    Logout From EC Application

TC04 Find Vendor Data
    Login To EC Application
    Open Vendor Screen
    Find Vendor Record
    Verify Vendor Record Found
    Logout From EC Application

TC05 Delete Vendor Data
    Login To EC Application
    Open Vendor Screen
    Delete Vendor Record And Save
    Verify Vendor Record Removed
    Logout From EC Application
