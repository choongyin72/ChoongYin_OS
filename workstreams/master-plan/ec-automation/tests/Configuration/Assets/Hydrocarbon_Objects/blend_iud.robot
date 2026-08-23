*** Settings ***
Documentation       EC IUD Test - Blend (Configuration > Assets > Hydrocarbon Objects > Blend, CO.0219).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BLEND).
...                 Layered: this test -> blend_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_BLEND) rather than a
...                 generated unique code - confirmed absent from OV_BLEND before this was wired in.
...                 Every run must complete TC05 (delete) so the code is free for the next run - EC
...                 never lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in Suite
...                 Setup - not 5 separate browser launches. Converted from the partial label-driven
...                 pattern to the full properties-file-driven, grid-filter-wired "Bank pattern"
...                 (Batch 7, 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Hydrocarbon_Objects/blend_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    blend


*** Variables ***
${TEST_CODE}        AUTOTEST_BLEND
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Blend Screen
    Verify Blend Record Does Not Exist
    Logout From EC Application

TC02 Insert Blend Data
    Login To EC Application
    Open Blend Screen
    Insert Blend Record And Save
    Verify Blend Record Exists
    Logout From EC Application

TC03 Update Blend Data
    Login To EC Application
    Open Blend Screen
    Update Blend Record And Save
    Verify Blend Record Updated
    Logout From EC Application

TC04 Find Blend Data
    Login To EC Application
    Open Blend Screen
    Find Blend Record
    Verify Blend Record Found
    Logout From EC Application

TC05 Delete Blend Data
    Login To EC Application
    Open Blend Screen
    Delete Blend Record And Save
    Verify Blend Record Removed
    Logout From EC Application
