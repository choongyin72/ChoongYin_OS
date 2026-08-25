*** Settings ***
Documentation       EC IUD Test - Other Split Key (Configuration > Assets > Revenue Split Keys
...                 > Other Split Key, BF_CODE CD.0046, class SPLIT_KEY). Custom-URL OV screen
...                 (grid id nav:form:T_data, NO gating navigator/GO - confirmed live 2026-08-25:
...                 7 existing rows render immediately on open, before any GO/navButton click).
...                 DELETE = End Date = Start Date (true delete in OV_SPLIT_KEY). Layered: this
...                 test -> other_split_key_page (T3) -> manage_object (T2) + common (T1). NEVER
...                 touch existing data. Uses a FIXED test code (AUTOTEST_SPLITKEY_OTHER) rather
...                 than a generated unique code - confirmed absent from OV_SPLIT_KEY before this
...                 was wired in (2026-08-25, tmp/scripts/_check_split_key_other2.py). Every run
...                 must complete TC05 (delete) so the code is free for the next run. EACH test
...                 case does its own real Login/Logout on ONE browser opened once in Suite
...                 Setup, matching Bank/Product Split Key's convention
...                 (docs/rf-suite-styles.md).
...
...                 One of 6 sibling "* Split Key" screens sharing the SAME base view
...                 (OV_SPLIT_KEY), distinguished server-side by SPLIT_TYPE (this one:
...                 SPLIT_ITEM_OTHER). Each sibling uses its own distinctly-scoped fixed test
...                 code (AUTOTEST_SPLITKEY_OTHER here) so the 6 parallel builds cannot collide
...                 on the shared view - do NOT rename this to a generic AUTOTEST_SPLIT_KEY.
...
...                 NOT to be confused with the already-automated "Split Item Other" (CD.0017,
...                 split_item_other_iud.robot, same folder) - that is a DIFFERENT BF_CODE/
...                 class/URL controller (manage_object_nav, not manage_object_split_key)
...                 despite living in the same treeview area. Also NOT "Other Split Key Shares"
...                 (CD.0047, a related but genuinely different percentage-share screen, not
...                 built this round).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/other_split_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    other-split-key


*** Variables ***
${TEST_CODE}        AUTOTEST_SPLITKEY_OTHER
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/other_split_key_insert.properties - TC02 verifies against it.
${OBJ_NAME}         AUTOTEST Other Split Key
# Must stay in sync with testdata/other_split_key_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Other Split Key UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Other Split Key Screen
    Verify Other Split Key Record Does Not Exist
    Logout From EC Application

TC02 Insert Other Split Key Data
    Login To EC Application
    Open Other Split Key Screen
    Insert Other Split Key Record And Save
    Verify Other Split Key Record Exists
    Logout From EC Application

TC03 Update Other Split Key Data
    Login To EC Application
    Open Other Split Key Screen
    Update Other Split Key Record And Save
    Verify Other Split Key Record Updated
    Logout From EC Application

TC04 Find Other Split Key Data
    Login To EC Application
    Open Other Split Key Screen
    Find Other Split Key Record
    Verify Other Split Key Record Found
    Logout From EC Application

TC05 Delete Other Split Key Data
    Login To EC Application
    Open Other Split Key Screen
    Delete Other Split Key Record And Save
    Verify Other Split Key Record Removed
    Logout From EC Application
