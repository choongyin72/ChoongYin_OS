*** Settings ***
Documentation       EC IUD Test - Facility Class 1 (Configuration > Assets > Facility_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area 2-level navigator cascade + GO. DELETE =
...                 End Date = Start Date (true delete in OV_FCTY_CLASS_1). NEVER touch existing
...                 data.
...                 Layered: this test -> facility_class_1_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Facility Class 1 remains
...                 OV-GM and still needs its genuine 2-level Production Unit -> Area navigator
...                 cascade + GO; this is a structural conversion, not a reclassification of the
...                 screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_FC1) rather than a generated/timestamped
...                 code - confirmed absent from OV_FCTY_CLASS_1 (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    facility_class_1


*** Variables ***
${TEST_CODE}        AUTOTEST_FC1
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Facility Class 1 Screen With Navigator Values Populated
    Verify Facility Class 1 Record Does Not Exist
    Logout From EC Application

TC02 Insert Facility Class 1 Data
    Login To EC Application
    Open Facility Class 1 Screen With Navigator Values Populated
    Insert Facility Class 1 Record And Save
    Verify Facility Class 1 Record Exists
    Logout From EC Application

TC03 Update Facility Class 1 Data
    Login To EC Application
    Open Facility Class 1 Screen With Navigator Values Populated
    Update Facility Class 1 Record And Save
    Verify Facility Class 1 Record Updated
    Logout From EC Application

TC04 Find Facility Class 1 Data
    Login To EC Application
    Open Facility Class 1 Screen With Navigator Values Populated
    Find Facility Class 1 Record
    Verify Facility Class 1 Record Found
    Logout From EC Application

TC05 Delete Facility Class 1 Data
    Login To EC Application
    Open Facility Class 1 Screen With Navigator Values Populated
    Delete Facility Class 1 Record And Save
    Verify Facility Class 1 Record Removed
    Logout From EC Application
