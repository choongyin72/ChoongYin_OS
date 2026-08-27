*** Settings ***
Documentation       EC IUD Test - Lifting Account (Configuration > Assets > Transport_Objects).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by a mandatory
...                 navigator (ONE group, cascade spanning 2 rows) + GO. DELETE = End Date = Start
...                 Date (true delete in OV_LIFTING_ACCOUNT). NEVER touch existing data.
...                 Layered: this test -> lifting_account_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-27), upgrading the pre-existing hand-built driver (py/
...                 lifting_account_iud.py, commit 6e88e371) to properties-file-driven +
...                 shared-keyword navigator fill, reusing its exact proven nav scope/insert data.
...                 Uses a FIXED test code (AUTOTEST_LA_001, same as the pre-existing driver) -
...                 confirmed absent from OV_LIFTING_ACCOUNT (2026-08-27, fresh oracledb check)
...                 before this was wired in. Every run must complete TC05 (delete) so the code
...                 is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/lifting_account_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    lifting_account


*** Variables ***
${TEST_CODE}        AUTOTEST_LA_001
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Lifting Account Screen With Navigator Values Populated
    Verify Lifting Account Record Does Not Exist
    Logout From EC Application

TC02 Insert Lifting Account Data
    Login To EC Application
    Open Lifting Account Screen With Navigator Values Populated
    Insert Lifting Account Record And Save
    Verify Lifting Account Record Exists
    Logout From EC Application

TC03 Update Lifting Account Data
    Login To EC Application
    Open Lifting Account Screen With Navigator Values Populated
    Update Lifting Account Record And Save
    Verify Lifting Account Record Updated
    Logout From EC Application

TC04 Find Lifting Account Data
    Login To EC Application
    Open Lifting Account Screen With Navigator Values Populated
    Find Lifting Account Record
    Verify Lifting Account Record Found
    Logout From EC Application

TC05 Delete Lifting Account Data
    Login To EC Application
    Open Lifting Account Screen With Navigator Values Populated
    Delete Lifting Account Record And Save
    Verify Lifting Account Record Removed
    Logout From EC Application
