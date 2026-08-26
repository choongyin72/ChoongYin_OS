*** Settings ***
Documentation       EC IUD Test - Sub Area (Configuration > Assets > Basic Objects > Sub Area).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area 2-level navigator cascade + GO. DELETE =
...                 End Date = Start Date (true delete in OV_SUB_AREA). NEVER touch existing
...                 data.
...                 Layered: this test -> sub_area_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Sub Area remains OV-GM and
...                 still needs its genuine 2-level Production Unit -> Area navigator cascade +
...                 GO; this is a structural conversion, not a reclassification of the screen as
...                 plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_SUB_AREA) rather than a generated/timestamped
...                 code - confirmed absent from OV_SUB_AREA (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    sub-area


*** Variables ***
${TEST_CODE}        AUTOTEST_SUB_AREA
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Sub Area Screen With Navigator Values Populated
    Verify Sub Area Record Does Not Exist
    Logout From EC Application

TC02 Insert Sub Area Data
    Login To EC Application
    Open Sub Area Screen With Navigator Values Populated
    Insert Sub Area Record And Save
    Verify Sub Area Record Exists
    Logout From EC Application

TC03 Update Sub Area Data
    Login To EC Application
    Open Sub Area Screen With Navigator Values Populated
    Update Sub Area Record And Save
    Verify Sub Area Record Updated
    Logout From EC Application

TC04 Find Sub Area Data
    Login To EC Application
    Open Sub Area Screen With Navigator Values Populated
    Find Sub Area Record
    Verify Sub Area Record Found
    Logout From EC Application

TC05 Delete Sub Area Data
    Login To EC Application
    Open Sub Area Screen With Navigator Values Populated
    Delete Sub Area Record And Save
    Verify Sub Area Record Removed
    Logout From EC Application
