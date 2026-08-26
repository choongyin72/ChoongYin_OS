*** Settings ***
Documentation       EC IUD Test - Price Object (Configuration > Assets > Sales_Objects, CO.3016).
...                 OV-GM (groupmodel manage-object) screen: the grid is filtered by the
...                 mandatory single Business Unit navigator + GO. DELETE = End Date = Start
...                 Date (true delete in OV_PRICE_OBJECT). NEVER touch existing data.
...                 Layered: this test -> price_object_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 Converted to the Area-pattern full STRUCTURE (2026-08-26) - Price Object
...                 remains OV-GM and still needs its genuine Business Unit navigator gesture;
...                 this is a structural conversion, not a reclassification as plain
...                 Bank-shaped.
...                 Uses a FIXED test code (AUTOTEST_PRICE_OBJECT) rather than a generated
...                 unique code - confirmed absent from OV_PRICE_OBJECT (2026-08-26) before
...                 this was wired in. Every run must complete TC05 (delete) so the code is
...                 free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup - matches Area/Bank/Berth's own convention.
...
...                 NOT the same screen as "Product Price Object" (CD.0011, PR #502) - that
...                 is a distinct custom-URL screen with no navigator, untouched by this file.

Resource            ../../../../pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    price_object


*** Variables ***
${TEST_CODE}        AUTOTEST_PRICE_OBJECT
${START_DATE}       2020-01-01
${END_DATE}         ${START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Price Object Screen With Navigator Values Populated
    Verify Price Object Record Does Not Exist
    Logout From EC Application

TC02 Insert Price Object Data
    Login To EC Application
    Open Price Object Screen With Navigator Values Populated
    Insert Price Object Record And Save
    Verify Price Object Record Exists
    Logout From EC Application

TC03 Update Price Object Data
    Login To EC Application
    Open Price Object Screen With Navigator Values Populated
    Update Price Object Record And Save
    Verify Price Object Record Updated
    Logout From EC Application

TC04 Find Price Object Data
    Login To EC Application
    Open Price Object Screen With Navigator Values Populated
    Find Price Object Record
    Verify Price Object Record Found
    Logout From EC Application

TC05 Delete Price Object Data
    Login To EC Application
    Open Price Object Screen With Navigator Values Populated
    Delete Price Object Record And Save
    Verify Price Object Record Removed
    Logout From EC Application
