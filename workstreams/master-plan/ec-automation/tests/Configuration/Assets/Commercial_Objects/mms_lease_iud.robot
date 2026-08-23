*** Settings ***
Documentation       EC IUD Test - MMS Lease (Configuration > Assets > Commercial Objects > MMS Lease).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_MMS_LEASE).
...                 Layered: this test -> mms_lease_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_MMS_LEASE,
...                 matching Bank/State/Country/Object List's convention) rather than a generated
...                 unique code - confirmed absent from OV_MMS_LEASE before this was wired in
...                 (2026-08-23). Every run must complete TC05 (delete) so the code is free
...                 for the next run - EC never lets a DELETED code be reused, but this
...                 fixed code only stays reusable if each run actually cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/State/Country/Object List's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    mms-lease


*** Variables ***
${TEST_CODE}        AUTOTEST_MMS_LEASE
${OBJ_NAME}         AUTOTEST MMS Lease
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/mms_lease_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST MMS Lease UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open MMS Lease Screen
    Verify MMS Lease Record Does Not Exist
    Logout From EC Application

TC02 Insert MMS Lease Data
    Login To EC Application
    Open MMS Lease Screen
    Insert MMS Lease Record And Save
    Verify MMS Lease Record Exists
    Logout From EC Application

TC03 Update MMS Lease Data
    Login To EC Application
    Open MMS Lease Screen
    Update MMS Lease Record And Save
    Verify MMS Lease Record Updated
    Logout From EC Application

TC04 Find MMS Lease Data
    Login To EC Application
    Open MMS Lease Screen
    Find MMS Lease Record
    Verify MMS Lease Record Found
    Logout From EC Application

TC05 Delete MMS Lease Data
    Login To EC Application
    Open MMS Lease Screen
    Delete MMS Lease Record And Save
    Verify MMS Lease Record Removed
    Logout From EC Application
