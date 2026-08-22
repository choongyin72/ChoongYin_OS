*** Settings ***
Documentation       EC IUD Test - Revenue Order (Configuration > Assets > Financial Objects > Revenue Order).
...                 Custom-URL OV screen (NO navigator, NO GO button) - grid is nav:form:T_data,
...                 reload via toolbar Refresh (T2's Save And Refresh List auto-detects this).
...                 DELETE = End Date = Start Date (true delete in OV_FIN_REVENUE_ORDER).
...                 Layered: this test -> revenue_order_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_REVENUE_ORDER,
...                 matching Bank/State's convention) rather than a generated unique code -
...                 confirmed absent from OV_FIN_REVENUE_ORDER before this was wired in
...                 (2026-08-22). Every run must complete TC05 (delete) so the code is free for
...                 the next run - EC never lets a DELETED code be reused, but this fixed code
...                 only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/revenue_order_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    revenue-order


*** Variables ***
${TEST_CODE}        AUTOTEST_REVENUE_ORDER
${OBJ_NAME}         AUTOTEST Revenue Order
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/revenue_order_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Revenue Order UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Revenue Order Screen
    Verify Revenue Order Record Does Not Exist
    Logout From EC Application

TC02 Insert Revenue Order Data
    Login To EC Application
    Open Revenue Order Screen
    Insert Revenue Order Record And Save
    Verify Revenue Order Record Exists
    Logout From EC Application

TC03 Update Revenue Order Data
    Login To EC Application
    Open Revenue Order Screen
    Update Revenue Order Record And Save
    Verify Revenue Order Record Updated
    Logout From EC Application

TC04 Find Revenue Order Data
    Login To EC Application
    Open Revenue Order Screen
    Find Revenue Order Record
    Verify Revenue Order Record Found
    Logout From EC Application

TC05 Delete Revenue Order Data
    Login To EC Application
    Open Revenue Order Screen
    Delete Revenue Order Record And Save
    Verify Revenue Order Record Removed
    Logout From EC Application
