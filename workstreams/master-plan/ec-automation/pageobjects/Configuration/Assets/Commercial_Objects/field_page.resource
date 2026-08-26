*** Settings ***
Documentation       T3 (screen) — Field page object.
...                 Screen: Configuration > Assets > Commercial Objects > Field.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Area navigator dropdown is set + GO. Converted to the
...                 Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner standing
...                 rule 2026-08-26: any EC screen with a navigator matching Area's layout must
...                 follow Area's FULL pattern, not just the navigator-fill piece already done
...                 in PR #525) while KEEPING this genuine navigator gesture - Field is still
...                 OV-GM, not plain Bank-shaped; the Area+GO step is real and required, not
...                 something this conversion removed. Real labels confirmed live (2026-08-26):
...                 objectForm/updateAttributes use SCREEN-PREFIXED "Field Code"/"Field Name"
...                 (like Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name"
...                 Bank/Object List use - every T2 call below passes code_label=Field Code
...                 accordingly. Grid headers confirmed live: Field Code/Field Name/Start
...                 Date/End Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables            ../../../../resources/credentials.py


*** Variables ***
${FIELD_SCREEN}         Field
${FIELD_TABLE}          manageObject:form:T_data
# navigator (groupmodel): Area dropdown — MANDATORY before the grid loads.
# Kept only as documentation of the DOM id (row 1, C:1) and the required value - the
# properties-driven fill (below) resolves to the same id/value, not a different one.
${FIELD_NAV0}           nav:form:G:0:R:1:C:1:dd
${FIELD_NAV_VALUE}      Offshore area
${FIELD_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/field_navigator.properties
${FIELD_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/field_insert.properties
${FIELD_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/field_update.properties
${FIELD_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/field_form_verify.properties
${FIELD_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/field_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Bank's ${BANK_DEL_ENDDATE}/Area's ${AREA_DEL_ENDDATE}: this row
# packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# Playwright driver (screens/.../Field/playwright/ec_iud_field.py: del_end) and unchanged since.
${FIELD_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Field's own form-field label set (Start Date/End Date deliberately excluded - they live only in
# objectdates, not updateAttributes/objectForm's fill-once trio; Geo Area deliberately excluded
# from round-trip comparison - it's filled via a resolved reference value which can re-render
# different display text after reload, same caveat as every other converted screen's dropdown
# fields, e.g. Area's Op Production Unit).
@{FIELD_FORM_LABELS}    Field Code    Field Name


*** Keywords ***
Find Field Row By Filter
    [Documentation]    Explicitly filter the Field grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${FIELD_TABLE}    ${code}

Clear Field Row Filter
    [Documentation]    Clear the Code column filter (see Find Field Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${FIELD_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Field's OWN credentials (${FIELD_EC_USER}/${FIELD_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${FIELD_EC_USER}    ${FIELD_EC_PASS}

Open Field Screen With Navigator Values Populated
    [Documentation]    Navigate to the Field screen, THEN fill + submit the mandatory Area
    ...    navigator (dropdown + GO) - Field's grid stays empty until this happens, so this
    ...    single keyword bundles both steps for the test case (matches Area's exact convention).
    ...    Assumes the caller already logged in this test case (via Login To EC Application) -
    ...    matches every other Bank-pattern-converted screen's "Open <Screen> Screen"
    ...    convention, extended here with the genuine OV-GM navigator gesture that already
    ...    existed in this screen's own prior "Open Field Screen" keyword (just wrapped/renamed
    ...    into this shape, not reinvented). Navigator fill delegates to the shared T2 "Apply
    ...    Navigator From Properties" (resources/manage_object.resource, already added for Area
    ...    and already delegated to for Field in PR #525), driven by
    ...    testdata/field_navigator.properties.
    Open EC Screen    ${FIELD_SCREEN}
    Apply Navigator From Properties    ${FIELD_NAVIGATOR_PROPERTIES}

Insert Field Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so field_iud.robot's test case body reads as
    ...    a plain business step. Also owns the integrity check that the inserted Field Code
    ...    matches the suite's ${TEST_CODE}. ${FIELD_INSERT_PROPERTIES}'s Geo Area value MUST
    ...    equal ${FIELD_NAV_VALUE} or the new row is not visible under this navigator scope
    ...    (OV-GM constraint) - same rationale as Area's Op Production Unit.
    [Arguments]    ${properties_path}=${FIELD_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Field Code
    RETURN    ${code}

Verify Field Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Field Code/Field Name's LIVE SCREEN value is compared to
    ...    testdata/field_insert.properties. Filters via Find Field Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Row By Filter    ${code}
    Verify Object Insert Exists    ${FIELD_TABLE}    ${code}    Field    ${FIELD_INSERT_PROPERTIES}
    ...    @{FIELD_FORM_LABELS}    code_label=Field Code
    Clear Field Row Filter

Update Field Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Field
    ...    Name is listed in testdata/field_update.properties - Field Code is read-only in
    ...    updateAttributes. Filters via Find Field Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${FIELD_UPDATE_PROPERTIES}
    Find Field Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${FIELD_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Field Code
    Clear Field Row Filter
    RETURN    ${data}

Verify Field Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Field Name's LIVE SCREEN value to
    ...    testdata/field_update.properties. Filters via Find Field Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Row By Filter    ${code}
    Verify Object Form Record    ${FIELD_TABLE}    ${code}    Field    ${FIELD_UPDATE_PROPERTIES}
    ...    Field Name    code_label=Field Code
    Clear Field Row Filter

Find Field Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Field
    ...    Row By Filter first. Deliberately does NOT clear the filter afterward - Verify Field
    ...    Record Found (called right after, same TC) needs the grid still filtered to ${code} for
    ...    its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Row By Filter    ${code}
    Find Object Record    ${FIELD_TABLE}    ${code}    Field    code_label=Field Code

Verify Field Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Field Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${FIELD_TABLE}    ${code}    ${FIELD_GRID_VERIFY_PROPERTIES}
    ...    ${FIELD_FORM_VERIFY_PROPERTIES}    @{FIELD_FORM_LABELS}
    Clear Field Row Filter

Delete Field Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the field, set End Date = Start Date (EC true delete for OV_FIELD), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Field Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Field Row By Filter    ${code}
    Delete Object Via End Date    ${FIELD_TABLE}    ${FIELD_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Field Row Filter

Verify Field Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_FIELD) - the DB check lives here, in the shared
    ...    T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that pattern
    ...    was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${FIELD_TABLE}    OV_FIELD    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Field Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${FIELD_TABLE}    ${code}
