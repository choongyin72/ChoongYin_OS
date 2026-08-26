*** Settings ***
Documentation       T3 (screen) — Chemical Tank page object.
...                 Screen: Configuration > Assets > Chemical Objects > Chemical Tank (CO.0070).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory 3-level Production Unit -> Area -> Facility Class 1 navigator
...                 cascade (same row, C:1/C:2/C:3 - confirmed live 2026-08-26,
...                 tmp/recon_ct_navigator_cascade.py: C:1/C:2/C:3 present, C:4 absent) is set +
...                 GO. Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Chemical Tank
...                 remains OV-GM, its genuine 3-level cascade + GO is KEPT, now filled via the
...                 shared T2 "Apply Navigator From Properties" with EXPLICIT values (Op
...                 Production Unit=AS1 EC Exploration Norway, Op Area=AS1_Area, Op Facility
...                 Class 1=AS1_Facility_01 - captured live from what the previously-proven
...                 "Apply OV-GM Navigator First Available" already resolved to), instead of a
...                 reclassification of the screen as plain Bank-shaped.
...                 Real labels confirmed live (pre-existing driver + fresh 2026-08-26 grid-header
...                 scan, tmp/recon_ct_grid_headers.py): objectForm/updateAttributes use
...                 SCREEN-PREFIXED "Chemical Tank Code"/"Chemical Tank Name" (like Area's "Area
...                 Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use; grid
...                 columns are Chemical Tank Code / Chemical Tank Name / Start Date / End Date -
...                 same 4-column shape as Area/Facility Class 1.
...                 Extra mandatory over the plain OV: "Measure unit" dropdown (kept __FIRST__ -
...                 already-proven driver behavior, py/chemical_tank_iud.py). "Op Production
...                 Unit" on objectForm MUST equal the navigator's own PU value or the inserted
...                 row is not visible under this OV-GM navigator scope (same rule Area's own
...                 insert.properties documents).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CT_SCREEN}            Chemical Tank
${CT_TABLE}             manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1 3-level cascade - MANDATORY
# before the grid loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/chemical_tank_navigator.properties.
${CT_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_tank_navigator.properties
${CT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_tank_insert.properties
${CT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_tank_update.properties
${CT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_tank_form_verify.properties
${CT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_tank_grid_verify.properties
# objectdates End Date input (Delete = End Date = Start Date) - EC-wide stable id, same convention
# as Area's/Facility Class 1's own del-enddate constant: this row packs Start Date (C:1) and End
# Date (C:3) together with the End Date label at C:2, a shape the one-field-per-row label scan
# cannot safely resolve. Value confirmed live via the pre-existing driver (py/chemical_tank_iud.py
# via ec_object_iud's shared END_DATE_ID convention).
${CT_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Chemical Tank's own form-field label set (Start Date/End Date deliberately excluded - they live
# only in objectdates, not updateAttributes/objectForm's fill-once trio; Measure unit/Op
# Production Unit deliberately excluded from round-trip comparison - they are filled via
# resolved reference values which can re-render different display text after reload, same caveat
# as every other converted screen's dropdown fields).
@{CT_FORM_LABELS}       Chemical Tank Code    Chemical Tank Name


*** Keywords ***
Find Chemical Tank Row By Filter
    [Documentation]    Explicitly filter the Chemical Tank grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area/Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CT_TABLE}    ${code}

Clear Chemical Tank Row Filter
    [Documentation]    Clear the Code column filter (see Find Chemical Tank Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Chemical Tank's OWN credentials
    ...    (${CHEMICAL_TANK_EC_USER}/${CHEMICAL_TANK_EC_PASS} from credentials.py) on the current
    ...    page - works whether this is the very first login (page freshly loaded on the login
    ...    form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${CHEMICAL_TANK_EC_USER}    ${CHEMICAL_TANK_EC_PASS}

Open Chemical Tank Screen With Navigator Values Populated
    [Documentation]    Navigate to the Chemical Tank screen, THEN fill + submit the mandatory
    ...    3-level Production Unit -> Area -> Facility Class 1 navigator (dropdowns + GO) - the
    ...    grid stays empty until this happens, so this single keyword bundles both steps for the
    ...    test case (Area's exact skeleton calls this as ONE line per TC, not two). Assumes the
    ...    caller already logged in this test case (via Login To EC Application). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by testdata/chemical_tank_navigator.properties,
    ...    instead of the screen's prior bespoke "Apply OV-GM Navigator First Available" call.
    Open EC Screen    ${CT_SCREEN}
    Apply Navigator From Properties    ${CT_NAVIGATOR_PROPERTIES}

Insert Chemical Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so chemical_tank_iud.robot's test case body reads as a
    ...    plain business step. Also owns the integrity check that the inserted Chemical Tank Code
    ...    matches the suite's ${TEST_CODE}. ${CT_INSERT_PROPERTIES}'s Op Production Unit is
    ...    DELIBERATELY __FIRST__, not the navigator's own PU value - live recon (2026-08-26,
    ...    tmp/recon_ct_insert_exact_properties_order.py) proved Op Production Unit's option list
    ...    is FILTERED once Start Date/Measure unit are set and does NOT include this screen's
    ...    nav PU value; the already-proven driver's __FIRST__ choice is what keeps the row
    ...    grid-visible under this navigator scope, unlike Area's "must equal nav PU" rule.
    [Arguments]    ${properties_path}=${CT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Chemical Tank Code
    RETURN    ${code}

Verify Chemical Tank Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Chemical Tank Code/Chemical Tank Name's LIVE SCREEN value is compared to
    ...    testdata/chemical_tank_insert.properties. Filters via Find Chemical Tank Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Tank Row By Filter    ${code}
    Verify Object Insert Exists    ${CT_TABLE}    ${code}    Chemical Tank    ${CT_INSERT_PROPERTIES}
    ...    @{CT_FORM_LABELS}    code_label=Chemical Tank Code
    Clear Chemical Tank Row Filter

Update Chemical Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Chemical Tank Name is listed in testdata/chemical_tank_update.properties - Chemical
    ...    Tank Code is read-only in updateAttributes. Filters via Find Chemical Tank Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CT_UPDATE_PROPERTIES}
    Find Chemical Tank Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Chemical Tank Code
    Clear Chemical Tank Row Filter
    RETURN    ${data}

Verify Chemical Tank Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Chemical Tank Name's LIVE SCREEN value to
    ...    testdata/chemical_tank_update.properties. Filters via Find Chemical Tank Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Tank Row By Filter    ${code}
    Verify Object Form Record    ${CT_TABLE}    ${code}    Chemical Tank    ${CT_UPDATE_PROPERTIES}
    ...    Chemical Tank Name    code_label=Chemical Tank Code
    Clear Chemical Tank Row Filter

Find Chemical Tank Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Chemical
    ...    Tank Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Chemical Tank Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Tank Row By Filter    ${code}
    Find Object Record    ${CT_TABLE}    ${code}    Chemical Tank    code_label=Chemical Tank Code

Verify Chemical Tank Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Chemical Tank Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CT_TABLE}    ${code}    ${CT_GRID_VERIFY_PROPERTIES}
    ...    ${CT_FORM_VERIFY_PROPERTIES}    @{CT_FORM_LABELS}
    Clear Chemical Tank Row Filter

Delete Chemical Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the tank, set End Date = Start Date (EC true delete for OV_CHEM_TANK), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Chemical Tank Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Chemical Tank Row By Filter    ${code}
    Delete Object Via End Date    ${CT_TABLE}    ${CT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Chemical Tank Row Filter

Verify Chemical Tank Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_CHEM_TANK) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that
    ...    pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CT_TABLE}    OV_CHEM_TANK    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Chemical Tank Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CT_TABLE}    ${code}
