*** Settings ***
Documentation       EC IUD Test - Pipeline Segment (Configuration > Assets > Dispatching Objects,
...                 OV_PIPELINE_SEGMENT). OV-GM (BU-gated) with a mandatory "Pipeline Name"
...                 dropdown on the insert form. The grid is filtered by the mandatory Business
...                 Unit navigator + GO. DELETE = End Date = Start Date (true delete in
...                 OV_PIPELINE_SEGMENT). NEVER touch existing data.
...                 Layered: this test -> pipeline_segment_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the full Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Pipeline Segment
...                 remains OV-GM and still needs its genuine Business Unit navigator gesture and
...                 its genuine mandatory Pipeline Name dropdown; this is a structural conversion,
...                 not a reclassification of the screen.
...                 Uses a FIXED test code (AUTOTEST_PIPELINE_SEGMENT) rather than a generated/
...                 timestamped code - confirmed absent from OV_PIPELINE_SEGMENT (2026-08-26,
...                 fresh oracledb connection) before this was wired in. Every run must complete
...                 TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Meter/Chemical Stream/Tank's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    pipeline_segment


*** Variables ***
${TEST_CODE}        AUTOTEST_PIPELINE_SEGMENT
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Pipeline Segment Screen With Navigator Values Populated
    Verify Pipeline Segment Record Does Not Exist
    Logout From EC Application

TC02 Insert Pipeline Segment Data
    Login To EC Application
    Open Pipeline Segment Screen With Navigator Values Populated
    Insert Pipeline Segment Record And Save
    Verify Pipeline Segment Record Exists
    Logout From EC Application

TC03 Update Pipeline Segment Data
    Login To EC Application
    Open Pipeline Segment Screen With Navigator Values Populated
    Update Pipeline Segment Record And Save
    Verify Pipeline Segment Record Updated
    Logout From EC Application

TC04 Find Pipeline Segment Data
    Login To EC Application
    Open Pipeline Segment Screen With Navigator Values Populated
    Find Pipeline Segment Record
    Verify Pipeline Segment Record Found
    Logout From EC Application

TC05 Delete Pipeline Segment Data
    Login To EC Application
    Open Pipeline Segment Screen With Navigator Values Populated
    Delete Pipeline Segment Record And Save
    Verify Pipeline Segment Record Removed
    Logout From EC Application
