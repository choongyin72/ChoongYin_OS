*** Settings ***
Documentation       EC IUD Test - Contract Area (Configuration > Assets > Contract Objects > Contract Area).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Business Unit navigator + GO. DELETE = End Date = Start Date
...                 (true delete in OV_CONTRACT_AREA). NEVER touch existing data.
...                 Layered: this test -> contract_area_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26, mirroring area_iud.robot exactly) - Contract Area remains OV-GM
...                 and still needs its genuine Business Unit navigator gesture; this is a
...                 structural conversion, not a reclassification of Contract Area as plain
...                 Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_CONTRACT_AREA) rather than a generated unique
...                 code - confirmed absent from OV_CONTRACT_AREA (2026-08-26) before this was
...                 wired in. Every run must complete TC05 (delete) so the code is free for the
...                 next run.
...                 EACH test case does its own real Login/Logout - matches Area/Bank/Berth's own
...                 convention.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_area_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    contract_area


*** Variables ***
${TEST_CODE}        AUTOTEST_CONTRACT_AREA
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Contract Area Screen With Navigator Values Populated
    Verify Contract Area Record Does Not Exist
    Logout From EC Application

TC02 Insert Contract Area Data
    Login To EC Application
    Open Contract Area Screen With Navigator Values Populated
    Insert Contract Area Record And Save
    Verify Contract Area Record Exists
    Logout From EC Application

TC03 Update Contract Area Data
    Login To EC Application
    Open Contract Area Screen With Navigator Values Populated
    Update Contract Area Record And Save
    Verify Contract Area Record Updated
    Logout From EC Application

TC04 Find Contract Area Data
    Login To EC Application
    Open Contract Area Screen With Navigator Values Populated
    Find Contract Area Record
    Verify Contract Area Record Found
    Logout From EC Application

TC05 Delete Contract Area Data
    Login To EC Application
    Open Contract Area Screen With Navigator Values Populated
    Delete Contract Area Record And Save
    Verify Contract Area Record Removed
    Logout From EC Application
