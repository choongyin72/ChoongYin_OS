*** Settings ***
Documentation       T3 (screen) — Chemical Product page object.
...                 Screen: Configuration > Assets > Chemical Objects > Chemical Product
...                 (CO.0072). Manage-Object (OV) screen, versioned. Holds Chemical Product's
...                 locators + thin IUD wrappers that delegate to T2 (manage_object) and T1
...                 (common). Built from scratch 2026-08-24 (Phase 3) via
...                 ec-bank-pattern-new-screen — no prior RF/Playwright automation existed for
...                 this screen.
...
...                 DELETE WORKAROUND (documented EC PRODUCT DEFECT, not an automation gap):
...                 ec-ui-knowledge/EC_KNOWN_ISSUES.md "OV_CHEM_PRODUCT (Chemical Product,
...                 CO.0072) — End=Start delete blocked by a child-FK dependency" — CHEM_PRODUCT
...                 auto-creates a 1:1 CHEM_USAGE_REPORT_CONF child row on insert; that child's
...                 NO-ACTION FK blocks the standard zero-length-window (End Date = Start Date)
...                 close, and the web UI swallows the resulting ORA-02292/ORA-20102 so Save
...                 looks like it succeeded while OBJECT_END_DATE stays NULL. There is NO UI
...                 screen for CHEM_USAGE_REPORT_CONF. Delete Chemical Product Record And Save
...                 below applies that same doc's prescribed fix — remove the child row at DB
...                 level FIRST (via the screen-scoped libraries/ChemicalProductCleanup.py, NOT
...                 a shared T1/T2 file) — so the normal UI End=Start Save that follows actually
...                 persists.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Library             ../../../../libraries/ChemicalProductCleanup.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CHEMICAL_PRODUCT_SCREEN}    Chemical Product
${CHEM_PRODUCT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_product_insert.properties
${CHEM_PRODUCT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_product_update.properties
${CHEM_PRODUCT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_product_form_verify.properties
${CHEM_PRODUCT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_product_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal — confirmed
# live via scan_ec_screen.py (2026-08-24): manage_object_nav_nav:form:T_data, same manage-object
# family as Bank/Berth/Chemical Transport Tank.
${CHEM_PRODUCT_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Same framework-invariant id already
# confirmed live on Bank/State/Berth/Chemical Transport Tank's objectdates tab, confirmed again
# live for Chemical Product by scan_ec_screen.py (2026-08-24).
${CHEM_PRODUCT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Chemical Product's own form-field label set. Labels are "Chemical Product Code"/"Chemical
# Product Name" (screen-prefixed) - confirmed live via scan_ec_screen.py (2026-08-24), NOT the
# generic "Code"/"Name" Bank/Object List use. Meas. Units included (the one mandatory dropdown,
# filled at Insert and still present/readable in updateAttributes). Start Date deliberately
# excluded - Insert-only, not present in updateAttributes (same as Bank/Berth/Chemical
# Transport Tank). Defined ONCE here so both Verify Chemical Product Record Exists (TC02) and
# Verify Chemical Product Record Found (TC04) share the same list.
@{CHEM_PRODUCT_FORM_LABELS}    Chemical Product Code    Chemical Product Name    Meas. Units


*** Keywords ***
Find Chemical Product Row By Filter
    [Documentation]    Explicitly filter the Chemical Product grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Berth/Chemical Transport Tank's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CHEM_PRODUCT_TABLE}    ${code}

Clear Chemical Product Row Filter
    [Documentation]    Clear the Code column filter (see Find Chemical Product Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CHEM_PRODUCT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Chemical Product's OWN credentials
    ...    (${CHEMICAL_PRODUCT_EC_USER}/${CHEMICAL_PRODUCT_EC_PASS} from credentials.py) on the
    ...    current page. Every EC screen gets its own dedicated credential pair (standing
    ...    decision, 2026-08-22). Zero-argument wrapper so chemical_product_iud.robot's test
    ...    cases read as a plain business step; supplies Chemical Product's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the actual
    ...    login mechanics.
    Login To EC Screen    ${CHEMICAL_PRODUCT_EC_USER}    ${CHEMICAL_PRODUCT_EC_PASS}

Open Chemical Product Screen
    [Documentation]    Navigate to the Chemical Product screen and load the list (GO). Assumes
    ...    the caller already logged in this test case (via Login To EC Application).
    [Arguments]    ${user}=${CHEMICAL_PRODUCT_EC_USER}    ${pass}=${CHEMICAL_PRODUCT_EC_PASS}
    Open EC Screen    ${CHEMICAL_PRODUCT_SCREEN}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Insert Chemical Product Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so chemical_product_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth/Chemical Transport Tank.
    [Arguments]    ${properties_path}=${CHEM_PRODUCT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Chemical Product Code
    RETURN    ${code}

Verify Chemical Product Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here, matching Bank/Berth's TC02 convention): row exists in the grid, then
    ...    the form shows what was just inserted (Chemical Product Code/Chemical Product Name/
    ...    Meas. Units). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find Chemical
    ...    Product Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Product Row By Filter    ${code}
    Verify Object Insert Exists    ${CHEM_PRODUCT_TABLE}    ${code}    Chemical Product
    ...    ${CHEM_PRODUCT_INSERT_PROPERTIES}    @{CHEM_PRODUCT_FORM_LABELS}
    ...    code_label=Chemical Product Code
    Clear Chemical Product Row Filter

Update Chemical Product Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked. Filters via Find Chemical Product
    ...    Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CHEM_PRODUCT_UPDATE_PROPERTIES}
    Find Chemical Product Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CHEM_PRODUCT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Chemical Product Code
    Clear Chemical Product Row Filter
    RETURN    ${data}

Verify Chemical Product Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification: the
    ...    form shows the updated Chemical Product Name. Delegates the full sequence (select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Form Record. Filters via Find
    ...    Chemical Product Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Product Row By Filter    ${code}
    Verify Object Form Record    ${CHEM_PRODUCT_TABLE}    ${code}    Chemical Product
    ...    ${CHEM_PRODUCT_UPDATE_PROPERTIES}    Chemical Product Name    code_label=Chemical Product Code
    Clear Chemical Product Row Filter

Find Chemical Product Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Chemical Product Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Chemical Product Record Found (called
    ...    right after, same TC) needs the grid still filtered to ${code}; it clears the filter
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Product Row By Filter    ${code}
    Find Object Record    ${CHEM_PRODUCT_TABLE}    ${code}    Chemical Product
    ...    code_label=Chemical Product Code

Verify Chemical Product Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the form record match the expected (post-update) data. Delegates the full sequence
    ...    (grid-compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller
    ...    must already have selected the row (TC04 does, via Find Chemical Product Record before
    ...    this) AND left the Code filter active from that same call - clears the filter itself
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CHEM_PRODUCT_TABLE}    ${code}    ${CHEM_PRODUCT_GRID_VERIFY_PROPERTIES}
    ...    ${CHEM_PRODUCT_FORM_VERIFY_PROPERTIES}    @{CHEM_PRODUCT_FORM_LABELS}
    Clear Chemical Product Row Filter

Delete Chemical Product Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    FIRST removes the auto-created CHEM_USAGE_REPORT_CONF child row via
    ...    Remove Chem Usage Report Conf Child (libraries/ChemicalProductCleanup.py) - the
    ...    documented fix for this screen's known EC product defect (see this file's
    ...    Documentation header) - THEN selects the chemical product, sets End Date = Start Date
    ...    (true delete), Save. Without that pre-step the UI Save silently no-ops (OBJECT_END_DATE
    ...    stays NULL) because of the NO-ACTION child FK. Captures the TC05 evidence screenshot
    ...    right after the End Date is filled but BEFORE Save is clicked. Filters via Find
    ...    Chemical Product Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Remove Chem Usage Report Conf Child    ${code}
    Find Chemical Product Row By Filter    ${code}
    Delete Object Via End Date    ${CHEM_PRODUCT_TABLE}    ${CHEM_PRODUCT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Chemical Product Row Filter

Verify Chemical Product Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CHEM_PRODUCT_TABLE}    OV_CHEM_PRODUCT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Chemical Product Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CHEM_PRODUCT_TABLE}    ${code}
