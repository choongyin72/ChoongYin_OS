*** Settings ***
Documentation       EC IUD Test - Product Price Object (Configuration > Assets > Sales Objects >
...                 Product Price Object, BF_CODE CD.0011, class PRICE_OBJECT). Custom-URL OV
...                 screen (grid id nav:form:T_data, NO navigator - confirmed live 2026-08-25).
...                 DELETE = End Date = Start Date (true delete in OV_PRICE_OBJECT). Layered:
...                 this test -> product_price_object_page (T3) -> manage_object (T2) + common
...                 (T1). NEVER touch existing data. Uses a FIXED test code
...                 (AUTOTEST_PPO) rather than a generated unique code - confirmed absent from
...                 OV_PRICE_OBJECT before this was wired in (2026-08-25, tmp/check_product_price_object.py).
...                 Every run must complete TC05 (delete) so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Cost Centre's convention (docs/rf-suite-styles.md).
...
...                 NOT to be confused with the already-automated "Price Object" (CO.3016,
...                 price_object_iud.robot) - that is a DIFFERENT BF_CODE/menu entry/URL
...                 (OV-GM, manage_object_navmodel_nav, mandatory Business Unit nav gate)
...                 despite sharing the same underlying class/view (PRICE_OBJECT/OV_PRICE_OBJECT).
...                 This suite's own AUTOTEST_PPO test code is independent of CO.3016's own
...                 AUTOTEST_ code, so the two suites cannot collide.

Resource            ../../../../pageobjects/Configuration/Assets/Sales_Objects/product_price_object_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    product-price-object


*** Variables ***
${TEST_CODE}        AUTOTEST_PPO
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/product_price_object_insert.properties - TC02 verifies against it.
${OBJ_NAME}         AUTOTEST Product Price Object
# Must stay in sync with testdata/product_price_object_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Product Price Object UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Product Price Object Screen
    Verify Product Price Object Record Does Not Exist
    Logout From EC Application

TC02 Insert Product Price Object Data
    Login To EC Application
    Open Product Price Object Screen
    Insert Product Price Object Record And Save
    Verify Product Price Object Record Exists
    Logout From EC Application

TC03 Update Product Price Object Data
    Login To EC Application
    Open Product Price Object Screen
    Update Product Price Object Record And Save
    Verify Product Price Object Record Updated
    Logout From EC Application

TC04 Find Product Price Object Data
    Login To EC Application
    Open Product Price Object Screen
    Find Product Price Object Record
    Verify Product Price Object Record Found
    Logout From EC Application

TC05 Delete Product Price Object Data
    Login To EC Application
    Open Product Price Object Screen
    Delete Product Price Object Record And Save
    Verify Product Price Object Record Removed
    Logout From EC Application
