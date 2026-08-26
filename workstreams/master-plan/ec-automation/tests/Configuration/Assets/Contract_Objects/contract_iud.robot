*** Settings ***
Documentation       EC IUD Test - Contract (Configuration > Assets > Contract_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Business Unit navigator + GO. DELETE = End Date = Start Date
...                 (true delete in OV_CONTRACT). NEVER touch existing data.
...                 Layered: this test -> contract_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Contract remains OV-GM and still needs its genuine Business
...                 Unit navigator gesture; this is a structural conversion, not a
...                 reclassification of Contract as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_CONTRACT) rather than a generated unique
...                 code - confirmed absent from OV_CONTRACT (2026-08-26) before this was wired
...                 in. Every run must complete TC05 (delete) so the code is free for the next
...                 run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    contract


*** Variables ***
${TEST_CODE}        AUTOTEST_CONTRACT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Contract Screen With Navigator Values Populated
    Verify Contract Record Does Not Exist
    Logout From EC Application

TC02 Insert Contract Data
    Login To EC Application
    Open Contract Screen With Navigator Values Populated
    Insert Contract Record And Save
    Verify Contract Record Exists
    Logout From EC Application

TC03 Update Contract Data
    Login To EC Application
    Open Contract Screen With Navigator Values Populated
    Update Contract Record And Save
    Verify Contract Record Updated
    Logout From EC Application

TC04 Find Contract Data
    Login To EC Application
    Open Contract Screen With Navigator Values Populated
    Find Contract Record
    Verify Contract Record Found
    Logout From EC Application

TC05 Delete Contract Data
    Login To EC Application
    Open Contract Screen With Navigator Values Populated
    Delete Contract Record And Save
    Verify Contract Record Removed
    Logout From EC Application
