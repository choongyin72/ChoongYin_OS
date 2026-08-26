*** Settings ***
Documentation       EC IUD Test - Well (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory 3-level P1 navigator cascade (Production Unit -> Area -> Facility 1)
...                 + GO. DELETE = End Date = Start Date (true delete in OV_WELL). NEVER touch
...                 existing data.
...                 Layered: this test -> well_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Well remains OV-GM and still needs its genuine 3-level P1
...                 navigator gesture; this is a structural conversion, not a reclassification of
...                 Well as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_WELL) rather than a generated unique code -
...                 confirmed absent from OV_WELL (2026-08-26, fresh oracledb query) before this
...                 was wired in. Every run must complete TC05 (delete) so the code is free for
...                 the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    well


*** Variables ***
${TEST_CODE}        AUTOTEST_WELL
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Well Screen With Navigator Values Populated
    Verify Well Record Does Not Exist
    Logout From EC Application

TC02 Insert Well Data
    Login To EC Application
    Open Well Screen With Navigator Values Populated
    Insert Well Record And Save
    Verify Well Record Exists
    Logout From EC Application

TC03 Update Well Data
    Login To EC Application
    Open Well Screen With Navigator Values Populated
    Update Well Record And Save
    Verify Well Record Updated
    Logout From EC Application

TC04 Find Well Data
    Login To EC Application
    Open Well Screen With Navigator Values Populated
    Find Well Record
    Verify Well Record Found
    Logout From EC Application

TC05 Delete Well Data
    Login To EC Application
    Open Well Screen With Navigator Values Populated
    Delete Well Record And Save
    Verify Well Record Removed
    Logout From EC Application
