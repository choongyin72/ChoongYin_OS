*** Settings ***
Documentation       EC IUD Test - Chemical Product (Configuration > Assets > Chemical Objects >
...                 Chemical Product, CO.0072). Manage-Object (OV) screen, versioned. DELETE =
...                 End Date = Start Date (true delete in OV_CHEM_PRODUCT), with a documented EC
...                 product defect workaround - see chemical_product_page.resource's
...                 Documentation header (a NO-ACTION child FK on the auto-created
...                 CHEM_USAGE_REPORT_CONF row blocks the standard UI delete unless that child
...                 row is removed first, per ec-ui-knowledge/EC_KNOWN_ISSUES.md).
...                 Layered: this test -> chemical_product_page (T3) -> manage_object (T2) +
...                 common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_CHEMPROD,
...                 confirmed absent from CHEM_PRODUCT before this was wired in, 2026-08-24),
...                 matching Bank/Berth/Chemical Transport Tank's convention, rather than a
...                 generated unique code. Every run must complete TC05 (delete) so the code is
...                 free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup, matching Bank/Berth's convention (docs/rf-suite-styles.md).

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_product_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown       Ensure Logged Out From EC Application

Test Tags           iud    chemical_product


*** Variables ***
${TEST_CODE}        AUTOTEST_CHEMPROD
${OBJ_NAME}         AUTOTEST Chemical Product
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# Must stay in sync with testdata/chemical_product_update.properties - TC03 verifies against it.
${OBJ_NAME_UPD}     AUTOTEST Chemical Product UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Chemical Product Screen
    Verify Chemical Product Record Does Not Exist
    Logout From EC Application

TC02 Insert Chemical Product Data
    Login To EC Application
    Open Chemical Product Screen
    Insert Chemical Product Record And Save
    Verify Chemical Product Record Exists
    Logout From EC Application

TC03 Update Chemical Product Data
    Login To EC Application
    Open Chemical Product Screen
    Update Chemical Product Record And Save
    Verify Chemical Product Record Updated
    Logout From EC Application

TC04 Find Chemical Product Data
    Login To EC Application
    Open Chemical Product Screen
    Find Chemical Product Record
    Verify Chemical Product Record Found
    Logout From EC Application

TC05 Delete Chemical Product Data
    Login To EC Application
    Open Chemical Product Screen
    Delete Chemical Product Record And Save
    Verify Chemical Product Record Removed
    Logout From EC Application
