*** Settings ***
Documentation       EC IUD Test - Sales Order (Configuration > Assets > Financial Objects >
...                 Sales Order). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_PRODUCT_SALES_ORDER).
...                 Layered: this test -> sales_order_page (T3) -> manage_object (T2) + common
...                 (T1). NEVER touch existing data. Uses a FIXED test code (AUTOTEST_SO) rather
...                 than a generated unique code - confirmed absent from OV_PRODUCT_SALES_ORDER
...                 before this was wired in. Every run must complete TC05 (delete) so the code
...                 is free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches. Converted from the older
...                 hardcoded-field-id pattern to the label-driven, properties-file-driven "Bank
...                 pattern" (Batch 5, 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/sales_order_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    sales-order


*** Variables ***
${TEST_CODE}        AUTOTEST_SO
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Sales Order Screen
    Verify Sales Order Record Does Not Exist
    Logout From EC Application

TC02 Insert Sales Order Data
    Login To EC Application
    Open Sales Order Screen
    Insert Sales Order Record And Save
    Verify Sales Order Record Exists
    Logout From EC Application

TC03 Update Sales Order Data
    Login To EC Application
    Open Sales Order Screen
    Update Sales Order Record And Save
    Verify Sales Order Record Updated
    Logout From EC Application

TC04 Find Sales Order Data
    Login To EC Application
    Open Sales Order Screen
    Find Sales Order Record
    Verify Sales Order Record Found
    Logout From EC Application

TC05 Delete Sales Order Data
    Login To EC Application
    Open Sales Order Screen
    Delete Sales Order Record And Save
    Verify Sales Order Record Removed
    Logout From EC Application
