*** Settings ***
Documentation       T3 (screen) — Chemical Injection Point page object.
...                 Screen: Configuration > Assets > Chemical Objects > Chemical Injection Point (CO.0212).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area -> Facility Class 1 navigator cascade
...                 (3-level, C:1/C:2/C:3 same row, C:4 absent - confirmed live 2026-08-26) is
...                 set + GO. Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern, not just the
...                 navigator-fill piece) - Chemical Injection Point remains OV-GM, its genuine
...                 3-level Production Unit -> Area -> Facility Class 1 cascade + GO is KEPT,
...                 now driven EXPLICITLY via testdata/chem_injection_point_navigator.properties
...                 (Op Production Unit=AS1 EC Exploration Norway, Op Area=AS1_Area, Op Facility
...                 Class 1=AS1_Facility_01 - the SAME first-available picks the previously-proven
...                 driver, py/chem_injection_point_iud.py, already selected; verify_screen PASS
...                 2026-07-30). This is a STRUCTURAL conversion, not a reclassification of the
...                 screen as plain Bank-shaped.
...                 Real labels confirmed live (2026-08-26, objectForm/grid-header scan):
...                 objectForm/updateAttributes use SCREEN-PREFIXED "Chem Inj Point Code"/"Chem
...                 Inj Point Name" (like Area's "Area Code"/"Area Name"), NOT the generic
...                 "Code"/"Name" Bank/Object List use - every T2 call below passes
...                 code_label=Chem Inj Point Code accordingly. Grid columns confirmed live
...                 (manageObject:form:T_head scan): Chem Inj Point Code / Chem Inj Point Name /
...                 Start Date / End Date - same 4-column shape as Area/Facility Class 1.
...                 The proven driver's insert explicitly sets "Op Production Unit" (unlike
...                 Facility Class 1's own driver, which leaves it blank) - kept as an explicit
...                 field in testdata/chem_injection_point_insert.properties, matching the
...                 already-proven, currently-passing behavior.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CIP_SCREEN}           Chemical Injection Point
${CIP_TABLE}            manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1 3-level cascade —
# MANDATORY before the grid loads. The fill goes through the shared T2 "Apply Navigator From
# Properties" (resources/manage_object.resource), driven by
# testdata/chem_injection_point_navigator.properties.
${CIP_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/chem_injection_point_navigator.properties
${CIP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/chem_injection_point_insert.properties
${CIP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/chem_injection_point_update.properties
${CIP_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chem_injection_point_form_verify.properties
${CIP_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chem_injection_point_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# Playwright driver (py/chem_injection_point_iud.py: END_DATE_ID convention shared across every
# OV-GM screen).
${CIP_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Chemical Injection Point's own form-field label set (Start Date/End Date deliberately excluded -
# they live only in objectdates, not updateAttributes/objectForm's fill-once trio; Op Production
# Unit/Op Area/Op Facility Class 1 deliberately excluded from round-trip comparison - filled via
# resolved reference values which can re-render different display text after reload, same caveat
# as every other converted screen's dropdown fields).
@{CIP_FORM_LABELS}      Chem Inj Point Code    Chem Inj Point Name


*** Keywords ***
Find Chemical Injection Point Row By Filter
    [Documentation]    Explicitly filter the Chemical Injection Point grid's Code column to
    ...    ${code} via the shared T2 Find Object Row By Filter (resources/manage_object.resource),
    ...    matching every other Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CIP_TABLE}    ${code}

Clear Chemical Injection Point Row Filter
    [Documentation]    Clear the Code column filter (see Find Chemical Injection Point Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${CIP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Chemical Injection Point's OWN credentials
    ...    (${CHEMICAL_INJECTION_POINT_EC_USER}/${CHEMICAL_INJECTION_POINT_EC_PASS} from
    ...    credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${CHEMICAL_INJECTION_POINT_EC_USER}    ${CHEMICAL_INJECTION_POINT_EC_PASS}

Open Chemical Injection Point Screen With Navigator Values Populated
    [Documentation]    Navigate to the Chemical Injection Point screen, THEN fill + submit the
    ...    mandatory 3-level Production Unit -> Area -> Facility Class 1 navigator (dropdowns +
    ...    GO) - the grid stays empty until this happens, so this single keyword bundles both
    ...    steps for the test case (Area's exact skeleton calls this as ONE line per TC, not
    ...    two). Assumes the caller already logged in this test case (via Login To EC
    ...    Application). Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource), driven by
    ...    testdata/chem_injection_point_navigator.properties.
    Open EC Screen    ${CIP_SCREEN}
    Apply Navigator From Properties    ${CIP_NAVIGATOR_PROPERTIES}

Insert Chemical Injection Point Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so chem_injection_point_iud.robot's test case body
    ...    reads as a plain business step. Also owns the integrity check that the inserted Chem
    ...    Inj Point Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${CIP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Chem Inj Point Code
    RETURN    ${code}

Verify Chemical Injection Point Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Chem Inj Point Code/Chem Inj Point Name's LIVE SCREEN value is compared to
    ...    testdata/chem_injection_point_insert.properties. Filters via Find Chemical Injection
    ...    Point Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Injection Point Row By Filter    ${code}
    Verify Object Insert Exists    ${CIP_TABLE}    ${code}    Chemical Injection Point
    ...    ${CIP_INSERT_PROPERTIES}    @{CIP_FORM_LABELS}    code_label=Chem Inj Point Code
    Clear Chemical Injection Point Row Filter

Update Chemical Injection Point Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Chem
    ...    Inj Point Name is listed in testdata/chem_injection_point_update.properties - Chem Inj
    ...    Point Code is read-only in updateAttributes. Filters via Find Chemical Injection Point
    ...    Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CIP_UPDATE_PROPERTIES}
    Find Chemical Injection Point Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CIP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Chem Inj Point Code
    Clear Chemical Injection Point Row Filter
    RETURN    ${data}

Verify Chemical Injection Point Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Chem Inj Point Name's LIVE SCREEN value to
    ...    testdata/chem_injection_point_update.properties. Filters via Find Chemical Injection
    ...    Point Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Injection Point Row By Filter    ${code}
    Verify Object Form Record    ${CIP_TABLE}    ${code}    Chemical Injection Point
    ...    ${CIP_UPDATE_PROPERTIES}    Chem Inj Point Name    code_label=Chem Inj Point Code
    Clear Chemical Injection Point Row Filter

Find Chemical Injection Point Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Chemical Injection Point Row By Filter first. Deliberately does NOT clear the filter
    ...    afterward - Verify Chemical Injection Point Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check; it clears the filter
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Injection Point Row By Filter    ${code}
    Find Object Record    ${CIP_TABLE}    ${code}    Chemical Injection Point
    ...    code_label=Chem Inj Point Code

Verify Chemical Injection Point Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Chemical Injection Point Record before this) AND left the
    ...    Code filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CIP_TABLE}    ${code}    ${CIP_GRID_VERIFY_PROPERTIES}
    ...    ${CIP_FORM_VERIFY_PROPERTIES}    @{CIP_FORM_LABELS}
    Clear Chemical Injection Point Row Filter

Delete Chemical Injection Point Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the point, set End Date = Start Date (EC true delete for OV_CHEM_INJ_POINT),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Chemical Injection Point Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Chemical Injection Point Row By Filter    ${code}
    Delete Object Via End Date    ${CIP_TABLE}    ${CIP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Chemical Injection Point Row Filter

Verify Chemical Injection Point Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_CHEM_INJ_POINT) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CIP_TABLE}    OV_CHEM_INJ_POINT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Chemical Injection Point Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CIP_TABLE}    ${code}
