*** Settings ***
Documentation       EC IUD Test - Transport Zone (Configuration > Assets > Dispatching Objects >
...                 Transport Zone). OV-GM (groupmodel manage-object) screen: the grid is filtered
...                 by the mandatory Business Unit navigator + GO. DELETE = End Date = Start Date
...                 (true delete in OV_TRANSPORT_ZONE). NEVER touch existing data.
...                 Layered: this test -> transport_zone_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Transport Zone remains OV-GM and still needs its genuine
...                 Business Unit navigator gesture; this is a structural conversion, not a
...                 reclassification of Transport Zone as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_TRANSPORT_ZONE) rather than a generated
...                 unique code - confirmed absent from OV_TRANSPORT_ZONE (2026-08-26, fresh
...                 independent oracledb connection) before this was wired in. Every run must
...                 complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    transport_zone


*** Variables ***
${TEST_CODE}        AUTOTEST_TRANSPORT_ZONE
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Transport Zone Screen With Navigator Values Populated
    Verify Transport Zone Record Does Not Exist
    Logout From EC Application

TC02 Insert Transport Zone Data
    Login To EC Application
    Open Transport Zone Screen With Navigator Values Populated
    Insert Transport Zone Record And Save
    Verify Transport Zone Record Exists
    Logout From EC Application

TC03 Update Transport Zone Data
    Login To EC Application
    Open Transport Zone Screen With Navigator Values Populated
    Update Transport Zone Record And Save
    Verify Transport Zone Record Updated
    Logout From EC Application

TC04 Find Transport Zone Data
    Login To EC Application
    Open Transport Zone Screen With Navigator Values Populated
    Find Transport Zone Record
    Verify Transport Zone Record Found
    Logout From EC Application

TC05 Delete Transport Zone Data
    Login To EC Application
    Open Transport Zone Screen With Navigator Values Populated
    Delete Transport Zone Record And Save
    Verify Transport Zone Record Removed
    Logout From EC Application
