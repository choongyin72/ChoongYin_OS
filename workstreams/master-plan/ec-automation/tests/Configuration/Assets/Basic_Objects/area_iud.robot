*** Settings ***
Documentation       EC IUD Test - Area (Configuration > Assets > Basic Objects > Area).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit navigator + GO. DELETE = End Date = Start Date
...                 (true delete in OV_AREA). NEVER touch existing data.
...                 Layered: this test -> area_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner-directed exception, 2026-08-25) - Area remains OV-GM and still needs
...                 its genuine Production Unit navigator gesture; this is a structural
...                 conversion, not a reclassification of Area as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_AREA, owner-requested) rather than a
...                 generated unique code - confirmed absent from OV_AREA (2026-08-25) before
...                 this was wired in. Every run must complete TC05 (delete) so the code is
...                 free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/area_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    area


*** Variables ***
${TEST_CODE}        AUTOTEST_AREA
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Area Screen With Navigator Values Populated
    Verify Area Record Does Not Exist
    Logout From EC Application

TC02 Insert Area Data
    Login To EC Application
    Open Area Screen With Navigator Values Populated
    Insert Area Record And Save
    Verify Area Record Exists
    Logout From EC Application

TC03 Update Area Data
    Login To EC Application
    Open Area Screen With Navigator Values Populated
    Update Area Record And Save
    Verify Area Record Updated
    Logout From EC Application

TC04 Find Area Data
    Login To EC Application
    Open Area Screen With Navigator Values Populated
    Find Area Record
    Verify Area Record Found
    Logout From EC Application

TC05 Delete Area Data
    Login To EC Application
    Open Area Screen With Navigator Values Populated
    Delete Area Record And Save
    Verify Area Record Removed
    Logout From EC Application
