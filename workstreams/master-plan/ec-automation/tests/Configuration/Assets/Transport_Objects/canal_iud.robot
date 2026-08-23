*** Settings ***
Documentation       EC IUD Test - Canal (Configuration > Assets > Transport Objects > Canal, CO.2069).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CANAL).
...                 Layered: this test -> canal_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (CANAL_KIEL, Batch 7
...                 2026-08-23) rather than a generated unique code - confirmed absent from
...                 OV_CANAL before this was wired in (only real rows are SUEZ/PANAMA). Every run
...                 must complete TC05 (delete) so the code is free for the next run - EC never
...                 lets a DELETED code be reused, but this fixed code only stays reusable if each
...                 run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches (matches Bank's own shape).

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/canal_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    canal


*** Variables ***
${TEST_CODE}        CANAL_KIEL
${OBJ_NAME}         Kiel Canal
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# This value must stay in sync with testdata/canal_insert.properties - TC02 DB-verifies it
# against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}     Kiel Canal UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Canal Screen
    Verify Canal Record Does Not Exist
    Logout From EC Application

TC02 Insert Canal Data
    Login To EC Application
    Open Canal Screen
    Insert Canal Record And Save
    Verify Canal Record Exists
    Logout From EC Application

TC03 Update Canal Data
    Login To EC Application
    Open Canal Screen
    Update Canal Record And Save
    Verify Canal Record Updated
    Logout From EC Application

TC04 Find Canal Data
    Login To EC Application
    Open Canal Screen
    Find Canal Record
    Verify Canal Record Found
    Logout From EC Application

TC05 Delete Canal Data
    Login To EC Application
    Open Canal Screen
    Delete Canal Record And Save
    Verify Canal Record Removed
    Logout From EC Application
