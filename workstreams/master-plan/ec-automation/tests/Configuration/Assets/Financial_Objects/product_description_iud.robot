*** Settings ***
Documentation       EC IUD Test - Product Description (Configuration > Assets > Financial
...                 Objects > Product Description). Manage-Object (OV) screen. DELETE = End
...                 Date = Start Date (true delete in OV_PRODUCT_NODE_ITEM). Layered: this
...                 test -> product_description_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_PD) rather than
...                 a generated unique code - confirmed absent from OV_PRODUCT_NODE_ITEM before
...                 this was wired in. Every run must complete TC05 (delete) so the code is
...                 free for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches. Converted from the old
...                 hardcoded-field-id pattern to the label-driven, properties-file-driven,
...                 T2-consolidated "Bank pattern" (Batch 4, 2026-08-23).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/product_description_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    product-description


*** Variables ***
${TEST_CODE}        AUTOTEST_PD
${START_DATE}       2003-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Product Description Screen
    Verify Product Description Record Does Not Exist
    Logout From EC Application

TC02 Insert Product Description Data
    Login To EC Application
    Open Product Description Screen
    Insert Product Description Record And Save
    Verify Product Description Record Exists
    Logout From EC Application

TC03 Update Product Description Data
    Login To EC Application
    Open Product Description Screen
    Update Product Description Record And Save
    Verify Product Description Record Updated
    Logout From EC Application

TC04 Find Product Description Data
    Login To EC Application
    Open Product Description Screen
    Find Product Description Record
    Verify Product Description Record Found
    Logout From EC Application

TC05 Delete Product Description Data
    Login To EC Application
    Open Product Description Screen
    Delete Product Description Record And Save
    Verify Product Description Record Removed
    Logout From EC Application
