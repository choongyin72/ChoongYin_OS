*** Settings ***
Documentation       EC IUD Test - Chemical Tank (Configuration > Assets > Chemical Objects >
...                 Chemical Tank, CO.0070). OV-GM (groupmodel manage-object) screen: the grid is
...                 filtered by the mandatory 3-level Production Unit -> Area -> Facility Class 1
...                 navigator cascade + GO. DELETE = End Date = Start Date (true delete in
...                 OV_CHEM_TANK). NEVER touch existing data.
...                 Layered: this test -> chemical_tank_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Chemical Tank remains OV-GM
...                 and still needs its genuine 3-level Production Unit -> Area -> Facility Class
...                 1 navigator cascade + GO; this is a structural conversion, not a
...                 reclassification of the screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_CT) rather than a generated/timestamped
...                 code - confirmed absent from OV_CHEM_TANK (2026-08-26, fresh oracledb
...                 connection) before this was wired in. Every run must complete TC05 (delete) so
...                 the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_tank_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    chemical_tank


*** Variables ***
${TEST_CODE}        AUTOTEST_CT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Chemical Tank Screen With Navigator Values Populated
    Verify Chemical Tank Record Does Not Exist
    Logout From EC Application

TC02 Insert Chemical Tank Data
    Login To EC Application
    Open Chemical Tank Screen With Navigator Values Populated
    Insert Chemical Tank Record And Save
    Verify Chemical Tank Record Exists
    Logout From EC Application

TC03 Update Chemical Tank Data
    Login To EC Application
    Open Chemical Tank Screen With Navigator Values Populated
    Update Chemical Tank Record And Save
    Verify Chemical Tank Record Updated
    Logout From EC Application

TC04 Find Chemical Tank Data
    Login To EC Application
    Open Chemical Tank Screen With Navigator Values Populated
    Find Chemical Tank Record
    Verify Chemical Tank Record Found
    Logout From EC Application

TC05 Delete Chemical Tank Data
    Login To EC Application
    Open Chemical Tank Screen With Navigator Values Populated
    Delete Chemical Tank Record And Save
    Verify Chemical Tank Record Removed
    Logout From EC Application
