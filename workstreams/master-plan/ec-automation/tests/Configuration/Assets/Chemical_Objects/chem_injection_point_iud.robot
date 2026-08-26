*** Settings ***
Documentation       EC IUD Test - Chemical Injection Point (Configuration > Assets > Chemical
...                 Objects > Chemical Injection Point, CO.0212).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area -> Facility Class 1 3-level navigator
...                 cascade + GO. DELETE = End Date = Start Date (true delete in
...                 OV_CHEM_INJ_POINT). NEVER touch existing data.
...                 Layered: this test -> chem_injection_point_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Chemical Injection Point
...                 remains OV-GM and still needs its genuine 3-level Production Unit -> Area ->
...                 Facility Class 1 navigator cascade + GO; this is a structural conversion, not
...                 a reclassification of the screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_CIP) rather than a generated/timestamped
...                 code - confirmed absent from OV_CHEM_INJ_POINT (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete)
...                 so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chem_injection_point_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    chem_injection_point


*** Variables ***
${TEST_CODE}        AUTOTEST_CIP
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Chemical Injection Point Screen With Navigator Values Populated
    Verify Chemical Injection Point Record Does Not Exist
    Logout From EC Application

TC02 Insert Chemical Injection Point Data
    Login To EC Application
    Open Chemical Injection Point Screen With Navigator Values Populated
    Insert Chemical Injection Point Record And Save
    Verify Chemical Injection Point Record Exists
    Logout From EC Application

TC03 Update Chemical Injection Point Data
    Login To EC Application
    Open Chemical Injection Point Screen With Navigator Values Populated
    Update Chemical Injection Point Record And Save
    Verify Chemical Injection Point Record Updated
    Logout From EC Application

TC04 Find Chemical Injection Point Data
    Login To EC Application
    Open Chemical Injection Point Screen With Navigator Values Populated
    Find Chemical Injection Point Record
    Verify Chemical Injection Point Record Found
    Logout From EC Application

TC05 Delete Chemical Injection Point Data
    Login To EC Application
    Open Chemical Injection Point Screen With Navigator Values Populated
    Delete Chemical Injection Point Record And Save
    Verify Chemical Injection Point Record Removed
    Logout From EC Application
