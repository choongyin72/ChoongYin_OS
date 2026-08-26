*** Settings ***
Documentation       EC IUD Test - Tract (Configuration > Assets > Royalty Objects > Tract).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory Unit Agreement navigator (nav:form:G:1, NOT G:0 - see tract_page.
...                 resource) + GO. DELETE = End Date = Start Date (true delete in OV_TRACT).
...                 NEVER touch existing data.
...                 Layered: this test -> tract_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the full Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE 2026-08-26, correcting this branch's own first commit (docs-only,
...                 wrongly declined the conversion). Tract remains OV-GM and still needs its
...                 genuine Unit Agreement navigator gesture; this is a structural conversion,
...                 not a reclassification of Tract as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_TRACT) rather than a generated unique code -
...                 confirmed absent from OV_TRACT (fresh oracledb connection, 2026-08-26) before
...                 this was wired in. Every run must complete TC05 (delete) so the code is free
...                 for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    tract


*** Variables ***
${TEST_CODE}        AUTOTEST_TRACT
# Unit Agreement 1-4 are all effective from 2010-01-01 (confirmed live via a fresh oracledb
# query on OV_UNIT_AGR.OBJECT_START_DATE, 2026-08-26) - Start Date must be >= that. Reusing
# 2011-01-01, the value the screen's own prior driver already proved live.
${START_DATE}       2011-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Tract Screen With Navigator Values Populated
    Verify Tract Record Does Not Exist
    Logout From EC Application

TC02 Insert Tract Data
    Login To EC Application
    Open Tract Screen With Navigator Values Populated
    Insert Tract Record And Save
    Verify Tract Record Exists
    Logout From EC Application

TC03 Update Tract Data
    Login To EC Application
    Open Tract Screen With Navigator Values Populated
    Update Tract Record And Save
    Verify Tract Record Updated
    Logout From EC Application

TC04 Find Tract Data
    Login To EC Application
    Open Tract Screen With Navigator Values Populated
    Find Tract Record
    Verify Tract Record Found
    Logout From EC Application

TC05 Delete Tract Data
    Login To EC Application
    Open Tract Screen With Navigator Values Populated
    Delete Tract Record And Save
    Verify Tract Record Removed
    Logout From EC Application
