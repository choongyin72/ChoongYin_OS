*** Settings ***
Documentation       EC IUD Test - Storage (Configuration > Assets > Tank_and_Storage_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area -> Facility Class 1 3-level navigator
...                 cascade + GO. DELETE = End Date = Start Date (true delete in OV_STORAGE).
...                 NEVER touch existing data.
...                 Layered: this test -> storage_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Storage remains OV-GM and
...                 still needs its genuine 3-level Production Unit -> Area -> Facility Class 1
...                 navigator cascade + GO; this is a structural conversion, not a
...                 reclassification of the screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_STG) rather than a generated/timestamped
...                 code - confirmed absent from OV_STORAGE (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    storage


*** Variables ***
${TEST_CODE}        AUTOTEST_STG
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Storage Screen With Navigator Values Populated
    Verify Storage Record Does Not Exist
    Logout From EC Application

TC02 Insert Storage Data
    Login To EC Application
    Open Storage Screen With Navigator Values Populated
    Insert Storage Record And Save
    Verify Storage Record Exists
    Logout From EC Application

TC03 Update Storage Data
    Login To EC Application
    Open Storage Screen With Navigator Values Populated
    Update Storage Record And Save
    Verify Storage Record Updated
    Logout From EC Application

TC04 Find Storage Data
    Login To EC Application
    Open Storage Screen With Navigator Values Populated
    Find Storage Record
    Verify Storage Record Found
    Logout From EC Application

TC05 Delete Storage Data
    Login To EC Application
    Open Storage Screen With Navigator Values Populated
    Delete Storage Record And Save
    Verify Storage Record Removed
    Logout From EC Application
