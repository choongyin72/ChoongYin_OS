*** Settings ***
Documentation       EC IUD Test - Chemical Stream (Configuration > Assets > Chemical_Objects).
...                 OV-GM with a mandatory From Connection POPUP (stream_node_ref_popup: inner
...                 Object Type CHEM_TANK + inner GO + grid manage_object_nav_nav:form:T_data -
...                 screen-local picker, PRESERVED UNCHANGED by this conversion). The grid is
...                 filtered by the mandatory 3-level Production Unit -> Area -> Facility Class 1
...                 navigator cascade + GO. DELETE = End Date = Start Date (true delete in
...                 OV_CHEM_STREAM). NEVER touch existing data.
...                 Layered: this test -> chemical_stream_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the full Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Chemical Stream
...                 remains OV-GM and still needs its genuine 3-level navigator cascade + GO and
...                 its genuine mandatory From Connection popup; this is a structural conversion,
...                 not a reclassification of the screen or a change to the popup mechanism.
...                 Uses a FIXED test code (AUTOTEST_CHS) rather than a generated/timestamped
...                 code - confirmed absent from OV_CHEM_STREAM (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    chemical-stream


*** Variables ***
${TEST_CODE}        AUTOTEST_CHS
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Chemical Stream Screen With Navigator Values Populated
    Verify Chemical Stream Record Does Not Exist
    Logout From EC Application

TC02 Insert Chemical Stream Data
    Login To EC Application
    Open Chemical Stream Screen With Navigator Values Populated
    Insert Chemical Stream Record And Save
    Verify Chemical Stream Record Exists
    Logout From EC Application

TC03 Update Chemical Stream Data
    Login To EC Application
    Open Chemical Stream Screen With Navigator Values Populated
    Update Chemical Stream Record And Save
    Verify Chemical Stream Record Updated
    Logout From EC Application

TC04 Find Chemical Stream Data
    Login To EC Application
    Open Chemical Stream Screen With Navigator Values Populated
    Find Chemical Stream Record
    Verify Chemical Stream Record Found
    Logout From EC Application

TC05 Delete Chemical Stream Data
    Login To EC Application
    Open Chemical Stream Screen With Navigator Values Populated
    Delete Chemical Stream Record And Save
    Verify Chemical Stream Record Removed
    Logout From EC Application
