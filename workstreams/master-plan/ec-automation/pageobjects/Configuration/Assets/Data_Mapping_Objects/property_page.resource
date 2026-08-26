*** Settings ***
Documentation       T3 (screen) - Property page object.
...                 Screen: Configuration > Assets > Data_Mapping_Objects > Property (SP.0059).
...                 OV-GM (manage-object, groupmodel) screen: the grid loads ONLY after the
...                 navigator's single mandatory Business Unit dropdown is set + GO. Confirmed
...                 LIVE 2026-08-26 (tmp/recon_property_nav.py, read-only recon, no Save/Insert/
...                 Delete) that the navigator has 2 DOM groups - G:0 ("Date") and G:1
...                 ("Business Unit") - but this does NOT disqualify it from the Area pattern:
...                 G:0's Date field already carries a non-empty default on load
...                 (MandatoryCellStyleWhite = already-filled style), so G:1's Business Unit
...                 dropdown is the ONLY genuinely mandatory+empty field - exactly the same
...                 single-group-needs-fill shape already proven to fit on Tract. Business
...                 Unit's dropdown sits at G:1, C:0 (not the usual G:0, C:1), so the shared T2
...                 "Apply Navigator From Properties" is called with ${group}=1 ${start_col}=0
...                 (both optional args added to that keyword this session, additive-only,
...                 default behavior for every other caller unchanged).
...                 Converted to the Area-pattern full STRUCTURE (2026-08-26): 5 TCs, per-TC
...                 login/logout, fixed test code, properties-file-driven insert/update/verify,
...                 explicit grid-filter wiring, zero inline DB-verify calls in the .robot file.
...                 Real labels confirmed live via the prior hand-written driver
...                 (py/property_iud.py): objectForm/updateAttributes use "Property Code"/
...                 "Property Name"/"Business Unit Name" - every T2 call below passes
...                 code_label=Property Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PROPERTY_SCREEN}          Property
${PROPERTY_TABLE}           manageObject:form:T_data
# navigator (groupmodel): single Business Unit dropdown at G:1/C:0 - MANDATORY before the grid
# loads. G:0's Date field already has a non-empty default, so this is the ONLY field to fill.
# Value confirmed LIVE this session (2026-08-26, tmp/recon_property_nav.py): "Royalty Canada"
# is present among 16 live Business Unit options, matching the prior hand-written driver.
# The fill itself goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource, ${group}=1 ${start_col}=0), driven by
# testdata/property_navigator.properties. ${PROPERTY_NAV_BU}/${PROPERTY_NAV_BU_VALUE} are kept
# only as documentation of the DOM id and required value - the properties-driven fill resolves
# to the same id/value, not a different one.
${PROPERTY_NAV_BU}          nav:form:G:1:R:1:C:0:dd
${PROPERTY_NAV_BU_VALUE}    Royalty Canada
${PROPERTY_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/property_navigator.properties
${PROPERTY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/property_insert.properties
${PROPERTY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/property_update.properties
${PROPERTY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/property_form_verify.properties
${PROPERTY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/property_grid_verify.properties
# objectdates field ID (Delete - End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented rationale as every other converted OV-GM screen's del-enddate
# id: this row packs Start Date (C:1) and End Date (C:3) together with the End Date label at
# C:2, a shape the one-field-per-row label scan cannot safely resolve. Value confirmed live via
# the prior hand-written driver's own DOM (same framework-invariant layout as every other
# OV-GM screen).
${PROPERTY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Property's own form-field label set (Start Date/End Date deliberately excluded - they live
# only in objectdates, not updateAttributes/objectForm's fill-once trio; Business Unit Name
# deliberately excluded from round-trip comparison - it's filled via a resolved reference value
# which can re-render different display text after reload, same caveat as every other converted
# screen's dropdown fields).
@{PROPERTY_FORM_LABELS}    Property Code    Property Name


*** Keywords ***
Find Property Row By Filter
    [Documentation]    Explicitly filter the Property grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PROPERTY_TABLE}    ${code}

Clear Property Row Filter
    [Documentation]    Clear the Code column filter (see Find Property Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PROPERTY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Property's OWN credentials (${PROPERTY_EC_USER}/
    ...    ${PROPERTY_EC_PASS} from credentials.py) on the current page - works whether this
    ...    is the very first login (page freshly loaded on the login form via the shared T1
    ...    Open EC Application) or a re-login after Logout From EC Application.
    Login To EC Screen    ${PROPERTY_EC_USER}    ${PROPERTY_EC_PASS}

Open Property Screen With Navigator Values Populated
    [Documentation]    Navigate to the Property screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - the grid stays empty until this happens,
    ...    so this single keyword bundles both steps for the test case (one line per TC).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    ...    Navigator fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource, ${group}=1 ${start_col}=0 - Property's Business
    ...    Unit dropdown lives in its own G:1 group at C:0, not the usual G:0/C:1), driven by
    ...    testdata/property_navigator.properties.
    Open EC Screen    ${PROPERTY_SCREEN}
    Apply Navigator From Properties    ${PROPERTY_NAVIGATOR_PROPERTIES}    group=1    start_col=0

Insert Property Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so property_iud.robot's test case body reads
    ...    as a plain business step. ${PROPERTY_INSERT_PROPERTIES}'s Business Unit Name value
    ...    MUST equal ${PROPERTY_NAV_BU_VALUE} or the new row is not visible under this
    ...    navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${PROPERTY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Property Code
    RETURN    ${code}

Verify Property Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here - that's TC02's own separate DbVerify assertion): row
    ...    exists in the grid, then Property Code/Property Name's LIVE SCREEN value is compared
    ...    to testdata/property_insert.properties. Filters via Find Property Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Property Row By Filter    ${code}
    Verify Object Insert Exists    ${PROPERTY_TABLE}    ${code}    Property
    ...    ${PROPERTY_INSERT_PROPERTIES}    @{PROPERTY_FORM_LABELS}
    ...    code_label=Property Code
    Clear Property Row Filter

Update Property Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Property Name is listed in testdata/property_update.properties - Property Code is
    ...    read-only in updateAttributes. Filters via Find Property Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PROPERTY_UPDATE_PROPERTIES}
    Find Property Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PROPERTY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Property Code
    Clear Property Row Filter
    RETURN    ${data}

Verify Property Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification: selects the row, compares Property Name's LIVE SCREEN value to
    ...    testdata/property_update.properties. Filters via Find Property Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Property Row By Filter    ${code}
    Verify Object Form Record    ${PROPERTY_TABLE}    ${code}    Property
    ...    ${PROPERTY_UPDATE_PROPERTIES}    Property Name    code_label=Property Code
    Clear Property Row Filter

Find Property Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls
    ...    Find Property Row By Filter first. Deliberately does NOT clear the filter afterward
    ...    - Verify Property Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Property Row By Filter    ${code}
    Find Object Record    ${PROPERTY_TABLE}    ${code}    Property    code_label=Property Code

Verify Property Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the full form record match the expected data. Caller must already have
    ...    selected the row (TC04 does, via Find Property Record before this) AND left the
    ...    Code filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PROPERTY_TABLE}    ${code}    ${PROPERTY_GRID_VERIFY_PROPERTIES}
    ...    ${PROPERTY_FORM_VERIFY_PROPERTIES}    @{PROPERTY_FORM_LABELS}
    Clear Property Row Filter

Delete Property Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/
    ...    ${END_DATE}). Select the object, set End Date = Start Date (EC true delete for
    ...    OV_PROPERTY), Save. Versioned groupmodel grids redraw lazily after a delete - Save
    ...    And Refresh List (inside T2) already re-applies the navigator, so the assertion
    ...    reads a fresh list. Filters via Find Property Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Property Row By Filter    ${code}
    Delete Object Via End Date    ${PROPERTY_TABLE}    ${PROPERTY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Property Row Filter

Verify Property Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_PROPERTY) - the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper
    ...    keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PROPERTY_TABLE}    OV_PROPERTY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Property Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (grid-only check) - delegates to the shared T2 Verify Object Does Not
    ...    Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PROPERTY_TABLE}    ${code}
