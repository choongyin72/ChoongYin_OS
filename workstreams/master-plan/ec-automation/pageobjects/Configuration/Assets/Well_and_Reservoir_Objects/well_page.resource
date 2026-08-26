*** Settings ***
Documentation       T3 (screen) — Well page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well (CO.0049).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 genuine 3-level P1 navigator cascade (Production Unit -> Area -> Facility 1,
...                 same-row C:1/C:2/C:3) is set + GO — owner screenshot ground truth (2026-07-30):
...                 SPECIFIC P1 values, not first-available (first-available AS1 left a deeper
...                 level empty = the original park). Converted to the Area-pattern 5-TC/
...                 per-TC-login/pure-screen-verify STRUCTURE (2026-08-26) while KEEPING this
...                 genuine navigator gesture — Well is still OV-GM, not plain Bank-shaped; the
...                 3-level cascade + GO step is real and required, not something this conversion
...                 removed. Real labels confirmed live via the pre-existing driver: objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Well Code"/"Well Name" (like Area's
...                 "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use —
...                 every T2 call below passes code_label=Well Code accordingly. Well Type
...                 (mandatory dd, first-available) is preserved via the __FIRST__ sentinel.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${WELL_SCREEN}          Well
${WELL_TABLE}           manageObject:form:T_data
# navigator (groupmodel): 3-level P1 cascade — MANDATORY before the grid loads.
# Values confirmed live (owner screenshot ground truth, 2026-07-30, carried over verbatim from
# the pre-existing "Apply Well Navigator" keyword this conversion replaces):
# C:1 = P1 Production Unit, C:2 = P1 Area, C:3 = P1 Facility 1.
# 2026-08-26: the fill itself now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource — this screen's 3-level cascade is explicitly documented
# there as a proven case), driven by testdata/well_navigator.properties.
${WELL_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/well_navigator.properties
${WELL_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/well_insert.properties
${WELL_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/well_update.properties
${WELL_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_form_verify.properties
${WELL_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven —
# same documented rationale as Area's ${AREA_DEL_ENDDATE}/Bank's ${BANK_DEL_ENDDATE}. Value reused
# verbatim from the pre-existing Well driver's own ${DEL_ENDDATE}.
${WELL_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Well's own form-field label set (Start Date/End Date deliberately excluded — they live only in
# objectdates, not updateAttributes/objectForm's fill-once trio; Well Type deliberately excluded
# from round-trip comparison — it's filled via __FIRST__/a resolved reference value which can
# re-render different display text after reload, same caveat as every other converted screen's
# dropdown fields).
@{WELL_FORM_LABELS}    Well Code    Well Name


*** Keywords ***
Find Well Row By Filter
    [Documentation]    Explicitly filter the Well grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${WELL_TABLE}    ${code}

Clear Well Row Filter
    [Documentation]    Clear the Code column filter (see Find Well Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${WELL_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Well's OWN credentials (${WELL_EC_USER}/${WELL_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${WELL_EC_USER}    ${WELL_EC_PASS}

Open Well Screen With Navigator Values Populated
    [Documentation]    Navigate to the Well screen, THEN fill + submit the mandatory 3-level P1
    ...    navigator cascade (Production Unit -> Area -> Facility 1, dropdown + GO) - Well's grid
    ...    stays empty until this happens, so this single keyword bundles both steps for the test
    ...    case (owner's exact skeleton calls this as ONE line per TC, not two). Assumes the
    ...    caller already logged in this test case (via Login To EC Application) - matches every
    ...    other Area-pattern-converted screen's "Open <Screen> Screen" convention, extended here
    ...    with the genuine OV-GM navigator gesture that already existed in this screen's own
    ...    prior "Open Well Screen"/"Apply Well Navigator" keywords (just wrapped/renamed into
    ...    this shape, not reinvented). Navigator fill delegates to the shared T2 "Apply Navigator
    ...    From Properties" (resources/manage_object.resource, added 2026-08-26), driven by
    ...    testdata/well_navigator.properties, instead of inlining three "Select EC Dropdown
    ...    Option" calls + "Apply Navigator" here.
    Open EC Screen    ${WELL_SCREEN}
    Apply Navigator From Properties    ${WELL_NAVIGATOR_PROPERTIES}

Insert Well Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so well_iud.robot's test case body reads as a plain
    ...    business step. Also owns the integrity check that the inserted Well Code matches the
    ...    suite's ${TEST_CODE}. testdata/well_insert.properties' Well Type=__FIRST__ preserves
    ...    the pre-existing driver's mandatory-dropdown handling.
    [Arguments]    ${properties_path}=${WELL_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Well Code
    RETURN    ${code}

Verify Well Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Well Code/Well Name's LIVE SCREEN value is compared to testdata/well_insert.properties.
    ...    Filters via Find Well Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Row By Filter    ${code}
    Verify Object Insert Exists    ${WELL_TABLE}    ${code}    Well    ${WELL_INSERT_PROPERTIES}
    ...    @{WELL_FORM_LABELS}    code_label=Well Code
    Clear Well Row Filter

Update Well Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Well
    ...    Name is listed in testdata/well_update.properties - Well Code is read-only in
    ...    updateAttributes. Filters via Find Well Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${WELL_UPDATE_PROPERTIES}
    Find Well Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${WELL_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Well Code
    Clear Well Row Filter
    RETURN    ${data}

Verify Well Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Well Name's LIVE SCREEN value to testdata/well_update.properties.
    ...    Filters via Find Well Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Row By Filter    ${code}
    Verify Object Form Record    ${WELL_TABLE}    ${code}    Well    ${WELL_UPDATE_PROPERTIES}
    ...    Well Name    code_label=Well Code
    Clear Well Row Filter

Find Well Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Well Row
    ...    By Filter first. Deliberately does NOT clear the filter afterward - Verify Well Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Row By Filter    ${code}
    Find Object Record    ${WELL_TABLE}    ${code}    Well    code_label=Well Code

Verify Well Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Well Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${WELL_TABLE}    ${code}    ${WELL_GRID_VERIFY_PROPERTIES}
    ...    ${WELL_FORM_VERIFY_PROPERTIES}    @{WELL_FORM_LABELS}
    Clear Well Row Filter

Delete Well Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the well, set End Date = Start Date (EC true delete for OV_WELL), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Well Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Well Row By Filter    ${code}
    Delete Object Via End Date    ${WELL_TABLE}    ${WELL_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Well Row Filter

Verify Well Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_WELL) - the DB check lives here, in the shared
    ...    T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that pattern
    ...    was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${WELL_TABLE}    OV_WELL    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Well Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${WELL_TABLE}    ${code}
