*** Settings ***
Documentation       EC IUD Test - Production Separator (Configuration > Assets > Facility_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area -> Facility Class 1 3-level navigator
...                 cascade + GO. DELETE = End Date = Start Date (true delete in
...                 OV_PRODSEPARATOR). NEVER touch existing data.
...                 Layered: this test -> production_separator_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Production Separator remains
...                 OV-GM and still needs its genuine 3-level Production Unit -> Area -> Facility
...                 Class 1 navigator cascade + GO; this is a structural conversion, not a
...                 reclassification of the screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_PSEP) rather than a generated/timestamped
...                 code - confirmed absent from OV_PRODSEPARATOR (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    production_separator


*** Variables ***
${TEST_CODE}        AUTOTEST_PSEP
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Production Separator Screen With Navigator Values Populated
    Verify Production Separator Record Does Not Exist
    Logout From EC Application

TC02 Insert Production Separator Data
    Login To EC Application
    Open Production Separator Screen With Navigator Values Populated
    Insert Production Separator Record And Save
    Verify Production Separator Record Exists
    Logout From EC Application

TC03 Update Production Separator Data
    Login To EC Application
    Open Production Separator Screen With Navigator Values Populated
    Update Production Separator Record And Save
    Verify Production Separator Record Updated
    Logout From EC Application

TC04 Find Production Separator Data
    Login To EC Application
    Open Production Separator Screen With Navigator Values Populated
    Find Production Separator Record
    Verify Production Separator Record Found
    Logout From EC Application

TC05 Delete Production Separator Data
    Login To EC Application
    Open Production Separator Screen With Navigator Values Populated
    Delete Production Separator Record And Save
    Verify Production Separator Record Removed
    Logout From EC Application
