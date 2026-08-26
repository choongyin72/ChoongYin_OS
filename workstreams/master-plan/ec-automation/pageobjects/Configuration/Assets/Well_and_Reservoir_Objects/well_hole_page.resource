*** Settings ***
Documentation       T3 (screen) — Well Hole page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well Hole (CO.0051).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after a 3-level
...                 same-row navigator cascade (Op Production Unit -> Op Area -> Op Facility Class 1,
...                 nav:form:G:0:R:1:C:1/C:2/C:3) is filled + GO. Converted from the OLD
...                 "Apply OV-GM Navigator First Available" pattern to Area's full pattern
...                 (2026-08-26): 5-TC/per-TC-login/pure-screen-verify structure, navigator fill
...                 delegated to the shared T2 "Apply Navigator From Properties"
...                 (resources/manage_object.resource) driven by testdata/well_hole_navigator.properties,
...                 using the SAME SPECIFIC "P1" scope already proven live by the sibling Well
...                 screen (pageobjects/.../well_page.resource - owner screenshot ground truth
...                 2026-07-30), NOT first-available - confirmed live 2026-08-26 that this scope
...                 also lists real OV_WELL_HOLE rows and that "P1 Production Unit" is a valid
...                 Insert-form "Op Production Unit" option. Real labels confirmed live via the
...                 pre-existing well_hole_page.resource: objectForm/updateAttributes use
...                 SCREEN-PREFIXED "Well Hole Code"/"Well Hole Name" (like Area's "Area Code"),
...                 NOT the generic "Code"/"Name" Bank/Object List use - every T2 call below passes
...                 code_label=Well Hole Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${WELL_HOLE_SCREEN}          Well Hole
${WELL_HOLE_TABLE}           manageObject:form:T_data
# navigator (groupmodel): 3-level same-row cascade, C:1 Op Production Unit -> C:2 Op Area ->
# C:3 Op Facility Class 1 - MANDATORY before the grid loads. Values confirmed live (2026-08-26):
# the SPECIFIC "P1" scope (not first-available) that the sibling Well screen already proved
# (owner screenshot ground truth 2026-07-30) also lists real Well Hole rows.
# The fill itself goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/well_hole_navigator.properties.
${WELL_HOLE_NAV_PU}          nav:form:G:0:R:1:C:1:dd
${WELL_HOLE_NAV_PU_VALUE}    P1 Production Unit
${WELL_HOLE_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hole_navigator.properties
${WELL_HOLE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hole_insert.properties
${WELL_HOLE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hole_update.properties
${WELL_HOLE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hole_form_verify.properties
${WELL_HOLE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hole_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's ${AREA_DEL_ENDDATE}: this row packs Start Date (C:1) and
# End Date (C:3) together with the End Date label at C:2. Value confirmed live via the
# pre-existing well_hole_page.resource's own ${DEL_ENDDATE}.
${WELL_HOLE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Well Hole's own form-field label set (Start Date/End Date deliberately excluded - they live only
# in objectdates, not updateAttributes/objectForm's fill-once trio; Op Production Unit
# deliberately excluded from round-trip comparison - it's filled via a resolved reference value
# which can re-render different display text after reload, same caveat as every other converted
# screen's dropdown fields).
@{WELL_HOLE_FORM_LABELS}    Well Hole Code    Well Hole Name


*** Keywords ***
Find Well Hole Row By Filter
    [Documentation]    Explicitly filter the Well Hole grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${WELL_HOLE_TABLE}    ${code}

Clear Well Hole Row Filter
    [Documentation]    Clear the Code column filter (see Find Well Hole Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${WELL_HOLE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Well Hole's OWN credentials (${WELL_HOLE_EC_USER}/
    ...    ${WELL_HOLE_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${WELL_HOLE_EC_USER}    ${WELL_HOLE_EC_PASS}

Open Well Hole Screen With Navigator Values Populated
    [Documentation]    Navigate to the Well Hole screen, THEN fill + submit the mandatory 3-level
    ...    navigator cascade (dropdowns + GO) - Well Hole's grid stays empty until this happens, so
    ...    this single keyword bundles both steps for the test case (owner's exact skeleton calls
    ...    this as ONE line per TC, not two). Assumes the caller already logged in this test case
    ...    (via Login To EC Application) - matches every other Area-pattern-converted screen's
    ...    "Open <Screen> Screen" convention. Navigator fill delegates to the shared T2
    ...    "Apply Navigator From Properties" (resources/manage_object.resource), driven by
    ...    testdata/well_hole_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" here - so any other OV-GM screen with a
    ...    navigator can reuse the same shared keyword with its own properties file.
    Open EC Screen    ${WELL_HOLE_SCREEN}
    Apply Navigator From Properties    ${WELL_HOLE_NAVIGATOR_PROPERTIES}

Insert Well Hole Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, called
    ...    with ZERO arguments so well_hole_iud.robot's test case body reads as a plain business
    ...    step. Also owns the integrity check that the inserted Well Hole Code matches the
    ...    suite's ${TEST_CODE}. ${WELL_HOLE_INSERT_PROPERTIES}'s Op Production Unit value MUST
    ...    equal ${WELL_HOLE_NAV_PU_VALUE} or the new row is not visible under this navigator
    ...    scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${WELL_HOLE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Well Hole Code
    RETURN    ${code}

Verify Well Hole Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Well Hole Code/Well Hole Name's LIVE SCREEN value is compared to
    ...    testdata/well_hole_insert.properties. Filters via Find Well Hole Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Hole Row By Filter    ${code}
    Verify Object Insert Exists    ${WELL_HOLE_TABLE}    ${code}    Well Hole
    ...    ${WELL_HOLE_INSERT_PROPERTIES}    @{WELL_HOLE_FORM_LABELS}    code_label=Well Hole Code
    Clear Well Hole Row Filter

Update Well Hole Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Well
    ...    Hole Name is listed in testdata/well_hole_update.properties - Well Hole Code is
    ...    read-only in updateAttributes and Well Hole has no Description field (confirmed live:
    ...    OV_WELL_HOLE has no such column). Filters via Find Well Hole Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${WELL_HOLE_UPDATE_PROPERTIES}
    Find Well Hole Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${WELL_HOLE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Well Hole Code
    Clear Well Hole Row Filter
    RETURN    ${data}

Verify Well Hole Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Well Hole Name's LIVE SCREEN value to
    ...    testdata/well_hole_update.properties. Filters via Find Well Hole Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Hole Row By Filter    ${code}
    Verify Object Form Record    ${WELL_HOLE_TABLE}    ${code}    Well Hole
    ...    ${WELL_HOLE_UPDATE_PROPERTIES}    Well Hole Name    code_label=Well Hole Code
    Clear Well Hole Row Filter

Find Well Hole Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Well
    ...    Hole Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Well Hole Record Found (called right after, same TC) needs the grid still filtered to
    ...    ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Hole Row By Filter    ${code}
    Find Object Record    ${WELL_HOLE_TABLE}    ${code}    Well Hole    code_label=Well Hole Code

Verify Well Hole Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Well Hole Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${WELL_HOLE_TABLE}    ${code}    ${WELL_HOLE_GRID_VERIFY_PROPERTIES}
    ...    ${WELL_HOLE_FORM_VERIFY_PROPERTIES}    @{WELL_HOLE_FORM_LABELS}
    Clear Well Hole Row Filter

Delete Well Hole Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the Well Hole, set End Date = Start Date (EC true delete for OV_WELL_HOLE), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Well Hole Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Well Hole Row By Filter    ${code}
    Delete Object Via End Date    ${WELL_HOLE_TABLE}    ${WELL_HOLE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Well Hole Row Filter

Verify Well Hole Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_WELL_HOLE) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${WELL_HOLE_TABLE}    OV_WELL_HOLE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Well Hole Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${WELL_HOLE_TABLE}    ${code}
