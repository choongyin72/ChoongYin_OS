*** Settings ***
Documentation       EC IUD Test - UOP Key (Configuration > Assets > Revenue_Lists > UOP Key, CD.0099).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 OV_FIN_UOP_DEPR_KEY). Layered: this test -> uop_key_page (T3) -> manage_object
...                 (T2) + common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (UOP_AUTOTEST) rather than a generated unique code - confirmed absent from
...                 OV_FIN_UOP_DEPR_KEY before this was wired in. Every run must complete TC05
...                 (delete) so the code is free for the next run.
...                 Converted (2026-08-25) from the prior 2026-07-26 generator-scaffolded build to
...                 full Bank-pattern shape: EACH test case does its own real Login/Logout on ONE
...                 browser opened once in Suite Setup (matches Bank's convention) - not 5
...                 separate browser launches. PURE SCREEN verification only - zero inline
...                 DB-verify keyword calls in this file (the prior build's TC02/TC03/TC04 called
...                 `Code/Field Should ... In View` directly here, which is the exact deviation
...                 already fixed on County/DOA Credit Limit/Document Template/Document Sequence/
...                 Calculation Context/Royalty Depositor/Stream Item Category via Issue #504).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Lists/uop_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    uop_key


*** Variables ***
${TEST_CODE}        UOP_AUTOTEST
${OBJ_NAME}        Autotest UOP Key
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
${OBJ_NAME_UPD}      Autotest UOP Key UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open UOP Key Screen
    Verify UOP Key Record Does Not Exist
    Logout From EC Application

TC02 Insert UOP Key Data
    Login To EC Application
    Open UOP Key Screen
    Insert UOP Key Record And Save
    Verify UOP Key Record Exists
    Logout From EC Application

TC03 Update UOP Key Data
    Login To EC Application
    Open UOP Key Screen
    Update UOP Key Record And Save
    Verify UOP Key Record Updated
    Logout From EC Application

TC04 Find UOP Key Data
    Login To EC Application
    Open UOP Key Screen
    Find UOP Key Record
    Verify UOP Key Record Found
    Logout From EC Application

TC05 Delete UOP Key Data
    Login To EC Application
    Open UOP Key Screen
    Delete UOP Key Record And Save
    Verify UOP Key Record Removed
    Logout From EC Application
