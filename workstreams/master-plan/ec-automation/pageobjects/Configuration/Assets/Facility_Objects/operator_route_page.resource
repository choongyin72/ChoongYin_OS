*** Settings ***
Documentation       T3 (screen) — Operator Route page object.
...                 Screen: Configuration > Assets > Facility_Objects > Operator Route.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area navigator cascade (2-level, C:1/C:2 same
...                 row - confirmed live pre-conversion via this screen's own prior bespoke
...                 "Open Operator Route Screen" keyword and py/operator_route_iud.py) is set +
...                 GO. Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Operator Route
...                 remains OV-GM, its genuine 2-level PU->Area cascade + GO is KEPT exactly as
...                 proven (Apply Navigator From Properties, EXPLICIT values from
...                 testdata/operator_route_navigator.properties: Op Production Unit=P3
...                 Production Unit, Op Area=P3 Area - the same PROVEN explicit values this
...                 screen's own pre-existing driver already used). This is a STRUCTURAL
...                 conversion, not a reclassification of the screen as plain Bank-shaped.
...                 Labels confirmed (ec-ui-knowledge/screens/operator_route.md, verify_screen
...                 PASS 2026-08-01): objectForm/updateAttributes use SCREEN-PREFIXED "Operator
...                 Route Code"/"Operator Route Name" (like Area's "Area Code"/"Area Name") -
...                 every T2 call below passes code_label=Operator Route Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${OR_SCREEN}            Operator Route
${OR_TABLE}              manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area 2-level cascade — MANDATORY before the grid
# loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/operator_route_navigator.properties.
${OR_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_route_navigator.properties
${OR_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_route_insert.properties
${OR_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_route_update.properties
${OR_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_route_form_verify.properties
${OR_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_route_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Bank's/Facility Class 1's own del-enddate constant: this row
# packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value carried over unchanged from this
# screen's own pre-conversion page object (proven live).
${OR_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Operator Route's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectdates, not updateAttributes/objectForm's fill-once trio).
@{OR_FORM_LABELS}       Operator Route Code    Operator Route Name


*** Keywords ***
Find Operator Route Row By Filter
    [Documentation]    Explicitly filter the Operator Route grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${OR_TABLE}    ${code}

Clear Operator Route Row Filter
    [Documentation]    Clear the Code column filter (see Find Operator Route Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${OR_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Operator Route's OWN credentials
    ...    (${OPERATOR_ROUTE_EC_USER}/${OPERATOR_ROUTE_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${OPERATOR_ROUTE_EC_USER}    ${OPERATOR_ROUTE_EC_PASS}

Open Operator Route Screen With Navigator Values Populated
    [Documentation]    Navigate to the Operator Route screen, THEN fill + submit the mandatory
    ...    2-level Production Unit -> Area navigator (dropdowns + GO) - the grid stays empty until
    ...    this happens, so this single keyword bundles both steps for the test case (Area's exact
    ...    skeleton calls this as ONE line per TC, not two). Assumes the caller already logged in
    ...    this test case (via Login To EC Application). Navigator fill delegates to the shared T2
    ...    "Apply Navigator From Properties" (resources/manage_object.resource), driven by
    ...    testdata/operator_route_navigator.properties.
    Open EC Screen    ${OR_SCREEN}
    Apply Navigator From Properties    ${OR_NAVIGATOR_PROPERTIES}

Insert Operator Route Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so operator_route_iud.robot's test case body reads as
    ...    a plain business step. Also owns the integrity check that the inserted Operator Route
    ...    Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${OR_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Operator Route Code
    RETURN    ${code}

Verify Operator Route Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Operator Route Code/Operator Route Name's LIVE SCREEN value is compared to
    ...    testdata/operator_route_insert.properties. Filters via Find Operator Route Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Operator Route Row By Filter    ${code}
    Verify Object Insert Exists    ${OR_TABLE}    ${code}    Operator Route
    ...    ${OR_INSERT_PROPERTIES}    @{OR_FORM_LABELS}    code_label=Operator Route Code
    Clear Operator Route Row Filter

Update Operator Route Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Operator Route Name is listed in testdata/operator_route_update.properties - Operator
    ...    Route Code is read-only in updateAttributes. Filters via Find Operator Route Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${OR_UPDATE_PROPERTIES}
    Find Operator Route Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${OR_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Operator Route Code
    Clear Operator Route Row Filter
    RETURN    ${data}

Verify Operator Route Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Operator Route Name's LIVE SCREEN value to
    ...    testdata/operator_route_update.properties. Filters via Find Operator Route Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Operator Route Row By Filter    ${code}
    Verify Object Form Record    ${OR_TABLE}    ${code}    Operator Route
    ...    ${OR_UPDATE_PROPERTIES}    Operator Route Name    code_label=Operator Route Code
    Clear Operator Route Row Filter

Find Operator Route Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Operator
    ...    Route Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Operator Route Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Operator Route Row By Filter    ${code}
    Find Object Record    ${OR_TABLE}    ${code}    Operator Route    code_label=Operator Route Code

Verify Operator Route Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Operator Route Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${OR_TABLE}    ${code}    ${OR_GRID_VERIFY_PROPERTIES}
    ...    ${OR_FORM_VERIFY_PROPERTIES}    @{OR_FORM_LABELS}
    Clear Operator Route Row Filter

Delete Operator Route Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for OV_OPERATOR_ROUTE),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Operator Route Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Operator Route Row By Filter    ${code}
    Delete Object Via End Date    ${OR_TABLE}    ${OR_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Operator Route Row Filter

Verify Operator Route Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_OPERATOR_ROUTE) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${OR_TABLE}    OV_OPERATOR_ROUTE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Operator Route Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${OR_TABLE}    ${code}
