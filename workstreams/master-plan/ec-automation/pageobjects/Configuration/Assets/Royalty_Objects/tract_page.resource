*** Settings ***
Documentation       T3 (screen) — Tract page object.
...                 Screen: Configuration > Assets > Royalty Objects > Tract.
...                 OV-GM (groupmodel manage-object) screen: the grid (manageObject:form:T_data)
...                 loads ONLY after the mandatory Unit Agreement navigator dropdown is set + GO.
...                 Converted to the full Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE 2026-08-26, correcting this branch's own first commit (which wrongly
...                 concluded Tract does NOT fit the Area pattern because its navigator spans TWO
...                 separate groups — nav:form:G:0 for Date, nav:form:G:1 for Unit Agreement).
...                 Live re-recon (2026-08-26) confirmed: G:0's Date field already carries a
...                 non-empty default on load and needs no fill at all; G:1's Unit Agreement
...                 dropdown is the ONLY mandatory-and-empty nav field. That means Tract's REAL
...                 navigator-fill requirement is exactly ONE mandatory dropdown — structurally
...                 the same shape as Area's own single-dropdown navigator, just living at group
...                 index 1 / column 0 instead of group 0 / column 1. The shared T2 keyword
...                 "Apply Navigator From Properties" (resources/manage_object.resource) gained two
...                 new OPTIONAL, backward-compatible arguments this session (${group}, ${start_col})
...                 specifically to address this — confirmed via live DOM recon, not assumed.
...                 Real labels confirmed live 2026-08-26 (objectForm text dump): screen-prefixed
...                 "Tract Code"/"Tract Name" (like Area Code/Area Name), plus "Unit Agreement"
...                 (generic, not prefixed) — every T2 call below passes code_label=Tract Code.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${TRACT_SCREEN}         Tract
${TRACT_TABLE}          manageObject:form:T_data
# navigator (groupmodel, TWO separate groups): G:0 = Date (already carries a non-empty default
# on load, confirmed live 2026-08-26 - value 'ui-state-filled', no fill needed); G:1 = Unit
# Agreement dropdown, MANDATORY before the grid loads, addressed at COLUMN 0 (not column 1,
# unlike Area/Well/etc - confirmed live via a DOM scan: nav:form:G:1:R:1:C:0:dd carried class
# "{mandatory:true} MandatoryCellStyle"). ${TRACT_NAV_UA} is kept only as documentation of the
# real DOM id - the properties-driven fill (Apply Navigator From Properties ... group=1
# start_col=0) resolves to this exact id, not a different one.
${TRACT_NAV_UA}         nav:form:G:1:R:1:C:0:dd
${TRACT_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/tract_navigator.properties
${TRACT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/tract_insert.properties
${TRACT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/tract_update.properties
${TRACT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/tract_form_verify.properties
${TRACT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/tract_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area/Bank's own ${..._DEL_ENDDATE}. Value confirmed live by the
# pre-existing (pre-Area-pattern) driver, unchanged by this conversion.
${TRACT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Tract's own form-field label set (Start Date/End Date deliberately excluded - they live only in
# objectdates, not updateAttributes/objectForm's fill-once trio; Unit Agreement deliberately
# excluded from round-trip comparison - it's filled via a resolved reference value which can
# re-render different display text after reload, same caveat as every other converted OV-GM
# screen's dropdown fields).
@{TRACT_FORM_LABELS}    Tract Code    Tract Name


*** Keywords ***
Find Tract Row By Filter
    [Documentation]    Explicitly filter the Tract grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Area/Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${TRACT_TABLE}    ${code}

Clear Tract Row Filter
    [Documentation]    Clear the Code column filter (see Find Tract Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${TRACT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Tract's OWN credentials (${TRACT_EC_USER}/${TRACT_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${TRACT_EC_USER}    ${TRACT_EC_PASS}

Open Tract Screen With Navigator Values Populated
    [Documentation]    Navigate to the Tract screen, THEN fill + submit the mandatory Unit
    ...    Agreement navigator (dropdown + GO) - Tract's grid stays empty until this happens, so
    ...    this single keyword bundles both steps for the test case (one line per TC). Navigator
    ...    fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by testdata/tract_navigator.properties,
    ...    with group=1 (Unit Agreement lives in nav:form:G:1, not G:0 - G:0 is the Date field,
    ...    already defaulted, deliberately left untouched) and start_col=0 (Tract's Unit
    ...    Agreement dropdown is addressed at column 0, not column 1 - confirmed by live DOM
    ...    recon 2026-08-26, not assumed from another screen's convention).
    Open EC Screen    ${TRACT_SCREEN}
    Apply Navigator From Properties    ${TRACT_NAVIGATOR_PROPERTIES}    group=1    start_col=0

Insert Tract Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so tract_iud.robot's test case body reads as a plain
    ...    business step. ${TRACT_INSERT_PROPERTIES}'s Unit Agreement value MUST equal the
    ...    navigator's own value (testdata/tract_navigator.properties) or the new row is not
    ...    visible under this navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${TRACT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Tract Code
    RETURN    ${code}

Verify Tract Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Tract Code/Tract Name's LIVE SCREEN value is compared to
    ...    testdata/tract_insert.properties. Filters via Find Tract Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Tract Row By Filter    ${code}
    Verify Object Insert Exists    ${TRACT_TABLE}    ${code}    Tract    ${TRACT_INSERT_PROPERTIES}
    ...    @{TRACT_FORM_LABELS}    code_label=Tract Code
    Clear Tract Row Filter

Update Tract Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Tract
    ...    Name is listed in testdata/tract_update.properties - Tract Code is read-only in
    ...    updateAttributes. Filters via Find Tract Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${TRACT_UPDATE_PROPERTIES}
    Find Tract Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${TRACT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Tract Code
    Clear Tract Row Filter
    RETURN    ${data}

Verify Tract Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Tract Name's LIVE SCREEN value to
    ...    testdata/tract_update.properties. Filters via Find Tract Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Tract Row By Filter    ${code}
    Verify Object Form Record    ${TRACT_TABLE}    ${code}    Tract    ${TRACT_UPDATE_PROPERTIES}
    ...    Tract Name    code_label=Tract Code
    Clear Tract Row Filter

Find Tract Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Tract
    ...    Row By Filter first. Deliberately does NOT clear the filter afterward - Verify Tract
    ...    Record Found (called right after, same TC) needs the grid still filtered to ${code}
    ...    for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Tract Row By Filter    ${code}
    Find Object Record    ${TRACT_TABLE}    ${code}    Tract    code_label=Tract Code

Verify Tract Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Tract Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${TRACT_TABLE}    ${code}    ${TRACT_GRID_VERIFY_PROPERTIES}
    ...    ${TRACT_FORM_VERIFY_PROPERTIES}    @{TRACT_FORM_LABELS}
    Clear Tract Row Filter

Delete Tract Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the tract, set End Date = Start Date (EC true delete for OV_TRACT), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Tract Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Tract Row By Filter    ${code}
    Delete Object Via End Date    ${TRACT_TABLE}    ${TRACT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Tract Row Filter

Verify Tract Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_TRACT) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${TRACT_TABLE}    OV_TRACT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Tract Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${TRACT_TABLE}    ${code}
