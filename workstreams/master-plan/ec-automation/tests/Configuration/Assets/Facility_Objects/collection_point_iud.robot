*** Settings ***
Documentation       EC IUD Test - Collection Point (Configuration > Assets > Facility_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area -> Operator Route 3-level navigator
...                 cascade + GO. DELETE = End Date = Start Date (true delete in
...                 OV_COLLECTION_POINT). NEVER touch existing data.
...                 Layered: this test -> collection_point_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule: any EC screen with a navigator matching Area's layout
...                 MUST follow Area's FULL pattern) - Collection Point remains OV-GM and still
...                 needs its genuine 3-level Production Unit -> Area -> Operator Route
...                 navigator cascade + GO; this is a structural conversion, not a
...                 reclassification of the screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_COLLECTION_POINT) rather than a
...                 generated/timestamped code - confirmed absent from OV_COLLECTION_POINT
...                 (2026-08-26, fresh oracledb connection, 0 rows) before this was wired in.
...                 Every run must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    collection_point


*** Variables ***
${TEST_CODE}        AUTOTEST_COLLECTION_POINT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Collection Point Screen With Navigator Values Populated
    Verify Collection Point Record Does Not Exist
    Logout From EC Application

TC02 Insert Collection Point Data
    Login To EC Application
    Open Collection Point Screen With Navigator Values Populated
    Insert Collection Point Record And Save
    Verify Collection Point Record Exists
    Logout From EC Application

TC03 Update Collection Point Data
    Login To EC Application
    Open Collection Point Screen With Navigator Values Populated
    Update Collection Point Record And Save
    Verify Collection Point Record Updated
    Logout From EC Application

TC04 Find Collection Point Data
    Login To EC Application
    Open Collection Point Screen With Navigator Values Populated
    Find Collection Point Record
    Verify Collection Point Record Found
    Logout From EC Application

TC05 Delete Collection Point Data
    Login To EC Application
    Open Collection Point Screen With Navigator Values Populated
    Delete Collection Point Record And Save
    Verify Collection Point Record Removed
    Logout From EC Application
