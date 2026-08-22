*** Settings ***
Documentation       EC IUD Test - Cost Centre (Configuration > Assets > Financial Objects > Cost Centre).
...                 Custom-URL OV screen (grid id nav:form:T_data, NO navigator GO button -
...                 confirmed live 2026-08-22). DELETE = End Date = Start Date (true delete
...                 in OV_FIN_COST_CENTER). Layered: this test -> cost_centre_page (T3) ->
...                 manage_object (T2) + common (T1). NEVER touch existing data. Uses a FIXED
...                 test code (AUTOTEST_COST_CENTRE, matching Bank/State's convention) rather
...                 than a generated unique code - confirmed absent from OV_FIN_COST_CENTER
...                 before this was wired in (2026-08-22). Every run must complete TC05
...                 (delete) so the code is free for the next run - EC never lets a DELETED
...                 code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself. EACH test case does its own real
...                 Login/Logout on ONE browser opened once in Suite Setup, matching
...                 Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/cost_centre_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    cost-centre


*** Variables ***
${TEST_CODE}        AUTOTEST_COST_CENTRE
${OBJ_NAME}         AUTOTEST Cost Centre
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/cost_centre_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Cost Centre UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Cost Centre Screen
    Verify Cost Centre Record Does Not Exist
    Logout From EC Application

TC02 Insert Cost Centre Data
    Login To EC Application
    Open Cost Centre Screen
    Insert Cost Centre Record And Save
    Verify Cost Centre Record Exists
    Logout From EC Application

TC03 Update Cost Centre Data
    Login To EC Application
    Open Cost Centre Screen
    Update Cost Centre Record And Save
    Verify Cost Centre Record Updated
    Logout From EC Application

TC04 Find Cost Centre Data
    Login To EC Application
    Open Cost Centre Screen
    Find Cost Centre Record
    Verify Cost Centre Record Found
    Logout From EC Application

TC05 Delete Cost Centre Data
    Login To EC Application
    Open Cost Centre Screen
    Delete Cost Centre Record And Save
    Verify Cost Centre Record Removed
    Logout From EC Application
