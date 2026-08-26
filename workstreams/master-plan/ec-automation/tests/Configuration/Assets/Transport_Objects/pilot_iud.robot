*** Settings ***
Documentation       EC IUD Test - Pilot (Configuration > Assets > Transport_Objects, CO.2079).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory 3-level same-row navigator cascade (Production Unit -> Area ->
...                 Facility Class 1) + GO. DELETE = End Date = Start Date (true delete in
...                 OV_PILOT). NEVER touch existing data.
...                 Layered: this test -> pilot_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Pilot remains OV-GM and still needs its genuine 3-level
...                 navigator gesture; this is a structural conversion, not a reclassification of
...                 Pilot as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_PILOT) rather than a generated unique code -
...                 confirmed absent from OV_PILOT (2026-08-26, fresh oracledb query) before this
...                 was wired in. Every run must complete TC05 (delete) so the code is free for
...                 the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Well/Bank's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/pilot_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    pilot


*** Variables ***
${TEST_CODE}        AUTOTEST_PILOT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Pilot Screen With Navigator Values Populated
    Verify Pilot Record Does Not Exist
    Logout From EC Application

TC02 Insert Pilot Data
    Login To EC Application
    Open Pilot Screen With Navigator Values Populated
    Insert Pilot Record And Save
    Verify Pilot Record Exists
    Logout From EC Application

TC03 Update Pilot Data
    Login To EC Application
    Open Pilot Screen With Navigator Values Populated
    Update Pilot Record And Save
    Verify Pilot Record Updated
    Logout From EC Application

TC04 Find Pilot Data
    Login To EC Application
    Open Pilot Screen With Navigator Values Populated
    Find Pilot Record
    Verify Pilot Record Found
    Logout From EC Application

TC05 Delete Pilot Data
    Login To EC Application
    Open Pilot Screen With Navigator Values Populated
    Delete Pilot Record And Save
    Verify Pilot Record Removed
    Logout From EC Application
