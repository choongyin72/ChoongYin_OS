*** Settings ***
Documentation       T3 (screen) — Shift page object.
...                 Screen: Configuration > Assets > Facility_Objects > Shift (CO.0224).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory 3-level Production Unit -> Area -> Facility Class 1 navigator
...                 cascade (C:1/C:2/C:3, same row - confirmed live via the pre-existing driver's
...                 literal locators nav:form:G:0:R:1:C:1/2/3:dd) is set + GO, with SPECIFIC P1
...                 values (P1 Production Unit -> P1 Area -> P1 Facility 1 - NOT first-available;
...                 P1 scope lists the 4 existing P1 shifts, owner screenshot 2026-07-31).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern) - Shift remains OV-GM, its
...                 genuine 3-level P1 navigator cascade + GO is KEPT exactly as the prior
...                 bespoke driver proved it (Apply Navigator From Properties, EXPLICIT values
...                 from testdata/shift_navigator.properties: Op Production Unit=P1 Production
...                 Unit, Op Area=P1 Area, Op Facility Class 1=P1 Facility 1). This is a
...                 STRUCTURAL conversion, not a reclassification of the screen as plain
...                 Bank-shaped.
...                 Shift ALSO has a MANDATORY FREE-TEXT extra on the insert form: Start Time
...                 (HH:MI) - value '07:00' (format read from the existing P1 S001 row, owner
...                 technique: scan an existing row's populated values). This conversion is about
...                 the navigator/TC-structure only - the Start Time requirement/handling is kept
...                 exactly as-is, just moved into the properties-file-driven insert (auto-detected
...                 as a plain text field by "Fill OV Field By Label Any Kind", same mechanism
...                 every other converted screen's insert already uses - no special-casing needed).
...                 Real labels confirmed live via the prior driver (py/shift_iud.py,
...                 verify_screen PASS + RF 4/4 + Playwright 8/8, 2026-07-31): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Shift Code"/"Shift Name" (like Area's
...                 "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use -
...                 every T2 call below passes code_label=Shift Code accordingly. Op Production
...                 Unit is filled = nav PU value (parent-matching, from the existing row's own
...                 values) - kept in shift_insert.properties, same as Area's own Op Production
...                 Unit entry.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${SHIFT_SCREEN}         Shift
${SHIFT_TABLE}          manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1, 3-level same-row cascade —
# MANDATORY before the grid loads. The fill goes through the shared T2 "Apply Navigator From
# Properties" (resources/manage_object.resource), driven by testdata/shift_navigator.properties
# with the SPECIFIC P1 values already proven live by the prior bespoke driver (shift_page.resource
# "Apply Shift Navigator" / py/shift_iud.py "apply_shift_navigator") - not first-available.
${SHIFT_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/shift_navigator.properties
${SHIFT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/shift_insert.properties
${SHIFT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/shift_update.properties
${SHIFT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/shift_form_verify.properties
${SHIFT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/shift_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# driver (shift_page.resource's own prior ${DEL_ENDDATE}, unchanged by this conversion).
${SHIFT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Shift's own form-field label set (Start Date/Start Time/Op Production Unit deliberately
# excluded from this round-trip comparison set - Start Date/End Date live only in objectdates,
# not updateAttributes/objectForm's fill-once trio; Start Time and Op Production Unit are
# insert-only fields not present in updateAttributes, same caveat as every other converted
# screen's dropdown/free-text fields not being part of the Update round-trip).
@{SHIFT_FORM_LABELS}    Shift Code    Shift Name


*** Keywords ***
Find Shift Row By Filter
    [Documentation]    Explicitly filter the Shift grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${SHIFT_TABLE}    ${code}

Clear Shift Row Filter
    [Documentation]    Clear the Code column filter (see Find Shift Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${SHIFT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Shift's OWN credentials (${SHIFT_EC_USER}/${SHIFT_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${SHIFT_EC_USER}    ${SHIFT_EC_PASS}

Open Shift Screen With Navigator Values Populated
    [Documentation]    Navigate to the Shift screen, THEN fill + submit the mandatory 3-level
    ...    Production Unit -> Area -> Facility Class 1 navigator (dropdowns + GO, SPECIFIC P1
    ...    values) - the grid stays empty until this happens, so this single keyword bundles both
    ...    steps for the test case (Area's exact skeleton calls this as ONE line per TC, not two).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    ...    Navigator fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by testdata/shift_navigator.properties,
    ...    instead of inlining "Select EC Dropdown Option x3 + Apply Navigator" here (the prior
    ...    bespoke shape) - so this OV-GM screen's navigator now reuses the same shared keyword
    ...    every other converted OV-GM screen (Area/Well/Facility Class 1) already uses.
    Open EC Screen    ${SHIFT_SCREEN}
    Apply Navigator From Properties    ${SHIFT_NAVIGATOR_PROPERTIES}

Insert Shift Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so shift_iud.robot's test case body reads as a plain
    ...    business step. Also owns the integrity check that the inserted Shift Code matches the
    ...    suite's ${TEST_CODE}. testdata/shift_insert.properties carries the mandatory free-text
    ...    Start Time (HH:MI) and the parent-matching Op Production Unit = nav PU value - both
    ...    auto-detected/filled by the shared "Fill OV Field By Label Any Kind" mechanism, no
    ...    special-casing needed.
    [Arguments]    ${properties_path}=${SHIFT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Shift Code
    RETURN    ${code}

Verify Shift Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Shift Code/Shift Name's LIVE SCREEN value is compared to
    ...    testdata/shift_insert.properties. Filters via Find Shift Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Shift Row By Filter    ${code}
    Verify Object Insert Exists    ${SHIFT_TABLE}    ${code}    Shift    ${SHIFT_INSERT_PROPERTIES}
    ...    @{SHIFT_FORM_LABELS}    code_label=Shift Code
    Clear Shift Row Filter

Update Shift Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Shift
    ...    Name is listed in testdata/shift_update.properties - Shift Code is read-only in
    ...    updateAttributes. Filters via Find Shift Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${SHIFT_UPDATE_PROPERTIES}
    Find Shift Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${SHIFT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Shift Code
    Clear Shift Row Filter
    RETURN    ${data}

Verify Shift Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Shift Name's LIVE SCREEN value to testdata/shift_update.properties.
    ...    Filters via Find Shift Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Shift Row By Filter    ${code}
    Verify Object Form Record    ${SHIFT_TABLE}    ${code}    Shift    ${SHIFT_UPDATE_PROPERTIES}
    ...    Shift Name    code_label=Shift Code
    Clear Shift Row Filter

Find Shift Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Shift
    ...    Row By Filter first. Deliberately does NOT clear the filter afterward - Verify Shift
    ...    Record Found (called right after, same TC) needs the grid still filtered to ${code}
    ...    for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Shift Row By Filter    ${code}
    Find Object Record    ${SHIFT_TABLE}    ${code}    Shift    code_label=Shift Code

Verify Shift Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Shift Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${SHIFT_TABLE}    ${code}    ${SHIFT_GRID_VERIFY_PROPERTIES}
    ...    ${SHIFT_FORM_VERIFY_PROPERTIES}    @{SHIFT_FORM_LABELS}
    Clear Shift Row Filter

Delete Shift Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for OV_SHIFT), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Shift Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Shift Row By Filter    ${code}
    Delete Object Via End Date    ${SHIFT_TABLE}    ${SHIFT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Shift Row Filter

Verify Shift Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_SHIFT) - the DB check lives here, in the shared
    ...    T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${SHIFT_TABLE}    OV_SHIFT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Shift Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${SHIFT_TABLE}    ${code}
