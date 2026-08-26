*** Settings ***
Documentation       EC IUD Test - Chemical Stream Hookup (Configuration > Assets > Chemical_Objects,
...                 CO.0260). OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory 3-level cascade navigator (Production Unit -> Area -> Facility Class 1)
...                 + GO. DELETE = End Date = Start Date (true delete in OV_CHEM_STRM_HOOKUP). NEVER
...                 touch existing data.
...                 Layered: this test -> chemical_stream_hookup_page (T3) -> manage_object (T2) +
...                 common (T1). Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (2026-08-26) - Chemical Stream Hookup remains OV-GM and still needs its
...                 genuine 3-level cascade navigator gesture; this is a structural conversion, not a
...                 reclassification as plain Bank-shaped. Also KEEPS the mandatory_field_gate
...                 pre-flight check the pre-conversion automation already had (owner instruction).
...                 Uses a FIXED test code (AUTOTEST_CSH, owner-pattern per Area) rather than a
...                 generated unique code - confirmed absent from OV_CHEM_STRM_HOOKUP (2026-08-26)
...                 before this was wired in. Every run must complete TC05 (delete) so the code is
...                 free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    chemical_stream_hookup


*** Variables ***
${TEST_CODE}        AUTOTEST_CSH
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Chemical Stream Hookup Screen With Navigator Values Populated
    Verify Chemical Stream Hookup Record Does Not Exist
    Logout From EC Application

TC02 Insert Chemical Stream Hookup Data
    Login To EC Application
    Open Chemical Stream Hookup Screen With Navigator Values Populated
    Insert Chemical Stream Hookup Record And Save
    Verify Chemical Stream Hookup Record Exists
    Logout From EC Application

TC03 Update Chemical Stream Hookup Data
    Login To EC Application
    Open Chemical Stream Hookup Screen With Navigator Values Populated
    Update Chemical Stream Hookup Record And Save
    Verify Chemical Stream Hookup Record Updated
    Logout From EC Application

TC04 Find Chemical Stream Hookup Data
    Login To EC Application
    Open Chemical Stream Hookup Screen With Navigator Values Populated
    Find Chemical Stream Hookup Record
    Verify Chemical Stream Hookup Record Found
    Logout From EC Application

TC05 Delete Chemical Stream Hookup Data
    Login To EC Application
    Open Chemical Stream Hookup Screen With Navigator Values Populated
    Delete Chemical Stream Hookup Record And Save
    Verify Chemical Stream Hookup Record Removed
    Logout From EC Application
