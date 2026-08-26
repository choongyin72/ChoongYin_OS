*** Settings ***
Documentation       EC IUD Test - Field (Configuration > Assets > Commercial Objects > Field).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Area navigator + GO. DELETE = End Date = Start Date (true delete
...                 in OV_FIELD). NEVER touch existing data.
...                 Layered: this test -> field_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout must follow Area's FULL pattern) - Field remains OV-GM and
...                 still needs its genuine Area navigator gesture; this is a structural
...                 conversion, not a reclassification of Field as plain Bank-shaped. Follow-up
...                 to PR #525, which only converted the navigator-fill piece.
...                 Uses a FIXED test code (AUTOTEST_FIELD, confirmed absent from OV_FIELD
...                 2026-08-26) rather than a generated unique code. Every run must complete
...                 TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Bank/Berth/Area's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/field_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    field


*** Variables ***
${TEST_CODE}        AUTOTEST_FIELD
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Field Screen With Navigator Values Populated
    Verify Field Record Does Not Exist
    Logout From EC Application

TC02 Insert Field Data
    Login To EC Application
    Open Field Screen With Navigator Values Populated
    Insert Field Record And Save
    Verify Field Record Exists
    Logout From EC Application

TC03 Update Field Data
    Login To EC Application
    Open Field Screen With Navigator Values Populated
    Update Field Record And Save
    Verify Field Record Updated
    Logout From EC Application

TC04 Find Field Data
    Login To EC Application
    Open Field Screen With Navigator Values Populated
    Find Field Record
    Verify Field Record Found
    Logout From EC Application

TC05 Delete Field Data
    Login To EC Application
    Open Field Screen With Navigator Values Populated
    Delete Field Record And Save
    Verify Field Record Removed
    Logout From EC Application
