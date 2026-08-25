*** Settings ***
Documentation       EC IUD Test - Company Split Key (Configuration > Assets > Revenue Split
...                 Keys > Company Split Key, CD.0044). Custom-URL OV - no mandatory
...                 navigator field (confirmed live 2026-08-25: nav fields=[]) - grid
...                 nav:form:T_data renders directly on open. DELETE = End Date = Start Date
...                 (true delete in OV_SPLIT_KEY).
...                 One of 6 sibling "* Split Key" screens sharing the SAME OV_SPLIT_KEY view
...                 (discriminated server-side by SPLIT_TYPE='COMPANY' for this screen) - the
...                 other 5 (Product/Field/Stream Item Category/Other/Stream Item Split Key)
...                 are built independently in parallel; each uses its own distinctly-scoped
...                 fixed test code to avoid cross-screen collision.
...                 Layered: this test -> company_split_key_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_SPLITKEY_COMPANY - deliberately Company-scoped in its own name,
...                 NOT a generic AUTOTEST_SPLIT_KEY, to avoid collision with the 5 sibling
...                 builds happening in parallel on the same shared view), confirmed absent
...                 from OV_SPLIT_KEY before this was wired in (2026-08-25, fresh connection:
...                 0 rows for CODE='AUTOTEST_SPLITKEY_COMPANY', 0 AUTOTEST% rows of any kind
...                 in OV_SPLIT_KEY at all). Every run must complete TC05 (delete) so the code
...                 is free for the next run - EC never lets a DELETED code be reused, but
...                 this fixed code only stays reusable if each run actually cleans up after
...                 itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once
...                 in Suite Setup, matching Bank/WBS/Report Context's convention
...                 (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/company_split_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    company_split_key


*** Variables ***
${TEST_CODE}        AUTOTEST_SPLITKEY_COMPANY
${OBJ_NAME}         AUTOTEST SPLITKEY COMPANY
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/company_split_key_update.properties - TC03 DB-verifies against it.
${OBJ_NAME_UPD}     AUTOTEST SPLITKEY COMPANY UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Company Split Key Screen
    Verify Company Split Key Record Does Not Exist
    Logout From EC Application

TC02 Insert Company Split Key Data
    Login To EC Application
    Open Company Split Key Screen
    Insert Company Split Key Record And Save
    Verify Company Split Key Record Exists
    Logout From EC Application

TC03 Update Company Split Key Data
    Login To EC Application
    Open Company Split Key Screen
    Update Company Split Key Record And Save
    Verify Company Split Key Record Updated
    Logout From EC Application

TC04 Find Company Split Key Data
    Login To EC Application
    Open Company Split Key Screen
    Find Company Split Key Record
    Verify Company Split Key Record Found
    Logout From EC Application

TC05 Delete Company Split Key Data
    Login To EC Application
    Open Company Split Key Screen
    Delete Company Split Key Record And Save
    Verify Company Split Key Record Removed
    Logout From EC Application
