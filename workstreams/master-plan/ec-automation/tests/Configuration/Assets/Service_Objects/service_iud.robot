*** Settings ***
Documentation       EC IUD Test - Service (Configuration > Assets > Service_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Business Unit navigator + GO. DELETE = End Date = Start Date
...                 (true delete in OV_SERVICE). NEVER touch existing data.
...                 Layered: this test -> service_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Service remains OV-GM and still needs its genuine Business
...                 Unit navigator gesture; this is a structural conversion, not a
...                 reclassification of Service as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_SERVICE) rather than a generated unique
...                 code - confirmed absent from OV_SERVICE (2026-08-26) before this was wired
...                 in. Every run must complete TC05 (delete) so the code is free for the next
...                 run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Service_Objects/service_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    service


*** Variables ***
${TEST_CODE}        AUTOTEST_SERVICE
${START_DATE}       2011-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Service Screen With Navigator Values Populated
    Verify Service Record Does Not Exist
    Logout From EC Application

TC02 Insert Service Data
    Login To EC Application
    Open Service Screen With Navigator Values Populated
    Insert Service Record And Save
    Verify Service Record Exists
    Logout From EC Application

TC03 Update Service Data
    Login To EC Application
    Open Service Screen With Navigator Values Populated
    Update Service Record And Save
    Verify Service Record Updated
    Logout From EC Application

TC04 Find Service Data
    Login To EC Application
    Open Service Screen With Navigator Values Populated
    Find Service Record
    Verify Service Record Found
    Logout From EC Application

TC05 Delete Service Data
    Login To EC Application
    Open Service Screen With Navigator Values Populated
    Delete Service Record And Save
    Verify Service Record Removed
    Logout From EC Application
