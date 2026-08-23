*** Settings ***
Documentation       EC IUD Test - State Lease (Configuration > Assets > Commercial Objects > State Lease).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STATE_LEASE).
...                 Layered: this test -> state_lease_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_STL) rather than a
...                 generated unique code - confirmed absent from OV_STATE_LEASE before this was wired in.
...                 Every run must complete TC05 (delete) so the code is free for the next run - EC
...                 never lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in Suite
...                 Setup - not 5 separate browser launches. Converted from the old hardcoded-field-id
...                 pattern to the label-driven, properties-file-driven "Bank pattern" (Batch 4,
...                 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/state_lease_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    state-lease


*** Variables ***
${TEST_CODE}        AUTOTEST_STL
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open State Lease Screen
    Verify State Lease Record Does Not Exist
    Logout From EC Application

TC02 Insert State Lease Data
    Login To EC Application
    Open State Lease Screen
    Insert State Lease Record And Save
    Verify State Lease Record Exists
    Logout From EC Application

TC03 Update State Lease Data
    Login To EC Application
    Open State Lease Screen
    Update State Lease Record And Save
    Verify State Lease Record Updated
    Logout From EC Application

TC04 Find State Lease Data
    Login To EC Application
    Open State Lease Screen
    Find State Lease Record
    Verify State Lease Record Found
    Logout From EC Application

TC05 Delete State Lease Data
    Login To EC Application
    Open State Lease Screen
    Delete State Lease Record And Save
    Verify State Lease Record Removed
    Logout From EC Application
