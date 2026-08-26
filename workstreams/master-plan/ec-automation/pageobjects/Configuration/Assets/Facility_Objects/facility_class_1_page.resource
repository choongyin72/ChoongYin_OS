*** Settings ***
Documentation       T3 (screen) — Facility Class 1 page object.
...                 Screen: Configuration > Assets > Facility_Objects > Facility Class 1.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area navigator cascade (2-level, C:1/C:2 same
...                 row, C:3 absent - confirmed live 2026-08-26) is set + GO. Converted to the
...                 Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner standing
...                 rule 2026-08-26: any EC screen with a navigator matching Area's layout MUST
...                 follow Area's FULL pattern, not just the navigator-fill piece PR #526 did) -
...                 Facility Class 1 remains OV-GM, its genuine 2-level PU->Area cascade + GO is
...                 KEPT exactly as PR #526 left it (Apply Navigator From Properties, EXPLICIT
...                 values from testdata/facility_class_1_navigator.properties: Op Production
...                 Unit=AS1 EC Exploration Norway, Op Area=AS1_Area). This is a STRUCTURAL
...                 conversion, not a reclassification of the screen as plain Bank-shaped.
...                 Real labels confirmed live (2026-08-26, objectForm label scan): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Facility Class 1 Code"/"Facility Class
...                 1 Name" (like Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name"
...                 Bank/Object List use - every T2 call below passes code_label=Facility Class 1
...                 Code accordingly. Grid columns confirmed live (manageObject:form:T_head scan):
...                 Facility Class 1 Code / Facility Class 1 Name / Start Date / End Date - same
...                 4-column shape as Area.
...                 objectForm DOES expose "Op Production Unit"/"Op Area" fields (confirmed live
...                 2026-08-26 - broader than the original CO.0019 build's "no Op PU field" note),
...                 but the already-proven driver (py/facility_class_1_iud.py, verify_screen PASS
...                 2026-07-30, still passing) inserts successfully leaving them blank; trusting
...                 that proven behavior rather than hunting for an unstated requirement - they
...                 are NOT added to testdata/facility_class_1_insert.properties.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${FC1_SCREEN}           Facility Class 1
${FC1_TABLE}            manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area 2-level cascade — MANDATORY before the grid
# loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/facility_class_1_navigator.properties
# (added by PR #526, kept unchanged by this structural conversion).
${FC1_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/facility_class_1_navigator.properties
${FC1_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/facility_class_1_insert.properties
${FC1_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/facility_class_1_update.properties
${FC1_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/facility_class_1_form_verify.properties
${FC1_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/facility_class_1_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Bank's own del-enddate constant: this row packs Start Date
# (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the one-field-per-row
# label scan cannot safely resolve. Value confirmed live via the pre-existing Playwright driver
# (py/facility_class_1_iud.py: END_DATE_ID convention shared across every OV-GM screen).
${FC1_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Facility Class 1's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectdates, not updateAttributes/objectForm's fill-once trio; Op Production
# Unit/Op Area deliberately excluded - out of scope, see Documentation above).
@{FC1_FORM_LABELS}      Facility Class 1 Code    Facility Class 1 Name


*** Keywords ***
Find Facility Class 1 Row By Filter
    [Documentation]    Explicitly filter the Facility Class 1 grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${FC1_TABLE}    ${code}

Clear Facility Class 1 Row Filter
    [Documentation]    Clear the Code column filter (see Find Facility Class 1 Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${FC1_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Facility Class 1's OWN credentials
    ...    (${FACILITY_CLASS_1_EC_USER}/${FACILITY_CLASS_1_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${FACILITY_CLASS_1_EC_USER}    ${FACILITY_CLASS_1_EC_PASS}

Open Facility Class 1 Screen With Navigator Values Populated
    [Documentation]    Navigate to the Facility Class 1 screen, THEN fill + submit the mandatory
    ...    2-level Production Unit -> Area navigator (dropdowns + GO) - the grid stays empty until
    ...    this happens, so this single keyword bundles both steps for the test case (Area's exact
    ...    skeleton calls this as ONE line per TC, not two). Assumes the caller already logged in
    ...    this test case (via Login To EC Application). Navigator fill delegates to the shared T2
    ...    "Apply Navigator From Properties" (resources/manage_object.resource), driven by
    ...    testdata/facility_class_1_navigator.properties (PR #526's mechanism, unchanged here).
    Open EC Screen    ${FC1_SCREEN}
    Apply Navigator From Properties    ${FC1_NAVIGATOR_PROPERTIES}

Insert Facility Class 1 Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so facility_class_1_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted Facility
    ...    Class 1 Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${FC1_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Facility Class 1 Code
    RETURN    ${code}

Verify Facility Class 1 Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Facility Class 1 Code/Facility Class 1 Name's LIVE SCREEN value is compared to
    ...    testdata/facility_class_1_insert.properties. Filters via Find Facility Class 1 Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Facility Class 1 Row By Filter    ${code}
    Verify Object Insert Exists    ${FC1_TABLE}    ${code}    Facility Class 1
    ...    ${FC1_INSERT_PROPERTIES}    @{FC1_FORM_LABELS}    code_label=Facility Class 1 Code
    Clear Facility Class 1 Row Filter

Update Facility Class 1 Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Facility Class 1 Name is listed in testdata/facility_class_1_update.properties -
    ...    Facility Class 1 Code is read-only in updateAttributes. Filters via Find Facility
    ...    Class 1 Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${FC1_UPDATE_PROPERTIES}
    Find Facility Class 1 Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${FC1_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Facility Class 1 Code
    Clear Facility Class 1 Row Filter
    RETURN    ${data}

Verify Facility Class 1 Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Facility Class 1 Name's LIVE SCREEN value to
    ...    testdata/facility_class_1_update.properties. Filters via Find Facility Class 1 Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Facility Class 1 Row By Filter    ${code}
    Verify Object Form Record    ${FC1_TABLE}    ${code}    Facility Class 1
    ...    ${FC1_UPDATE_PROPERTIES}    Facility Class 1 Name    code_label=Facility Class 1 Code
    Clear Facility Class 1 Row Filter

Find Facility Class 1 Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Facility
    ...    Class 1 Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Facility Class 1 Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Facility Class 1 Row By Filter    ${code}
    Find Object Record    ${FC1_TABLE}    ${code}    Facility Class 1    code_label=Facility Class 1 Code

Verify Facility Class 1 Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Facility Class 1 Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${FC1_TABLE}    ${code}    ${FC1_GRID_VERIFY_PROPERTIES}
    ...    ${FC1_FORM_VERIFY_PROPERTIES}    @{FC1_FORM_LABELS}
    Clear Facility Class 1 Row Filter

Delete Facility Class 1 Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for OV_FCTY_CLASS_1),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Facility Class 1 Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Facility Class 1 Row By Filter    ${code}
    Delete Object Via End Date    ${FC1_TABLE}    ${FC1_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Facility Class 1 Row Filter

Verify Facility Class 1 Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_FCTY_CLASS_1) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${FC1_TABLE}    OV_FCTY_CLASS_1    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Facility Class 1 Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${FC1_TABLE}    ${code}
