*** Settings ***
Documentation       EC IUD Test - Customer (Configuration > Assets > Commercial Objects > Customer).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_customer).
...                 Layered: this test -> customer_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_CUST) rather than a
...                 generated unique code - confirmed absent from OV_CUSTOMER before this was wired in.
...                 Every run must complete TC05 (delete) so the code is free for the next run - EC
...                 never lets a DELETED code be reused, but this fixed code only stays reusable if
...                 each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in Suite
...                 Setup - not 5 separate browser launches. Converted from the old hardcoded-field-id
...                 pattern to the label-driven, properties-file-driven "Bank pattern" (Batch 3,
...                 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    customer


*** Variables ***
${TEST_CODE}        AUTOTEST_CUST
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Customer Screen
    Verify Customer Record Does Not Exist
    Logout From EC Application

TC02 Insert Customer Data
    Login To EC Application
    Open Customer Screen
    Insert Customer Record And Save
    Verify Customer Record Exists
    Logout From EC Application

TC03 Update Customer Data
    Login To EC Application
    Open Customer Screen
    Update Customer Record And Save
    Verify Customer Record Updated
    Logout From EC Application

TC04 Find Customer Data
    Login To EC Application
    Open Customer Screen
    Find Customer Record
    Verify Customer Record Found
    Logout From EC Application

TC05 Delete Customer Data
    Login To EC Application
    Open Customer Screen
    Delete Customer Record And Save
    Verify Customer Record Removed
    Logout From EC Application
