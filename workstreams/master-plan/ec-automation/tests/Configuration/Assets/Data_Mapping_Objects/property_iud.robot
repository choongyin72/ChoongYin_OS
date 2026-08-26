*** Settings ***
Documentation       EC IUD Test - Property (Configuration > Assets > Data_Mapping_Objects,
...                 SP.0059). OV-GM (groupmodel manage-object) screen: the grid is filtered by
...                 the mandatory single Business Unit navigator + GO (own G:1 group, not
...                 G:0/C:1 - see property_page.resource). DELETE = End Date = Start Date (true
...                 delete in OV_PROPERTY). NEVER touch existing data.
...                 Layered: this test -> property_page (T3) -> manage_object (T2) + common
...                 (T1).
...                 Converted to the Area-pattern full STRUCTURE (2026-08-26) - Property
...                 remains OV-GM and still needs its genuine Business Unit navigator gesture;
...                 this is a structural conversion, not a reclassification as plain
...                 Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_PROPERTY) rather than a generated unique
...                 code - confirmed absent from OV_PROPERTY (2026-08-26) before this was wired
...                 in. Every run must complete TC05 (delete) so the code is free for the next
...                 run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Price Object's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    property


*** Variables ***
${TEST_CODE}        AUTOTEST_PROPERTY
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Property Screen With Navigator Values Populated
    Verify Property Record Does Not Exist
    Logout From EC Application

TC02 Insert Property Data
    Login To EC Application
    Open Property Screen With Navigator Values Populated
    Insert Property Record And Save
    Verify Property Record Exists
    Logout From EC Application

TC03 Update Property Data
    Login To EC Application
    Open Property Screen With Navigator Values Populated
    Update Property Record And Save
    Verify Property Record Updated
    Logout From EC Application

TC04 Find Property Data
    Login To EC Application
    Open Property Screen With Navigator Values Populated
    Find Property Record
    Verify Property Record Found
    Logout From EC Application

TC05 Delete Property Data
    Login To EC Application
    Open Property Screen With Navigator Values Populated
    Delete Property Record And Save
    Verify Property Record Removed
    Logout From EC Application
