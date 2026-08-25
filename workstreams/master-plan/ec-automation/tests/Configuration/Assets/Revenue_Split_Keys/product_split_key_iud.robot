*** Settings ***
Documentation       EC IUD Test - Product Split Key (Configuration > Assets > Revenue Split
...                 Keys > Product Split Key, BF_CODE CD.0036, class SPLIT_KEY). Custom-URL OV
...                 screen (grid id nav:form:T_data, NO navigator/GO gate - confirmed live
...                 2026-08-25). DELETE = End Date = Start Date (true delete in OV_SPLIT_KEY).
...                 Layered: this test -> product_split_key_page (T3) -> manage_object (T2) +
...                 common (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_SPLITKEY_PRODUCT) rather than a generated unique code - confirmed
...                 absent from OV_SPLIT_KEY before this was wired in (2026-08-25,
...                 tmp/check_split_key_product.py). Every run must complete TC05 (delete) so
...                 the code is free for the next run. EACH test case does its own real
...                 Login/Logout on ONE browser opened once in Suite Setup, matching
...                 Bank/Product Price Object's convention (docs/rf-suite-styles.md).
...
...                 One of 6 sibling "* Split Key" screens sharing the SAME base view
...                 (OV_SPLIT_KEY), distinguished server-side by SPLIT_TYPE (this one:
...                 PRODUCT). Each sibling uses its own distinctly-scoped fixed test code
...                 (AUTOTEST_SPLITKEY_PRODUCT here) so the 6 parallel builds cannot collide on
...                 the shared view - do NOT rename this to a generic AUTOTEST_SPLIT_KEY.
...
...                 NOT to be confused with the already-automated "Split Item Other" (CD.0017,
...                 split_item_other_iud.robot, same folder) - that is a DIFFERENT BF_CODE/
...                 class/URL controller (manage_object_nav, not manage_object_split_key)
...                 despite living in the same treeview area.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/product_split_key_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    product-split-key


*** Variables ***
${TEST_CODE}        AUTOTEST_SPLITKEY_PRODUCT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/product_split_key_insert.properties - TC02 verifies against it.
${OBJ_NAME}         AUTOTEST Product Split Key
# Must stay in sync with testdata/product_split_key_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Product Split Key UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Product Split Key Screen
    Verify Product Split Key Record Does Not Exist
    Logout From EC Application

TC02 Insert Product Split Key Data
    Login To EC Application
    Open Product Split Key Screen
    Insert Product Split Key Record And Save
    Verify Product Split Key Record Exists
    Logout From EC Application

TC03 Update Product Split Key Data
    Login To EC Application
    Open Product Split Key Screen
    Update Product Split Key Record And Save
    Verify Product Split Key Record Updated
    Logout From EC Application

TC04 Find Product Split Key Data
    Login To EC Application
    Open Product Split Key Screen
    Find Product Split Key Record
    Verify Product Split Key Record Found
    Logout From EC Application

TC05 Delete Product Split Key Data
    Login To EC Application
    Open Product Split Key Screen
    Delete Product Split Key Record And Save
    Verify Product Split Key Record Removed
    Logout From EC Application
