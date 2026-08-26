*** Settings ***
Documentation       EC IUD Test - Well Hole (Configuration > Assets > Well_and_Reservoir_Objects > Well Hole, CO.0051).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory 3-level navigator cascade (Op Production Unit -> Op Area ->
...                 Op Facility Class 1) + GO. DELETE = End Date = Start Date (true delete in
...                 OV_WELL_HOLE). NEVER touch existing data.
...                 Layered: this test -> well_hole_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to Area's full pattern (2026-08-26): 5-TC/per-TC-login/
...                 pure-screen-verify STRUCTURE, replacing the OLD 4-TC/"Apply OV-GM Navigator
...                 First Available"/single-suite-login/generated-timestamp-code shape - Well
...                 Hole remains OV-GM and still needs its genuine 3-level navigator gesture;
...                 this is a structural conversion, not a reclassification.
...                 Uses a FIXED test code (AUTOTEST_WELL_HOLE) rather than a generated unique
...                 code - confirmed absent from OV_WELL_HOLE (2026-08-26) before this was wired
...                 in. Every run must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    well_hole


*** Variables ***
${TEST_CODE}        AUTOTEST_WELL_HOLE
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Well Hole Screen With Navigator Values Populated
    Verify Well Hole Record Does Not Exist
    Logout From EC Application

TC02 Insert Well Hole Data
    Login To EC Application
    Open Well Hole Screen With Navigator Values Populated
    Insert Well Hole Record And Save
    Verify Well Hole Record Exists
    Logout From EC Application

TC03 Update Well Hole Data
    Login To EC Application
    Open Well Hole Screen With Navigator Values Populated
    Update Well Hole Record And Save
    Verify Well Hole Record Updated
    Logout From EC Application

TC04 Find Well Hole Data
    Login To EC Application
    Open Well Hole Screen With Navigator Values Populated
    Find Well Hole Record
    Verify Well Hole Record Found
    Logout From EC Application

TC05 Delete Well Hole Data
    Login To EC Application
    Open Well Hole Screen With Navigator Values Populated
    Delete Well Hole Record And Save
    Verify Well Hole Record Removed
    Logout From EC Application
