*** Settings ***
Documentation       EC IUD Test - Shift (Configuration > Assets > Facility_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory 3-level Production Unit -> Area -> Facility Class 1 navigator
...                 cascade (SPECIFIC P1 values) + GO. Insert form ALSO requires a mandatory
...                 free-text Start Time (HH:MI), kept exactly as the prior driver proved it -
...                 this conversion is about the navigator/TC-structure only. DELETE = End
...                 Date = Start Date (true delete in OV_SHIFT). NEVER touch existing data.
...                 Layered: this test -> shift_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Shift remains OV-GM and
...                 still needs its genuine 3-level P1 navigator cascade + GO; this is a
...                 structural conversion, not a reclassification of the screen as plain
...                 Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_SHIFT) rather than a generated/timestamped
...                 code - confirmed absent from OV_SHIFT (2026-08-26, fresh oracledb connection)
...                 before this was wired in. Every run must complete TC05 (delete) so the code
...                 is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/shift_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    shift


*** Variables ***
${TEST_CODE}        AUTOTEST_SHIFT
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Shift Screen With Navigator Values Populated
    Verify Shift Record Does Not Exist
    Logout From EC Application

TC02 Insert Shift Data
    Login To EC Application
    Open Shift Screen With Navigator Values Populated
    Insert Shift Record And Save
    Verify Shift Record Exists
    Logout From EC Application

TC03 Update Shift Data
    Login To EC Application
    Open Shift Screen With Navigator Values Populated
    Update Shift Record And Save
    Verify Shift Record Updated
    Logout From EC Application

TC04 Find Shift Data
    Login To EC Application
    Open Shift Screen With Navigator Values Populated
    Find Shift Record
    Verify Shift Record Found
    Logout From EC Application

TC05 Delete Shift Data
    Login To EC Application
    Open Shift Screen With Navigator Values Populated
    Delete Shift Record And Save
    Verify Shift Record Removed
    Logout From EC Application
