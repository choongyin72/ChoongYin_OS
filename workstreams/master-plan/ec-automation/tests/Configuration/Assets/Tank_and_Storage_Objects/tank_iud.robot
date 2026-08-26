*** Settings ***
Documentation       EC IUD Test - Tank (Configuration > Assets > Tank and Storage Objects > Tank).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Production Unit -> Area -> Facility Class 1 navigator cascade +
...                 GO. DELETE = End Date = Start Date (true delete in OV_TANK). NEVER touch
...                 existing data.
...                 Layered: this test -> tank_page (T3) -> manage_object (T2) + common (T1).
...                 Built from scratch (2026-08-26) as a lean RF-only Area-pattern suite, per
...                 the ec-area-pattern-new-screen skill - mirrors area_iud.robot's CURRENT
...                 5-TC/per-TC-login/pure-screen-verify shape exactly.
...                 Uses a FIXED test code (AUTOTEST_TANK, confirmed absent from OV_TANK
...                 2026-08-26) rather than a generated unique code. Every run must complete
...                 TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Tank_and_Storage_Objects/tank_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    tank


*** Variables ***
${TEST_CODE}        AUTOTEST_TANK
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Tank Screen With Navigator Values Populated
    Verify Tank Record Does Not Exist
    Logout From EC Application

TC02 Insert Tank Data
    Login To EC Application
    Open Tank Screen With Navigator Values Populated
    Insert Tank Record And Save
    Verify Tank Record Exists
    Logout From EC Application

TC03 Update Tank Data
    Login To EC Application
    Open Tank Screen With Navigator Values Populated
    Update Tank Record And Save
    Verify Tank Record Updated
    Logout From EC Application

TC04 Find Tank Data
    Login To EC Application
    Open Tank Screen With Navigator Values Populated
    Find Tank Record
    Verify Tank Record Found
    Logout From EC Application

TC05 Delete Tank Data
    Login To EC Application
    Open Tank Screen With Navigator Values Populated
    Delete Tank Record And Save
    Verify Tank Record Removed
    Logout From EC Application
