*** Settings ***
Documentation       EC IUD Test - Operator Lease (Configuration > Assets > Commercial Objects >
...                 Operator Lease). Manage-Object (OV) screen. DELETE = End Date = Start Date
...                 (true delete in OV_OPERATOR_LEASE). Layered: this test -> operator_lease_page
...                 (T3) -> manage_object (T2) + common (T1). NEVER touch existing data. Uses a
...                 FIXED test code (AUTOTEST_OPERATOR_LEASE, matching Bank/State/Country/Object
...                 List's convention) rather than a generated unique code - confirmed absent
...                 from OV_OPERATOR_LEASE before this was wired in (2026-08-23). Every run must
...                 complete TC05 (delete) so the code is free for the next run - EC never lets a
...                 DELETED code be reused, but this fixed code only stays reusable if each run
...                 actually cleans up after itself. EACH test case does its own real
...                 Login/Logout on ONE browser opened once in Suite Setup, matching
...                 Bank/State/Country/Object List's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    operator_lease


*** Variables ***
${TEST_CODE}        AUTOTEST_OPERATOR_LEASE
${OBJ_NAME}         AUTOTEST Operator Lease
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/operator_lease_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Operator Lease UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Operator Lease Screen
    Verify Operator Lease Record Does Not Exist
    Logout From EC Application

TC02 Insert Operator Lease Data
    Login To EC Application
    Open Operator Lease Screen
    Insert Operator Lease Record And Save
    Verify Operator Lease Record Exists
    Logout From EC Application

TC03 Update Operator Lease Data
    Login To EC Application
    Open Operator Lease Screen
    Update Operator Lease Record And Save
    Verify Operator Lease Record Updated
    Logout From EC Application

TC04 Find Operator Lease Data
    Login To EC Application
    Open Operator Lease Screen
    Find Operator Lease Record
    Verify Operator Lease Record Found
    Logout From EC Application

TC05 Delete Operator Lease Data
    Login To EC Application
    Open Operator Lease Screen
    Delete Operator Lease Record And Save
    Verify Operator Lease Record Removed
    Logout From EC Application
