*** Settings ***
Documentation       EC IUD Test - Well Bore (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM, PER-FIELD nav groups nav:form:G:1..G:4:R:1:C:0 (Production Unit / Area /
...                 Facility Class 1 / 'Well & Well Hookup') with SPECIFIC values (G:4 = a REAL
...                 well, P1 W008 OP - NOT the first-available 'P1 Graph 001'). G:5 ('Well') is
...                 scan-flagged mandatory but offers ZERO options under every scope tried -
...                 deliberately skipped; GO still succeeds and the grid loads on 4 levels. Because
...                 this navigator shape is PER-FIELD groups (not the shared T2 "Apply Navigator
...                 From Properties" same-row cascade), it is filled by well_bore_page.resource's
...                 own BESPOKE "Apply Well Bore Navigator From Properties" keyword - resources/
...                 manage_object.resource was NOT touched by this conversion.
...                 Mandatory objectForm field: 'Well' POPUP with list grid Objects:form:T_data
...                 (screen-local picker; picks the nav-scope well, not the popup's first row which
...                 is a graph object). DELETE = End Date = Start Date (true delete in
...                 OV_WELL_BORE). NEVER touch existing data.
...                 Layered: this test -> well_bore_page (T3) -> manage_object (T2) + navigator
...                 (T1) + common (T1).
...                 Converted to the full Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Well Bore remains
...                 OV-GM and still needs its genuine 4-level PER-FIELD navigator + GO and its
...                 genuine mandatory Well popup; this is a structural conversion, not a change to
...                 either mechanism.
...                 Uses a FIXED test code (AUTOTEST_WB) rather than a generated/timestamped code -
...                 confirmed absent from OV_WELL_BORE (2026-08-27, fresh oracledb connection)
...                 before this was wired in. Every run must complete TC05 (delete) so the code is
...                 free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Chemical Stream/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    well-bore


*** Variables ***
${TEST_CODE}        AUTOTEST_WB
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Well Bore Screen With Navigator Values Populated
    Verify Well Bore Record Does Not Exist
    Logout From EC Application

TC02 Insert Well Bore Data
    Login To EC Application
    Open Well Bore Screen With Navigator Values Populated
    Insert Well Bore Record And Save
    Verify Well Bore Record Exists
    Logout From EC Application

TC03 Update Well Bore Data
    Login To EC Application
    Open Well Bore Screen With Navigator Values Populated
    Update Well Bore Record And Save
    Verify Well Bore Record Updated
    Logout From EC Application

TC04 Find Well Bore Data
    Login To EC Application
    Open Well Bore Screen With Navigator Values Populated
    Find Well Bore Record
    Verify Well Bore Record Found
    Logout From EC Application

TC05 Delete Well Bore Data
    Login To EC Application
    Open Well Bore Screen With Navigator Values Populated
    Delete Well Bore Record And Save
    Verify Well Bore Record Removed
    Logout From EC Application
