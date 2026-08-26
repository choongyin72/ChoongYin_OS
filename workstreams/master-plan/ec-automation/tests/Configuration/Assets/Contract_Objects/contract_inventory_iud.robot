*** Settings ***
Documentation       EC IUD Test - Contract Inventory (Configuration > Assets > Contract_Objects,
...                 CO.2054). OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 navigator (Business Unit -> Contract Area, same-row increasing column) + GO.
...                 DELETE = End Date = Start Date (true delete in OV_CONTRACT_INVENTORY). NEVER
...                 touch existing data.
...                 Layered: this test -> contract_inventory_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Contract Inventory remains
...                 OV-GM and still needs its genuine navigator + GO; this is a structural
...                 conversion, not a reclassification of the screen as plain Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_CONTRACT_INVENTORY) rather than a generated/
...                 timestamped code - confirmed absent from OV_CONTRACT_INVENTORY (2026-08-26,
...                 fresh oracledb connection) before this was wired in. Every run must complete
...                 TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - matches Area/Facility Class 1's own convention.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    contract_inventory


*** Variables ***
${TEST_CODE}        AUTOTEST_CONTRACT_INVENTORY
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Contract Inventory Screen With Navigator Values Populated
    Verify Contract Inventory Record Does Not Exist
    Logout From EC Application

TC02 Insert Contract Inventory Data
    Login To EC Application
    Open Contract Inventory Screen With Navigator Values Populated
    Insert Contract Inventory Record And Save
    Verify Contract Inventory Record Exists
    Logout From EC Application

TC03 Update Contract Inventory Data
    Login To EC Application
    Open Contract Inventory Screen With Navigator Values Populated
    Update Contract Inventory Record And Save
    Verify Contract Inventory Record Updated
    Logout From EC Application

TC04 Find Contract Inventory Data
    Login To EC Application
    Open Contract Inventory Screen With Navigator Values Populated
    Find Contract Inventory Record
    Verify Contract Inventory Record Found
    Logout From EC Application

TC05 Delete Contract Inventory Data
    Login To EC Application
    Open Contract Inventory Screen With Navigator Values Populated
    Delete Contract Inventory Record And Save
    Verify Contract Inventory Record Removed
    Logout From EC Application
