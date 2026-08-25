*** Settings ***
Documentation       T3 (screen) — Area page object.
...                 Screen: Configuration > Assets > Basic Objects > Area.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit navigator dropdown is set + GO. Converted to the
...                 Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner-directed
...                 exception, 2026-08-25) while KEEPING this genuine navigator gesture - Area
...                 is still OV-GM, not plain Bank-shaped; the PU+GO step is real and required,
...                 not something this conversion removed. Real labels confirmed live (2026-08-25):
...                 objectForm/updateAttributes use SCREEN-PREFIXED "Area Code"/"Area Name" (like
...                 State's "State Code"), NOT the generic "Code"/"Name" Bank/Object List use -
...                 every T2 call below passes code_label=Area Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${AREA_SCREEN}          Area
${AREA_TABLE}           manageObject:form:T_data
# navigator (groupmodel): Production Unit dropdown — MANDATORY before the grid loads.
# Value confirmed live (2026-08-25): the "Production Unit" option is itself the PU's display
# name in this sandbox (matches the pre-existing suite's user-approved 2026-06-11 context).
# 2026-08-26: the fill itself now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/area_navigator.properties. ${AREA_NAV_PU}
# and ${AREA_NAV_PU_VALUE} are kept only as documentation of the DOM id (row 1, C:1) and the
# required value - the properties-driven fill resolves to the same id/value, not a different one.
${AREA_NAV_PU}          nav:form:G:0:R:1:C:1:dd
${AREA_NAV_PU_VALUE}    Production Unit
${AREA_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/area_navigator.properties
${AREA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/area_insert.properties
${AREA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/area_update.properties
${AREA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/area_form_verify.properties
${AREA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/area_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Bank's ${BANK_DEL_ENDDATE}: this row packs Start Date (C:1) and
# End Date (C:3) together with the End Date label at C:2, a shape the one-field-per-row label
# scan cannot safely resolve. Value confirmed live via the pre-existing Playwright driver
# (screens/.../Area/playwright/ec_iud_area.py: del_end).
${AREA_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Area's own form-field label set (Start Date/End Date deliberately excluded - they live only in
# objectdates, not updateAttributes/objectForm's fill-once trio; Op Production Unit deliberately
# excluded from round-trip comparison - it's filled via a resolved reference value which can
# re-render different display text after reload, same caveat as every other converted screen's
# dropdown fields).
@{AREA_FORM_LABELS}    Area Code    Area Name


*** Keywords ***
Find Area Row By Filter
    [Documentation]    Explicitly filter the Area grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${AREA_TABLE}    ${code}

Clear Area Row Filter
    [Documentation]    Clear the Code column filter (see Find Area Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${AREA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Area's OWN credentials (${AREA_EC_USER}/${AREA_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${AREA_EC_USER}    ${AREA_EC_PASS}

Open Area Screen With Navigator Values Populated
    [Documentation]    Navigate to the Area screen, THEN fill + submit the mandatory Production
    ...    Unit navigator (dropdown + GO) - Area's grid stays empty until this happens, so this
    ...    single keyword bundles both steps for the test case (owner's exact skeleton calls this
    ...    as ONE line per TC, not two). Assumes the caller already logged in this test case (via
    ...    Login To EC Application) - matches every other Bank-pattern-converted screen's "Open
    ...    <Screen> Screen" convention, extended here with the genuine OV-GM navigator gesture
    ...    that already existed in this screen's own prior "Open Area Screen" keyword (just
    ...    wrapped/renamed into this shape, not reinvented). Navigator fill delegates to the
    ...    shared T2 "Apply Navigator From Properties" (resources/manage_object.resource, added
    ...    2026-08-26), driven by testdata/area_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" here - so any other OV-GM screen with a
    ...    navigator can reuse the same shared keyword with its own properties file.
    Open EC Screen    ${AREA_SCREEN}
    Apply Navigator From Properties    ${AREA_NAVIGATOR_PROPERTIES}

Insert Area Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Area From Properties, called with
    ...    ZERO arguments so area_iud.robot's test case body reads as a plain business step. Also
    ...    owns the integrity check that the inserted Area Code matches the suite's ${TEST_CODE}.
    ...    ${AREA_INSERT_PROPERTIES}'s Op Production Unit value MUST equal ${AREA_NAV_PU_VALUE} or
    ...    the new row is not visible under this navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${AREA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Area Code
    RETURN    ${code}

Verify Area Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Area Code/Area Name's LIVE SCREEN value is compared to testdata/area_insert.properties.
    ...    Filters via Find Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Area Row By Filter    ${code}
    Verify Object Insert Exists    ${AREA_TABLE}    ${code}    Area    ${AREA_INSERT_PROPERTIES}
    ...    @{AREA_FORM_LABELS}    code_label=Area Code
    Clear Area Row Filter

Update Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Area
    ...    Name is listed in testdata/area_update.properties - Area Code is read-only in
    ...    updateAttributes and Area has no Description field (confirmed live: OV_AREA has no
    ...    such column). Filters via Find Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${AREA_UPDATE_PROPERTIES}
    Find Area Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${AREA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Area Code
    Clear Area Row Filter
    RETURN    ${data}

Verify Area Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Area Name's LIVE SCREEN value to testdata/area_update.properties.
    ...    Filters via Find Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Area Row By Filter    ${code}
    Verify Object Form Record    ${AREA_TABLE}    ${code}    Area    ${AREA_UPDATE_PROPERTIES}
    ...    Area Name    code_label=Area Code
    Clear Area Row Filter

Find Area Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Area Row
    ...    By Filter first. Deliberately does NOT clear the filter afterward - Verify Area Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Area Row By Filter    ${code}
    Find Object Record    ${AREA_TABLE}    ${code}    Area    code_label=Area Code

Verify Area Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Area Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${AREA_TABLE}    ${code}    ${AREA_GRID_VERIFY_PROPERTIES}
    ...    ${AREA_FORM_VERIFY_PROPERTIES}    @{AREA_FORM_LABELS}
    Clear Area Row Filter

Delete Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the area, set End Date = Start Date (EC true delete for OV_AREA), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Area Row By Filter    ${code}
    Delete Object Via End Date    ${AREA_TABLE}    ${AREA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Area Row Filter

Verify Area Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_AREA) - the DB check lives here, in the shared
    ...    T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that pattern
    ...    was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${AREA_TABLE}    OV_AREA    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Area Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${AREA_TABLE}    ${code}
