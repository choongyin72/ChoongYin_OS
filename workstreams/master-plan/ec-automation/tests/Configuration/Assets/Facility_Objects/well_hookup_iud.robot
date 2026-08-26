*** Settings ***
Documentation       EC IUD Test - Well Hookup (Configuration > Assets > Facility_Objects, CO.0108).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area -> Facility Class 1 3-level navigator
...                 cascade + GO. DELETE = End Date = Start Date (true delete in
...                 OV_WELL_HOOKUP). NEVER touch existing data.
...                 Layered: this test -> well_hookup_page (T3) -> manage_object (T2) + common
...                 (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Well Hookup remains OV-GM
...                 and still needs its genuine 3-level Production Unit -> Area -> Facility Class
...                 1 navigator cascade + GO; this is a structural conversion, not a
...                 reclassification of the screen as plain Bank/Area-shaped.
...                 Uses a FIXED test code (AUTOTEST_WH) rather than a generated/timestamped code
...                 - confirmed absent from OV_WELL_HOOKUP (2026-08-26, fresh oracledb connection)
...                 before this was wired in. Every run must complete TC05 (delete) so the code
...                 is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    well_hookup


*** Variables ***
${TEST_CODE}        AUTOTEST_WH
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Well Hookup Screen With Navigator Values Populated
    Verify Well Hookup Record Does Not Exist
    Logout From EC Application

TC02 Insert Well Hookup Data
    Login To EC Application
    Open Well Hookup Screen With Navigator Values Populated
    Insert Well Hookup Record And Save
    Verify Well Hookup Record Exists
    Logout From EC Application

TC03 Update Well Hookup Data
    Login To EC Application
    Open Well Hookup Screen With Navigator Values Populated
    Update Well Hookup Record And Save
    Verify Well Hookup Record Updated
    Logout From EC Application

TC04 Find Well Hookup Data
    Login To EC Application
    Open Well Hookup Screen With Navigator Values Populated
    Find Well Hookup Record
    Verify Well Hookup Record Found
    Logout From EC Application

TC05 Delete Well Hookup Data
    Login To EC Application
    Open Well Hookup Screen With Navigator Values Populated
    Delete Well Hookup Record And Save
    Verify Well Hookup Record Removed
    Logout From EC Application
