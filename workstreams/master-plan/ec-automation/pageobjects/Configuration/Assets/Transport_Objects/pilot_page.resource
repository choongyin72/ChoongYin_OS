*** Settings ***
Documentation       T3 (screen) — Pilot page object.
...                 Screen: Configuration > Assets > Transport_Objects > Pilot (CO.2079).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 genuine 3-level same-row navigator cascade (Production Unit -> Area ->
...                 Facility Class 1, C:1/C:2/C:3, one group G:0) is set + GO — confirmed live
...                 2026-08-26 (nav:form:G:0 has exactly 3 dropdowns at R:1:C:1/C:2/C:3, all
...                 MandatoryCellStyle; no per-field separate groups) — same proven shape as
...                 Well's P1 cascade. Converted to the Area-pattern 5-TC/per-TC-login/
...                 pure-screen-verify STRUCTURE (2026-08-26) while KEEPING this genuine
...                 navigator gesture — Pilot is still OV-GM, not plain Bank-shaped; the 3-level
...                 cascade + GO step is real and required, not something this conversion
...                 removed. Real labels confirmed live via the pre-existing driver: objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Pilot Code"/"Pilot Name" (like Well's
...                 "Well Code"/"Well Name"), NOT the generic "Code"/"Name" Bank/Object List use —
...                 every T2 call below passes code_label=Pilot Code accordingly. Op Production
...                 Unit (objectForm) is NOT mandatory-styled and its value domain is INDEPENDENT
...                 of the navigator's Production Unit (pre-existing py/pilot_iud.py comment:
...                 "the nav PU is not necessarily a valid Op PU option") — kept as __FIRST__,
...                 a live-evidenced exception to the generic field-reuse rule for this pair.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables            ../../../../resources/credentials.py


*** Variables ***
${PILOT_SCREEN}         Pilot
${PILOT_TABLE}          manageObject:form:T_data
# navigator (groupmodel): 3-level same-row cascade — MANDATORY before the grid loads.
# Values confirmed live (2026-08-26): the first-available option at each column (same value the
# pre-existing "Apply OV-GM Navigator First Available" driver already picked every run).
${PILOT_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/pilot_navigator.properties
${PILOT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/pilot_insert.properties
${PILOT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/pilot_update.properties
${PILOT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/pilot_form_verify.properties
${PILOT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/pilot_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven —
# same documented rationale as Area's/Well's ${AREA_DEL_ENDDATE}/${WELL_DEL_ENDDATE}. Value reused
# verbatim from the pre-existing Pilot driver's own ${DEL_ENDDATE}.
${PILOT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Pilot's own form-field label set (Start Date/End Date deliberately excluded — they live only in
# objectdates, not updateAttributes/objectForm's fill-once trio; Op Production Unit deliberately
# excluded from round-trip comparison — it's filled via __FIRST__/a resolved reference value which
# can re-render different display text after reload, same caveat as every other converted screen's
# dropdown fields).
@{PILOT_FORM_LABELS}    Pilot Code    Pilot Name


*** Keywords ***
Find Pilot Row By Filter
    [Documentation]    Explicitly filter the Pilot grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PILOT_TABLE}    ${code}

Clear Pilot Row Filter
    [Documentation]    Clear the Code column filter (see Find Pilot Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PILOT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Pilot's OWN credentials (${PILOT_EC_USER}/${PILOT_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${PILOT_EC_USER}    ${PILOT_EC_PASS}

Open Pilot Screen With Navigator Values Populated
    [Documentation]    Navigate to the Pilot screen, THEN fill + submit the mandatory 3-level
    ...    navigator cascade (Production Unit -> Area -> Facility Class 1, dropdown + GO) -
    ...    Pilot's grid stays empty until this happens, so this single keyword bundles both steps
    ...    for the test case (owner's exact skeleton calls this as ONE line per TC, not two).
    ...    Assumes the caller already logged in this test case (via Login To EC Application) -
    ...    matches every other Area-pattern-converted screen's "Open <Screen> Screen" convention,
    ...    extended here with the genuine OV-GM navigator gesture that already existed in this
    ...    screen's own prior "Open Pilot Screen"/"Apply OV-GM Navigator First Available"
    ...    keywords (just wrapped/renamed into this shape, not reinvented). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties" (resources/
    ...    manage_object.resource), driven by testdata/pilot_navigator.properties, instead of
    ...    inlining three "Select EC Dropdown Option" calls + "Apply Navigator" here.
    Open EC Screen    ${PILOT_SCREEN}
    Apply Navigator From Properties    ${PILOT_NAVIGATOR_PROPERTIES}

Insert Pilot Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so pilot_iud.robot's test case body reads as a plain
    ...    business step. Also owns the integrity check that the inserted Pilot Code matches the
    ...    suite's ${TEST_CODE}. testdata/pilot_insert.properties' Op Production Unit=__FIRST__
    ...    preserves the pre-existing driver's mandatory-dropdown handling.
    [Arguments]    ${properties_path}=${PILOT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Pilot Code
    RETURN    ${code}

Verify Pilot Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Pilot Code/Pilot Name's LIVE SCREEN value is compared to testdata/pilot_insert.properties.
    ...    Filters via Find Pilot Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Pilot Row By Filter    ${code}
    Verify Object Insert Exists    ${PILOT_TABLE}    ${code}    Pilot    ${PILOT_INSERT_PROPERTIES}
    ...    @{PILOT_FORM_LABELS}    code_label=Pilot Code
    Clear Pilot Row Filter

Update Pilot Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Pilot
    ...    Name is listed in testdata/pilot_update.properties - Pilot Code is read-only in
    ...    updateAttributes. Filters via Find Pilot Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PILOT_UPDATE_PROPERTIES}
    Find Pilot Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PILOT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Pilot Code
    Clear Pilot Row Filter
    RETURN    ${data}

Verify Pilot Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Pilot Name's LIVE SCREEN value to testdata/pilot_update.properties.
    ...    Filters via Find Pilot Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Pilot Row By Filter    ${code}
    Verify Object Form Record    ${PILOT_TABLE}    ${code}    Pilot    ${PILOT_UPDATE_PROPERTIES}
    ...    Pilot Name    code_label=Pilot Code
    Clear Pilot Row Filter

Find Pilot Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Pilot Row
    ...    By Filter first. Deliberately does NOT clear the filter afterward - Verify Pilot Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Pilot Row By Filter    ${code}
    Find Object Record    ${PILOT_TABLE}    ${code}    Pilot    code_label=Pilot Code

Verify Pilot Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Pilot Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PILOT_TABLE}    ${code}    ${PILOT_GRID_VERIFY_PROPERTIES}
    ...    ${PILOT_FORM_VERIFY_PROPERTIES}    @{PILOT_FORM_LABELS}
    Clear Pilot Row Filter

Delete Pilot Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the pilot, set End Date = Start Date (EC true delete for OV_PILOT), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Pilot Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Pilot Row By Filter    ${code}
    Delete Object Via End Date    ${PILOT_TABLE}    ${PILOT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Pilot Row Filter

Verify Pilot Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_PILOT) - the DB check lives here, in the shared
    ...    T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that pattern
    ...    was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PILOT_TABLE}    OV_PILOT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Pilot Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PILOT_TABLE}    ${code}
