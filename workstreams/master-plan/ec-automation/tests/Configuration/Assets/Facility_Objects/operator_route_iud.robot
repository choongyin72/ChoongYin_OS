*** Settings ***
Documentation       EC IUD Test - Operator Route (Configuration > Assets > Facility_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area 2-level navigator cascade + GO. DELETE =
...                 End Date = Start Date (true delete in OV_OPERATOR_ROUTE). NEVER touch
...                 existing data.
...                 Layered: this test -> operator_route_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Operator Route remains
...                 OV-GM and still needs its genuine 2-level Production Unit -> Area navigator
...                 cascade + GO; this is a structural conversion, not a reclassification of the
...                 screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_OR) rather than a generated/timestamped
...                 code - confirmed absent from OV_OPERATOR_ROUTE (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete)
...                 so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth/Facility Class 1's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    operator_route


*** Variables ***
${TEST_CODE}        AUTOTEST_OR
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Operator Route Screen With Navigator Values Populated
    Verify Operator Route Record Does Not Exist
    Logout From EC Application

TC02 Insert Operator Route Data
    Login To EC Application
    Open Operator Route Screen With Navigator Values Populated
    Insert Operator Route Record And Save
    Verify Operator Route Record Exists
    Logout From EC Application

TC03 Update Operator Route Data
    Login To EC Application
    Open Operator Route Screen With Navigator Values Populated
    Update Operator Route Record And Save
    Verify Operator Route Record Updated
    Logout From EC Application

TC04 Find Operator Route Data
    Login To EC Application
    Open Operator Route Screen With Navigator Values Populated
    Find Operator Route Record
    Verify Operator Route Record Found
    Logout From EC Application

TC05 Delete Operator Route Data
    Login To EC Application
    Open Operator Route Screen With Navigator Values Populated
    Delete Operator Route Record And Save
    Verify Operator Route Record Removed
    Logout From EC Application
