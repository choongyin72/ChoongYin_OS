*** Settings ***
Documentation       EC IUD Test - Meter (Configuration > Assets > Dispatching Objects, OV_METER).
...                 OV-GM (BU-gated) with a mandatory Delivery Point Name POPUP (the GENERIC T1
...                 "Pick From EC Object Popup", resources/popup.resource - preserved unchanged
...                 by this conversion; see meter_page.resource Documentation). The grid is
...                 filtered by the mandatory Business Unit navigator + GO. DELETE = End Date =
...                 Start Date (true delete in OV_METER). NEVER touch existing data.
...                 Layered: this test -> meter_page (T3) -> manage_object (T2) + common (T1).
...                 Converted to the full Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Meter remains
...                 OV-GM and still needs its genuine Business Unit navigator gesture and its
...                 genuine mandatory Delivery Point Name popup; this is a structural
...                 conversion, not a reclassification of the screen or a change to the popup
...                 mechanism. Meter's navigator was re-confirmed live 2026-08-26 as a
...                 single-dropdown shape identical to Area's own - this corrects an EARLIER
...                 WRONG "DOES NOT FIT" classification that had conflated the insert form's
...                 orthogonal Delivery Point popup with the navigator itself.
...                 Uses a FIXED test code (AUTOTEST_METER) rather than a generated/timestamped
...                 code - confirmed absent from OV_METER (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete)
...                 so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Chemical Stream/Tank's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    meter


*** Variables ***
${TEST_CODE}        AUTOTEST_METER
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Meter Screen With Navigator Values Populated
    Verify Meter Record Does Not Exist
    Logout From EC Application

TC02 Insert Meter Data
    Login To EC Application
    Open Meter Screen With Navigator Values Populated
    Insert Meter Record And Save
    Verify Meter Record Exists
    Logout From EC Application

TC03 Update Meter Data
    Login To EC Application
    Open Meter Screen With Navigator Values Populated
    Update Meter Record And Save
    Verify Meter Record Updated
    Logout From EC Application

TC04 Find Meter Data
    Login To EC Application
    Open Meter Screen With Navigator Values Populated
    Find Meter Record
    Verify Meter Record Found
    Logout From EC Application

TC05 Delete Meter Data
    Login To EC Application
    Open Meter Screen With Navigator Values Populated
    Delete Meter Record And Save
    Verify Meter Record Removed
    Logout From EC Application
