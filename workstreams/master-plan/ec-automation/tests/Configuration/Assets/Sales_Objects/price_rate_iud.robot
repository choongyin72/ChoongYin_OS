*** Settings ***
Documentation       EC IUD Test - Price Rate (Configuration > Assets > Sales_Objects > CO.3024).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Business Unit navigator + GO. DELETE = End Date = Start Date
...                 (true delete in OV_PRICE_RATE). NEVER touch existing data.
...                 Layered: this test -> price_rate_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Price Rate remains OV-GM and still needs its genuine Business
...                 Unit navigator gesture; this is a structural conversion, not a
...                 reclassification of Price Rate as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_PRICE_RATE) rather than a generated unique
...                 code - confirmed absent from OV_PRICE_RATE (2026-08-26) before this was wired
...                 in. Every run must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    price_rate


*** Variables ***
${TEST_CODE}        AUTOTEST_PRICE_RATE
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Price Rate Screen With Navigator Values Populated
    Verify Price Rate Record Does Not Exist
    Logout From EC Application

TC02 Insert Price Rate Data
    Login To EC Application
    Open Price Rate Screen With Navigator Values Populated
    Insert Price Rate Record And Save
    Verify Price Rate Record Exists
    Logout From EC Application

TC03 Update Price Rate Data
    Login To EC Application
    Open Price Rate Screen With Navigator Values Populated
    Update Price Rate Record And Save
    Verify Price Rate Record Updated
    Logout From EC Application

TC04 Find Price Rate Data
    Login To EC Application
    Open Price Rate Screen With Navigator Values Populated
    Find Price Rate Record
    Verify Price Rate Record Found
    Logout From EC Application

TC05 Delete Price Rate Data
    Login To EC Application
    Open Price Rate Screen With Navigator Values Populated
    Delete Price Rate Record And Save
    Verify Price Rate Record Removed
    Logout From EC Application
