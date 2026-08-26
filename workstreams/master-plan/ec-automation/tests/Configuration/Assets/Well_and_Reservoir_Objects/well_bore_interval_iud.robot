*** Settings ***
Documentation       EC IUD Test - Well Bore Interval (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM, PER-FIELD navigator groups (G:1 Production Unit / G:2 Area / G:3
...                 Facility Class 1 / G:4 'Well & Well Hookup' = a REAL well P1 W008 OP / G:6 =
...                 the WELL BORE P1 W008 WB001; G:5 skipped - present but zero usable options
...                 under this scope) + GO, filled via this screen's own BESPOKE T3
...                 "Apply Well Bore Interval Navigator" keyword (the shared T2 "Apply Navigator
...                 From Properties" only covers a single-row/increasing-column cascade, which
...                 this per-field-groups shape is not). Mandatory 'Well Bore' POPUP with list
...                 grid Objects:form:T_data (screen-local picker; reuses the navigator's own G:6
...                 value - FIELD-REUSE RULE). DELETE = End Date = Start Date (true delete in
...                 OV_WELL_BORE_INTERVAL).
...                 Layered: this test -> well_bore_interval_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-27) on top of the 2026-07-31 base build (verify_screen PASS, RF 4/4 +
...                 Playwright 8/8) - Well Bore Interval remains OV-GM and still needs its
...                 genuine per-field navigator + mandatory popup gesture; this is a structural
...                 conversion, not a reclassification.
...                 Uses a FIXED test code (AUTOTEST_WBI) rather than a generated unique code -
...                 confirmed absent from OV_WELL_BORE_INTERVAL (2026-08-27, fresh oracledb
...                 query) before this was wired in. Every run must complete TC05 (delete) so the
...                 code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Well/Well Hookup's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    well-bore-interval


*** Variables ***
${TEST_CODE}        AUTOTEST_WBI
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Well Bore Interval Screen With Navigator Values Populated
    Verify Well Bore Interval Record Does Not Exist
    Logout From EC Application

TC02 Insert Well Bore Interval Data
    Login To EC Application
    Open Well Bore Interval Screen With Navigator Values Populated
    Insert Well Bore Interval Record And Save
    Verify Well Bore Interval Record Exists
    Logout From EC Application

TC03 Update Well Bore Interval Data
    Login To EC Application
    Open Well Bore Interval Screen With Navigator Values Populated
    Update Well Bore Interval Record And Save
    Verify Well Bore Interval Record Updated
    Logout From EC Application

TC04 Find Well Bore Interval Data
    Login To EC Application
    Open Well Bore Interval Screen With Navigator Values Populated
    Find Well Bore Interval Record
    Verify Well Bore Interval Record Found
    Logout From EC Application

TC05 Delete Well Bore Interval Data
    Login To EC Application
    Open Well Bore Interval Screen With Navigator Values Populated
    Delete Well Bore Interval Record And Save
    Verify Well Bore Interval Record Removed
    Logout From EC Application
