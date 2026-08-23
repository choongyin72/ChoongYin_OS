*** Settings ***
Documentation       EC IUD Test - Unit Agreement (Configuration > Assets > Royalty Objects > Unit Agreement).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_unit_agr).
...                 Layered: this test -> unit_agreement_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_UA, confirmed absent
...                 from ov_unit_agr before this was wired in). Every run must complete TC05 (delete)
...                 so the code is free for the next run - EC never lets a DELETED code be reused, but
...                 this fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in Suite
...                 Setup - not 5 separate browser launches (matches bank_iud.robot convention).
...                 Converted 2026-08-23 (Batch 5) from the older hardcoded-field-id pattern to the
...                 newer label-driven, properties-file-driven, T2-consolidated Bank pattern.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    unit_agreement


*** Variables ***
${TEST_CODE}        AUTOTEST_UA
${OBJ_NAME}        AUTOTEST Unit Agreement
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These 2 values must stay in sync with testdata/unit_agreement_insert.properties - TC02
# form-verifies them against what that file actually set, not an independent assumption.
${OBJ_COMMENTS}     AUTOTEST Comments
# These 2 values must stay in sync with testdata/unit_agreement_update.properties - TC03
# form-verifies them against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}      AUTOTEST Unit Agreement UPDATED
${OBJ_COMMENTS_UPD}    AUTOTEST Comments UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Unit Agreement Screen
    Verify Unit Agreement Record Does Not Exist
    Logout From EC Application

TC02 Insert Unit Agreement Data
    Login To EC Application
    Open Unit Agreement Screen
    Insert Unit Agreement Record And Save
    Verify Unit Agreement Record Exists
    Logout From EC Application

TC03 Update Unit Agreement Data
    Login To EC Application
    Open Unit Agreement Screen
    Update Unit Agreement Record And Save
    Verify Unit Agreement Record Updated
    Logout From EC Application

TC04 Find Unit Agreement Data
    Login To EC Application
    Open Unit Agreement Screen
    Find Unit Agreement Record
    Verify Unit Agreement Record Found
    Logout From EC Application

TC05 Delete Unit Agreement Data
    Login To EC Application
    Open Unit Agreement Screen
    Delete Unit Agreement Record And Save
    Verify Unit Agreement Record Removed
    Logout From EC Application
