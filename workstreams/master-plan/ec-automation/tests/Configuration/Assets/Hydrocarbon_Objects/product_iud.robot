*** Settings ***
Documentation       EC IUD Test - Product (Configuration > Assets > Hydrocarbon Objects >
...                 Product, screen CO.0007, class PRODUCT). Manage-Object (OV) screen.
...                 DELETE = End Date = Start Date (true delete in ov_product). Layered: this
...                 test -> product_page (T3) -> manage_object (T2) + common (T1). NEVER touch
...                 existing data. Uses a FIXED test code (AUTOTEST_PRODUCT) rather than a
...                 generated unique code - confirmed absent from PRODUCT (base table,
...                 OBJECT_CODE column) before this was wired in. Every run must complete TC05
...                 (delete) so the code is free for the next run - EC never lets a DELETED code
...                 be reused, but this fixed code only stays reusable if each run actually
...                 cleans up after itself.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches. TC03/TC04/TC05 still depend on
...                 TC02's inserted record existing.
...                 NOT to be confused with the already-automated siblings "Product Description"
...                 (CD.0012, product_description_iud.robot) or "Product Group" (RC.0053,
...                 product_group_iud.robot) - this is PRODUCT_MAINTAIN, a different class.

Resource            ../../../../pageobjects/Configuration/Assets/Hydrocarbon_Objects/product_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    product


*** Variables ***
${TEST_CODE}        AUTOTEST_PRODUCT
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These values must stay in sync with testdata/product_insert.properties - TC02 DB-verifies
# them against what that file actually set, not an independent assumption.
${OBJ_NAME}         Autotest Product
${OBJ_DESC}         Autotest product description
${OBJ_SORT_ORDER}   10
# These values must stay in sync with testdata/product_update.properties - TC03 DB-verifies
# them against what that file actually set, not an independent assumption.
${OBJ_NAME_UPD}     Autotest Product UPDATED
${OBJ_DESC_UPD}     Autotest product description UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Product Screen
    Verify Product Record Does Not Exist
    Logout From EC Application

TC02 Insert Product Data
    Login To EC Application
    Open Product Screen
    Insert Product Record And Save
    Verify Product Record Exists
    Logout From EC Application

TC03 Update Product Data
    Login To EC Application
    Open Product Screen
    Update Product Record And Save
    Verify Product Record Updated
    Logout From EC Application

TC04 Find Product Data
    Login To EC Application
    Open Product Screen
    Find Product Record
    Verify Product Record Found
    Logout From EC Application

TC05 Delete Product Data
    Login To EC Application
    Open Product Screen
    Delete Product Record And Save
    Verify Product Record Removed
    Logout From EC Application
