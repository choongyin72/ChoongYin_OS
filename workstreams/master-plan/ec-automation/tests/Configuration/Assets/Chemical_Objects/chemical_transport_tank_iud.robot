*** Settings ***
Documentation       EC IUD Test - Chemical Transport Tank (Configuration > Assets > Chemical_Objects
...                 > Chemical Transport Tank, CO.0257). Manage-Object (OV) screen. DELETE = End
...                 Date = Start Date (true delete in OV_CHEM_TRANS_TANK).
...                 Layered: this test -> chemical_transport_tank_page (T3) -> manage_object (T2)
...                 + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_CTT, confirmed
...                 absent from OV_CHEM_TRANS_TANK before this was wired in, 2026-08-23), matching
...                 Bank/Berth's convention, rather than a generated unique code. Every run must
...                 complete TC05 (delete) so the code is free for the next run - EC never lets a
...                 DELETED code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_transport_tank_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    chemical_transport_tank


*** Variables ***
${TEST_CODE}        AUTOTEST_CTT
${OBJ_NAME}         AUTOTEST Chemical Transport Tank
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/chemical_transport_tank_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Chemical Transport Tank UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Chemical Transport Tank Screen
    Verify Chemical Transport Tank Record Does Not Exist
    Logout From EC Application

TC02 Insert Chemical Transport Tank Data
    Login To EC Application
    Open Chemical Transport Tank Screen
    Insert Chemical Transport Tank Record And Save
    Verify Chemical Transport Tank Record Exists
    Logout From EC Application

TC03 Update Chemical Transport Tank Data
    Login To EC Application
    Open Chemical Transport Tank Screen
    Update Chemical Transport Tank Record And Save
    Verify Chemical Transport Tank Record Updated
    Logout From EC Application

TC04 Find Chemical Transport Tank Data
    Login To EC Application
    Open Chemical Transport Tank Screen
    Find Chemical Transport Tank Record
    Verify Chemical Transport Tank Record Found
    Logout From EC Application

TC05 Delete Chemical Transport Tank Data
    Login To EC Application
    Open Chemical Transport Tank Screen
    Delete Chemical Transport Tank Record And Save
    Verify Chemical Transport Tank Record Removed
    Logout From EC Application
