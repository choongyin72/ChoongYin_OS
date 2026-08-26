*** Settings ***
Documentation       EC IUD Test - External Location (Configuration > Assets > Facility_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid loads on GO ALONE - the
...                 navigator has NO mandatory scope (fields are optional filters), UNLIKE Area/
...                 Well/Test Separator/Chemical Tank. DELETE = End Date = Start Date (true
...                 delete in OV_EXTERNAL_LOCATION). NEVER touch existing data.
...                 Layered: this test -> external_location_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator section,
...                 matching Area's screen layout, follows Area's FULL pattern) - External
...                 Location's genuine GO-only/no-mandatory-nav-scope navigator behavior is KEPT
...                 EXACTLY as-is; this is a structural conversion, not a reclassification of the
...                 screen's navigator shape.
...                 Uses a FIXED test code (AUTOTEST_EXTERNAL_LOCATION, matching the AUTOTEST_
...                 <SCREEN> convention used by Area/Bank/Berth) rather than a generated unique
...                 code - confirmed absent from OV_EXTERNAL_LOCATION (2026-08-26) before this was
...                 wired in. Every run must complete TC05 (delete) so the code is free for the
...                 next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    external_location


*** Variables ***
${TEST_CODE}        AUTOTEST_EXTERNAL_LOCATION
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open External Location Screen With Navigator Values Populated
    Verify External Location Record Does Not Exist
    Logout From EC Application

TC02 Insert External Location Data
    Login To EC Application
    Open External Location Screen With Navigator Values Populated
    Insert External Location Record And Save
    Verify External Location Record Exists
    Logout From EC Application

TC03 Update External Location Data
    Login To EC Application
    Open External Location Screen With Navigator Values Populated
    Update External Location Record And Save
    Verify External Location Record Updated
    Logout From EC Application

TC04 Find External Location Data
    Login To EC Application
    Open External Location Screen With Navigator Values Populated
    Find External Location Record
    Verify External Location Record Found
    Logout From EC Application

TC05 Delete External Location Data
    Login To EC Application
    Open External Location Screen With Navigator Values Populated
    Delete External Location Record And Save
    Verify External Location Record Removed
    Logout From EC Application
