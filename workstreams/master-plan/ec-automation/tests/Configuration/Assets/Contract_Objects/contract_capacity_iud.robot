*** Settings ***
Documentation       EC IUD Test — Contract Capacity (Configuration > Assets > Contract Objects,
...                 CO.2044). OV-GM (groupmodel manage-object): the grid is filtered by the
...                 mandatory Business Unit navigator + GO. DELETE = End Date = Start Date (true
...                 delete in OV_CONTRACT_CAPACITY). NEVER touch existing data.
...                 Layered: this test -> contract_capacity_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify/
...                 properties-driven STRUCTURE (this conversion, 2026-08-26) — Contract Capacity
...                 remains OV-GM and still needs its genuine Business Unit navigator gesture;
...                 this is a structural conversion, not a reclassification as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_CONTRACT_CAPACITY, confirmed absent from
...                 OV_CONTRACT_CAPACITY before this was wired in) rather than a generated unique
...                 code. Every run must complete TC05 (delete) so the code is free for the next
...                 run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup — matches Area/Bank/Berth's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    contract_capacity


*** Variables ***
${TEST_CODE}        AUTOTEST_CONTRACT_CAPACITY
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Contract Capacity Screen With Navigator Values Populated
    Verify Contract Capacity Record Does Not Exist
    Logout From EC Application

TC02 Insert Contract Capacity Data
    Login To EC Application
    Open Contract Capacity Screen With Navigator Values Populated
    Insert Contract Capacity Record And Save
    Verify Contract Capacity Record Exists
    Logout From EC Application

TC03 Update Contract Capacity Data
    Login To EC Application
    Open Contract Capacity Screen With Navigator Values Populated
    Update Contract Capacity Record And Save
    Verify Contract Capacity Record Updated
    Logout From EC Application

TC04 Find Contract Capacity Data
    Login To EC Application
    Open Contract Capacity Screen With Navigator Values Populated
    Find Contract Capacity Record
    Verify Contract Capacity Record Found
    Logout From EC Application

TC05 Delete Contract Capacity Data
    Login To EC Application
    Open Contract Capacity Screen With Navigator Values Populated
    Delete Contract Capacity Record And Save
    Verify Contract Capacity Record Removed
    Logout From EC Application
