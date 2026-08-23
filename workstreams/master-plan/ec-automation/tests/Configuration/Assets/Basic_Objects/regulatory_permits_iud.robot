*** Settings ***
Documentation       EC IUD Test - Regulatory Permits (Configuration > Assets > Basic Objects >
...                 Regulatory Permits). Custom-URL OV screen (confirmed live 2026-08-23: grid
...                 nav:form:T_data, WITH a GO button unlike Account/Cost Centre - Save And
...                 Refresh List auto-detects either shape). DELETE = End Date = Start Date (true
...                 delete in OV_REGULATORY_PERMITS). Layered: this test -> regulatory_permits_page
...                 (T3) -> manage_object (T2) + common (T1). NEVER touch existing data. Uses a
...                 FIXED test code (AUTOTEST_REGULATORY_PERMITS, matching Bank/Account's
...                 convention) rather than a generated unique code - confirmed absent from
...                 OV_REGULATORY_PERMITS before this was wired in (2026-08-23; the view itself
...                 was 0 rows on this sandbox). Every run must complete TC05 (delete) so the code
...                 is free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Account's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/regulatory_permits_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    regulatory-permits


*** Variables ***
${TEST_CODE}        AUTOTEST_REGULATORY_PERMITS
${OBJ_NAME}         AUTOTEST Regulatory Permits
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/regulatory_permits_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Regulatory Permits UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Regulatory Permits Screen
    Verify Regulatory Permits Record Does Not Exist
    Logout From EC Application

TC02 Insert Regulatory Permits Data
    Login To EC Application
    Open Regulatory Permits Screen
    Insert Regulatory Permits Record And Save
    Verify Regulatory Permits Record Exists
    Logout From EC Application

TC03 Update Regulatory Permits Data
    Login To EC Application
    Open Regulatory Permits Screen
    Update Regulatory Permits Record And Save
    Verify Regulatory Permits Record Updated
    Logout From EC Application

TC04 Find Regulatory Permits Data
    Login To EC Application
    Open Regulatory Permits Screen
    Find Regulatory Permits Record
    Verify Regulatory Permits Record Found
    Logout From EC Application

TC05 Delete Regulatory Permits Data
    Login To EC Application
    Open Regulatory Permits Screen
    Delete Regulatory Permits Record And Save
    Verify Regulatory Permits Record Removed
    Logout From EC Application
